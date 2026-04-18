# Arquitectura técnica

## Componentes

| Componente | Responsabilidad | Tecnología |
|------------|-----------------|------------|
| `sheets.client` | Lee/escribe la Google Sheet | gspread + service account |
| `video.downloader` | Descarga el video fuente | yt-dlp |
| `video.transcriber` | Transcripción con timestamps | faster-whisper (local) u OpenAI Whisper API |
| `video.analyzer` | Selecciona los highlights | Anthropic Claude (claude-sonnet-4-6) |
| `video.editor` | Corte, vertical 9:16, subtítulos ASS, título | ffmpeg |
| `copywriter` | Caption + hashtags por plataforma | Anthropic Claude |
| `publishers.instagram` | Sube reel y publica | Instagram Graph API |
| `publishers.linkedin` | Sube video y publica | LinkedIn Marketing API |
| `worker` | Bucle que lee pendientes y orquesta | Python asyncio |

## Estados de cada fila

`PENDING → DOWNLOADING → TRANSCRIBING → ANALYZING → EDITING → PUBLISHING → DONE`

Cualquier fallo pasa a `ERROR` con el mensaje en la columna `error`.

## Selección de highlights

Se pasa a Claude la transcripción con timestamps y se pide un JSON con N
clips (4–6) cumpliendo estas reglas:

- Duración objetivo 40–60 s (hard limit 90 s).
- Empezar en un corte natural (inicio de frase).
- Contener una "frase gancho" que se mostrará como título.
- No solaparse entre sí.
- Ordenados por `punch_score` (0–100).

Prompt completo en `src/video/analyzer.py`.

## Render

1. Cortar el fragmento (`ffmpeg -ss -to -c copy` + re-encode si hace falta).
2. Escalar/crop a 1080×1920 (centrado, con blur de fondo si el original es
   horizontal).
3. Generar subtítulos `.ass` a partir del segmento de Whisper, con estilo
   grande, negrita, contorno y resaltado de palabras.
4. Quemar los subtítulos (`-vf "ass=clip.ass"`).
5. Superponer el título (2 líneas máx, bloque con margen inferior o superior
   según el layout).
6. Añadir watermark / handle del creador (opcional).

## Publicación

### Instagram
1. `POST /{ig-user-id}/media` con `media_type=REELS`, `video_url` (enlace
   público temporal — subimos antes a S3/Cloudflare R2).
2. Esperar a `status_code=FINISHED`.
3. `POST /{ig-user-id}/media_publish` con el `creation_id`.

### LinkedIn
1. `registerUpload` en `/rest/assets?action=registerUpload`.
2. PUT binario al `uploadUrl`.
3. `POST /rest/posts` con el asset y el texto.

## Almacenamiento intermedio

- `data/downloads/<video_id>.mp4` — fuente
- `data/clips/<video_id>/clip_<n>.mp4` — cortes
- `data/renders/<video_id>/reel_<n>.mp4` — render final
- `data/logs/<run_id>.log` — traza por ejecución

Los renders finales se suben a un bucket (S3/R2) para obtener URL pública
requerida por Instagram Graph.

## Escalabilidad (cuando pase a SaaS)

- Worker pasa a Celery/RQ con Redis.
- Render en cola dedicada con GPU (Whisper-large + ffmpeg NVENC).
- Un tenant = una Google Sheet + sus credenciales cifradas en DB (Postgres).
- Frontend en Next.js para onboarding, billing (Stripe) y OAuth de Instagram
  / LinkedIn.
