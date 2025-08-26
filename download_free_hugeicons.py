import re
import requests
from pathlib import Path

FONT_URL = "https://use.hugeicons.com/font/hgi-stroke-rounded.svg"
CDN_URL = "https://cdn.hugeicons.com/icons/{name}-stroke-rounded.svg?v=2.0"

# Mapping for glyphs that have different CDN names
GLYPH_OVERRIDES = {
    # "glyph-name-in-font": "actual-cdn-name"
    # "apple-music": "",
    "arrange-by-numbers-nine-1": "arrange-by-numbers-9-1",
    "arrange-by-numbers-one-9": "arrange-by-numbers-1-9",
    "component-1": "qwen",
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
    "mp-four-01": "mp-4-01",
    "mp-four-02": "mp-4-02",
    "mp-three-01": "mp3-01",
    "mp-three-02": "mp-3-02",
    "printer-three-d": "printer-3d",
    "root-first-bracket": "root-1st-bracket",
    "root-second-bracket": "root-2nd-bracket",
    "root-third-bracket": "root-3rd-bracket",
    # "scan-image": "",
    "second-bracket-circle": "2nd-bracket-circle",
    "second-bracket-square": "2nd-bracket-square",
    "second-bracket": "2nd-bracket",
    "seven-z-01": "7z-01",
    "seven-z-02": "7z-02",
    "ski-dice-faces-01": "ski",
    "sorting-nine-1": "sorting-9-1",
    "sorting-one-9": "sorting-1-9",
    "third-bracket-circle": "3rd-bracket-circle",
    "third-bracket-square": "3rd-bracket-square",
    "third-bracket": "3rd-bracket",
    "three-d-move": "3d-move",
    "three-d-rotate": "3d-rotate",
    "three-d-scale": "3d-scale",
    "three-d-view": "3-d-view",
    "w-three-schools": "w-3-schools",
}

# Extra icons not in font but shown on website
EXTRA_GLYPHS = [
    "3d-printer",
    "add-invoice",
    "add-money-circle",
    "arrow-up-right-03",
    "car-signal",
    "circle-arrow-up-right-02",
    "computer-terminal-01",
    "computer-terminal-02",
    "cursor-magic-selection-03",
    "cursor-magic-selection-04",
    "frisbee",
    "fuel",
    "insert-column-right",
    "lifebuoy",
    "restaurant",
    "semi-truck",
    "square-arrow-up-right-02",
    "tanker-truck",
    "taxi-02",
    "tinder-square",
    "tinder",
    "webflow-ellipse",
    "webflow-rectangle",
]

# Hidden icons: not in font, not on site, but downloadable via CDN
HIDDEN_GLYPHS = [
    "folder-move-in",
    "folder-move-to",
    "tinder-square",
    "tinder",
]

OUTPUT_DIR = Path("svg/stroke-rounded")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

success_count = 0
fail_count = 0

def fetch_font_svg():
    print("Fetching font file...")
    resp = requests.get(FONT_URL)
    resp.raise_for_status()
    return resp.text

def parse_glyph_names(font_svg):
    # The font SVG typically has: <glyph glyph-name="abacus" ...
    return re.findall(r'glyph-name="([^"]+)"', font_svg)

def download_icon(name, cdn_name=None):
    global success_count, fail_count
    url_name = cdn_name or name
    url = CDN_URL.format(name=url_name)
    resp = requests.get(url)

    if resp.status_code == 200:
        path = OUTPUT_DIR / f"{url_name}.svg"
        path.write_text(resp.text)
        success_count += 1
        print(f"✔ Downloaded: {name}.svg")
    else:
        fail_count += 1
        print(f"✘ Failed: {name} ({url})")

def main():
    font_svg = fetch_font_svg()
    glyph_names = parse_glyph_names(font_svg)
    print(f"Found {len(glyph_names)} glyph names.")

    for name in glyph_names:
        cdn_name = GLYPH_OVERRIDES.get(name)
        download_icon(name, cdn_name)

    extras = EXTRA_GLYPHS + HIDDEN_GLYPHS
    for name in extras:
        if name in glyph_names:
            print(f"⚠ Skipped duplicate (extra/hidden also in font): {name}")
        else:
            download_icon(name)

    print("\nDownload finished.")
    print(f"✔ Success: {success_count}")
    print(f"✘ Failed:  {fail_count}")
    print(f"📦 Total icons saved: {success_count}")

if __name__ == "__main__":
    main()
