"""Create the `queue` and `clips` tabs with headers in an existing spreadsheet.

Usage:
    python scripts/create_sheet_template.py <SPREADSHEET_ID>

The service account in `GOOGLE_SA_JSON` must already have edit access to the
spreadsheet.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import gspread
from google.oauth2.service_account import Credentials

from src.config import load_settings
from src.sheets.client import CLIPS_HEADERS, QUEUE_HEADERS, SCOPES


def main(spreadsheet_id: str) -> int:
    settings = load_settings()
    creds = Credentials.from_service_account_file(
        str(settings.google_sa_json), scopes=SCOPES
    )
    sh = gspread.authorize(creds).open_by_key(spreadsheet_id)

    for tab_name, headers in (
        (settings.queue_tab, QUEUE_HEADERS),
        (settings.clips_tab, CLIPS_HEADERS),
    ):
        try:
            ws = sh.worksheet(tab_name)
        except gspread.WorksheetNotFound:
            ws = sh.add_worksheet(tab_name, rows=200, cols=max(20, len(headers)))
        ws.update("A1", [headers])
        ws.freeze(rows=1)
        ws.format("A1:Z1", {"textFormat": {"bold": True}})

    print(f"Template created in spreadsheet {spreadsheet_id}.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
