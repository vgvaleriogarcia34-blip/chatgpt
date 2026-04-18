"""Resolve a user input (local path or remote URL) into a SourceVideo."""
from __future__ import annotations

import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

import yt_dlp


@dataclass
class SourceVideo:
    id: str
    title: str
    duration_s: float
    path: Path
    language: str = ""


_SAFE = re.compile(r"[^A-Za-z0-9._-]+")


def _safe(name: str) -> str:
    return _SAFE.sub("_", name)[:80]


def _is_url(s: str) -> bool:
    try:
        return bool(urlparse(s).scheme in ("http", "https"))
    except Exception:
        return False


def _probe_duration(path: Path) -> float:
    """Return duration in seconds via ffprobe. 0.0 if it cannot be read."""
    try:
        out = subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
            stderr=subprocess.STDOUT,
        )
        return float(out.decode().strip())
    except Exception:
        return 0.0


def resolve(source: str, out_dir: Path, max_minutes: int) -> SourceVideo:
    """Accept a local file path or a URL, return a SourceVideo ready to process."""
    if _is_url(source):
        return _download(source, out_dir, max_minutes)
    return _ingest_local(Path(source).expanduser().resolve(), out_dir, max_minutes)


def _ingest_local(path: Path, out_dir: Path, max_minutes: int) -> SourceVideo:
    if not path.is_file():
        raise FileNotFoundError(f"Source video not found: {path}")
    duration = _probe_duration(path)
    if duration and duration > max_minutes * 60:
        raise ValueError(
            f"Video exceeds max allowed duration "
            f"({duration:.0f}s > {max_minutes*60}s)"
        )
    out_dir.mkdir(parents=True, exist_ok=True)
    safe_stem = _safe(path.stem) or "local"
    dest = out_dir / f"{safe_stem}{path.suffix.lower()}"
    if dest != path and not dest.exists():
        shutil.copy2(path, dest)
    return SourceVideo(
        id=safe_stem,
        title=path.stem,
        duration_s=duration,
        path=dest,
    )


def _download(url: str, out_dir: Path, max_minutes: int) -> SourceVideo:
    out_dir.mkdir(parents=True, exist_ok=True)
    ydl_opts = {
        "format": "bv*[height<=1080]+ba/b[height<=1080]",
        "outtmpl": str(out_dir / "%(id)s.%(ext)s"),
        "merge_output_format": "mp4",
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        duration = float(info.get("duration") or 0)
        if duration > max_minutes * 60:
            raise ValueError(
                f"Video exceeds max allowed duration "
                f"({duration:.0f}s > {max_minutes*60}s)"
            )
        info = ydl.extract_info(url, download=True)
        path = Path(ydl.prepare_filename(info)).with_suffix(".mp4")
        if not path.exists():
            path = Path(ydl.prepare_filename(info))
        return SourceVideo(
            id=_safe(info["id"]),
            title=info.get("title") or info["id"],
            duration_s=duration,
            path=path,
            language=info.get("language") or "",
        )


# Backwards-compatible alias — old pipeline still calls `download`.
download = resolve
