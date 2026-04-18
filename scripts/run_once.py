"""Process the first pending row and exit — for local testing."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rich.logging import RichHandler

from src.config import load_settings
from src.sheets.client import SheetsClient
from src.video.pipeline import process_row


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(message)s",
                        handlers=[RichHandler(markup=True)])
    settings = load_settings()
    sheets = SheetsClient(settings)
    pending = sheets.fetch_pending()
    if not pending:
        print("No pending rows.")
        return 0
    process_row(pending[0], sheets, settings)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
