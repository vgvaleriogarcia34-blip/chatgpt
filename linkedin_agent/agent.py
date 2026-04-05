"""Bucle autónomo del agente de LinkedIn usando el Claude Agent SDK."""
from __future__ import annotations

import asyncio
from dataclasses import dataclass

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    TextBlock,
    ToolResultBlock,
    ToolUseBlock,
    create_sdk_mcp_server,
)

from .config import Config
from .leads_store import LeadsStore
from .linkedin_client import LinkedInClient
from .tools import build_tools


SYSTEM_PROMPT = """Eres un agente de growth especializado en LinkedIn. Tu objetivo
es hacer crecer la presencia del autor y generar leads cualificados de forma
autónoma y ética.

Debes:
1. Proponer y publicar contenido de alto valor (posts profesionales en
   español, 900-1800 caracteres, sin spam, sin emojis salvo que aporten).
2. Tras publicar, recuperar el engagement del post con fetch_engagement.
3. Revisar los comentarios y likes, puntuar cada lead con score_lead (0-100)
   según su potencial (rol, empresa, mensaje, intent).
4. Priorizar los leads con mayor score, marcarlos como 'qualified' cuando
   muestren interés claro y anotar en notes por qué.
5. Nunca enviar mensajes privados (la API no lo permite): limítate a la
   gestión pública y al scoring.

Trabaja en ciclos cortos: planifica, ejecuta con tools, evalúa resultados.
Si falta información, razona con los datos disponibles antes de pedir ayuda.
"""


@dataclass
class AgentRuntime:
    config: Config
    client: LinkedInClient
    store: LeadsStore

    @classmethod
    def from_env(cls) -> "AgentRuntime":
        cfg = Config.from_env()
        return cls(
            config=cfg,
            client=LinkedInClient(cfg.linkedin_access_token, cfg.linkedin_author_urn),
            store=LeadsStore(cfg.leads_db_path),
        )

    def close(self) -> None:
        self.client.close()


async def run_agent(objective: str, *, runtime: AgentRuntime | None = None) -> None:
    """Ejecuta el agente contra un objetivo en lenguaje natural."""
    owns_runtime = runtime is None
    runtime = runtime or AgentRuntime.from_env()

    tools = build_tools(runtime.client, runtime.store)
    server = create_sdk_mcp_server(name="linkedin", version="0.1.0", tools=tools)

    tool_names = [
        "mcp__linkedin__publish_post",
        "mcp__linkedin__list_my_posts",
        "mcp__linkedin__fetch_engagement",
        "mcp__linkedin__score_lead",
        "mcp__linkedin__update_lead_status",
        "mcp__linkedin__list_leads",
    ]

    options = ClaudeAgentOptions(
        system_prompt=SYSTEM_PROMPT,
        mcp_servers={"linkedin": server},
        allowed_tools=tool_names,
        model="claude-opus-4-6",
    )

    try:
        async with ClaudeSDKClient(options=options) as claude:
            await claude.query(objective)
            async for message in claude.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            print(block.text)
                        elif isinstance(block, ToolUseBlock):
                            print(f"🔧 tool → {block.name} {block.input}")
                        elif isinstance(block, ToolResultBlock):
                            print(f"✅ result ← {block.content}")
    finally:
        if owns_runtime:
            runtime.close()


async def run_loop(objective: str, interval_seconds: int = 3600) -> None:
    """Ejecuta el agente en bucle, pausando entre iteraciones."""
    runtime = AgentRuntime.from_env()
    try:
        while True:
            await run_agent(objective, runtime=runtime)
            await asyncio.sleep(interval_seconds)
    finally:
        runtime.close()
