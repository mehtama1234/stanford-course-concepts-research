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
- `analysis/concepts/concept-atlas.json`: canonical first-principles concepts.
- `analysis/themes/theme-map.json`: cross-course themes.
- `analysis/themes/subtheme-map.json`: fine-grained subthemes.
- `analysis/evidence/evidence-ledger.json`: transcript-backed evidence records.
- `analysis/throughlines/primitives.json`: reusable mathematical primitives.
- `analysis/throughlines/method-families.json`: method and paper-family map.
- `analysis/throughlines/big-picture-map.md`: human-readable synthesis.
- `analysis/audits/atlas-validation-report.md`: validation and evidence-scope report.
- `site/`: generated reader-facing HTML lab.

## Commands

Download or refresh the transcript corpus:

```bash
python3 scripts/download_youtube_course_transcripts.py
```

Rebuild clean text and indexes from files already on disk:

```bash
python3 scripts/download_youtube_course_transcripts.py --summary-only
```

Rebuild the first-principles atlas from the transcript index:

```bash
python3 scripts/build_first_principles_atlas.py
```

Build the reader-facing HTML lab:

```bash
python3 scripts/build_site.py
```

Run the full local validation gate:

```bash
python3 scripts/validate_all.py
```

Open the generated lab at:

```text
site/index.html
```

## Current atlas scope

The generated lab covers 28 concepts, 6 themes, 15 subthemes, 10 reusable
mathematical primitives, 9 method families, and transcript-backed evidence
anchors. The writing standard is plain everyday language first, with equations
included only when the relationship is explained in words.
