#!/usr/bin/env python3
"""Transcribe downloaded lecture VODs into .srt + .txt sitting beside the video.

Transcription is delegated to the local Captioneer engine at
``D:\\coding\\captioneer-english`` (faster-whisper large-v3 + WhisperX forced
alignment, running on the GPU). That project is an MCP server, but it is not
connected to this session, so we drive its CLI directly through its own venv.

It emits a flat word list — ``[{text, start, end, probability}, ...]`` — which
this script groups into readable cues:

  * break on sentence-ending punctuation,
  * or after a silent gap,
  * or when a cue gets too long to read.

Outputs, next to the .mp4:
    <name>.srt         subtitles, for playback
    <name>.txt         plain paragraphs, for reading and searching
    <name>.words.json  raw word timings (git-ignored intermediate)

    python scripts/transcribe_vods.py             # everything downloaded
    python scripts/transcribe_vods.py --only 70704
    python scripts/transcribe_vods.py --force     # redo even if .srt exists
    python scripts/transcribe_vods.py --model medium
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = Path(__file__).resolve().parent / "vods.json"
CAPTIONEER = Path(r"D:\coding\captioneer-english")

# Cue-splitting thresholds.
GAP_SECONDS = 0.7      # silence that ends a cue
MAX_CHARS = 90         # longest cue we will show
MAX_SECONDS = 7.0      # longest cue duration
SENTENCE_END = ".?!"

# Seconds to let CUDA release VRAM between consecutive transcriptions.
VRAM_SETTLE = 25

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")


def slug(entry: dict) -> str:
    return f"week{entry['week']:02d} - {entry['title']}"


def video_path(entry: dict) -> Path:
    return REPO_ROOT / "semester 7" / entry["course"] / "lectures" / "vod" / f"{slug(entry)}.mp4"


def run_captioneer(video: Path, words_json: Path, model: str, attempts: int = 3) -> bool:
    """Drive Captioneer's CLI, retrying on transient CUDA OOM.

    large-v3 plus the WhisperX alignment model nearly fills 8 GB. Back-to-back
    runs can collide: CUDA has not finished releasing the previous process's
    VRAM when the next one allocates. It is transient, so wait and retry rather
    than dropping to a smaller model.
    """
    python = CAPTIONEER / "venv" / "Scripts" / "python.exe"
    if not python.exists():
        print(f"  !! Captioneer venv not found at {python}", file=sys.stderr)
        return False

    env = dict(os.environ)
    # Captioneer prints arrows and check marks; the Windows console is cp1252.
    env["PYTHONIOENCODING"] = "utf-8"

    for attempt in range(1, attempts + 1):
        proc = subprocess.run(
            [
                str(python), "-m", "caption_engine.cli", str(video),
                "--transcribe-only", "-j", str(words_json),
                "--model", model, "--language", "en",
            ],
            cwd=str(CAPTIONEER),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if proc.returncode == 0 and words_json.exists():
            return True

        out = proc.stdout or ""
        if "out of memory" in out.lower() and attempt < attempts:
            print(f"    CUDA OOM — waiting {VRAM_SETTLE}s for VRAM, retry {attempt + 1}/{attempts}",
                  flush=True)
            time.sleep(VRAM_SETTLE)
            continue

        tail = "\n".join(out.strip().splitlines()[-8:])
        print(f"  !! transcription failed ({proc.returncode}):\n{tail}", file=sys.stderr)
        return False
    return False


def group(words: list[dict]) -> list[dict]:
    """Group the flat word list into readable cues."""
    cues: list[dict] = []
    cur: list[dict] = []

    def flush():
        if not cur:
            return
        text = " ".join(w["text"].strip() for w in cur if w["text"].strip())
        if text:
            cues.append({"start": cur[0]["start"], "end": cur[-1]["end"], "text": text})
        cur.clear()

    for i, w in enumerate(words):
        if cur:
            gap = w["start"] - cur[-1]["end"]
            span = w["end"] - cur[0]["start"]
            length = sum(len(x["text"]) + 1 for x in cur)
            if gap > GAP_SECONDS or span > MAX_SECONDS or length > MAX_CHARS:
                flush()
        cur.append(w)
        if w["text"].strip().endswith(tuple(SENTENCE_END)):
            # Keep very short exclamations attached to what follows.
            if sum(len(x["text"]) for x in cur) > 20:
                flush()
    flush()
    return cues


def ts(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(cues: list[dict], path: Path) -> None:
    lines = []
    for i, c in enumerate(cues, 1):
        lines += [str(i), f"{ts(c['start'])} --> {ts(c['end'])}", c["text"], ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_txt(cues: list[dict], path: Path, entry: dict) -> None:
    """Readable transcript with a timestamp every ~2 minutes."""
    out = [
        f"# {entry['course'].split(' - ')[0]} — {entry['title']} (week {entry['week']})",
        "",
        f"Transcript of the eClass VOD ({entry['duration']}). Machine-generated with",
        "faster-whisper large-v3 — expect occasional errors in names and jargon.",
        "",
    ]
    para: list[str] = []
    next_mark = 0.0
    for c in cues:
        if c["start"] >= next_mark:
            if para:
                out += [" ".join(para), ""]
                para = []
            mins = int(c["start"] // 60)
            out += [f"## [{mins:02d}:{int(c['start'] % 60):02d}]", ""]
            next_mark = c["start"] + 120
        para.append(c["text"])
    if para:
        out += [" ".join(para), ""]
    path.write_text("\n".join(out), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--only", type=int, action="append", help="module id (repeatable)")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--model", default="large-v3",
                    choices=["tiny", "base", "small", "medium", "large-v3"])
    args = ap.parse_args()

    vods = json.loads(MANIFEST.read_text(encoding="utf-8"))["vods"]
    if args.only:
        vods = [v for v in vods if v["mod"] in args.only]

    done, skipped, failed = 0, 0, []
    for entry in vods:
        video = video_path(entry)
        if not video.exists():
            print(f"  · {slug(entry)} — not downloaded yet, skipping")
            skipped += 1
            continue

        srt = video.with_suffix(".srt")
        if srt.exists() and not args.force:
            print(f"  = {srt.name} — already transcribed")
            skipped += 1
            continue

        words_json = video.with_suffix(".words.json")
        if not words_json.exists() or args.force:
            print(f"  ♪ transcribing {video.name} ({entry['duration']}) with {args.model} …",
                  flush=True)
            if not run_captioneer(video, words_json, args.model):
                failed.append(entry["mod"])
                continue
            time.sleep(VRAM_SETTLE)  # let the GPU settle before the next one

        words = json.loads(words_json.read_text(encoding="utf-8"))
        cues = group(words)
        write_srt(cues, srt)
        write_txt(cues, video.with_suffix(".txt"), entry)
        print(f"    {len(words):,} words → {len(cues):,} cues → {srt.name} + {video.stem}.txt")
        done += 1

    print(f"\ntranscribed {done}, skipped {skipped}" + (f", failed {failed}" if failed else ""))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
