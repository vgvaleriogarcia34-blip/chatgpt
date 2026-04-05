# Agente autónomo de LinkedIn

Agente construido sobre el [Claude Agent SDK](https://docs.anthropic.com/en/api/agent-sdk)
que publica contenido en LinkedIn y gestiona los leads generados a partir de las
interacciones públicas (comentarios y likes) del perfil autenticado.

## Capacidades

- Publicar posts de texto en el perfil del autor (`UGC Posts` API).
- Recuperar el engagement de un post (comentarios y likes).
- Convertir cada interacción pública en un lead y almacenarlo en SQLite.
- Puntuar leads (0-100) y actualizar su estado (`new → contacted → qualified | lost`).
- Ejecutarse en modo one-shot o en bucle con cadencia configurable.

> La API pública de LinkedIn **no permite enviar mensajes privados**. Por
> diseño, el agente sólo opera sobre señales públicas y gestión interna del
> pipeline de leads. Cualquier contacto directo debe hacerlo un humano.

## Instalación

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # y rellena las credenciales
```

Necesitas:

- `ANTHROPIC_API_KEY`
- `LINKEDIN_ACCESS_TOKEN` con scopes `w_member_social`, `r_liteprofile`
- `LINKEDIN_AUTHOR_URN` (ej. `urn:li:person:xxxx`)

## Uso

Ejecución puntual:

```bash
python main.py "Publica un post sobre IA aplicada a ventas B2B y cualifica los comentarios que lleguen"
```

Bucle autónomo (cada 1h):

```bash
python main.py --loop 3600 "Mantén 1 post diario y cualifica los nuevos leads"
```

## Arquitectura

```
linkedin_agent/
├── agent.py           # Orquestación con Claude Agent SDK
├── tools.py           # Tools MCP expuestas al modelo
├── linkedin_client.py # Cliente HTTP de la API REST de LinkedIn
├── leads_store.py     # Persistencia SQLite de posts y leads
└── config.py          # Carga de configuración desde .env
```

El modelo (`claude-opus-4-6`) decide autónomamente cuándo llamar a cada tool
guiado por el objetivo en lenguaje natural y el system prompt de `agent.py`.
