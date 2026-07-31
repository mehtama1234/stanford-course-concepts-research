#!/usr/bin/env python3
from __future__ import annotations

import os
import socket
import struct
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
REPORT = ROOT / "analysis/audits/site-render-report.md"
SCREENSHOTS = ROOT / "analysis/audits/screenshots"
BROWSER_LIBS = ROOT / "analysis/audits/browser-libs"
BROWSER_LIB_PATH = BROWSER_LIBS / "root/usr/lib/x86_64-linux-gnu"
CHROME = Path.home() / ".cache/ms-playwright/chromium_headless_shell-1228/chrome-headless-shell-linux64/chrome-headless-shell"

PAGES = [
    ("desktop-index", "index.html", "1280,900"),
    ("desktop-tokenization", "concepts/tokenization.html", "1280,900"),
    ("desktop-vision-transformers", "concepts/vision_transformers.html", "1280,900"),
    ("mobile-index", "index.html", "390,844"),
    ("mobile-tokenization", "concepts/tokenization.html", "390,844"),
]


def run(
    cmd: list[str],
    env: dict[str, str] | None = None,
    timeout: int = 90,
    cwd: Path | None = None,
) -> tuple[int, str]:
    proc = subprocess.run(
        cmd,
        cwd=cwd or ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
    )
    return proc.returncode, proc.stdout.strip()


def port_free(port: int) -> bool:
    sock = socket.socket()
    try:
        sock.bind(("127.0.0.1", port))
        return True
    except OSError:
        return False
    finally:
        sock.close()


def find_port() -> int:
    for port in range(8876, 8896):
        if port_free(port):
            return port
    raise RuntimeError("no free localhost port found in 8876-8895")


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        signature = handle.read(8)
        if signature != b"\x89PNG\r\n\x1a\n":
            raise ValueError(f"{path} is not a PNG")
        length = struct.unpack(">I", handle.read(4))[0]
        chunk_type = handle.read(4)
        if chunk_type != b"IHDR" or length < 8:
            raise ValueError(f"{path} has no readable IHDR")
        width, height = struct.unpack(">II", handle.read(8))
        return width, height


def browser_env() -> dict[str, str]:
    env = os.environ.copy()
    if BROWSER_LIB_PATH.exists():
        existing = env.get("LD_LIBRARY_PATH", "")
        env["LD_LIBRARY_PATH"] = str(BROWSER_LIB_PATH) + (":" + existing if existing else "")
    return env


def chrome_missing_libs(env: dict[str, str]) -> list[str]:
    if not CHROME.exists():
        return ["playwright chromium executable missing"]
    code, output = run(["ldd", str(CHROME)], env=env, timeout=30)
    if code != 0:
        return [output or "ldd failed"]
    return [line.strip() for line in output.splitlines() if "not found" in line]


def prepare_browser_libs(env: dict[str, str]) -> tuple[dict[str, str], list[str]]:
    notes: list[str] = []
    missing = chrome_missing_libs(env)
    if not missing:
        if BROWSER_LIB_PATH.exists():
            return env, ["Chromium dependencies satisfied by ignored local browser-lib cache."]
        return env, ["Chromium dependencies satisfied by system libraries."]
    if not shutil_available(["apt-get", "dpkg-deb"]):
        return env, [f"Missing browser libraries and no local package extractor available: {', '.join(missing)}"]

    packages = ["libnspr4", "libnss3", "libasound2t64"]
    package_dir = BROWSER_LIBS / "packages"
    root_dir = BROWSER_LIBS / "root"
    package_dir.mkdir(parents=True, exist_ok=True)
    root_dir.mkdir(parents=True, exist_ok=True)
    code, output = run(["apt-get", "download", *packages], env=env, timeout=120, cwd=package_dir)
    notes.append("Downloaded browser runtime packages into ignored audit cache." if code == 0 else output)
    if code == 0:
        for deb in package_dir.glob("*.deb"):
            run(["dpkg-deb", "-x", str(deb), str(root_dir)], env=env, timeout=60)
    env = browser_env()
    missing = chrome_missing_libs(env)
    if missing:
        notes.append("Still missing browser libraries: " + "; ".join(missing))
    else:
        notes.append("Chromium dependencies satisfied by ignored local browser-lib cache.")
    return env, notes


def shutil_available(commands: list[str]) -> bool:
    from shutil import which

    return all(which(command) for command in commands)


def main() -> int:
    if not SITE.exists():
        print("site directory is missing; run scripts/build_site.py first", file=sys.stderr)
        return 1
    SCREENSHOTS.mkdir(parents=True, exist_ok=True)
    env, notes = prepare_browser_libs(browser_env())
    missing = chrome_missing_libs(env)
    errors: list[str] = []
    if missing:
        errors.extend(missing)

    port = find_port()
    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port), "--directory", str(SITE)],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(0.5)
    rows: list[tuple[str, str, str, int, int, int]] = []
    try:
        for name, page, viewport in PAGES:
            target = SCREENSHOTS / f"{name}.png"
            url = f"http://127.0.0.1:{port}/{page}"
            code, output = run(
                [
                    "npx",
                    "-y",
                    "playwright",
                    "screenshot",
                    f"--viewport-size={viewport}",
                    "--wait-for-timeout=500",
                    url,
                    str(target),
                ],
                env=env,
                timeout=120,
            )
            if code != 0:
                errors.append(f"{name} screenshot failed: {output}")
                continue
            width, height = png_size(target)
            bytes_on_disk = target.stat().st_size
            expected_width, expected_height = [int(part) for part in viewport.split(",")]
            if (width, height) != (expected_width, expected_height):
                errors.append(f"{name} screenshot has unexpected size {width}x{height}, expected {viewport}")
            if bytes_on_disk < 20_000:
                errors.append(f"{name} screenshot is suspiciously small: {bytes_on_disk} bytes")
            rows.append((name, page, viewport, width, height, bytes_on_disk))
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()

    lines = [
        "# Site Render Report",
        "",
        "This audit uses Playwright to render representative desktop and mobile pages from the generated static site. It checks that Chromium can launch, screenshots are produced at the expected dimensions, and captured files are non-trivial in size. The PNG files are stored in `analysis/audits/screenshots/` for manual inspection.",
        "",
        "## Browser Setup",
        "",
    ]
    lines.extend(f"- {note}" for note in notes)
    lines.extend(["", "## Screenshots", ""])
    for name, page, viewport, width, height, bytes_on_disk in rows:
        lines.append(f"- {name}: `{page}`, viewport {viewport}, captured {width}x{height}, {bytes_on_disk} bytes")
    lines.extend(["", "## Errors", ""])
    if errors:
        lines.extend(f"- {error}" for error in errors)
    else:
        lines.append("- None")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"render-audited {len(rows)} screenshots; errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
