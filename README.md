# Outlook AI Assistant

Aplicación web local que conecta con tu cuenta de Outlook (Microsoft 365 / outlook.com), te muestra los correos recibidos, los pasa a una IA (Anthropic Claude) para analizarlos y te ayuda a redactar respuestas o correos nuevos, que luego puedes enviar desde tu propia cuenta.

## Características

- Login con Microsoft (OAuth2 / Microsoft Graph)
- Listado de bandeja de entrada
- Análisis de correos con Claude (resumen, intención, urgencia, acciones)
- Generación de borradores de respuesta con instrucciones personalizadas
- Envío de respuestas y de correos nuevos desde tu cuenta

## Requisitos previos

1. **Python 3.10+**
2. **Cuenta de Microsoft** (personal o corporativa)
3. **Registro de app en Azure**:
   - Ve a https://portal.azure.com → Azure Active Directory → App registrations → New registration
   - Tipo de cuenta: *"Accounts in any organizational directory and personal Microsoft accounts"*
   - Redirect URI (tipo **Web**): `http://localhost:8000/auth/callback`
   - Tras crear la app, anota el **Application (client) ID** → `MS_CLIENT_ID`
   - En *Certificates & secrets* → New client secret → copia el **value** → `MS_CLIENT_SECRET`
   - En *API permissions* → Add a permission → Microsoft Graph → **Delegated**:
     - `Mail.Read`
     - `Mail.Send`
     - `User.Read`
     - `offline_access`
   - (Si tu cuenta es corporativa, pulsa *Grant admin consent*)
4. **API key de Anthropic**: https://console.anthropic.com

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edita .env y rellena MS_CLIENT_ID, MS_CLIENT_SECRET, ANTHROPIC_API_KEY, SESSION_SECRET
```

## Ejecutar

```bash
uvicorn app.main:app --reload --port 8000
```

Abre http://localhost:8000 y pulsa *Iniciar sesión con Microsoft*.

## Uso

1. Tras iniciar sesión, verás tu bandeja de entrada.
2. Pulsa cualquier correo para abrirlo.
3. **Analizar con IA**: genera resumen, intención, tono, acciones y urgencia.
4. **Generar borrador**: redacta una respuesta editable (puedes dar instrucciones extra, p.ej. *"tono más formal"*, *"propón reunión el martes"*).
5. Edita el borrador y pulsa **Enviar respuesta**.
6. Para un correo nuevo desde cero, usa **✏️ Nuevo correo**: describe lo que quieres decir y la IA generará asunto + cuerpo.

## Estructura

```
app/
  main.py        # Rutas FastAPI
  auth.py        # OAuth2 con MSAL
  graph.py       # Llamadas a Microsoft Graph (inbox, send, reply)
  ai.py          # Integración con Claude
  config.py      # Carga de variables de entorno
  templates/     # HTML (Jinja2)
```

## Notas de seguridad

- El token se guarda en una cookie de sesión firmada. Cambia `SESSION_SECRET` por un valor largo y aleatorio.
- No subas tu `.env` al repositorio (ya está en `.gitignore`).
- Esta app está pensada para uso local. Si la despliegas en Internet añade HTTPS y revisa los redirect URIs en Azure.
