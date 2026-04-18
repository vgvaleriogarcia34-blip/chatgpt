"""Long-running worker that polls the queue and processes pending rows."""
from __future__ import annotations

import logging
import time

from rich.logging import RichHandler

from src.config import load_settings
from src.sheets.client import SheetsClient
from src.video.pipeline import process_row


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[RichHandler(markup=True, rich_tracebacks=True)],
    )
    log = logging.getLogger("reelforge")
    settings = load_settings()
    sheets = SheetsClient(settings)

    log.info("ReelForge worker started (poll=%ss)", settings.worker_poll_seconds)
    while True:
        try:
            pending = sheets.fetch_pending()
            if pending:
                log.info("Found %d pending row(s)", len(pending))
                for row in pending:
                    log.info("→ Processing [bold]%s[/] %s", row.id, row.source_url)
                    process_row(row, sheets, settings)
            else:
                log.debug("No pending rows")
        except Exception:  # keep loop alive on transient errors
            log.exception("Worker loop error")
        time.sleep(settings.worker_poll_seconds)


if __name__ == "__main__":
    main()
