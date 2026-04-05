"""Ejecuta el agente con un LinkedInClient simulado.

Útil para ver el razonamiento del modelo y las tool-calls sin necesidad de
credenciales reales de LinkedIn. Solo se requiere ANTHROPIC_API_KEY.

Uso:
    ANTHROPIC_API_KEY=sk-ant-... python -m examples.run_mock
    ANTHROPIC_API_KEY=sk-ant-... python -m examples.run_mock "Publica sobre IA en ventas B2B"
"""
from __future__ import annotations

import asyncio
import os
import sys
import tempfile
from typing import Any

from linkedin_agent.agent import AgentRuntime, run_agent
from linkedin_agent.config import Config
from linkedin_agent.leads_store import LeadsStore


class FakeLinkedInClient:
    """Cliente de LinkedIn simulado para pruebas locales."""

    author_urn = "urn:li:person:FAKE123"

    def __init__(self) -> None:
        self._counter = 0
        self._posts: dict[str, str] = {}

    # ------------------------------------------------------------- posts
    def create_text_post(self, text: str, visibility: str = "PUBLIC") -> dict[str, Any]:
        self._counter += 1
        post_id = f"urn:li:ugcPost:fake{self._counter:03d}"
        self._posts[post_id] = text
        print(f"\n[FAKE LINKEDIN] 📢 Post publicado ({visibility}) id={post_id}")
        print(f"[FAKE LINKEDIN]    {text[:120]}{'...' if len(text) > 120 else ''}\n")
        return {"id": post_id}

    # -------------------------------------------------------- engagement
    def get_post_comments(self, post_urn: str) -> list[dict[str, Any]]:
        return [
            {
                "actor": "urn:li:person:ANA01",
                "message": {"text": "Muy interesante, ¿tenéis caso de uso en retail?"},
            },
            {
                "actor": "urn:li:person:BOB02",
                "message": {"text": "+1, nos encantaría agendar una demo"},
            },
            {
                "actor": "urn:li:person:CAR03",
                "message": {"text": "Gracias por compartir"},
            },
        ]

    def get_post_likes(self, post_urn: str) -> list[dict[str, Any]]:
        return [
            {"actor": "urn:li:person:DAN04"},
            {"actor": "urn:li:person:EVA05"},
        ]

    # ------------------------------------------------------------ people
    def get_profile(self, person_urn: str) -> dict[str, Any]:
        return {"id": person_urn, "localizedFirstName": "Demo", "localizedLastName": "User"}

    def me(self) -> dict[str, Any]:
        return {"id": "FAKE123"}

    def close(self) -> None:  # pragma: no cover - interfaz compatible
        pass


async def main() -> None:
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("ERROR: define ANTHROPIC_API_KEY antes de ejecutar.", file=sys.stderr)
        sys.exit(1)

    objective = (
        sys.argv[1]
        if len(sys.argv) > 1
        else (
            "Publica un post breve en español sobre cómo los agentes de IA "
            "ayudan a equipos de ventas B2B. Después recupera el engagement "
            "del post publicado, puntúa cada lead con score_lead y marca como "
            "'qualified' a quienes muestren intención de compra."
        )
    )

    # DB temporal para no ensuciar el entorno
    tmp_db = tempfile.NamedTemporaryFile(suffix=".sqlite3", delete=False)
    tmp_db.close()

    runtime = AgentRuntime(
        config=Config(
            anthropic_api_key=os.environ["ANTHROPIC_API_KEY"],
            linkedin_access_token="fake-token",
            linkedin_author_urn=FakeLinkedInClient.author_urn,
            leads_db_path=tmp_db.name,
        ),
        client=FakeLinkedInClient(),  # type: ignore[arg-type]
        store=LeadsStore(tmp_db.name),
    )

    print(f"▶️  Objetivo: {objective}\n")
    print(f"📂 SQLite temporal: {tmp_db.name}\n")

    try:
        await run_agent(objective, runtime=runtime)
    finally:
        runtime.close()

    # Dump final del estado del store
    print("\n─── Estado final ──────────────────────────────────────────")
    for p in runtime.store.list_posts():
        print(f"POST {p['id']}: {p['text'][:80]}...")
    for lead in runtime.store.list_leads():
        print(
            f"LEAD {lead['person_urn']} score={lead['score']} "
            f"status={lead['status']} notes={lead.get('notes')}"
        )


if __name__ == "__main__":
    asyncio.run(main())
