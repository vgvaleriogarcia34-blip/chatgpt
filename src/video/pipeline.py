"""End-to-end orchestration for a single queue row."""
from __future__ import annotations

import logging
from pathlib import Path

from src.config import Settings, CLIPS, DOWNLOADS, RENDERS
from src.copywriter import write_captions
from src.publishers import instagram as ig, linkedin as li, storage
from src.sheets.client import ClipRow, QueueRow, SheetsClient
from src.video import analyzer, downloader, transcriber
from src.video.editor import RenderOptions, render_clip

log = logging.getLogger(__name__)


def process_row(row: QueueRow, sheets: SheetsClient, settings: Settings) -> None:
    try:
        sheets.set_status(row, "DOWNLOADING")
        source = downloader.download(
            row.source_url, DOWNLOADS, settings.source_max_minutes
        )
        sheets.update_queue_fields(
            row, duration_s=source.duration_s, language=source.language
        )

        sheets.set_status(row, "TRANSCRIBING")
        transcript = transcriber.transcribe(
            source.path, settings.whisper_model, settings.whisper_device
        )
        sheets.update_queue_fields(row, language=transcript.language)

        sheets.set_status(row, "ANALYZING")
        highlights = analyzer.pick_highlights(
            transcript,
            settings.anthropic_api_key,
            settings.claude_model,
            n_clips=row.clips_target or settings.clips_per_video_default,
            min_seconds=settings.clip_min_seconds,
            max_seconds=settings.clip_max_seconds,
            extra_notes=row.notes,
        )

        sheets.set_status(row, "EDITING")
        opts = RenderOptions(
            font_path=settings.brand_font,
            color_primary=settings.brand_color_primary,
            color_text=settings.brand_color_text,
            watermark=settings.brand_watermark,
        )
        rendered: list[tuple[ClipRow, int, Path, str]] = []
        clips_dir = RENDERS / source.id
        for i, h in enumerate(highlights, start=1):
            clip_id = f"{row.id}-{i}"
            out = clips_dir / f"reel_{i:02d}.mp4"
            render_clip(source.path, h.start_s, h.end_s, transcript,
                        h.hook_phrase, out, opts)
            clip_transcript = " ".join(
                w.text for w in transcript.words_in_range(h.start_s, h.end_s)
            )
            captions = write_captions(
                h.hook_phrase, clip_transcript, source.title,
                settings.anthropic_api_key, settings.claude_model, row.notes,
            )
            clip_row = ClipRow(
                clip_id=clip_id, queue_id=row.id,
                start_s=round(h.start_s, 2), end_s=round(h.end_s, 2),
                punch_score=h.punch_score, hook_phrase=h.hook_phrase,
                ig_caption=captions.ig_caption, li_caption=captions.li_caption,
                status="RENDERED",
            )
            sheet_row = sheets.append_clip(clip_row)
            rendered.append((clip_row, sheet_row, out, source.id))

        sheets.update_queue_fields(row, clips_generated=len(rendered))

        sheets.set_status(row, "PUBLISHING")
        ig_ok, li_ok = 0, 0
        for clip_row, sheet_row, path, vid in rendered:
            try:
                key = f"reels/{vid}/{path.name}"
                public_url = storage.upload_public(path, key, settings)
                sheets.update_clip(sheet_row, render_url=public_url)
            except Exception as e:  # storage failure is fatal for IG
                sheets.update_clip(sheet_row, status="ERROR", error=f"upload: {e}")
                continue

            if settings.ig_user_id and settings.ig_access_token:
                try:
                    ig_url = ig.publish_reel(
                        settings.ig_user_id, settings.ig_access_token,
                        public_url, clip_row.ig_caption,
                    )
                    sheets.update_clip(sheet_row, ig_post_url=ig_url,
                                       status="PUBLISHED_IG")
                    ig_ok += 1
                except Exception as e:
                    sheets.update_clip(sheet_row, error=f"ig: {e}")

            if settings.li_access_token and settings.li_author_urn:
                try:
                    li_url = li.publish_video(
                        path, clip_row.li_caption,
                        settings.li_author_urn, settings.li_access_token,
                    )
                    sheets.update_clip(sheet_row, li_post_url=li_url,
                                       status="DONE")
                    li_ok += 1
                except Exception as e:
                    sheets.update_clip(sheet_row, error=f"li: {e}")

        sheets.update_queue_fields(row, ig_published=ig_ok, li_published=li_ok)
        sheets.set_status(row, "DONE")
        log.info("Queue %s: generated %d clips (IG=%d, LI=%d)",
                 row.id, len(rendered), ig_ok, li_ok)

    except Exception as e:
        log.exception("Pipeline failed for %s", row.id)
        sheets.set_status(row, "ERROR", error=str(e)[:500])
