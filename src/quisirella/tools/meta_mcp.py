"""Client for Meta's official Ads MCP server (https://mcp.facebook.com/ads).

- Transport: streamable HTTP via langchain-mcp-adapters / mcp SDK.
- Auth: OAuth 2.1 with dynamic client registration handled by the mcp SDK.
  First run opens the browser for Meta Business login; tokens are cached in
  credentials/meta_mcp_tokens.json so subsequent runs are non-interactive.
- Safety: only read-only tools are exposed to agents. Anything that can
  create/update/activate entities or mutate catalogs is filtered out.
"""

from __future__ import annotations

import asyncio
import json
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from langchain.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient
from mcp.client.auth import OAuthClientProvider, TokenStorage
from mcp.shared.auth import OAuthClientInformationFull, OAuthClientMetadata, OAuthToken
from pydantic import AnyUrl

from quisirella.settings import CREDENTIALS_DIR, META_ACCESS_TOKEN, META_MCP_URL

CALLBACK_PORT = 3030
CALLBACK_URL = f"http://localhost:{CALLBACK_PORT}/callback"

# Verbs that indicate a mutating tool. Every ads/catalog write tool published
# by the Meta Ads MCP (ads_create_campaign, ads_update_entity,
# ads_activate_entity, add_products, update_product_set, ...) matches one.
WRITE_VERBS = (
    "create",
    "update",
    "activate",
    "delete",
    "remove",
    "add",
    "upload",
    "manage",
    "pause",
    "publish",
    "send",
    "write",
)


def is_read_only(tool_name: str) -> bool:
    lowered = tool_name.lower()
    return not any(verb in lowered for verb in WRITE_VERBS)


class FileTokenStorage(TokenStorage):
    """Persist OAuth tokens + client registration in the credentials dir."""

    def __init__(self) -> None:
        CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True)
        self._tokens_file: Path = CREDENTIALS_DIR / "meta_mcp_tokens.json"
        self._client_file: Path = CREDENTIALS_DIR / "meta_mcp_client.json"

    async def get_tokens(self) -> OAuthToken | None:
        if self._tokens_file.exists():
            return OAuthToken.model_validate_json(
                self._tokens_file.read_text(encoding="utf-8")
            )
        return None

    async def set_tokens(self, tokens: OAuthToken) -> None:
        self._tokens_file.write_text(tokens.model_dump_json(), encoding="utf-8")

    async def get_client_info(self) -> OAuthClientInformationFull | None:
        if self._client_file.exists():
            return OAuthClientInformationFull.model_validate_json(
                self._client_file.read_text(encoding="utf-8")
            )
        return None

    async def set_client_info(self, client_info: OAuthClientInformationFull) -> None:
        self._client_file.write_text(client_info.model_dump_json(), encoding="utf-8")


class _CallbackHandler(BaseHTTPRequestHandler):
    """Receives the OAuth redirect and stores code/state on the server object."""

    def do_GET(self) -> None:  # noqa: N802 (http.server API)
        parsed = urlparse(self.path)
        if parsed.path != "/callback":
            self.send_response(404)
            self.end_headers()
            return
        params = parse_qs(parsed.query)
        self.server.oauth_code = params.get("code", [None])[0]  # type: ignore[attr-defined]
        self.server.oauth_state = params.get("state", [None])[0]  # type: ignore[attr-defined]
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(
            "<h2>Quisirella: Meta OAuth thành công.</h2>"
            "<p>Bạn có thể đóng tab này và quay lại terminal.</p>".encode("utf-8")
        )

    def log_message(self, *args: object) -> None:  # silence request logging
        pass


async def _wait_for_callback() -> tuple[str, str | None]:
    """Run a one-shot local HTTP server until the OAuth redirect arrives."""

    server = HTTPServer(("localhost", CALLBACK_PORT), _CallbackHandler)
    server.oauth_code = None  # type: ignore[attr-defined]
    server.oauth_state = None  # type: ignore[attr-defined]

    def _serve() -> None:
        while server.oauth_code is None:  # type: ignore[attr-defined]
            server.handle_request()

    thread = threading.Thread(target=_serve, daemon=True)
    thread.start()
    while server.oauth_code is None:  # type: ignore[attr-defined]
        await asyncio.sleep(0.5)
    server.server_close()
    return server.oauth_code, server.oauth_state  # type: ignore[attr-defined]


async def _open_browser(authorization_url: str) -> None:
    print(f"\nMở trình duyệt để đăng nhập Meta Business:\n{authorization_url}\n")
    webbrowser.open(authorization_url)


def build_oauth_provider() -> OAuthClientProvider:
    return OAuthClientProvider(
        server_url=META_MCP_URL,
        client_metadata=OAuthClientMetadata(
            client_name="Quisirella Agent System",
            redirect_uris=[AnyUrl(CALLBACK_URL)],
            grant_types=["authorization_code", "refresh_token"],
            response_types=["code"],
        ),
        storage=FileTokenStorage(),
        redirect_handler=_open_browser,
        callback_handler=_wait_for_callback,
    )


def build_mcp_client() -> MultiServerMCPClient:
    """Prefer a manual access token (META_ACCESS_TOKEN) when configured.

    Meta's hosted MCP currently rejects OAuth dynamic client registration from
    custom clients ("Dynamic registration is not available for this client"),
    so the practical path is a bearer token obtained via the official Meta Ads
    CLI (`meta auth login`) or a Meta Business System User token (ads_read).
    The OAuth provider remains as fallback in case Meta opens DCR later.
    """
    connection: dict = {
        "transport": "streamable_http",
        "url": META_MCP_URL,
    }
    if META_ACCESS_TOKEN:
        connection["headers"] = {"Authorization": f"Bearer {META_ACCESS_TOKEN}"}
    else:
        connection["auth"] = build_oauth_provider()
    return MultiServerMCPClient({"meta_ads": connection})


async def get_meta_readonly_tools() -> list[BaseTool]:
    """Load Meta Ads MCP tools and keep only the read-only ones."""
    client = build_mcp_client()
    tools = await client.get_tools()
    readonly = [t for t in tools if is_read_only(t.name)]
    blocked = sorted(t.name for t in tools if not is_read_only(t.name))
    if blocked:
        print(f"[meta_mcp] Đã chặn {len(blocked)} tool ghi: {', '.join(blocked)}")
    print(f"[meta_mcp] Cấp {len(readonly)} tool read-only cho agent.")
    return readonly


def _leaf_exceptions(exc: BaseException) -> list[BaseException]:
    """Unwrap (nested) ExceptionGroups to the root-cause exceptions."""
    if isinstance(exc, BaseExceptionGroup):
        leaves: list[BaseException] = []
        for sub in exc.exceptions:
            leaves.extend(_leaf_exceptions(sub))
        return leaves
    return [exc]


async def run_auth() -> None:
    """Verify the Meta Ads MCP connection (CLI command: quisirella auth)."""
    if META_ACCESS_TOKEN:
        print("[meta_mcp] Dùng META_ACCESS_TOKEN từ .env để kết nối.")
    else:
        print(
            "[meta_mcp] Chưa có META_ACCESS_TOKEN trong .env - thử OAuth flow "
            "(Meta hiện có thể từ chối client tự đăng ký)."
        )
    try:
        tools = await get_meta_readonly_tools()
    except Exception as exc:
        message = " | ".join(str(e) for e in _leaf_exceptions(exc))
        print(f"\nKết nối Meta Ads MCP THẤT BẠI: {message}")
        if "Dynamic registration" in message or "invalid_client_metadata" in message:
            print(
                "\nNguyên nhân: Meta chỉ cho phép OAuth với các client được duyệt sẵn "
                "(claude.ai, ChatGPT, Cursor...), chưa mở cho client tự viết.\n"
                "Cách khắc phục - lấy access token thủ công rồi điền vào .env:\n"
                "  1. Cài Meta Ads CLI chính thức:  npm install -g @meta/ads-cli\n"
                "  2. Đăng nhập Meta Business:      meta auth login\n"
                "  3. Lấy token CLI đã lưu và điền vào .env: META_ACCESS_TOKEN=...\n"
                "  Hoặc tạo System User token (scope ads_read) trong Meta Business "
                "Settings > System Users."
            )
        raise SystemExit(1)
    names = sorted(t.name for t in tools)
    print("\nKết nối Meta Ads MCP thành công. Tools read-only khả dụng:")
    print(json.dumps(names, indent=2, ensure_ascii=False))
