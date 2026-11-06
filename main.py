import io
import re
import tarfile
import requests
from pathlib import Path

FONT_URL = "https://use.hugeicons.com/font/hgi-stroke-rounded.svg"
CDN_URL = "https://cdn.hugeicons.com/icons/{name}-stroke-rounded.svg?v=2.0"
# The CDN still serves the old drawings, the npm package has the current (v4) ones
NPM_URL = "https://registry.npmjs.org/@hugeicons/core-free-icons/latest"

# Mapping for glyphs that have different CDN names
GLYPH_OVERRIDES = {
    # "glyph-name-in-font": "actual-cdn-name"
    # "apple-music": "",
    "arrange-by-numbers-nine-1": "arrange-by-numbers-9-1",
    "arrange-by-numbers-one-9": "arrange-by-numbers-1-9",
    "arrow-down-one-0": "arrow-down-1-0",
    "arrow-down-zero-1": "arrow-down-0-1",
    "arrow-up-one-0": "arrow-up-1-0",
    "arrow-up-zero-1": "arrow-up-0-1",
    "axis-three-d": "axis-3d",
    "columns-three-cog": "columns-3-cog",
    "component-1": "qwen",
    "file-axis-three-d": "file-axis-3d",
    "first-bracket-circle": "1st-bracket-circle",
    "first-bracket-square": "1st-bracket-square",
    "first-bracket": "1st-bracket",
    "five-g-signal": "5-g-signal",
    "four-g-signal": "4-g-signal",
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
    "move-three-d": "move-3d",
    "mp-three-02": "mp-3-02",
    "navigation-two-off": "navigation-2-off",
    "printer-three-d": "printer-3d",
    "root-first-bracket": "root-1st-bracket",
    "root-second-bracket": "root-2nd-bracket",
    "root-third-bracket": "root-3rd-bracket",
    "rotate-three-d": "rotate-3d",
    "scale-three-d": "scale-3d",
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
    "three-g-signal": "3-g-signal",
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

# Glyphs where '-1' is intentional even though the name without it also exists
VALID_MINUS_ONE_GLYPHS = {
    "component-1",
}


OUTPUT_DIR = Path("svg/stroke-rounded")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

success_count = 0
fail_count = 0
npm_icons = {}


def fetch_font_svg():
    print("Fetching font file...")
    resp = requests.get(FONT_URL)
    resp.raise_for_status()
    return resp.text


def parse_glyph_names(font_svg):
    # The font SVG typically has: <glyph glyph-name="abacus" ...
    return re.findall(r'glyph-name="([^"]+)"', font_svg)


DIGIT_WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def npm_key(name: str) -> str:
    """Same key for npm names (ArrowDownOneZero, ThreeDPrinter) and font names (arrow-down-one-0, 3d-printer)."""
    words = re.findall(r"[A-Z]?[a-z]+|[A-Z](?![a-z])|\d+", name.replace("24", "TwentyFour"))
    return "-".join(DIGIT_WORDS[int(w)] if len(w) == 1 and w.isdigit() else w.lower() for w in words)


def element_to_svg(tag, attrs):
    parts = []
    for key, value in re.findall(r'(\w+): "([^"]*)"', attrs):
        if key == "key":
            continue
        key = re.sub(r"[A-Z]", lambda m: "-" + m.group(0).lower(), key)
        parts.append(f'{key}="{value.replace("currentColor", "#141B34")}"')
    return f"<{tag} {' '.join(parts)}/>"


def fetch_npm_icons():
    meta = requests.get(NPM_URL).json()
    print(f"Fetching @hugeicons/core-free-icons {meta['version']}...")
    resp = requests.get(meta["dist"]["tarball"])
    resp.raise_for_status()

    with tarfile.open(fileobj=io.BytesIO(resp.content)) as tar:
        index = tar.extractfile("package/dist/esm/index.js").read().decode()
        # Only the icon's own name: some aliases point to a different icon (Foursquare -> FourSquare)
        for file in re.findall(r"from '\./(\w+)Icon\.js';", index):
            source = tar.extractfile(f"package/dist/esm/{file}Icon.js").read().decode()
            elements = re.findall(r'\["(\w+)", \{ (.*?) \}\]', source)
            svg = "\n".join(
                ['<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">']
                + [element_to_svg(tag, attrs) for tag, attrs in elements]
                + ["</svg>\n"]
            )
            npm_icons[npm_key(file)] = svg


def normalize_glyph_name(name: str, all_names: set[str]) -> str:
    """
    Remove trailing '-1' ONLY if it is a font-generated duplicate,
    i.e. the name without it is also in the font.
    Keep '-1' for known valid glyphs.
    """
    if (
        name.endswith("-1")
        and name[:-2] in all_names
        and name not in VALID_MINUS_ONE_GLYPHS
    ):
        return name[:-2]
    return name


def download_icon(name, cdn_name=None):
    global success_count, fail_count

    # Check if the name ends with a hyphen and remove it
    if name.endswith("-"):
        name = name[:-1]

    url_name = cdn_name or name
    path = OUTPUT_DIR / f"{url_name}.svg"

    svg = npm_icons.get(npm_key(name)) or npm_icons.get(npm_key(url_name))
    if svg:
        path.write_text(svg)
        success_count += 1
        return

    print(f"⚠ Not in npm package, using CDN: {name}")
    url = CDN_URL.format(name=url_name)
    resp = requests.get(url)

    if resp.status_code == 200:
        path.write_text(resp.text)
        success_count += 1
        # print(f"✔ Downloaded: {name}.svg")
    else:
        fail_count += 1
        print(f"✘ Failed: {name} ({url})")


def main():
    fetch_npm_icons()
    font_svg = fetch_font_svg()

    raw_glyph_names = parse_glyph_names(font_svg)
    print(f"Found {len(raw_glyph_names)} raw glyph names.")

    all_names = set(raw_glyph_names)
    glyph_names = sorted(
        {normalize_glyph_name(name, all_names) for name in raw_glyph_names}
    )
    print(f"After removing '-1' duplicates: {len(glyph_names)} unique glyph names.")

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
