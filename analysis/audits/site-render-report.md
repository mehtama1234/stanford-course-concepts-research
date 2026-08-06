# Site Render Report

This audit uses Playwright to render representative desktop and mobile pages from the generated static site. It checks that Chromium can launch, screenshots are produced at the expected dimensions, and captured files are non-trivial in size. The PNG files are stored in `analysis/audits/screenshots/` for manual inspection.

## Browser Setup

- Chromium dependencies satisfied by ignored local browser-lib cache.

## Screenshots

- desktop-index: `index.html`, viewport 1280,900, captured 1280x900, 124915 bytes
- desktop-tokenization: `concepts/tokenization.html`, viewport 1280,900, captured 1280x900, 198692 bytes
- desktop-vision-transformers: `concepts/vision_transformers.html`, viewport 1280,900, captured 1280x900, 217699 bytes
- mobile-index: `index.html`, viewport 390,844, captured 390x844, 72385 bytes
- mobile-tokenization: `concepts/tokenization.html`, viewport 390,844, captured 390x844, 86484 bytes

## Errors

- None
