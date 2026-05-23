import httpx
from .config import GRAPH_BASE


async def _headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}", "Accept": "application/json"}


async def get_me(token: str) -> dict:
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(f"{GRAPH_BASE}/me", headers=await _headers(token))
        r.raise_for_status()
        return r.json()


async def list_inbox(token: str, top: int = 20) -> list[dict]:
    params = {
        "$top": str(top),
        "$select": "id,subject,from,receivedDateTime,bodyPreview,isRead",
        "$orderby": "receivedDateTime desc",
    }
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(
            f"{GRAPH_BASE}/me/mailFolders/Inbox/messages",
            headers=await _headers(token),
            params=params,
        )
        r.raise_for_status()
        return r.json().get("value", [])


async def get_message(token: str, message_id: str) -> dict:
    params = {"$select": "id,subject,from,toRecipients,receivedDateTime,body,bodyPreview,conversationId"}
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(
            f"{GRAPH_BASE}/me/messages/{message_id}",
            headers=await _headers(token),
            params=params,
        )
        r.raise_for_status()
        return r.json()


async def send_mail(token: str, to: list[str], subject: str, body: str, cc: list[str] | None = None) -> None:
    payload = {
        "message": {
            "subject": subject,
            "body": {"contentType": "Text", "content": body},
            "toRecipients": [{"emailAddress": {"address": a}} for a in to],
            "ccRecipients": [{"emailAddress": {"address": a}} for a in (cc or [])],
        },
        "saveToSentItems": True,
    }
    headers = await _headers(token)
    headers["Content-Type"] = "application/json"
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(f"{GRAPH_BASE}/me/sendMail", headers=headers, json=payload)
        if r.status_code >= 400:
            raise RuntimeError(f"sendMail failed: {r.status_code} {r.text}")


async def reply_mail(token: str, message_id: str, body: str) -> None:
    payload = {"comment": body}
    headers = await _headers(token)
    headers["Content-Type"] = "application/json"
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(
            f"{GRAPH_BASE}/me/messages/{message_id}/reply",
            headers=headers,
            json=payload,
        )
        if r.status_code >= 400:
            raise RuntimeError(f"reply failed: {r.status_code} {r.text}")
