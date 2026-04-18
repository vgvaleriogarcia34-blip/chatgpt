# ReelForge — De video largo a reels listos para publicar

Pipeline que convierte **cualquier video** (archivo local o URL de YouTube /
Vimeo) en 4–6 clips verticales (~50 s) con subtítulos quemados, título
gancho y watermark — listos para revisar antes de subirlos a Instagram o
LinkedIn.

> **Fase actual**: edición local. La publicación automática a redes está
> implementada pero desactivada hasta que conectes las credenciales.

## TL;DR (modo local)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
echo "ANTHROPIC_API_KEY=sk-ant-…" > .env

# procesa un archivo local:
python scripts/make_reels.py inbox/mi_video.mp4

# o una URL:
python scripts/make_reels.py https://youtu.be/XXXXXXX --clips 6 \
    --notes "audiencia B2B, tono cercano"
```

Los mp4 finales + `manifest.json` + `transcript.txt` quedan en
`data/renders/<id>/`.

Alternativa: arranca un *watcher* y deja videos en `inbox/`:

```bash
python scripts/watch_inbox.py
```

## Qué hace, paso a paso

```
video (path|URL)
   └─► ingest       (yt-dlp o copia local)
   └─► transcribe   (faster-whisper, timestamps por palabra)
   └─► analyze      (Claude → 4–6 highlights con "hook phrase")
   └─► render       (ffmpeg → 1080×1920, subs ASS, título, watermark)
   └─► manifest     (json con duración, score, captions IG/LinkedIn)
```

## Agentes que gestionan el proyecto

En `.claude/agents/` hay tres subagentes que puedes invocar desde Claude
Code para que automaticen el flujo:

| Agente | Rol |
|--------|-----|
| `reel-producer` | Project manager. Recibe la orden de alto nivel y delega. |
| `reel-orchestrator` | Ejecuta el pipeline completo (ingest → render). |
| `reel-qa` | Audita los mp4 generados y decide si son publicables. |

Ejemplo de uso en Claude Code:

> "Procesa `inbox/podcast.mp4`, saca 5 reels para audiencia B2B."

Claude llamará a `reel-producer`, que a su vez invoca a `reel-orchestrator`
y cuando termine a `reel-qa`, y te devuelve un informe compacto.

## Estructura del repo

```
.
├── inbox/                     Dropa aquí videos para procesarlos
├── data/
│   ├── downloads/             Fuentes normalizadas
│   └── renders/<id>/          mp4 finales + manifest.json + transcript.txt
├── scripts/
│   ├── make_reels.py          CLI principal (un video → reels)
│   ├── watch_inbox.py         Daemon que vigila inbox/
│   ├── run_once.py            Usa la Google Sheet (fase 2)
│   └── create_sheet_template.py
├── src/
│   ├── local_pipeline.py      Pipeline sin dependencias de Sheets/APIs
│   ├── video/
│   │   ├── downloader.py      local o URL
│   │   ├── transcriber.py     faster-whisper
│   │   ├── analyzer.py        Claude → highlights
│   │   └── editor.py          ffmpeg vertical 9:16 + subs + título
│   ├── copywriter.py          Claude → IG/LinkedIn captions
│   ├── publishers/            ⚠ fase 2 (IG Graph + LinkedIn UGC)
│   └── sheets/                ⚠ fase 2 (Google Sheets como control panel)
├── .claude/agents/            Subagentes de Claude Code
├── docs/                      architecture / setup / marketing plan / pricing
├── requirements.txt
└── .env.example
```

## Requisitos

- Python 3.11+
- `ffmpeg` 6+ y `ffprobe` en el PATH
- Una API key de Anthropic (para análisis + copywriting)
- GPU opcional — Whisper también funciona en CPU

No necesitas ninguna credencial de Google, Instagram o LinkedIn para la
fase local.

## Fase 2 (cuando tú decidas)

1. Das de alta las credenciales en `.env` (ver `docs/setup.md`).
2. Arrancas `src/worker.py` o usas `scripts/run_once.py`.
3. El mismo flujo, pero además:
   - sube los mp4 a Cloudflare R2 / S3
   - publica en Instagram Reels y LinkedIn
   - va escribiendo en la Google Sheet URL de cada post.

Plan de monetización y tiers de suscripción en `docs/marketing-plan.md` y
`docs/pricing.md`.
