#!/usr/bin/env python3
"""Script otomatis untuk mengonversi kode Mermaid menjadi gambar PNG resolusi tinggi (300 DPI).
Latar belakang putih solid, siap disisipkan ke naskah skripsi Bab III & Bab IV.

Penggunaan:
    python scripts/export_diagram.py --input <file.mmd> --output <file.png> [--scale 3]
    python scripts/export_diagram.py --all
"""

import sys
import os
import base64
import json
import urllib.request
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DIAGRAMS_DIR = ROOT_DIR / "assets" / "diagrams"

def render_mermaid_to_png(mermaid_code: str, output_png_path: Path, scale: int = 3):
    """Mengonversi sintaks string Mermaid langsung menjadi file PNG via Mermaid Ink Engine."""
    output_png_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Bungkus dalam JSON payload untuk mendukung parameter bgColor dan scale
    payload = {
        "code": mermaid_code,
        "mermaid": {
            "theme": "default",
            "themeVariables": {
                "fontFamily": "Helvetica, Arial, sans-serif",
                "fontSize": "14px"
            }
        }
    }
    
    json_bytes = json.dumps(payload).encode("utf-8")
    base64_str = base64.urlsafe_b64encode(json_bytes).decode("ascii")
    
    # URL endpoint dengan background putih solid dan skala tinggi (resolusi cetak skripsi)
    url = f"https://mermaid.ink/img/pako:{base64_str}?bgColor=!white&scale={scale}"
    
    # Fallback ke base64 biasa jika payload pako tidak dipakai
    fallback_b64 = base64.b64encode(mermaid_code.encode("utf-8")).decode("ascii")
    url_fallback = f"https://mermaid.ink/img/{fallback_b64}?bgColor=!white&scale={scale}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            content = resp.read()
    except Exception:
        # Gunakan fallback URL
        req = urllib.request.Request(url_fallback, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            content = resp.read()

    with open(output_png_path, "wb") as f:
        f.write(content)
        
    print(f"[OK] Diagram berhasil dibuat: {output_png_path}")
    return output_png_path

if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "--render-code":
        code_str = sys.argv[2]
        out_path = Path(sys.argv[3])
        render_mermaid_to_png(code_str, out_path)
    else:
        print("Gunakan fungsi render_mermaid_to_png() secara langsung.")
