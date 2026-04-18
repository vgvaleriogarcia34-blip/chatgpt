"""Watch an inbox directory: any video dropped there gets processed and
moved to `processed/`. Renders end up in `data/renders/<name>/`.

Usage:
    python scripts/watch_inbox.py            # watches ./inbox
    python scripts/watch_inbox.py path/to/dir
"""
from __future__ import annotations

import logging
import shutil
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rich.logging import RichHandler

from src.config import load_settings
from src.local_pipeline import run

VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".webm", ".m4v", ".avi"}
POLL_SECONDS = 5


def _ready(path: Path) -> bool:
    """Consider the file ready when its size is stable across two reads."""
    try:
        size1 = path.stat().st_size
        time.sleep(1.0)
        size2 = path.stat().st_size
        return size1 == size2 and size1 > 0
    except FileNotFoundError:
        return False


def main(inbox_arg: str | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(message)s",
                        handlers=[RichHandler(markup=True)])
    log = logging.getLogger("inbox")
    settings = load_settings()

    inbox = Path(inbox_arg or "inbox").resolve()
    processed = inbox / "processed"
    failed = inbox / "failed"
    inbox.mkdir(parents=True, exist_ok=True)
    processed.mkdir(parents=True, exist_ok=True)
    failed.mkdir(parents=True, exist_ok=True)

    log.info("Watching %s (drop videos here)", inbox)
    while True:
        for item in sorted(inbox.iterdir()):
            if item.is_dir() or item.suffix.lower() not in VIDEO_EXTS:
                continue
            if not _ready(item):
                continue
            log.info("→ New video: %s", item.name)
            try:
                run(source=str(item), settings=settings)
                shutil.move(str(item), str(processed / item.name))
                log.info("✓ Processed; moved to %s", processed)
            except Exception as e:
                log.exception("Failed to process %s", item.name)
                shutil.move(str(item), str(failed / item.name))
                (failed / f"{item.name}.error.txt").write_text(str(e))
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else None))
