"""Standalone pipeline that takes a local file (or URL) and produces
reels on disk, ready for manual review before publication.

No Google Sheets, no Instagram/LinkedIn APIs — only the editing stages.
"""
from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

from src.config import Settings, load_settings, RENDERS
from src.copywriter import write_captions
from src.video import analyzer, downloader, transcriber
from src.video.editor import RenderOptions, render_clip

log = logging.getLogger(__name__)


@dataclass
class ReelArtifact:
    index: int
    clip_id: str
    start_s: float
    end_s: float
    duration_s: float
    punch_score: int
    hook_phrase: str
    reason: str
    file: str
    ig_caption: str
    li_caption: str


@dataclass
class RunManifest:
    run_id: str
    source: str
    source_title: str
    source_duration_s: float
    language: str
    out_dir: str
    reels: list[ReelArtifact]


def run(
    source: str,
    out_dir: Path | None = None,
    clips_target: int | None = None,
    notes: str = "",
    settings: Settings | None = None,
    skip_captions: bool = False,
) -> RunManifest:
    """Execute the full local pipeline on `source`.

    `source` can be a local path (mp4/mov/mkv/webm...) or a remote URL
    supported by yt-dlp (YouTube, Vimeo, etc.).
    """
    settings = settings or load_settings()
    n_clips = clips_target or settings.clips_per_video_default

    log.info("[1/4] Ingesting source: %s", source)
    src = downloader.resolve(source, Path("data/downloads"),
                             settings.source_max_minutes)
    log.info("      title=%s duration=%.1fs", src.title, src.duration_s)

    log.info("[2/4] Transcribing with Whisper (%s)…", settings.whisper_model)
    transcript = transcriber.transcribe(
        src.path, settings.whisper_model, settings.whisper_device
    )
    log.info("      language=%s segments=%d",
             transcript.language, len(transcript.segments))

    log.info("[3/4] Selecting %d highlights with Claude…", n_clips)
    highlights = analyzer.pick_highlights(
        transcript,
        settings.anthropic_api_key,
        settings.claude_model,
        n_clips=n_clips,
        min_seconds=settings.clip_min_seconds,
        max_seconds=settings.clip_max_seconds,
        extra_notes=notes,
    )
    if not highlights:
        raise RuntimeError("Claude returned 0 highlights — revisa la transcripción.")
    log.info("      picked=%d (scores %s)", len(highlights),
             [h.punch_score for h in highlights])

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    final_out = (out_dir or RENDERS / src.id).resolve()
    final_out.mkdir(parents=True, exist_ok=True)

    opts = RenderOptions(
        font_path=settings.brand_font,
        color_primary=settings.brand_color_primary,
        color_text=settings.brand_color_text,
        watermark=settings.brand_watermark,
    )

    log.info("[4/4] Rendering reels to %s", final_out)
    reels: list[ReelArtifact] = []
    for i, h in enumerate(highlights, start=1):
        out_path = final_out / f"reel_{i:02d}.mp4"
        render_clip(src.path, h.start_s, h.end_s, transcript,
                    h.hook_phrase, out_path, opts)
        clip_transcript = " ".join(
            w.text for w in transcript.words_in_range(h.start_s, h.end_s)
        )
        ig_caption = li_caption = ""
        if not skip_captions:
            try:
                captions = write_captions(
                    h.hook_phrase, clip_transcript, src.title,
                    settings.anthropic_api_key, settings.claude_model, notes,
                )
                ig_caption, li_caption = captions.ig_caption, captions.li_caption
            except Exception as e:
                log.warning("Caption generation failed for clip %d: %s", i, e)

        reels.append(ReelArtifact(
            index=i,
            clip_id=f"{src.id}-{i}",
            start_s=round(h.start_s, 2),
            end_s=round(h.end_s, 2),
            duration_s=round(h.end_s - h.start_s, 2),
            punch_score=h.punch_score,
            hook_phrase=h.hook_phrase,
            reason=h.reason,
            file=out_path.name,
            ig_caption=ig_caption,
            li_caption=li_caption,
        ))
        log.info("      ✓ reel %d/%d [%s]", i, len(highlights), h.hook_phrase)

    manifest = RunManifest(
        run_id=run_id,
        source=source,
        source_title=src.title,
        source_duration_s=round(src.duration_s, 2),
        language=transcript.language,
        out_dir=str(final_out),
        reels=reels,
    )
    manifest_path = final_out / "manifest.json"
    manifest_path.write_text(
        json.dumps(asdict(manifest), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    transcript_path = final_out / "transcript.txt"
    transcript_path.write_text(transcript.full_text, encoding="utf-8")
    log.info("Done. Manifest: %s", manifest_path)
    return manifest
