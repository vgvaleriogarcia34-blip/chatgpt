"""Publish a native video post on LinkedIn (UGC Posts API)."""
from __future__ import annotations

from pathlib import Path

import requests
from tenacity import retry, stop_after_attempt, wait_exponential

API = "https://api.linkedin.com/v2"
HEADERS_JSON = {
    "X-Restli-Protocol-Version": "2.0.0",
    "Content-Type": "application/json",
}


def _auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2))
def _register_upload(author_urn: str, token: str) -> dict:
    body = {
        "registerUploadRequest": {
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-video"],
            "owner": author_urn,
            "serviceRelationships": [
                {"relationshipType": "OWNER",
                 "identifier": "urn:li:userGeneratedContent"}
            ],
        }
    }
    r = requests.post(
        f"{API}/assets?action=registerUpload",
        headers={**HEADERS_JSON, **_auth(token)},
        json=body, timeout=30,
    )
    r.raise_for_status()
    return r.json()["value"]


def _upload_bytes(upload_url: str, video_path: Path, token: str) -> None:
    with video_path.open("rb") as f:
        r = requests.put(
            upload_url, data=f,
            headers={**_auth(token), "Content-Type": "application/octet-stream"},
            timeout=600,
        )
    r.raise_for_status()


def _create_ugc_post(author_urn: str, asset_urn: str, caption: str,
                     token: str) -> str:
    body = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": caption},
                "shareMediaCategory": "VIDEO",
                "media": [
                    {"status": "READY", "media": asset_urn,
                     "title": {"text": caption[:100]}}
                ],
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }
    r = requests.post(
        f"{API}/ugcPosts",
        headers={**HEADERS_JSON, **_auth(token)},
        json=body, timeout=60,
    )
    r.raise_for_status()
    return r.json().get("id") or r.headers.get("x-restli-id", "")


def publish_video(video_path: Path, caption: str, author_urn: str,
                  access_token: str) -> str:
    register = _register_upload(author_urn, access_token)
    mech = register["uploadMechanism"][
        "com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"
    ]
    upload_url = mech["uploadUrl"]
    asset_urn = register["asset"]
    _upload_bytes(upload_url, video_path, access_token)
    post_urn = _create_ugc_post(author_urn, asset_urn, caption, access_token)
    # Canonical share URL — LinkedIn resolves this to the post.
    share_id = post_urn.rsplit(":", 1)[-1]
    return f"https://www.linkedin.com/feed/update/{post_urn}" if post_urn else \
           f"https://www.linkedin.com/feed/update/urn:li:share:{share_id}"
