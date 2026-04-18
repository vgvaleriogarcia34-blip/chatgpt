"""Select the most powerful ~50-second moments of a video using Claude."""
from __future__ import annotations

import json
from dataclasses import dataclass

from anthropic import Anthropic

from src.video.transcriber import Transcript


SYSTEM_PROMPT = """You are a social-media video editor. Given a timestamped
transcript, you must pick the best standalone moments that could be turned
into short vertical clips (Instagram Reels / LinkedIn video).

Rules for each clip:
- Duration between {min_s} and {max_s} seconds (hard cap 90).
- Must start at a natural sentence boundary.
- Must contain one "hook_phrase" that works as on-screen title — punchy,
  <=70 chars, no quotes, no emoji.
- Must stand alone: understandable without the rest of the video.
- Clips must NOT overlap.
- Prefer moments with: counter-intuitive claims, strong opinions, numeric
  proofs, emotional peaks, concrete stories.

Return STRICT JSON of the form:
{{"clips": [
  {{"start_s": float, "end_s": float, "hook_phrase": "string",
    "punch_score": int 0-100, "reason": "short why"}}
]}}

Return exactly {n} clips, sorted by punch_score desc."""


@dataclass
class Highlight:
    start_s: float
    end_s: float
    hook_phrase: str
    punch_score: int
    reason: str


def pick_highlights(
    transcript: Transcript,
    api_key: str,
    model: str,
    n_clips: int,
    min_seconds: int,
    max_seconds: int,
    extra_notes: str = "",
) -> list[Highlight]:
    client = Anthropic(api_key=api_key)
    system = SYSTEM_PROMPT.format(n=n_clips, min_s=min_seconds, max_s=max_seconds)
    user = (
        f"Transcript language: {transcript.language}\n"
        f"Creator notes (may be empty): {extra_notes or '-'}\n\n"
        "TRANSCRIPT:\n" + transcript.timecoded_text()
    )
    msg = client.messages.create(
        model=model,
        max_tokens=2000,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    text = "".join(b.text for b in msg.content if b.type == "text").strip()
    data = _extract_json(text)
    highlights = [Highlight(**c) for c in data["clips"]]
    return _dedupe_sorted(highlights)


def _extract_json(text: str) -> dict:
    # Claude is usually clean, but fence-guard just in case.
    if "```" in text:
        text = text.split("```", 2)[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text)


def _dedupe_sorted(hs: list[Highlight]) -> list[Highlight]:
    hs = sorted(hs, key=lambda h: -h.punch_score)
    kept: list[Highlight] = []
    for h in hs:
        if any(_overlap(h, k) for k in kept):
            continue
        kept.append(h)
    return kept


def _overlap(a: Highlight, b: Highlight) -> bool:
    return not (a.end_s <= b.start_s or b.end_s <= a.start_s)
