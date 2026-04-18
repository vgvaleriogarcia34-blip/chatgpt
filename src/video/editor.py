"""Render vertical 9:16 reels with burnt subtitles, title and watermark."""
from __future__ import annotations

import subprocess
import textwrap
from dataclasses import dataclass
from pathlib import Path

from src.video.transcriber import Transcript, Word


@dataclass
class RenderOptions:
    font_path: Path
    color_primary: str
    color_text: str
    watermark: str


def _hex_to_ass(hex_color: str) -> str:
    """Convert #RRGGBB to ASS &HBBGGRR& (opaque)."""
    h = hex_color.lstrip("#")
    r, g, b = h[0:2], h[2:4], h[4:6]
    return f"&H00{b}{g}{r}".upper()


def _ass_timestamp(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"


def build_ass(words: list[Word], out_path: Path, opts: RenderOptions,
              max_chars_per_line: int = 22) -> None:
    """Simple karaoke-ish subtitle file: show 3–4 words at a time, highlighted."""
    primary = _hex_to_ass(opts.color_text)
    accent = _hex_to_ass(opts.color_primary)
    outline = "&H00000000"

    header = textwrap.dedent(f"""\
        [Script Info]
        ScriptType: v4.00+
        PlayResX: 1080
        PlayResY: 1920
        ScaledBorderAndShadow: yes

        [V4+ Styles]
        Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
        Style: Base,Inter,72,{primary},{primary},{outline},{outline},1,0,0,0,100,100,0,0,1,5,0,2,60,60,260,1
        Style: Hot,Inter,72,{accent},{accent},{outline},{outline},1,0,0,0,100,100,0,0,1,5,0,2,60,60,260,1

        [Events]
        Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
        """)

    lines: list[str] = []
    group: list[Word] = []
    group_len = 0
    for w in words:
        if group_len + len(w.text) > max_chars_per_line and group:
            lines.append(_group_to_ass_line(group))
            group, group_len = [], 0
        group.append(w)
        group_len += len(w.text) + 1
    if group:
        lines.append(_group_to_ass_line(group))

    out_path.write_text(header + "\n".join(lines), encoding="utf-8")


def _group_to_ass_line(group: list[Word]) -> str:
    start = _ass_timestamp(group[0].start)
    end = _ass_timestamp(group[-1].end)
    text = " ".join(w.text.strip() for w in group)
    return f"Dialogue: 0,{start},{end},Base,,0,0,0,,{text}"


def render_clip(
    source: Path,
    start_s: float,
    end_s: float,
    transcript: Transcript,
    hook_phrase: str,
    out_path: Path,
    opts: RenderOptions,
) -> None:
    """Cut, rescale to 1080x1920, burn subs + title + watermark."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    ass_path = out_path.with_suffix(".ass")
    words = transcript.words_in_range(start_s, end_s)
    build_ass(words, ass_path, opts)

    font_arg = opts.font_path.as_posix()
    title_escaped = hook_phrase.replace("'", r"\'").replace(":", r"\:")
    watermark = opts.watermark.replace("'", r"\'").replace(":", r"\:")

    duration = max(0.1, end_s - start_s)
    # Vertical layout: blurred bg + centered video + title top + watermark bottom.
    # Subtitles were built with timeline of the *clip* (0..duration),
    # so we seek the source first and let the filter graph work on t=0.
    vf = (
        "[0:v]split=2[main][bg];"
        "[bg]scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,boxblur=40:1[bgb];"
        "[main]scale=1080:-2[fg];"
        "[bgb][fg]overlay=(W-w)/2:(H-h)/2[base];"
        f"[base]ass={ass_path.as_posix()}[subbed];"
        f"[subbed]drawtext=fontfile='{font_arg}':text='{title_escaped}':"
        "fontsize=64:fontcolor=white:borderw=6:bordercolor=black:"
        "x=(w-text_w)/2:y=160:box=1:boxcolor=black@0.35:boxborderw=20[titled];"
        f"[titled]drawtext=fontfile='{font_arg}':text='{watermark}':"
        "fontsize=36:fontcolor=white:alpha=0.85:borderw=3:bordercolor=black:"
        "x=w-text_w-40:y=h-th-40[out]"
    )

    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-ss", f"{start_s:.3f}", "-i", str(source), "-t", f"{duration:.3f}",
        "-filter_complex", vf,
        "-map", "[out]", "-map", "0:a:0?",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast",
        "-crf", "20", "-c:a", "aac", "-b:a", "160k",
        "-movflags", "+faststart",
        str(out_path),
    ]
    subprocess.run(cmd, check=True)
