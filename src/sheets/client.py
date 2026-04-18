"""Google Sheets client that backs the ReelForge queue and clips tabs."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

import gspread
from google.oauth2.service_account import Credentials

from src.config import Settings

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

QUEUE_HEADERS = [
    "id", "source_url", "notes", "status", "clips_target", "language",
    "duration_s", "transcript_url", "clips_generated", "ig_published",
    "li_published", "started_at", "finished_at", "error",
]

CLIPS_HEADERS = [
    "clip_id", "queue_id", "start_s", "end_s", "duration_s", "punch_score",
    "hook_phrase", "render_url", "ig_caption", "ig_post_url",
    "li_caption", "li_post_url", "status", "error",
]

Status = str  # PENDING, DOWNLOADING, TRANSCRIBING, ANALYZING, EDITING, PUBLISHING, DONE, ERROR


@dataclass
class QueueRow:
    row_index: int  # 1-based row number in the sheet (incl. header)
    id: str
    source_url: str
    notes: str = ""
    status: Status = "PENDING"
    clips_target: int = 5
    language: str = ""
    duration_s: float = 0.0
    transcript_url: str = ""
    clips_generated: int = 0
    ig_published: int = 0
    li_published: int = 0
    started_at: str = ""
    finished_at: str = ""
    error: str = ""


@dataclass
class ClipRow:
    clip_id: str
    queue_id: str
    start_s: float
    end_s: float
    punch_score: int
    hook_phrase: str
    render_url: str = ""
    ig_caption: str = ""
    ig_post_url: str = ""
    li_caption: str = ""
    li_post_url: str = ""
    status: str = "RENDERED"
    error: str = ""

    @property
    def duration_s(self) -> float:
        return round(self.end_s - self.start_s, 2)

    def to_row(self) -> list[Any]:
        return [
            self.clip_id, self.queue_id, self.start_s, self.end_s,
            self.duration_s, self.punch_score, self.hook_phrase,
            self.render_url, self.ig_caption, self.ig_post_url,
            self.li_caption, self.li_post_url, self.status, self.error,
        ]


class SheetsClient:
    def __init__(self, settings: Settings) -> None:
        creds = Credentials.from_service_account_file(
            str(settings.google_sa_json), scopes=SCOPES
        )
        self._gc = gspread.authorize(creds)
        self._sh = self._gc.open_by_key(settings.spreadsheet_id)
        self._queue = self._sh.worksheet(settings.queue_tab)
        self._clips = self._sh.worksheet(settings.clips_tab)

    # ── queue ───────────────────────────────────────────────
    def fetch_pending(self) -> list[QueueRow]:
        records = self._queue.get_all_records()
        rows: list[QueueRow] = []
        for idx, r in enumerate(records, start=2):  # header is row 1
            if (r.get("status") or "PENDING").upper() == "PENDING" and r.get("source_url"):
                rows.append(
                    QueueRow(
                        row_index=idx,
                        id=str(r.get("id") or f"auto-{idx}"),
                        source_url=str(r["source_url"]).strip(),
                        notes=str(r.get("notes", "")),
                        clips_target=int(r.get("clips_target") or 5),
                    )
                )
        return rows

    def set_status(self, row: QueueRow, status: Status, error: str = "") -> None:
        row.status = status
        updates = {"status": status, "error": error}
        if status == "DOWNLOADING":
            updates["started_at"] = _now_iso()
        if status in ("DONE", "ERROR"):
            updates["finished_at"] = _now_iso()
        self._update_queue(row, updates)

    def update_queue_fields(self, row: QueueRow, **fields: Any) -> None:
        self._update_queue(row, fields)

    def _update_queue(self, row: QueueRow, fields: dict[str, Any]) -> None:
        cells = []
        for k, v in fields.items():
            if k not in QUEUE_HEADERS:
                continue
            col = QUEUE_HEADERS.index(k) + 1
            cells.append(gspread.Cell(row.row_index, col, str(v)))
            setattr(row, k, v)
        if cells:
            self._queue.update_cells(cells)

    # ── clips ───────────────────────────────────────────────
    def append_clip(self, clip: ClipRow) -> int:
        self._clips.append_row(clip.to_row(), value_input_option="USER_ENTERED")
        # Return the row index we just wrote into.
        return len(self._clips.get_all_values())

    def update_clip(self, row_index: int, **fields: Any) -> None:
        cells = []
        for k, v in fields.items():
            if k not in CLIPS_HEADERS:
                continue
            col = CLIPS_HEADERS.index(k) + 1
            cells.append(gspread.Cell(row_index, col, str(v)))
        if cells:
            self._clips.update_cells(cells)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
