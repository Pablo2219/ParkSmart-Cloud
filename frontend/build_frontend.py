import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")

if DIST.exists():
    shutil.rmtree(DIST)
DIST.mkdir()

for item in ROOT.iterdir():
    if item.name in {"dist", "build_frontend.py"}:
        continue
    target = DIST / item.name
    if item.is_dir():
        shutil.copytree(item, target)
    else:
        shutil.copy2(item, target)

(DIST / "config.js").write_text(
    "window.PARKSMART_CONFIG = {apiBaseUrl: " + repr(API_BASE_URL) + "};\n"
    "const termsScript = document.createElement('script');\n"
    "termsScript.src = 'js/terms.js';\n"
    "termsScript.defer = true;\n"
    "document.head.appendChild(termsScript);\n",
    encoding="utf-8",
)
print(f"Frontend preparado para API: {API_BASE_URL}")
