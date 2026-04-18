# Setup

## 1. Requisitos del sistema

- Python 3.11+
- `ffmpeg` 6+ (`apt install ffmpeg` / `brew install ffmpeg`)
- `yt-dlp` (se instala vía pip)
- Opcional: GPU NVIDIA para Whisper-large y NVENC
- Una cuenta de Google Cloud, una cuenta de Meta Developers y una de LinkedIn
  Developers.

## 2. Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## 3. Credenciales

### 3.1 Google Sheets + Drive
1. Crea un proyecto en Google Cloud Console.
2. Habilita **Google Sheets API** y **Google Drive API**.
3. Crea una *Service Account*, genera una key JSON.
4. Guárdala como `secrets/google-sa.json`.
5. Comparte tu Google Sheet con el email de la service account (permiso
   editor).
6. Copia el Spreadsheet ID en `.env` (`SPREADSHEET_ID`).

### 3.2 Anthropic
- Crea una API key en <https://console.anthropic.com>.
- `ANTHROPIC_API_KEY=...` en `.env`.

### 3.3 Instagram Graph API
Requiere una cuenta **Business** o **Creator** de Instagram vinculada a una
Página de Facebook.
1. Crea una App en Meta Developers.
2. Activa el producto *Instagram Graph API*.
3. Genera un token de usuario de larga duración con permisos
   `instagram_basic`, `instagram_content_publish`, `pages_show_list`,
   `pages_read_engagement`.
4. Obtén el `ig_user_id` y configúralo en `.env` junto con `IG_ACCESS_TOKEN`.

### 3.4 LinkedIn
1. Crea una App en <https://www.linkedin.com/developers>.
2. Solicita el producto *Share on LinkedIn* y *Marketing Developer Platform*
   si quieres publicar en páginas de empresa.
3. OAuth flow con scopes `w_member_social`, `r_liteprofile`,
   `w_organization_social` (si publicas en página).
4. Guarda `LI_ACCESS_TOKEN` y `LI_AUTHOR_URN` (`urn:li:person:XXXX` o
   `urn:li:organization:XXXX`) en `.env`.

### 3.5 Storage público (para Instagram)
Instagram necesita una URL pública del mp4. Usa Cloudflare R2 o AWS S3:

```env
R2_ACCOUNT_ID=...
R2_BUCKET=reelforge
R2_ACCESS_KEY=...
R2_SECRET_KEY=...
R2_PUBLIC_BASE=https://cdn.tu-dominio.com
```

## 4. Crear la Sheet

```bash
python scripts/create_sheet_template.py $SPREADSHEET_ID
```

## 5. Primer video de prueba

1. Añade una fila en la pestaña `queue` con tu URL de YouTube.
2. Lanza:
   ```bash
   python scripts/run_once.py
   ```
3. Revisa `data/renders/<video_id>/` y la pestaña `clips`.

## 6. Modo producción

```bash
python src/worker.py
```

Polling cada 60 segundos. Procesa la primera fila en `PENDING`.

Systemd unit de ejemplo en `docs/deployment/reelforge.service` (se añadirá en
la fase 2 del proyecto).
