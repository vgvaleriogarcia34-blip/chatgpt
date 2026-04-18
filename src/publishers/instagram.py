"""Publish a reel to Instagram via the Graph API.

Flow:
  1. POST /{ig-user-id}/media with media_type=REELS and video_url
  2. Poll GET /{creation_id}?fields=status_code until FINISHED
  3. POST /{ig-user-id}/media_publish with the creation_id
"""
from __future__ import annotations

import time

import requests
from tenacity import retry, stop_after_attempt, wait_exponential

API = "https://graph.facebook.com/v21.0"


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2))
def _post(url: str, data: dict) -> dict:
    r = requests.post(url, data=data, timeout=60)
    r.raise_for_status()
    return r.json()


def _get(url: str, params: dict) -> dict:
    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()
    return r.json()


def publish_reel(
    ig_user_id: str,
    access_token: str,
    video_url: str,
    caption: str,
    poll_timeout_s: int = 300,
) -> str:
    """Return the permalink of the published reel."""
    create = _post(
        f"{API}/{ig_user_id}/media",
        {
            "media_type": "REELS",
            "video_url": video_url,
            "caption": caption,
            "share_to_feed": "true",
            "access_token": access_token,
        },
    )
    creation_id = create["id"]

    deadline = time.time() + poll_timeout_s
    while time.time() < deadline:
        status = _get(f"{API}/{creation_id}",
                      {"fields": "status_code", "access_token": access_token})
        code = status.get("status_code")
        if code == "FINISHED":
            break
        if code == "ERROR":
            raise RuntimeError(f"IG processing failed: {status}")
        time.sleep(5)
    else:
        raise TimeoutError("Instagram did not finish processing in time")

    published = _post(
        f"{API}/{ig_user_id}/media_publish",
        {"creation_id": creation_id, "access_token": access_token},
    )
    media_id = published["id"]
    permalink = _get(f"{API}/{media_id}",
                     {"fields": "permalink", "access_token": access_token})
    return permalink.get("permalink", f"https://www.instagram.com/reel/{media_id}")
