"""Chunk and search knowledge base for meta-analyst RAG (Phase C hybrid + rerank)."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
from pathlib import Path
from typing import Any, Iterator

from langchain_chroma import Chroma
from langchain_core.documents import Document

from quisirella.retrieval.compression import compress_chunks
from quisirella.retrieval.embeddings import get_embeddings, prefix_for_passage
from quisirella.retrieval.grading import grade_retrieval
from quisirella.retrieval.hybrid import hybrid_search, save_bm25_corpus
from quisirella.retrieval.query_expand import expand_query
from quisirella.retrieval.rerank import rerank_chunks
from quisirella.settings import (
    CURSOR_RULES_DIR,
    KNOWLEDGE_INDEX_DIR,
    OUTPUT_DIR,
    PROJECT_ROOT,
    RAG_HYBRID_FETCH_K,
    SKILL_DIR,
)

COLLECTION_NAME = "quisirella_knowledge"
DEFAULT_TOP_K = 10
CHUNK_CHAR_TARGET = 2400
MANIFEST_FILE = "manifest.json"

KNOWLEDGE_GLOBS = [
    (OUTPUT_DIR, "00-*.md"),
    (OUTPUT_DIR, "0[1-6]-*.md"),
    (CURSOR_RULES_DIR, "quisirella-meta-*.mdc"),
    (SKILL_DIR, "SKILL.md"),
    (SKILL_DIR / "references", "*.md"),
]

EXCLUDE_NAMES = {
    "07-session-log.md",
    "09-session-checkpoints.md",
}

DOC_PRIORITY = {
    "report": 3,
    "rule": 2,
    "skill": 2,
    "policy": 1,
    "other": 1,
}


def _doc_type(path: Path) -> str:
    name = path.name
    if name.startswith("00-"):
        return "policy"
    if re.match(r"0[1-6]-", name):
        return "report"
    if path.suffix == ".mdc":
        return "rule"
    if "references" in path.parts:
        return "skill"
    if name == "SKILL.md":
        return "skill"
    return "other"


def _iter_source_files() -> Iterator[Path]:
    seen: set[Path] = set()
    for base, pattern in KNOWLEDGE_GLOBS:
        if not base.exists():
            continue
        for path in sorted(base.glob(pattern)):
            if not path.is_file():
                continue
            if path.name in EXCLUDE_NAMES:
                continue
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            yield path


def _split_markdown(text: str) -> list[tuple[str, str]]:
    lines = text.splitlines()
    sections: list[tuple[str, str]] = []
    current_title = "preamble"
    current_lines: list[str] = []

    for line in lines:
        if line.startswith("## ") and not line.startswith("### "):
            if current_lines:
                sections.append((current_title, "\n".join(current_lines).strip()))
            current_title = line[3:].strip()
            current_lines = []
        else:
            current_lines.append(line)

    if current_lines:
        sections.append((current_title, "\n".join(current_lines).strip()))

    if not sections:
        return [("full", text.strip())]

    out: list[tuple[str, str]] = []
    for title, body in sections:
        if len(body) <= CHUNK_CHAR_TARGET:
            out.append((title, body))
            continue
        start = 0
        part = 0
        while start < len(body):
            chunk = body[start : start + CHUNK_CHAR_TARGET]
            out.append((f"{title} (part {part})", chunk))
            start += CHUNK_CHAR_TARGET - 200
            part += 1
    return out


def _chunk_id(source_file: str, section_title: str) -> str:
    raw = f"{source_file}::{section_title}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def _file_to_documents(path: Path) -> list[Document]:
    try:
        text = path.read_text(encoding="utf-8")
        mtime = int(path.stat().st_mtime)
    except OSError:
        return []

    rel = path.relative_to(PROJECT_ROOT).as_posix()
    doc_type = _doc_type(path)
    priority = DOC_PRIORITY.get(doc_type, 1)
    docs: list[Document] = []

    for section_title, body in _split_markdown(text):
        if not body.strip():
            continue
        plain = f"[{rel}] {section_title}\n\n{body}"
        content = prefix_for_passage(plain)
        cid = _chunk_id(rel, section_title)
        docs.append(
            Document(
                page_content=content,
                metadata={
                    "chunk_id": cid,
                    "source_file": rel,
                    "section_title": section_title,
                    "doc_type": doc_type,
                    "doc_priority": priority,
                    "mtime": mtime,
                },
            )
        )
    return docs


def _manifest_path() -> Path:
    return KNOWLEDGE_INDEX_DIR / MANIFEST_FILE


def _load_manifest() -> dict[str, Any]:
    path = _manifest_path()
    if not path.exists():
        return {"files": {}}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _save_manifest(manifest: dict[str, Any]) -> None:
    KNOWLEDGE_INDEX_DIR.mkdir(parents=True, exist_ok=True)
    with open(_manifest_path(), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


def _file_fingerprint(path: Path) -> dict[str, Any]:
    stat = path.stat()
    content = path.read_bytes()
    return {
        "mtime": int(stat.st_mtime),
        "size": stat.st_size,
        "sha256": hashlib.sha256(content).hexdigest(),
    }


def _docs_to_bm25_records(docs: list[Document]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for doc in docs:
        meta = doc.metadata or {}
        plain = doc.page_content.removeprefix("passage: ").strip()
        records.append(
            {
                "chunk_id": meta.get("chunk_id", ""),
                "source_file": meta.get("source_file", ""),
                "section_title": meta.get("section_title", ""),
                "doc_type": meta.get("doc_type", ""),
                "doc_priority": meta.get("doc_priority", 1),
                "mtime": meta.get("mtime", 0),
                "content": plain,
                "search_text": plain,
            }
        )
    return records


def _rebuild_bm25_from_store(store: Chroma) -> None:
    data = store.get(include=["metadatas", "documents"])
    docs = data.get("documents") or []
    metas = data.get("metadatas") or []
    records: list[dict[str, Any]] = []
    for text, meta in zip(docs, metas):
        if not meta:
            continue
        plain = (text or "").removeprefix("passage: ").strip()
        records.append(
            {
                "chunk_id": meta.get("chunk_id", ""),
                "source_file": meta.get("source_file", ""),
                "section_title": meta.get("section_title", ""),
                "doc_type": meta.get("doc_type", ""),
                "doc_priority": meta.get("doc_priority", 1),
                "mtime": meta.get("mtime", 0),
                "content": plain,
                "search_text": plain,
            }
        )
    save_bm25_corpus(records)


def build_knowledge_index(*, reset: bool = True, incremental: bool = False) -> dict[str, Any]:
    source_paths = list(_iter_source_files())
    if not source_paths:
        raise ValueError("No knowledge documents found to index")

    if reset and not incremental and KNOWLEDGE_INDEX_DIR.exists():
        shutil.rmtree(KNOWLEDGE_INDEX_DIR)
    KNOWLEDGE_INDEX_DIR.mkdir(parents=True, exist_ok=True)

    manifest = _load_manifest() if incremental else {"files": {}}
    file_entries = manifest.setdefault("files", {})

    current_sources = {p.relative_to(PROJECT_ROOT).as_posix() for p in source_paths}
    removed = [rel for rel in list(file_entries) if rel not in current_sources]

    store: Chroma | None = None
    if incremental and KNOWLEDGE_INDEX_DIR.exists() and any(KNOWLEDGE_INDEX_DIR.iterdir()):
        store = _load_store()
    elif not incremental:
        store = None

    if store is None and not incremental:
        all_docs: list[Document] = []
        sources: list[str] = []
        for path in source_paths:
            docs = _file_to_documents(path)
            if docs:
                rel = path.relative_to(PROJECT_ROOT).as_posix()
                sources.append(rel)
                file_entries[rel] = _file_fingerprint(path)
                all_docs.extend(docs)

        Chroma.from_documents(
            documents=all_docs,
            embedding=get_embeddings(),
            collection_name=COLLECTION_NAME,
            persist_directory=str(KNOWLEDGE_INDEX_DIR),
        )
        save_bm25_corpus(_docs_to_bm25_records(all_docs))
        _save_manifest(manifest)
        return {
            "status": "ok",
            "mode": "full",
            "chunks": len(all_docs),
            "source_files": len(sources),
            "sources": sources,
            "removed": [],
            "index_dir": str(KNOWLEDGE_INDEX_DIR),
            "embedding_model": get_embeddings().model_name,
        }

    # incremental path
    store = store or Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=get_embeddings(),
        persist_directory=str(KNOWLEDGE_INDEX_DIR),
    )

    added = 0
    updated = 0
    sources: list[str] = []

    for rel in removed:
        try:
            store.delete(where={"source_file": rel})
        except Exception:
            pass
        file_entries.pop(rel, None)

    for path in source_paths:
        rel = path.relative_to(PROJECT_ROOT).as_posix()
        fp = _file_fingerprint(path)
        prev = file_entries.get(rel)
        if prev and prev.get("sha256") == fp["sha256"]:
            sources.append(rel)
            continue

        if prev:
            try:
                store.delete(where={"source_file": rel})
            except Exception:
                pass
            updated += 1
        else:
            added += 1

        docs = _file_to_documents(path)
        if docs:
            store.add_documents(docs)
            file_entries[rel] = fp
            sources.append(rel)

    _rebuild_bm25_from_store(store)
    _save_manifest(manifest)

    data = store.get(include=["metadatas"])
    chunk_count = len(data.get("ids") or [])

    return {
        "status": "ok",
        "mode": "incremental",
        "chunks": chunk_count,
        "source_files": len(sources),
        "sources": sources,
        "added_files": added,
        "updated_files": updated,
        "removed_files": removed,
        "index_dir": str(KNOWLEDGE_INDEX_DIR),
        "embedding_model": get_embeddings().model_name,
    }


def _load_store() -> Chroma | None:
    if not KNOWLEDGE_INDEX_DIR.exists():
        return None
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=get_embeddings(),
        persist_directory=str(KNOWLEDGE_INDEX_DIR),
    )


def search_knowledge(
    query: str,
    top_k: int = DEFAULT_TOP_K,
    doc_type: str | None = None,
    *,
    compress: bool = True,
    expand: bool = True,
    store: Chroma | None = None,
) -> dict[str, Any]:
    store = store if store is not None else _load_store()
    if store is None:
        return {
            "status": "index_missing",
            "query": query,
            "grade": "missing",
            "retrieval_confidence": 0.0,
            "chunks": [],
            "message": "Run: python -m quisirella index-knowledge",
        }

    variants = expand_query(query) if expand else [query]
    candidates = hybrid_search(
        store,
        query,
        top_k=top_k,
        fetch_k=RAG_HYBRID_FETCH_K,
        doc_type=doc_type,
        query_variants=variants,
    )

    chunks = rerank_chunks(query, candidates, top_k=top_k)
    grade, confidence = grade_retrieval(chunks)

    if compress and chunks:
        chunks = compress_chunks(query, chunks)

    return {
        "status": "ok",
        "query": query,
        "query_variants": variants,
        "grade": grade,
        "retrieval_confidence": round(confidence, 4),
        "chunk_count": len(chunks),
        "chunks": chunks,
        "index_dir": str(KNOWLEDGE_INDEX_DIR),
    }
