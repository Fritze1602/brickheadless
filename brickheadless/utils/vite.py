# brickheadless/utils/vite.py

import json
from pathlib import Path
from django.conf import settings

MANIFEST_PATH = (
    Path(settings.BASE_DIR) / "brickheadless" / "static" / ".vite" / "manifest.json"
)


def get_vite_asset(filename: str) -> str:
    """
    Returns the hashed JS or CSS asset path from the Vite manifest for src/main.ts.
    """
    print(f"[vite] Checking for manifest at: {MANIFEST_PATH}")

    if not MANIFEST_PATH.exists():
        print("[vite] Manifest not found.")
        raise FileNotFoundError(f"Vite manifest not found at {MANIFEST_PATH}")

    with MANIFEST_PATH.open(encoding="utf-8") as f:
        manifest = json.load(f)

    print(f"[vite] Manifest loaded: {list(manifest.keys())}")

    entry = manifest.get("src/main.ts")
    if not entry:
        print("[vite] Entry 'src/main.ts' not found in manifest!")
        raise KeyError("Manifest is missing 'src/main.ts' entry")

    if filename.endswith(".js"):
        js_file = entry.get("file")
        if js_file:
            print(f"[vite] Returning JS: {js_file}")
            return f"/static/{js_file}"
    elif filename.endswith(".css"):
        css_files = entry.get("css", [])
        if css_files:
            print(f"[vite] Returning CSS: {css_files[0]}")
            return f"/static/{css_files[0]}"

    print(f"[vite] Asset '{filename}' not found in manifest entry.")
    raise KeyError(f"Asset '{filename}' not found in manifest.")
