import re
import requests
from pathlib import Path

# URLs
FONT_URL = "https://use.hugeicons.com/font/hgi-stroke-rounded.svg"
SVG_URL_TEMPLATE = "https://cdn.hugeicons.com/icons/{name}-stroke-rounded.svg?v=2.0"

# Output folder
OUTPUT_DIR = Path("svg/stroke-rounded")
OUTPUT_DIR.mkdir(exist_ok=True)

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
    url = SVG_URL_TEMPLATE.format(name=name)
    try:
        r = requests.get(url)
        r.raise_for_status()
        (OUTPUT_DIR / f"{name}.svg").write_bytes(r.content)
        print(f"Downloaded: {name}")
    except requests.HTTPError as e:
        print(f"Failed: {name} ({e})")

print("Done.")
