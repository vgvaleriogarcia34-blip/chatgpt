import secrets
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from . import auth, graph, ai, config

app = FastAPI(title="Outlook AI Assistant")
app.add_middleware(SessionMiddleware, secret_key=config.SESSION_SECRET, max_age=60 * 60 * 8)
templates = Jinja2Templates(directory="app/templates")


async def _get_token(request: Request) -> str:
    cache_str = request.session.get("token_cache")
    if not cache_str:
        raise HTTPException(status_code=401, detail="No autenticado")
    token, new_cache = auth.acquire_token_silent(cache_str)
    request.session["token_cache"] = new_cache
    if not token:
        raise HTTPException(status_code=401, detail="Sesion expirada")
    return token


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    if not request.session.get("token_cache"):
        return templates.TemplateResponse("login.html", {"request": request})
    return RedirectResponse("/inbox", status_code=303)


@app.get("/auth/login")
async def login(request: Request):
    state = secrets.token_urlsafe(16)
    request.session["oauth_state"] = state
    return RedirectResponse(auth.build_auth_url(state))


@app.get("/auth/callback")
async def callback(request: Request, code: str = "", state: str = "", error: str = "", error_description: str = ""):
    if error:
        return HTMLResponse(f"<h3>Error de autenticacion: {error}</h3><p>{error_description}</p>", status_code=400)
    if state != request.session.get("oauth_state"):
        raise HTTPException(status_code=400, detail="Estado OAuth invalido")
    try:
        result = auth.exchange_code(code)
    except Exception as e:
        return HTMLResponse(f"<h3>Error: {e}</h3>", status_code=400)
    request.session["token_cache"] = result["cache"]
    return RedirectResponse("/inbox", status_code=303)


@app.get("/auth/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)


@app.get("/inbox", response_class=HTMLResponse)
async def inbox(request: Request):
    token = await _get_token(request)
    me = await graph.get_me(token)
    messages = await graph.list_inbox(token, top=25)
    return templates.TemplateResponse(
        "inbox.html",
        {"request": request, "me": me, "messages": messages},
    )


@app.get("/message/{message_id}", response_class=HTMLResponse)
async def view_message(request: Request, message_id: str):
    token = await _get_token(request)
    msg = await graph.get_message(token, message_id)
    return templates.TemplateResponse(
        "message.html",
        {"request": request, "msg": msg, "analysis": None, "draft": None},
    )


@app.post("/message/{message_id}/analyze", response_class=HTMLResponse)
async def analyze(request: Request, message_id: str):
    token = await _get_token(request)
    msg = await graph.get_message(token, message_id)
    try:
        analysis = ai.analyze_email(msg)
    except Exception as e:
        analysis = f"Error IA: {e}"
    return templates.TemplateResponse(
        "message.html",
        {"request": request, "msg": msg, "analysis": analysis, "draft": None},
    )


@app.post("/message/{message_id}/draft", response_class=HTMLResponse)
async def draft(request: Request, message_id: str, instructions: str = Form("")):
    token = await _get_token(request)
    msg = await graph.get_message(token, message_id)
    try:
        draft_text = ai.draft_reply(msg, instructions)
    except Exception as e:
        draft_text = f"Error IA: {e}"
    return templates.TemplateResponse(
        "message.html",
        {"request": request, "msg": msg, "analysis": None, "draft": draft_text, "instructions": instructions},
    )


@app.post("/message/{message_id}/send-reply")
async def send_reply(request: Request, message_id: str, body: str = Form(...)):
    token = await _get_token(request)
    try:
        await graph.reply_mail(token, message_id, body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return RedirectResponse("/inbox?sent=1", status_code=303)


@app.get("/compose", response_class=HTMLResponse)
async def compose_form(request: Request):
    await _get_token(request)
    return templates.TemplateResponse(
        "compose.html",
        {"request": request, "subject": "", "body": "", "to": "", "cc": "", "instructions": ""},
    )


@app.post("/compose/draft", response_class=HTMLResponse)
async def compose_draft(
    request: Request,
    instructions: str = Form(...),
    to: str = Form(""),
    cc: str = Form(""),
):
    await _get_token(request)
    try:
        draft = ai.draft_new_email(instructions)
    except Exception as e:
        draft = {"subject": "", "body": f"Error IA: {e}"}
    return templates.TemplateResponse(
        "compose.html",
        {
            "request": request,
            "subject": draft["subject"],
            "body": draft["body"],
            "to": to,
            "cc": cc,
            "instructions": instructions,
        },
    )


@app.post("/compose/send")
async def compose_send(
    request: Request,
    to: str = Form(...),
    cc: str = Form(""),
    subject: str = Form(...),
    body: str = Form(...),
):
    token = await _get_token(request)
    to_list = [a.strip() for a in to.split(",") if a.strip()]
    cc_list = [a.strip() for a in cc.split(",") if a.strip()]
    if not to_list:
        raise HTTPException(status_code=400, detail="Falta destinatario")
    try:
        await graph.send_mail(token, to_list, subject, body, cc_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return RedirectResponse("/inbox?sent=1", status_code=303)
