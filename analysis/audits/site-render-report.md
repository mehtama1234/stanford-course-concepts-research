# Site Render Report

This audit uses Playwright to render representative desktop and mobile pages from the generated static site. It checks that Chromium can launch, screenshots are produced at the expected dimensions, and captured files are non-trivial in size. The PNG files are stored in `analysis/audits/screenshots/` for manual inspection.

## Browser Setup

- Chromium dependencies satisfied by ignored local browser-lib cache.

## Screenshots

- desktop-index: `index.html`, viewport 1280,900, captured 1280x900, 127127 bytes
- desktop-tokenization: `concepts/tokenization.html`, viewport 1280,900, captured 1280x900, 200783 bytes
- desktop-vision-transformers: `concepts/vision_transformers.html`, viewport 1280,900, captured 1280x900, 219507 bytes
- mobile-index: `index.html`, viewport 390,844, captured 390x844, 74697 bytes
- mobile-tokenization: `concepts/tokenization.html`, viewport 390,844, captured 390x844, 87235 bytes

## Errors

- None
