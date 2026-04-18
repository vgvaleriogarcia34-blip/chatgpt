"""Upload a local file to Cloudflare R2 (S3-compatible) and return a
public URL — Instagram Graph API requires a reachable URL."""
from __future__ import annotations

from pathlib import Path

import boto3
from botocore.config import Config

from src.config import Settings


def upload_public(path: Path, key: str, settings: Settings) -> str:
    endpoint = f"https://{settings.r2_account_id}.r2.cloudflarestorage.com"
    s3 = boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=settings.r2_access_key,
        aws_secret_access_key=settings.r2_secret_key,
        config=Config(signature_version="s3v4"),
    )
    s3.upload_file(
        str(path), settings.r2_bucket, key,
        ExtraArgs={"ContentType": "video/mp4", "ACL": "public-read"},
    )
    base = settings.r2_public_base.rstrip("/")
    return f"{base}/{key}"
