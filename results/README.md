# results/ — Direktori Keluaran Log Benchmark & Telemetri

Direktori ini menampung seluruh berkas hasil eksperimen dan pengujian benchmark dari sistem smart kiosk.

## Konvensi Penamaan Berkas & Sub-Direktori
Setiap kali eksperimen dijalankan, berkas atau folder hasil pengujian dibuat dengan format cap waktu terstruktur:
```text
results/
├── benchmark_YYYYMMDD_HHMMSS.csv     # Rekaman metrik tabular
├── benchmark_YYYYMMDD_HHMMSS.jsonl    # Log telemetri event per detik
└── <YYYYMMDD_HHMMSS>_<jenis>_<tag>/   # Folder paket eksperimen lengkap (meta.json, run.log, results.csv)
```

## Integritas Data & Aturan Sitasi Bab IV
1. **Dilarang Menghapus Run Gagal:** Run yang mengalami error/OOM tetap disimpan untuk dianalisis sebagai batas kapasitas sistem (*system failure threshold*).
2. **Kutipan Naskah Skripsi:** Setiap angka, tabel, atau grafik yang dicantumkan pada naskah Bab IV harus merujuk langsung ke berkas hasil spesifik di direktori ini.
