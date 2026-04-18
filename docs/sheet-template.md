# Plantilla de la Google Sheet

La hoja se llama **ReelForge Queue** y contiene dos pestañas: `queue` y
`clips`.

## Pestaña `queue`

Una fila por video fuente. El usuario solo rellena columnas A–C; el resto las
escribe el worker.

| Col | Campo | Quién rellena | Descripción |
|-----|-------|---------------|-------------|
| A | `id` | usuario | ID libre (p.ej. `V001`). Clave primaria. |
| B | `source_url` | usuario | URL de YouTube del video fuente. |
| C | `notes` | usuario | Opcional: enfoque, tono, audiencia objetivo. |
| D | `status` | worker | PENDING / DOWNLOADING / ... / DONE / ERROR |
| E | `clips_target` | usuario | Nº deseado de reels (4–6). Default 5. |
| F | `language` | worker | Idioma detectado por Whisper. |
| G | `duration_s` | worker | Duración del video fuente. |
| H | `transcript_url` | worker | Link a `.txt` en Drive con la transcripción. |
| I | `clips_generated` | worker | Nº de reels realmente generados. |
| J | `ig_published` | worker | Nº reels publicados en Instagram. |
| K | `li_published` | worker | Nº posts publicados en LinkedIn. |
| L | `started_at` | worker | Timestamp ISO inicio. |
| M | `finished_at` | worker | Timestamp ISO fin. |
| N | `error` | worker | Mensaje de error si status=ERROR. |

## Pestaña `clips`

Una fila por reel generado. Se autogenera.

| Col | Campo | Descripción |
|-----|-------|-------------|
| A | `clip_id` | `<queue.id>-<n>` ej. `V001-3` |
| B | `queue_id` | FK a `queue.id` |
| C | `start_s` | Segundo de inicio en el video fuente |
| D | `end_s` | Segundo de fin |
| E | `duration_s` | `end_s - start_s` |
| F | `punch_score` | 0–100 (criterio del analyzer) |
| G | `hook_phrase` | La frase gancho (se usa como título) |
| H | `render_url` | URL pública del mp4 final |
| I | `ig_caption` | Caption generado para Instagram |
| J | `ig_post_url` | URL del reel publicado |
| K | `li_caption` | Caption generado para LinkedIn |
| L | `li_post_url` | URL del post publicado |
| M | `status` | RENDERED / PUBLISHED_IG / PUBLISHED_LI / DONE / ERROR |
| N | `error` | Si aplica |

## Cómo crearla

Ejecuta `python scripts/create_sheet_template.py SPREADSHEET_ID` y el script
crea las dos pestañas con las cabeceras correctas y el formato
(texto negrita, freeze de cabecera, validación de `status`).
