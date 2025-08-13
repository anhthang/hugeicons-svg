# hugeicons-svg

A utility script to **download all free Hugeicons "stroke-rounded" SVGs** and keep them up-to-date for use in projects such as [Iconify](https://iconify.design).

This script:

- Parses the Hugeicons web font (`hgi-stroke-rounded.svg`) to extract **all available free icon names**.
- Downloads each icon in **individual SVG format** from Hugeicons CDN.
- Saves them locally for further processing (e.g., adding to Iconify collections).
- Makes it easier to maintain and update free Hugeicons assets without manually browsing their site.

## Features

- **Free icons only** → Covers the `stroke-rounded` style from Hugeicons free version.
- **Automated fetching** → No need to manually check which icons are available.
- **Iconify-ready** → Downloaded SVGs can be processed into Iconify JSON sets for web/app use.
- **Version-independent** → Uses the live font file to detect icon list, so it works even if Hugeicons adds new icons.

## Requirements

- Python 3.8+
- `requests` library

Install dependencies:

```bash
pip install requests
```

## Usage

Run the script:

```bash
python download_free_hugeicons.py
```

Icons will be saved into the `hugeicons_svgs/` folder.

## Updating

Re-run the script to get the latest icons.  
It will detect new glyphs from the font and download them automatically.

## License

- **Code:** MIT
- **Icons:** © Hugeicons — follow their license terms.
