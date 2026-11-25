import urllib.request
import base64
from pathlib import Path

OUT_DIR = Path("assets/diagrams")
OUT_DIR.mkdir(parents=True, exist_ok=True)

code = """flowchart LR
    classDef step fill:#F9FAFB,stroke:#1F2937,stroke-width:1.5px
    classDef startEnd fill:#F3F4F6,stroke:#1F2937,stroke-width:2px
    classDef act fill:#E0F2FE,stroke:#0284C7,stroke-width:2px
    classDef eval fill:#FEE2E2,stroke:#DC2626,stroke-width:2px

    A([Mulai]):::startEnd --> S1[3.3.1 Verifikasi Hardware dan Lingkungan]:::step
    S1 --> S2[3.3.2 Pemilihan dan Pengujian Mandiri Model AI]:::step
    S2 --> S3[3.3.3 Perancangan Arsitektur Microservices dan UI Kiosk]:::step
    S3 --> S4[3.3.4 Implementasi dan Kontainerisasi Layanan AI]:::step
    S4 --> S5[3.3.5 Pengembangan Orkestrator dan Resource Management]:::act
    S5 --> S6[3.3.6 Integrasi Sistem dan Uji Fungsional End-to-End]:::step
    S6 --> S7[3.3.7 Pengujian Kinerja Komparatif 4 Strategi]:::act
    S7 --> S8[3.3.8 Analisis Data, Trade-off, dan Kesimpulan]:::eval
    S8 --> Z([Selesai]):::startEnd
"""

b64 = base64.urlsafe_b64encode(code.strip().encode("utf-8")).decode("ascii")
url = f"https://mermaid.ink/img/{b64}?bgColor=!white"
out_file = OUT_DIR / "bab3_05_tahapan_pelaksanaan_penelitian.png"

print("Mengunduh diagram alur tahapan pelaksanaan penelitian...")
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=30) as resp:
    out_file.write_bytes(resp.read())
print(f"-> Berhasil dibuat: {out_file} ({out_file.stat().st_size} bytes)")
