"""Configuración cargada desde variables de entorno."""
from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    anthropic_api_key: str
    linkedin_access_token: str
    linkedin_author_urn: str
    leads_db_path: str

    @classmethod
    def from_env(cls) -> "Config":
        missing = [
            k
            for k in ("ANTHROPIC_API_KEY", "LINKEDIN_ACCESS_TOKEN", "LINKEDIN_AUTHOR_URN")
            if not os.getenv(k)
        ]
        if missing:
            raise RuntimeError(
                f"Faltan variables de entorno requeridas: {', '.join(missing)}"
            )
        return cls(
            anthropic_api_key=os.environ["ANTHROPIC_API_KEY"],
            linkedin_access_token=os.environ["LINKEDIN_ACCESS_TOKEN"],
            linkedin_author_urn=os.environ["LINKEDIN_AUTHOR_URN"],
            leads_db_path=os.getenv("LEADS_DB_PATH", "./leads.sqlite3"),
        )
