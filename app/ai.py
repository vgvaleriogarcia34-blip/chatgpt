from anthropic import Anthropic
from . import config

_client: Anthropic | None = None


def _get_client() -> Anthropic:
    global _client
    if _client is None:
        if not config.ANTHROPIC_API_KEY:
            raise RuntimeError("ANTHROPIC_API_KEY no esta configurada")
        _client = Anthropic(api_key=config.ANTHROPIC_API_KEY)
    return _client


def _email_context(msg: dict) -> str:
    sender = msg.get("from", {}).get("emailAddress", {})
    sender_str = f"{sender.get('name', '')} <{sender.get('address', '')}>"
    body = msg.get("body", {}).get("content") or msg.get("bodyPreview", "")
    return (
        f"De: {sender_str}\n"
        f"Asunto: {msg.get('subject', '(sin asunto)')}\n"
        f"Fecha: {msg.get('receivedDateTime', '')}\n\n"
        f"{body}"
    )


def analyze_email(msg: dict) -> str:
    client = _get_client()
    prompt = (
        "Analiza el siguiente correo electronico. Devuelve en espanol:\n"
        "1. Resumen breve (2-3 frases).\n"
        "2. Intencion o tipo (consulta, peticion, comercial, notificacion, etc.).\n"
        "3. Tono detectado.\n"
        "4. Acciones requeridas por mi parte (lista corta).\n"
        "5. Urgencia (alta/media/baja) con justificacion en una linea.\n\n"
        "CORREO:\n" + _email_context(msg)
    )
    resp = client.messages.create(
        model=config.ANTHROPIC_MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")


def draft_reply(msg: dict, instructions: str = "") -> str:
    client = _get_client()
    extra = f"\n\nInstrucciones adicionales del usuario: {instructions}" if instructions else ""
    prompt = (
        "Redacta un borrador de respuesta en espanol al siguiente correo. "
        "Tono profesional, claro y conciso. Devuelve UNICAMENTE el cuerpo del correo "
        "(sin asunto, sin 'De:', sin explicaciones). Incluye saludo y despedida."
        + extra
        + "\n\nCORREO ORIGINAL:\n" + _email_context(msg)
    )
    resp = client.messages.create(
        model=config.ANTHROPIC_MODEL,
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")


def draft_new_email(instructions: str) -> dict:
    client = _get_client()
    prompt = (
        "Redacta un correo electronico nuevo en espanol a partir de estas instrucciones. "
        "Devuelve EXACTAMENTE este formato, sin nada mas:\n"
        "ASUNTO: <asunto sugerido>\n"
        "---\n"
        "<cuerpo del correo con saludo y despedida>\n\n"
        f"Instrucciones: {instructions}"
    )
    resp = client.messages.create(
        model=config.ANTHROPIC_MODEL,
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}],
    )
    text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
    subject = ""
    body = text
    if "---" in text:
        head, _, body = text.partition("---")
        for line in head.splitlines():
            if line.upper().startswith("ASUNTO:"):
                subject = line.split(":", 1)[1].strip()
                break
    return {"subject": subject, "body": body.strip()}
