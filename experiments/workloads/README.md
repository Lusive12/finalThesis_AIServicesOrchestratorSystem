# experiments/workloads/ — Data Input Uji Terkontrol

Direktori ini menyimpan rangkaian data uji (*test workload*) yang digunakan secara konsisten pada setiap pengujian benchmark.

## Kategori Data Input
1. `voice_queries.jsonl` — Daftar 50+ transkrip pertanyaan informasi kampus dalam Bahasa Indonesia dan Inggris.
2. `audio/` — File rekaman audio suara masukan standar untuk pengujian reproduktifitas latensi STT.
3. `images/` — Citra uji representatif untuk evaluasi model visual (Rekomendasi Busana, Try-on, Photobooth).

Semua file uji dihitung nilai SHA-256 hash-nya oleh `runlog.py` untuk menjamin integritas bukti ilmiah di Bab IV.
