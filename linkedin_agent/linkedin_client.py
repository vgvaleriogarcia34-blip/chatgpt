"""Wrapper mínimo sobre la API REST oficial de LinkedIn.

Usa los endpoints públicos de LinkedIn Marketing / UGC:
  - POST /v2/ugcPosts                (publicar)
  - GET  /v2/socialActions/{urn}/comments   (leer comentarios = leads)
  - GET  /v2/me                      (perfil del autor)

La mensajería directa NO está disponible en la API pública, por lo que los
"leads" se gestionan extrayendo interacciones públicas (comentarios, reacciones,
menciones) y registrándolos en el store local.
"""
from __future__ import annotations

from typing import Any
from urllib.parse import quote

import httpx

API_BASE = "https://api.linkedin.com"
HEADERS_VERSION = {"X-Restli-Protocol-Version": "2.0.0"}


class LinkedInClient:
    def __init__(self, access_token: str, author_urn: str, timeout: float = 30.0):
        self._token = access_token
        self.author_urn = author_urn
        self._client = httpx.Client(
            base_url=API_BASE,
            timeout=timeout,
            headers={
                "Authorization": f"Bearer {access_token}",
                **HEADERS_VERSION,
            },
        )

    # ------------------------------------------------------------------ posts
    def create_text_post(self, text: str, visibility: str = "PUBLIC") -> dict[str, Any]:
        """Publica un post de texto en nombre del autor autenticado."""
        payload = {
            "author": self.author_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": text},
                    "shareMediaCategory": "NONE",
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": visibility
            },
        }
        resp = self._client.post("/v2/ugcPosts", json=payload)
        resp.raise_for_status()
        return {"id": resp.headers.get("x-restli-id") or resp.json().get("id")}

    # ------------------------------------------------------------- engagement
    def get_post_comments(self, post_urn: str) -> list[dict[str, Any]]:
        """Devuelve los comentarios de un post (fuente de leads)."""
        encoded = quote(post_urn, safe="")
        resp = self._client.get(f"/v2/socialActions/{encoded}/comments")
        resp.raise_for_status()
        return resp.json().get("elements", [])

    def get_post_likes(self, post_urn: str) -> list[dict[str, Any]]:
        encoded = quote(post_urn, safe="")
        resp = self._client.get(f"/v2/socialActions/{encoded}/likes")
        resp.raise_for_status()
        return resp.json().get("elements", [])

    # ---------------------------------------------------------------- people
    def get_profile(self, person_urn: str) -> dict[str, Any]:
        encoded = quote(person_urn, safe="")
        resp = self._client.get(f"/v2/people/{encoded}")
        resp.raise_for_status()
        return resp.json()

    def me(self) -> dict[str, Any]:
        resp = self._client.get("/v2/me")
        resp.raise_for_status()
        return resp.json()

    def close(self) -> None:
        self._client.close()
