"""Whisper transcription with word-level timestamps."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from faster_whisper import WhisperModel


@dataclass
class Word:
    start: float
    end: float
    text: str


@dataclass
class Segment:
    start: float
    end: float
    text: str
    words: list[Word] = field(default_factory=list)


@dataclass
class Transcript:
    language: str
    segments: list[Segment]

    @property
    def full_text(self) -> str:
        return " ".join(s.text.strip() for s in self.segments)

    def timecoded_text(self) -> str:
        """Formatted like `[mm:ss] text` — what we pass to Claude."""
        return "\n".join(
            f"[{_ts(s.start)}-{_ts(s.end)}] {s.text.strip()}"
            for s in self.segments
        )

    def words_in_range(self, start: float, end: float) -> list[Word]:
        out: list[Word] = []
        for seg in self.segments:
            if seg.end < start or seg.start > end:
                continue
            for w in seg.words:
                if w.end < start or w.start > end:
                    continue
                out.append(Word(max(w.start, start) - start,
                                min(w.end, end) - start, w.text))
        return out


def transcribe(video_path: Path, model_size: str = "medium",
               device: str = "auto") -> Transcript:
    model = WhisperModel(model_size, device=device, compute_type="auto")
    segments_iter, info = model.transcribe(
        str(video_path), word_timestamps=True, vad_filter=True
    )
    segments: list[Segment] = []
    for s in segments_iter:
        words = [Word(w.start, w.end, w.word) for w in (s.words or [])]
        segments.append(Segment(s.start, s.end, s.text, words))
    return Transcript(language=info.language, segments=segments)


def _ts(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    return f"{m:02d}:{s:02d}"
