"""Central configuration loaded from .env and config/ YAML files."""

from __future__ import annotations

import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "config"
DATA_DIR = PROJECT_ROOT / "data"
FINANCE_FETCH_DIR = DATA_DIR / "finance_fetch"
OUTPUT_DIR = PROJECT_ROOT / "output"
CREDENTIALS_DIR = PROJECT_ROOT / "credentials"

load_dotenv(PROJECT_ROOT / ".env")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
MODEL = os.getenv("QUISIRELLA_MODEL", "claude-sonnet-4-6")

META_MCP_URL = os.getenv("META_MCP_URL", "https://mcp.facebook.com/ads")
META_APP_ID = os.getenv("META_APP_ID", "")
META_APP_SECRET = os.getenv("META_APP_SECRET", "")
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN", "")
META_AD_ACCOUNT_ID = os.getenv("META_AD_ACCOUNT_ID", "")

GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "")
GOOGLE_SERVICE_ACCOUNT_FILE = os.getenv(
    "GOOGLE_SERVICE_ACCOUNT_FILE", str(CREDENTIALS_DIR / "service_account.json")
)
# Deprecated: ranges live in config/finance_sheet.yaml (kept for legacy sheets.py callers)
GOOGLE_SHEET_RANGES = [
    r.strip() for r in os.getenv("GOOGLE_SHEET_RANGES", "").split(",") if r.strip()
]


def load_store_profile() -> dict:
    with open(CONFIG_DIR / "store_profile.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_relevance_rules() -> dict:
    with open(CONFIG_DIR / "relevance_rules.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_campaign_strategy() -> dict:
    with open(CONFIG_DIR / "campaign_strategy.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_finance_sheet() -> dict:
    with open(CONFIG_DIR / "finance_sheet.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def ensure_dirs() -> None:
    for d in (DATA_DIR, FINANCE_FETCH_DIR, OUTPUT_DIR, CREDENTIALS_DIR):
        d.mkdir(parents=True, exist_ok=True)
