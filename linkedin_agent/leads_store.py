"""Almacenamiento SQLite de leads y posts publicados por el agente."""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Any, Iterator


SCHEMA = """
CREATE TABLE IF NOT EXISTS posts (
    id          TEXT PRIMARY KEY,
    text        TEXT NOT NULL,
    created_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS leads (
    person_urn  TEXT PRIMARY KEY,
    name        TEXT,
    source_post TEXT,
    source_type TEXT,          -- comment | like | mention
    message     TEXT,
    score       INTEGER DEFAULT 0,
    status      TEXT DEFAULT 'new',  -- new | contacted | qualified | lost
    notes       TEXT,
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);
"""


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


class LeadsStore:
    def __init__(self, path: str):
        self._path = path
        with self._conn() as c:
            c.executescript(SCHEMA)

    @contextmanager
    def _conn(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self._path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    # -------------------------------------------------------------- posts
    def record_post(self, post_id: str, text: str) -> None:
        with self._conn() as c:
            c.execute(
                "INSERT OR REPLACE INTO posts(id, text, created_at) VALUES (?,?,?)",
                (post_id, text, _utcnow()),
            )

    def list_posts(self) -> list[dict[str, Any]]:
        with self._conn() as c:
            return [dict(r) for r in c.execute("SELECT * FROM posts ORDER BY created_at DESC")]

    # -------------------------------------------------------------- leads
    def upsert_lead(
        self,
        person_urn: str,
        *,
        name: str | None = None,
        source_post: str | None = None,
        source_type: str | None = None,
        message: str | None = None,
        score: int | None = None,
    ) -> None:
        now = _utcnow()
        with self._conn() as c:
            existing = c.execute(
                "SELECT person_urn FROM leads WHERE person_urn=?", (person_urn,)
            ).fetchone()
            if existing:
                c.execute(
                    """UPDATE leads
                       SET name=COALESCE(?, name),
                           source_post=COALESCE(?, source_post),
                           source_type=COALESCE(?, source_type),
                           message=COALESCE(?, message),
                           score=COALESCE(?, score),
                           updated_at=?
                       WHERE person_urn=?""",
                    (name, source_post, source_type, message, score, now, person_urn),
                )
            else:
                c.execute(
                    """INSERT INTO leads
                       (person_urn, name, source_post, source_type, message, score,
                        status, created_at, updated_at)
                       VALUES (?,?,?,?,?,?,?,?,?)""",
                    (
                        person_urn,
                        name,
                        source_post,
                        source_type,
                        message,
                        score or 0,
                        "new",
                        now,
                        now,
                    ),
                )

    def set_status(self, person_urn: str, status: str, notes: str | None = None) -> None:
        with self._conn() as c:
            c.execute(
                "UPDATE leads SET status=?, notes=COALESCE(?, notes), updated_at=? WHERE person_urn=?",
                (status, notes, _utcnow(), person_urn),
            )

    def list_leads(self, status: str | None = None) -> list[dict[str, Any]]:
        with self._conn() as c:
            if status:
                rows = c.execute(
                    "SELECT * FROM leads WHERE status=? ORDER BY score DESC, updated_at DESC",
                    (status,),
                )
            else:
                rows = c.execute(
                    "SELECT * FROM leads ORDER BY score DESC, updated_at DESC"
                )
            return [dict(r) for r in rows]
