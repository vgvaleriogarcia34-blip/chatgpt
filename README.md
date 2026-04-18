# ReelForge — Automatización de Reels desde YouTube a Instagram + LinkedIn

ReelForge es un pipeline que, a partir de un enlace de YouTube pegado en una
Google Sheet, descarga el video, identifica las frases con más gancho usando
Claude, corta de 4 a 6 clips verticales (~50 s), les añade subtítulos quemados
y un título llamativo, y los publica automáticamente en Instagram Reels y
LinkedIn. Cada fila de la hoja se va rellenando con el estado, los títulos,
los enlaces públicos y las métricas conforme avanza el proceso.

Está pensado para empaquetarse como **producto SaaS por suscripción** (ver
`docs/marketing-plan.md`).

## Flujo de alto nivel

```
Google Sheet (URL YouTube)
        │
        ▼
 worker.py (polling cada 60s)
        │
        ▼
 ┌──────────────────────────────────────────────┐
 │ 1. downloader  (yt-dlp) → MP4 local          │
 │ 2. transcriber (Whisper) → segmentos + texto │
 │ 3. analyzer    (Claude) → 4–6 highlights     │
 │ 4. editor      (ffmpeg) → vertical 9:16,     │
 │                subtítulos, título, branding  │
 │ 5. copywriter  (Claude) → caption + hashtags │
 │ 6. publishers  → Instagram Graph + LinkedIn  │
 │ 7. sheets      → rellena columnas + estado   │
 └──────────────────────────────────────────────┘
```

## Estructura del repositorio

```
.
├── docs/
│   ├── architecture.md      Diseño técnico detallado
│   ├── setup.md             Cómo arrancar local/servidor
│   ├── sheet-template.md    Plantilla de la Google Sheet
│   ├── marketing-plan.md    Plan de marketing + SaaS
│   └── pricing.md           Tiers de suscripción
├── src/
│   ├── config.py
│   ├── sheets/client.py
│   ├── video/
│   │   ├── downloader.py
│   │   ├── transcriber.py
│   │   ├── analyzer.py
│   │   ├── editor.py
│   │   └── pipeline.py
│   ├── copywriter.py
│   ├── publishers/
│   │   ├── instagram.py
│   │   └── linkedin.py
│   └── worker.py
├── scripts/
│   ├── run_once.py
│   └── create_sheet_template.py
├── assets/fonts/            Tipografías para los subtítulos
├── data/                    Cache de descargas y renders
├── requirements.txt
└── .env.example
```

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env           # rellena las claves
python scripts/create_sheet_template.py   # imprime plantilla de Sheet
python src/worker.py           # arranca el polling
```

Lee `docs/setup.md` para la configuración completa (credenciales de Google,
Instagram Graph, LinkedIn y Anthropic).
