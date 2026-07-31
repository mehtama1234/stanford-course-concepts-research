# Stanford Course Concepts Research

Transcript-backed research workspace for Stanford Online course material named in
the handoff thread.

The working standard follows
`../eigensteve-concepts-research/analysis/transcript-research-cli-guidance.md`:
keep raw transcript evidence separate from synthesis, build indexes before
writing pages, and explain mathematical ideas from first principles in plain
everyday language.

## Initial course corpus

- `stanford-cme295-transformers-llms-autumn-2025`: Transformers and LLMs.
- `stanford-cs224r-deep-rl-spring-2025`: Deep Reinforcement Learning.
- `stanford-cme296-diffusion-large-vision-models-spring-2026`: Diffusion and
  Large Vision Models.

## Layout

- `raw-material/youtube/course-manifests/`: course definitions and source URLs.
- `raw-material/youtube/playlists/`: raw yt-dlp playlist or search manifests.
- `raw-material/youtube/metadata/`: per-video info JSON.
- `raw-material/youtube/transcripts/<course>/raw-vtt/`: raw caption files.
- `raw-material/youtube/transcripts/<course>/clean/`: cleaned transcript text.
- `raw-material/youtube/transcript-index.json`: machine-readable transcript
  records.
- `analysis/`: concept, theme, subtheme, and evidence-ledger work.
- `site/`: generated pages when synthesis begins.

## Commands

Download or refresh the transcript corpus:

```bash
python3 scripts/download_youtube_course_transcripts.py
```

Rebuild clean text and indexes from files already on disk:

```bash
python3 scripts/download_youtube_course_transcripts.py --summary-only
```

