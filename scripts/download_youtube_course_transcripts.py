#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw-material/youtube"

COURSES: list[dict[str, Any]] = [
    {
        "slug": "stanford-cme295-transformers-llms-autumn-2025",
        "title": "Stanford CME295 Transformers & LLMs | Autumn 2025",
        "kind": "video-list",
        "seed_url": "https://www.youtube.com/watch?v=Ub3GoFaUcds",
        "source_note": "YouTube search for Stanford CME295 lectures; original seed URL had no playlist parameter.",
        "videos": [
            ("Ub3GoFaUcds", "Lecture 1 - Transformer"),
            ("yT84Y5zCnaA", "Lecture 2 - Transformer-Based Models & Tricks"),
            ("Q5baLehv5So", "Lecture 3 - Tranformers & Large Language Models"),
            ("VlA_jt_3Qc4", "Lecture 4 - LLM Training"),
            ("PmW_TMQ3l0I", "Lecture 5 - LLM tuning"),
            ("k5Fh-UgTuCo", "Lecture 6 - LLM Reasoning"),
            ("h-7S6HNq0Vg", "Lecture 7 - Agentic LLMs"),
            ("8fNP4N46RRo", "Lecture 8 - LLM Evaluation"),
            ("Q86qzJ1K1Ss", "Lecture 9 - Recap & Current Trends"),
        ],
    },
    {
        "slug": "stanford-cs224r-deep-rl-spring-2025",
        "title": "Stanford CS224R Deep Reinforcement Learning | Spring 2025",
        "kind": "video-list",
        "seed_url": "https://www.youtube.com/watch?v=EvHRQhMX7_w&t=1830s",
        "source_note": "YouTube search for Stanford CS224R lectures; original seed URL had no playlist parameter.",
        "videos": [
            ("EvHRQhMX7_w", "Lecture 1: Class Intro"),
            ("WxRDyObrm_M", "Lecture 2: Imitation Learning"),
            ("KCAOXd4IO9o", "Lecture 3: Policy Gradients"),
            ("oejFZShW9hU", "Lecture 4: Actor-Critic Methods"),
            ("cRGKc-nAWho", "Lecture 5: Off-Policy Actor Critic"),
            ("-7kv6jf0isQ", "Lecture 6: Q-Learning"),
            ("lRDaXnPIzks", "Lecture 7: Offline RL"),
            ("PDIxDhA9Z6Y", "Lecture 8: Reward Learning"),
            ("XKLGuwvSKvI", "Lecture 9: RL for LLMs"),
            ("O2VpNnwB4lM", "Lecture 10: RL for LLM Reasoning"),
            ("PvqyGnOirgA", "Lecture 11: Model-Based RL"),
            ("qNdsI_4AQJw", "Lecture 12: Multi-Task RL"),
            ("wSiyEpvoGkA", "Lecture 13: Meta RL"),
            ("4tlSKdi8teU", "Lecture 14: Exploration"),
            ("iKWYLSVAtfM", "Lecture 15: Hierarchical RL and IL"),
            ("rbaWQQLrzl0", "Lecture 16: RL for Robots"),
            ("Hp1WBWghrak", "Lecture 17: Advancing Robot Intelligence"),
            ("FacJ_1tTSx4", "Lecture 18: Frontiers"),
            ("07MQNMcxhZU", "Tutorial Session: Review of Q-Learning"),
        ],
    },
    {
        "slug": "stanford-cme296-diffusion-large-vision-models-spring-2026",
        "title": "Stanford CME296 Diffusion & Large Vision Models | Spring 2026",
        "kind": "playlist",
        "seed_url": "https://www.youtube.com/watch?v=tr-CUpw--ck&list=PLoROMvodv4rNdy8rt2rZ4T2xM0OjADnfu",
        "playlist_url": "https://www.youtube.com/playlist?list=PLoROMvodv4rNdy8rt2rZ4T2xM0OjADnfu",
        "source_note": "Playlist supplied in the original URL.",
        "videos": [
            ("tr-CUpw--ck", "Lecture 1 - Diffusion"),
            ("_WaR2fjZpEQ", "Lecture 2 - Score matching"),
            ("agN3AlfGFrk", "Lecture 3 - Flow matching"),
            ("WUUq6TVAu8U", "Lecture 4 - Latent Space & Guidance"),
            ("HpFdSlMeXzQ", "Lecture 5 - Architectures"),
            ("IvXTl3yj-4Y", "Lecture 6 - Model Training"),
            ("iNaRBp4T57Q", "Lecture 7 - Evaluation"),
            ("oyLUvz9nR6E", "Lecture 8 - Trending Topics"),
        ],
    },
]


def run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, check=check, text=True)


def dump_json(cmd: list[str]) -> dict[str, Any]:
    output = subprocess.check_output(cmd, cwd=ROOT, text=True)
    return json.loads(output)


def stable_playlist_manifest(data: dict[str, Any]) -> dict[str, Any]:
    data = dict(data)
    data.pop("epoch", None)
    return data


def video_url(video_id: str) -> str:
    return f"https://www.youtube.com/watch?v={video_id}"


def clean_vtt_text(vtt_path: Path) -> str:
    lines: list[str] = []
    seen_recent: set[str] = set()
    for raw in vtt_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line == "WEBVTT" or line.startswith("Kind:") or line.startswith("Language:"):
            continue
        if "-->" in line or re.match(r"^[0-9]+$", line):
            seen_recent.clear()
            continue
        line = re.sub(r"<[^>]+>", "", line)
        line = re.sub(r"&amp;", "&", line)
        line = re.sub(r"&lt;", "<", line)
        line = re.sub(r"&gt;", ">", line)
        line = re.sub(r"\s+", " ", line).strip()
        if not line or line in seen_recent:
            continue
        seen_recent.add(line)
        lines.append(line)
    return "\n".join(lines).strip() + "\n"


def ensure_dirs(course: dict[str, Any]) -> dict[str, Path]:
    slug = course["slug"]
    base = RAW / "transcripts" / slug
    paths = {
        "base": base,
        "raw_dir": base / "raw-vtt",
        "clean_dir": base / "clean",
        "meta_dir": RAW / "metadata" / slug,
        "playlist_dir": RAW / "playlists",
        "manifest_dir": RAW / "course-manifests",
    }
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    return paths


def write_course_manifest(course: dict[str, Any], paths: dict[str, Path]) -> None:
    manifest = {
        "slug": course["slug"],
        "title": course["title"],
        "kind": course["kind"],
        "seed_url": course["seed_url"],
        "playlist_url": course.get("playlist_url"),
        "source_note": course["source_note"],
        "videos": [
            {"index": i, "id": video_id, "expected_title": title, "url": video_url(video_id)}
            for i, (video_id, title) in enumerate(course["videos"], 1)
        ],
    }
    (paths["manifest_dir"] / f"{course['slug']}.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )


def capture_playlist_manifest(course: dict[str, Any], paths: dict[str, Path]) -> None:
    if course["kind"] == "playlist":
        data = stable_playlist_manifest(
            dump_json(["yt-dlp", "--flat-playlist", "--dump-single-json", course["playlist_url"]])
        )
    else:
        data = {
            "_type": "curated_video_list",
            "id": course["slug"],
            "title": course["title"],
            "source_note": course["source_note"],
            "entries": [
                {"id": video_id, "title": title, "url": video_url(video_id)}
                for video_id, title in course["videos"]
            ],
        }
    (paths["playlist_dir"] / f"{course['slug']}.json").write_text(
        json.dumps(data, indent=2) + "\n",
        encoding="utf-8",
    )


def download_video(course: dict[str, Any], index: int, video_id: str) -> bool:
    paths = ensure_dirs(course)
    slug = course["slug"]
    archive = paths["base"] / "download-archive.txt"
    output_tpl = str(paths["raw_dir"] / f"{index:03d}-%(id)s-%(title).120B.%(ext)s")
    result = run(
        [
            "yt-dlp",
            "--skip-download",
            "--write-info-json",
            "--write-subs",
            "--write-auto-subs",
            "--sub-langs",
            "en,en-US,en-orig",
            "--sub-format",
            "vtt",
            "--sleep-requests",
            "1",
            "--sleep-interval",
            "1",
            "--download-archive",
            str(archive),
            "-o",
            output_tpl,
            video_url(video_id),
        ],
        check=False,
    )
    for info in paths["raw_dir"].glob(f"{index:03d}-{video_id}-*.info.json"):
        target = paths["meta_dir"] / info.name
        if target.exists():
            target.unlink()
        info.replace(target)
    if result.returncode == 0:
        print(f"captured {slug} {index:03d} {video_id}")
        return True
    print(f"partial-or-failed {slug} {index:03d} {video_id} rc={result.returncode}")
    return False


def rebuild_clean_for_course(course: dict[str, Any]) -> dict[str, Any]:
    paths = ensure_dirs(course)
    for info in paths["raw_dir"].glob("*.info.json"):
        target = paths["meta_dir"] / info.name
        if target.exists():
            target.unlink()
        info.replace(target)

    preferred_vtt: dict[str, Path] = {}
    preference = {".en-US.vtt": 0, ".en.vtt": 1, ".en-orig.vtt": 2}
    for vtt in sorted(paths["raw_dir"].glob("*.vtt")):
        clean_name = re.sub(r"\.(en(?:-[A-Za-z0-9]+)*|en-US|en-orig)\.vtt$", ".txt", vtt.name)
        rank = next((score for suffix, score in preference.items() if vtt.name.endswith(suffix)), 99)
        current = preferred_vtt.get(clean_name)
        if current is None:
            preferred_vtt[clean_name] = vtt
            continue
        current_rank = next((score for suffix, score in preference.items() if current.name.endswith(suffix)), 99)
        if rank < current_rank:
            preferred_vtt[clean_name] = vtt

    for clean_file in paths["clean_dir"].glob("*.txt"):
        clean_file.unlink()

    for clean_name, vtt in sorted(preferred_vtt.items()):
        (paths["clean_dir"] / clean_name).write_text(clean_vtt_text(vtt), encoding="utf-8")

    return {
        "slug": course["slug"],
        "title": course["title"],
        "kind": course["kind"],
        "expected_videos": len(course["videos"]),
        "raw_vtt": len(list(paths["raw_dir"].glob("*.vtt"))),
        "clean_txt": len(list(paths["clean_dir"].glob("*.txt"))),
        "metadata_json": len(list(paths["meta_dir"].glob("*.info.json"))),
        "manifest": str(paths["manifest_dir"].relative_to(ROOT) / f"{course['slug']}.json"),
        "playlist_manifest": str(RAW.relative_to(ROOT) / "playlists" / f"{course['slug']}.json"),
    }


def metadata_by_video_id(course: dict[str, Any]) -> dict[str, Path]:
    paths = ensure_dirs(course)
    out: dict[str, Path] = {}
    for path in paths["meta_dir"].glob("*.info.json"):
        match = re.match(r"^[0-9]{3}-([A-Za-z0-9_-]{11})-", path.name)
        if match:
            out[match.group(1)] = path
    return out


def find_clean_path(course: dict[str, Any], index: int, video_id: str) -> Path | None:
    paths = ensure_dirs(course)
    matches = sorted(paths["clean_dir"].glob(f"{index:03d}-{video_id}-*.txt"))
    return matches[0] if matches else None


def find_raw_path(course: dict[str, Any], index: int, video_id: str) -> Path | None:
    paths = ensure_dirs(course)
    for suffix in ["en-US.vtt", "en.vtt", "en-orig.vtt"]:
        matches = sorted(paths["raw_dir"].glob(f"{index:03d}-{video_id}-*.{suffix}"))
        if matches:
            return matches[0]
    matches = sorted(paths["raw_dir"].glob(f"{index:03d}-{video_id}-*.vtt"))
    return matches[0] if matches else None


def word_count(path: Path | None) -> int:
    if path is None or not path.exists():
        return 0
    return len(re.findall(r"\b\S+\b", path.read_text(encoding="utf-8", errors="ignore")))


def build_transcript_index() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for course in COURSES:
        meta = metadata_by_video_id(course)
        for index, (video_id, expected_title) in enumerate(course["videos"], 1):
            meta_path = meta.get(video_id)
            clean = find_clean_path(course, index, video_id)
            raw = find_raw_path(course, index, video_id)
            info: dict[str, Any] = {}
            if meta_path and meta_path.exists():
                info = json.loads(meta_path.read_text(encoding="utf-8"))
            status = "available" if clean and clean.exists() and word_count(clean) > 0 else "missing"
            records.append(
                {
                    "id": video_id,
                    "course_slug": course["slug"],
                    "course_title": course["title"],
                    "course_index": index,
                    "expected_title": expected_title,
                    "title": info.get("title") or expected_title,
                    "url": video_url(video_id),
                    "raw_vtt": str(raw.relative_to(ROOT)) if raw else None,
                    "clean_txt": str(clean.relative_to(ROOT)) if clean else None,
                    "metadata_json": str(meta_path.relative_to(ROOT)) if meta_path else None,
                    "duration": info.get("duration"),
                    "upload_date": info.get("upload_date"),
                    "channel": info.get("channel"),
                    "word_count": word_count(clean),
                    "transcript_status": status,
                }
            )
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Regenerate clean transcripts, summary.json, and transcript-index.json from files already on disk.",
    )
    parser.add_argument(
        "--course",
        action="append",
        choices=[course["slug"] for course in COURSES],
        help="Limit work to one course slug. Can be passed more than once.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Limit downloaded videos per selected course. Ignored with --summary-only.",
    )
    args = parser.parse_args()

    selected = [course for course in COURSES if not args.course or course["slug"] in args.course]
    for course in selected:
        paths = ensure_dirs(course)
        write_course_manifest(course, paths)
        capture_playlist_manifest(course, paths)
        if not args.summary_only:
            videos = course["videos"][: args.limit] if args.limit else course["videos"]
            for index, (video_id, _title) in enumerate(videos, 1):
                download_video(course, index, video_id)

    summary = [rebuild_clean_for_course(course) for course in COURSES]
    (RAW / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (RAW / "transcript-index.json").write_text(
        json.dumps(build_transcript_index(), indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
