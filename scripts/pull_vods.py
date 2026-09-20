#!/usr/bin/env python3
"""Download eClass lecture VODs for offline study, and optionally extract audio.

The videos are Wowza HLS streams on vod.inha.ac.kr:8443. The stream endpoints
need no credentials — only the *discovery* of a stream URL does, via
``/mod/vod/viewer.php?id=<mod>`` on a logged-in eClass session. Those URLs are
cached in ``scripts/vods.json``; ask Claude to refresh it when new lectures
appear.

ffmpeg remuxes the HLS segments into an MP4 with ``-c copy``, so there is no
re-encode and no quality loss.

    python scripts/pull_vods.py              # download anything missing
    python scripts/pull_vods.py --list       # show what is on disk
    python scripts/pull_vods.py --audio      # also write 16 kHz mono .wav
    python scripts/pull_vods.py --only 70704 # one lecture
    python scripts/pull_vods.py --force      # re-download even if present

NOTE: watching a downloaded copy does NOT register attendance. eClass only
counts a view made in its own player.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = Path(__file__).resolve().parent / "vods.json"

# The Windows console defaults to cp1252, which cannot encode the status glyphs.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")


def slug(entry: dict) -> str:
    return f"week{entry['week']:02d} - {entry['title']}"


def target(entry: dict) -> Path:
    return REPO_ROOT / "semester 7" / entry["course"] / "lectures" / "vod" / f"{slug(entry)}.mp4"


def human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:,.1f} {unit}"
        n /= 1024
    return str(n)


def run(cmd: list[str]) -> bool:
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if proc.returncode != 0:
        tail = "\n".join(proc.stdout.strip().splitlines()[-6:])
        print(f"    ffmpeg failed ({proc.returncode}):\n{tail}", file=sys.stderr)
        return False
    return True


def download(entry: dict, force: bool) -> Path | None:
    out = target(entry)
    if out.exists() and not force:
        print(f"  = {out.name} ({human(out.stat().st_size)}) — already have it")
        return out

    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".part.mp4")
    tmp.unlink(missing_ok=True)

    print(f"  ↓ {out.name} ({entry['duration']}) …", flush=True)
    ok = run(
        [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin",
            "-i", entry["url"],
            "-c", "copy",
            "-bsf:a", "aac_adtstoasc",   # ADTS -> MP4 audio, required for HLS remux
            "-movflags", "+faststart",
            str(tmp),
        ]
    )
    if not ok or not tmp.exists():
        tmp.unlink(missing_ok=True)
        return None

    tmp.replace(out)
    print(f"    done — {human(out.stat().st_size)}")
    return out


def extract_audio(video: Path, force: bool) -> Path | None:
    """16 kHz mono WAV — what speech-to-text models expect."""
    wav = video.with_suffix(".wav")
    if wav.exists() and not force:
        print(f"    = {wav.name} already extracted")
        return wav
    ok = run(
        [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin", "-y",
            "-i", str(video),
            "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le",
            str(wav),
        ]
    )
    if ok:
        print(f"    audio — {wav.name} ({human(wav.stat().st_size)})")
        return wav
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--list", action="store_true", help="show status, download nothing")
    ap.add_argument("--audio", action="store_true", help="also extract 16 kHz mono wav")
    ap.add_argument("--only", type=int, action="append", help="module id (repeatable)")
    ap.add_argument("--force", action="store_true", help="re-download / re-extract")
    args = ap.parse_args()

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    vods = data["vods"]
    if args.only:
        vods = [v for v in vods if v["mod"] in args.only]
        if not vods:
            print(f"no manifest entry for {args.only}", file=sys.stderr)
            return 1

    if args.list:
        total = 0
        for v in vods:
            p = target(v)
            size = p.stat().st_size if p.exists() else 0
            total += size
            mark = "✓" if p.exists() else "·"
            print(f"  {mark} [{v['mod']}] {slug(v)}  {v['duration']}  {human(size) if size else '—'}")
        print(f"\n  {human(total)} on disk")
        return 0

    print(f"{len(vods)} VOD(s) from {MANIFEST.name}")
    failed = []
    for v in vods:
        path = download(v, args.force)
        if path is None:
            failed.append(v["mod"])
            continue
        if args.audio:
            extract_audio(path, args.force)

    if failed:
        print(f"\nfailed: {failed}", file=sys.stderr)
        return 1
    print("\nall done — these are git-ignored and stay local")
    return 0


if __name__ == "__main__":
    sys.exit(main())
