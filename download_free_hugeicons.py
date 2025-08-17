import re
import requests
from pathlib import Path

# URLs
FONT_URL = "https://use.hugeicons.com/font/hgi-stroke-rounded.svg"
SVG_URL_TEMPLATE = "https://cdn.hugeicons.com/icons/{name}-stroke-rounded.svg?v=2.0"

# Dictionary for special cases
GLYPH_OVERRIDES = {
    # "glyph-name-in-font": "actual-cdn-name"
    "arrange-by-numbers-nine-1": "arrange-by-numbers-9-1",
    "arrange-by-numbers-one-9": "arrange-by-numbers-1-9",
    "first-bracket-circle": "1st-bracket-circle",
    "first-bracket-square": "1st-bracket-square",
    "first-bracket": "1st-bracket",
    "four-k": "4k",
    "go-backward-five-sec": "go-backward-5-sec",
    "go-forward-five-sec": "go-forward-5-sec",
    "layout-three-column": "layout-3-column",
    "layout-three-row": "layout-3-row",
    "layout-two-column": "layout-2-column",
    "layout-two-row": "layout-2-row",
    "modern-tv-four-k": "modern-tv-4-k",
    "mp-four-01": "mp4-01",
    "mp-four-02": "mp-4-02",
    "mp-three-01": "mp3-01",
    "mp-three-02": "mp-3-02",
    "printer-three-d": "printer-3d",
    "root-first-bracket": "root-1st-bracket",
    "root-second-bracket": "root-2nd-bracket",
    "root-third-bracket": "root-3rd-bracket",
    "second-bracket-circle": "2nd-bracket-circle",
    "second-bracket-square": "2nd-bracket-square",
    "second-bracket": "2nd-bracket",
    "seven-z-01": "7z-01",
    "seven-z-02": "7z-02",
    "sorting-nine-1": "sorting-9-1",
    "sorting-one-9": "sorting-1-9",
    "third-bracket-circle": "3rd-bracket-circle",
    "third-bracket-square": "3rd-bracket-square",
    "third-bracket": "3rd-bracket",
    "three-d-move": "3d-move",
    "three-d-rotate": "3d-rotate",
    "three-d-scale": "3d-scale",
    "three-d-view": "3d-view",
    "w-three-schools": "w-3-schools",
}

# Output folder
OUTPUT_DIR = Path("svg/stroke-rounded")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. Download the font SVG
print("Downloading font file...")
font_svg = requests.get(FONT_URL)
font_svg.raise_for_status()

# 2. Extract glyph names
# The font SVG typically has: <glyph glyph-name="abacus" ...
glyph_names = re.findall(r'glyph-name="([^"]+)"', font_svg.text)

print(f"Found {len(glyph_names)} glyph names.")

# 3. Download each icon
for name in glyph_names:
    # Use override if defined
    cdn_name = GLYPH_OVERRIDES.get(name, name)
    url = SVG_URL_TEMPLATE.format(name=cdn_name)

    try:
        r = requests.get(url)
        r.raise_for_status()
        (OUTPUT_DIR / f"{cdn_name}.svg").write_bytes(r.content)
        print(f"Downloaded: {cdn_name}")
    except requests.HTTPError as e:
        print(f"Failed: {name} ({e})")

print("Done.")
