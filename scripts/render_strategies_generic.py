import urllib.request
import base64
from pathlib import Path

OUT_DIR = Path("assets/diagrams")
OUT_DIR.mkdir(parents=True, exist_ok=True)

DIAGRAMS = {
    "strategi_a_all_resident.png": """flowchart TD
    classDef startEnd fill:#F3F4F6,stroke:#1F2937,stroke-width:1.5px
    classDef process fill:#F9FAFB,stroke:#1F2937,stroke-width:1.5px
    classDef orch fill:#E0F2FE,stroke:#0284C7,stroke-width:2px
    classDef gpu fill:#DCFCE7,stroke:#16A34A,stroke-width:1.5px
    classDef cond fill:#FEF3C7,stroke:#D97706,stroke-width:1.5px

    A([Mulai: Inisialisasi Sistem Kiosk]):::startEnd --> B[Orkestrator Membaca services.yaml]:::process
    B --> C[Alokasikan Seluruh Model AI Sekaligus ke VRAM GPU<br/>Model 1 + Model 2 + Model N]:::gpu
    C --> D{Apakah Total VRAM &le; 7.5 GB?}:::cond
    D -- Tidak --> E[Peringatan: Risiko CUDA OOM<br/>Ganti ke Model Lebih Ringan / Gagal]:::startEnd
    D -- Ya --> F[Semua Layanan Berstatus READY]:::orch

    F --> G([Menunggu Permintaan Pengguna]):::startEnd
    G --> H[Permintaan Masuk: Input Diterima]:::process
    H --> I[Orkestrator Meneruskan Input Langsung ke Model Terkait]:::orch
    I --> J[Inferensi Dijalankan pada VRAM GPU Aktif]:::gpu
    J --> K[Kirim Hasil Inferensi ke UI Kiosk]:::process
    K --> L[Model Tetap Dipertahankan di VRAM GPU]:::gpu
    L --> G
""",
    "strategi_d_prefetch.png": """flowchart TD
    classDef startEnd fill:#F3F4F6,stroke:#1F2937,stroke-width:1.5px
    classDef process fill:#F9FAFB,stroke:#1F2937,stroke-width:1.5px
    classDef orch fill:#E0F2FE,stroke:#0284C7,stroke-width:2px
    classDef gpu fill:#DCFCE7,stroke:#16A34A,stroke-width:1.5px
    classDef cond fill:#FEF3C7,stroke:#D97706,stroke-width:1.5px

    A([Mulai: Permintaan Layanan Masuk]):::startEnd --> B[Model N Aktif: Inferensi Berjalan pada GPU]:::gpu
    B --> C[Orkestrator Mendeteksi Prediksi Alur: Model N+1 Siap Disiapkan]:::orch
    
    subgraph Parallel_Execution [Eksekusi Paralel / Overlap]
        direction TB
        D[Thread 1: Selesaikan Sisa Inferensi Model N]:::gpu
        E[Thread 2: Prefetch Bobot Model N+1 dari Host RAM ke VRAM GPU]:::gpu
    end

    C --> Parallel_Execution
    D --> F[Hasil Inferensi Model N Siap Diteruskan ke Model N+1]:::process
    E --> G{Apakah Model N+1 Sudah Ready di VRAM?}:::cond

    F --> H[Sinkronisasi Orkestrator: Handover Data Antar-Model]:::orch
    G -- Ya --> H
    G -- Belum --> I[Tunggu Prefetch Selesai: Minimal Delay]:::process
    I --> H

    H --> J[Kirim Perintah Background Unload untuk Model N yang Sudah Selesai]:::orch
    H --> K[Segera Eksekusi Inferensi Model N+1 Tanpa Menunggu Model N Selesai Dihapus]:::gpu
    K --> L[VRAM Model N Bebas Sepenuhnya]:::gpu
    L --> M([Lanjutkan Pola Prefetch ke Tahap Berikutnya N+2]):::startEnd
"""
}

for filename, code in DIAGRAMS.items():
    b64 = base64.urlsafe_b64encode(code.strip().encode("utf-8")).decode("ascii")
    url = f"https://mermaid.ink/img/{b64}?bgColor=!white"
    out_file = OUT_DIR / filename
    print(f"Mengunduh & merender {filename}...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        out_file.write_bytes(resp.read())
    print(f"-> Berhasil dibuat: {out_file} ({out_file.stat().st_size} bytes)")
