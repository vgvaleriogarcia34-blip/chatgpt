"""Local reel generator — no APIs beyond Anthropic.

Usage:
    python scripts/make_reels.py <video path or URL>             \\
        [--clips N] [--out OUT_DIR] [--notes "audiencia, tono"]  \\
        [--skip-captions]

Outputs: OUT_DIR/reel_XX.mp4 + manifest.json + transcript.txt
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rich.logging import RichHandler

from src.config import load_settings
from src.local_pipeline import run


def _cli() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Generate short reels from a video")
    p.add_argument("source", help="Local video path or URL (YouTube, Vimeo…)")
    p.add_argument("--clips", type=int, default=None,
                   help="Number of reels to generate (default from .env)")
    p.add_argument("--out", type=Path, default=None,
                   help="Output directory (default data/renders/<id>)")
    p.add_argument("--notes", default="",
                   help="Creator notes: tone, audience, focus")
    p.add_argument("--skip-captions", action="store_true",
                   help="Do not call Claude for IG/LinkedIn captions")
    p.add_argument("-v", "--verbose", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _cli().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(message)s",
        handlers=[RichHandler(markup=True, rich_tracebacks=True)],
    )
    settings = load_settings()
    manifest = run(
        source=args.source,
        out_dir=args.out,
        clips_target=args.clips,
        notes=args.notes,
        settings=settings,
        skip_captions=args.skip_captions,
    )
    print("")
    print(f"✓ {len(manifest.reels)} reels generated in {manifest.out_dir}")
    for r in manifest.reels:
        print(f"  · {r.file}  [{r.duration_s:>4.1f}s score={r.punch_score:>3}] "
              f"{r.hook_phrase}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
