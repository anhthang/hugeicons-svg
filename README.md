# hugeicons-svg

A utility script to **download all free Hugeicons "stroke-rounded" SVGs** and keep them up-to-date for use in projects such as [Iconify](https://iconify.design).

This script:

- Extracts free `stroke-rounded` icon names from the Hugeicons web font.
- Downloads each as an individual SVG from the CDN.
- Saves them locally for use or conversion (e.g., Iconify sets).
- Automatically picks up new icons from the live font file.

## Requirements & Usage

### Python

- Requires Python 3.8+
- Install dependencies and run:

```bash
pip install requests
python download_free_hugeicons.py
```

### uv (recommended)

- No separate Python setup needed
- Install and run in one go:

```bash
uv pip install requests
uv run python download_free_hugeicons.py
```

Icons will be saved into the `svg/stroke-rounded/` folder.

## Updating

Just re-run the script locally or trigger the GitHub Actions job.

## License

- **Code:** MIT
- **Icons:** © Hugeicons — follow their license terms.
