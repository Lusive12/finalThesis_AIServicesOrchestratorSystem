# runbook.md — Panduan Operasional Manual & Troubleshooting

> **Lokasi:** `docs/runbook.md`  
> **Fungsi:** Panduan langkah-demi-langkah bagi pengembang/mahasiswa untuk menjalankan sistem, mengeksekusi benchmark, memverifikasi GPU, dan menangani kendala teknis (troubleshooting).  
> **Kapan AI membaca:** Saat memberikan instruksi eksekusi perintah terminal atau membantu proses debugging.

---

## 1. Persiapan Lingkungan & Pengecekan Awal

### 1.1 Masuk ke Lingkungan Virtual (Virtual Environment)
```bash
# Di terminal Linux Ubuntu:
cd /path/to/proof-concept-smartkiosk
source .venv/bin/activate

# Verifikasi dependensi:
pip list | grep -E "torch|fastapi|pynvml"
```

### 1.2 Verifikasi Status GPU Fisik & Driver
```bash
# Periksa driver NVIDIA, suhu, dan alokasi VRAM awal (baseline):
nvidia-smi

# Periksa status monitor layar sentuh dan periferal USB:
lsusb
sudo libinput list-devices | grep -i -A4 touch
```

---

## 2. Menjalankan Komponen Sistem

### 2.1 Menjalankan Unified CLI (`run.py`)
Sistem dilengkapi satu pintu eksekusi utama melalui berkas `run.py`:

```bash
# Menampilkan menu bantuan dan daftar perintah:
python run.py --help

# 1. Menjalankan Gateway & Core Orchestrator:
python run.py server --host 127.0.0.1 --port 8000

# 2. Menjalankan UI Kiosk di Chromium Fullscreen:
python run.py kiosk

# 3. Menjalankan Benchmark Evaluasi 4 Strategi GPU:
python run.py benchmark --strategy all --rounds 10

# 4. Melakukan Audit Fisik Hardware (M0):
python run.py audit-hardware
```

### 2.2 Menjalankan Secara Terpisah (Manual Multi-Terminal)
Jika ingin melakukan debugging spesifik per modul:

```bash
# Terminal 1: Backend Gateway & Orchestrator
uvicorn src.orchestrator.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Peluncuran UI Kiosk (Chromium Potret 9:16)
bash scripts/launch_kiosk.sh
```

---

## 3. Eksekusi Pengujian Benchmark & Analisis Statistik

```bash
# 1. Jalankan benchmark terotomasi:
python experiments/run_benchmark.py --config configs/benchmark.yaml

# 2. Hitung statistik deskriptif dari data mentah terbaru:
python experiments/calculate_stats.py results/latest/results.csv
```

---

## 4. Troubleshooting & Penanganan Masalah Umum

### 4.1 Insiden `CUDA: Out of Memory` (OOM)
- **Gejala:** Worker AI crash, endpoint `/infer` mengembalikan HTTP 500/504, log terminal menampilkan error PyTorch CUDA OOM.
- **Penyebab:** Model sebelumnya belum melepaskan konteks VRAM sepenuhnya saat model baru dimuat.
- **Tindakan Pemulihan:**
  1. Hentikan worker bermasalah melalui orchestrator atau PID spesifik:
     ```bash
     # Cari PID worker AI:
     ps aux | grep "src.orchestrator"
     kill -9 <PID_SPESIFIK>
     ```
  2. Periksa kembali VRAM via `nvidia-smi` untuk memastikan memori kembali ke nilai baseline ($\le 1,0\text{ GB}$).
  3. Pastikan `vram_barrier.py` aktif pada konfigurasi mode eksklusif.

### 4.2 Layar Sentuh Tidak Merespons Input di Linux
- **Gejala:** Tampilan UI muncul di layar, namun sentuhan jari tidak menggerakkan kursor atau memicu event klik.
- **Tindakan:**
  1. Periksa kabel USB sentuh dari monitor ke Mini PC.
  2. Jalankan `sudo libinput debug-events` untuk memantau apakah event sentuhan terbaca pada tingkat kernel.
  3. Pastikan display server (Wayland/X11) mengenali pemetaan sentuhan ke monitor yang benar melalui `xinput` atau konfigurasi compositor.

### 4.3 Port Server Sudah Terpakai (Address Already in Use)
- **Gejala:** Uvicorn gagal start dengan error `[Errno 98] Address already in use: 8000`.
- **Tindakan:**
  ```bash
  sudo ss -ltnp | grep :8000
  # Hentikan HANYA proses milik proyek smart kiosk:
  kill -15 <PID>
  ```
