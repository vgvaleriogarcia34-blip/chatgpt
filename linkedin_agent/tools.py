"""Tools expuestas al agente de Claude mediante el Claude Agent SDK.

Cada tool encapsula una operación concreta sobre LinkedIn o el store de leads.
El agente decide cuándo invocarlas en función del objetivo en lenguaje natural.
"""
from __future__ import annotations

from typing import Any

from claude_agent_sdk import tool

from .leads_store import LeadsStore
from .linkedin_client import LinkedInClient


def build_tools(client: LinkedInClient, store: LeadsStore) -> list:
    """Registra las tools del agente enlazadas al cliente y al store."""

    @tool(
        "publish_post",
        "Publica un post de texto en el perfil de LinkedIn del autor autenticado.",
        {"text": str, "visibility": str},
    )
    async def publish_post(args: dict[str, Any]) -> dict[str, Any]:
        text = args["text"].strip()
        if not text:
            return {"content": [{"type": "text", "text": "error: texto vacío"}]}
        if len(text) > 3000:
            return {"content": [{"type": "text", "text": "error: el post supera 3000 caracteres"}]}
        visibility = args.get("visibility") or "PUBLIC"
        result = client.create_text_post(text, visibility=visibility)
        post_id = result["id"]
        store.record_post(post_id, text)
        return {
            "content": [
                {"type": "text", "text": f"Publicado con id={post_id}"}
            ]
        }

    @tool(
        "list_my_posts",
        "Lista los posts publicados por el agente que están registrados en el store.",
        {},
    )
    async def list_my_posts(_: dict[str, Any]) -> dict[str, Any]:
        posts = store.list_posts()
        return {"content": [{"type": "text", "text": str(posts)}]}

    @tool(
        "fetch_engagement",
        "Obtiene comentarios y likes de un post dado su URN y los registra como leads candidatos.",
        {"post_urn": str},
    )
    async def fetch_engagement(args: dict[str, Any]) -> dict[str, Any]:
        post_urn = args["post_urn"]
        comments = client.get_post_comments(post_urn)
        likes = client.get_post_likes(post_urn)

        added = 0
        for c in comments:
            actor = c.get("actor") or c.get("author")
            if not actor:
                continue
            message = (
                c.get("message", {}).get("text")
                if isinstance(c.get("message"), dict)
                else None
            )
            store.upsert_lead(
                person_urn=actor,
                source_post=post_urn,
                source_type="comment",
                message=message,
            )
            added += 1
        for lk in likes:
            actor = lk.get("actor")
            if not actor:
                continue
            store.upsert_lead(
                person_urn=actor,
                source_post=post_urn,
                source_type="like",
            )
            added += 1

        return {
            "content": [
                {
                    "type": "text",
                    "text": f"{added} interacciones registradas ({len(comments)} comentarios, {len(likes)} likes)",
                }
            ]
        }

    @tool(
        "score_lead",
        "Asigna una puntuación (0-100) a un lead en base al criterio que el agente considere.",
        {"person_urn": str, "score": int, "notes": str},
    )
    async def score_lead(args: dict[str, Any]) -> dict[str, Any]:
        store.upsert_lead(person_urn=args["person_urn"], score=int(args["score"]))
        if args.get("notes"):
            store.set_status(args["person_urn"], "new", notes=args["notes"])
        return {"content": [{"type": "text", "text": "ok"}]}

    @tool(
        "update_lead_status",
        "Actualiza el estado de un lead: new | contacted | qualified | lost.",
        {"person_urn": str, "status": str, "notes": str},
    )
    async def update_lead_status(args: dict[str, Any]) -> dict[str, Any]:
        status = args["status"]
        if status not in {"new", "contacted", "qualified", "lost"}:
            return {"content": [{"type": "text", "text": "error: estado inválido"}]}
        store.set_status(args["person_urn"], status, notes=args.get("notes"))
        return {"content": [{"type": "text", "text": "ok"}]}

    @tool(
        "list_leads",
        "Lista leads almacenados, opcionalmente filtrando por estado.",
        {"status": str},
    )
    async def list_leads(args: dict[str, Any]) -> dict[str, Any]:
        leads = store.list_leads(status=args.get("status") or None)
        return {"content": [{"type": "text", "text": str(leads)}]}

    return [
        publish_post,
        list_my_posts,
        fetch_engagement,
        score_lead,
        update_lead_status,
        list_leads,
    ]
