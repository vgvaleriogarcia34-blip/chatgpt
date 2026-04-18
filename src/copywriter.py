"""Generate captions and hashtags per platform using Claude."""
from __future__ import annotations

import json
from dataclasses import dataclass

from anthropic import Anthropic


SYSTEM_PROMPT = """You are a social-media copywriter. For a short vertical
clip, write ONE caption for Instagram and ONE for LinkedIn.

Instagram rules:
- Maximum 180 chars. First line is a hook. Allowed: 1–2 emojis.
- End with 8–12 niche hashtags in a second block.

LinkedIn rules:
- 300–600 chars. Professional, first-person, no emojis.
- Strong first line (hook) then 3–5 short lines. End with a question to
  invite comments. 3–5 hashtags (CamelCase) at the end.

Return STRICT JSON:
{"ig_caption": "string", "li_caption": "string"}"""


@dataclass
class Captions:
    ig_caption: str
    li_caption: str


def write_captions(
    hook_phrase: str,
    clip_transcript: str,
    source_title: str,
    api_key: str,
    model: str,
    notes: str = "",
) -> Captions:
    client = Anthropic(api_key=api_key)
    user = (
        f"Source video title: {source_title}\n"
        f"Hook phrase / on-screen title: {hook_phrase}\n"
        f"Creator notes: {notes or '-'}\n\n"
        "Clip transcript:\n" + clip_transcript
    )
    msg = client.messages.create(
        model=model,
        max_tokens=900,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user}],
    )
    text = "".join(b.text for b in msg.content if b.type == "text").strip()
    if "```" in text:
        text = text.split("```", 2)[1]
        if text.startswith("json"):
            text = text[4:]
    data = json.loads(text)
    return Captions(ig_caption=data["ig_caption"], li_caption=data["li_caption"])
