"""Centralised configuration loaded from environment variables."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DOWNLOADS = DATA / "downloads"
CLIPS = DATA / "clips"
RENDERS = DATA / "renders"
LOGS = DATA / "logs"
for _d in (DOWNLOADS, CLIPS, RENDERS, LOGS):
    _d.mkdir(parents=True, exist_ok=True)


def _env(name: str, default: str | None = None, required: bool = False) -> str:
    value = os.getenv(name, default)
    if required and not value:
        raise RuntimeError(f"Missing required env var: {name}")
    return value or ""


@dataclass(frozen=True)
class Settings:
    anthropic_api_key: str
    claude_model: str

    google_sa_json: Path
    spreadsheet_id: str
    queue_tab: str
    clips_tab: str

    ig_user_id: str
    ig_access_token: str

    li_access_token: str
    li_author_urn: str

    r2_account_id: str
    r2_bucket: str
    r2_access_key: str
    r2_secret_key: str
    r2_public_base: str

    clips_per_video_default: int
    clip_min_seconds: int
    clip_max_seconds: int
    source_max_minutes: int
    whisper_model: str
    whisper_device: str
    worker_poll_seconds: int

    brand_watermark: str
    brand_font: Path
    brand_color_primary: str
    brand_color_text: str


def load_settings(require_sheets: bool = False) -> Settings:
    return Settings(
        anthropic_api_key=_env("ANTHROPIC_API_KEY", required=True),
        claude_model=_env("CLAUDE_MODEL", "claude-sonnet-4-6"),
        google_sa_json=ROOT / _env("GOOGLE_SA_JSON", "secrets/google-sa.json"),
        spreadsheet_id=_env("SPREADSHEET_ID", required=require_sheets),
        queue_tab=_env("QUEUE_TAB", "queue"),
        clips_tab=_env("CLIPS_TAB", "clips"),
        ig_user_id=_env("IG_USER_ID"),
        ig_access_token=_env("IG_ACCESS_TOKEN"),
        li_access_token=_env("LI_ACCESS_TOKEN"),
        li_author_urn=_env("LI_AUTHOR_URN"),
        r2_account_id=_env("R2_ACCOUNT_ID"),
        r2_bucket=_env("R2_BUCKET"),
        r2_access_key=_env("R2_ACCESS_KEY"),
        r2_secret_key=_env("R2_SECRET_KEY"),
        r2_public_base=_env("R2_PUBLIC_BASE"),
        clips_per_video_default=int(_env("CLIPS_PER_VIDEO_DEFAULT", "5")),
        clip_min_seconds=int(_env("CLIP_MIN_SECONDS", "35")),
        clip_max_seconds=int(_env("CLIP_MAX_SECONDS", "60")),
        source_max_minutes=int(_env("SOURCE_MAX_MINUTES", "20")),
        whisper_model=_env("WHISPER_MODEL", "medium"),
        whisper_device=_env("WHISPER_DEVICE", "auto"),
        worker_poll_seconds=int(_env("WORKER_POLL_SECONDS", "60")),
        brand_watermark=_env("BRAND_WATERMARK", "@reelforge"),
        brand_font=ROOT / _env("BRAND_FONT", "assets/fonts/Inter-Bold.ttf"),
        brand_color_primary=_env("BRAND_COLOR_PRIMARY", "#FFDD2D"),
        brand_color_text=_env("BRAND_COLOR_TEXT", "#FFFFFF"),
    )


settings = load_settings(require_sheets=False) if os.getenv("ANTHROPIC_API_KEY") else None
