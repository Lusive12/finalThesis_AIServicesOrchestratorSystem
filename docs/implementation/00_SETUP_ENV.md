# 00_SETUP_ENV.md — Penyiapan Lingkungan Sistem dan Dependensi

> **Bagian dari:** [implementation.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/implementation.md)  
> **Tahap:** Fondasi Eksekusi & Persiapan M0  
> **Target Mesin:** Mini PC ASRock DeskMeet (Ubuntu 24.04 / 22.04 LTS, GPU NVIDIA RTX 5060 8 GB)

---

## 1. Tujuan Dokumen
Menyiapkan seluruh lingkungan runtime dasar pada mesin host Linux agar siap menjalankan:
1. Akselerasi komputasi GPU lokal via driver NVIDIA dan CUDA Toolkit.
2. Isolasi kontainer AI via Docker Engine dan NVIDIA Container Toolkit.
3. Lingkungan eksekusi Python 3.12 untuk API Gateway, Orchestrator, dan modul Resource Management.
4. Runtime Chromium Browser dengan display server untuk mode kios potret 9:16.

---

## 2. Struktur Direktori Proyek Target

Struktur repositori kode sumber yang harus dibuat pada mesin host:

```text
proof-concept-smartkiosk/
├── configs/
│   ├── services.yaml          # Registry konfigurasi model & alokasi VRAM
│   └── kiosk_config.json      # Konfigurasi tampilan & endpoint UI
├── src/
│   ├── gateway/               # FastAPI REST & WebSocket Server (TB 2)
│   ├── orchestrator/          # State Machine & Lifecycle Management (TB 2)
│   ├── resource_manager/      # 4 Strategi GPU & PyNVML Monitor (TB 3)
│   ├── services_adapters/     # Adapter untuk model AI (STT, LLM, TTS, Visual)
│   └── ui/                    # Web Application Chromium Kiosk (TB 1)
├── experiments/               # Skrip benchmark otomatis & simulasi workload
├── results/                   # Log mentah metrik evaluasi (CSV / JSONL)
├── scripts/                   # Skrip operasional (launch, audit, export)
└── docs/                      # Dokumentasi & panduan modular
```

---

## 3. Langkah Instalasi Dependensi Sistem

### 3.1 Pembaruan Paket Sistem & Tooling Dasar
Jalankan pada terminal host Linux:

```bash
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y build-essential curl wget git jq htop pciutils dmidecode net-tools
```

### 3.2 Driver NVIDIA & CUDA Toolkit
Pastikan driver resmi NVIDIA terpasang dan mengenali arsitektur Blackwell RTX 5060:

```bash
# Deteksi kartu grafis dan driver yang direkomendasikan
ubuntu-drivers devices

# Instal driver proprietary NVIDIA (versi 550+ atau sesuai arsitektur RTX 5060)
sudo apt-get install -y nvidia-driver-550
sudo reboot
```

Setelah reboot, verifikasi bahwa GPU terdeteksi:
```bash
nvidia-smi
```
*Pastikan output menampilkan `NVIDIA GeForce RTX 5060` dengan total VRAM terdeteksi ~8192 MiB.*

### 3.3 Instalasi Docker Engine & NVIDIA Container Toolkit
Diperlukan untuk kontainerisasi layanan AI yang membutuhkan isolasi dependensi runtime:

```bash
# 1. Pasang Docker Engine resmi
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# 2. Pasang NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# 3. Uji integrasi GPU dalam Docker
docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi
```

### 3.4 Python 3.12 Virtual Environment & Dependensi Inti
Gunakan virtual environment terpisah untuk orchestrator:

```bash
# Instal Python 3.12 venv
sudo apt-get install -y python3.12 python3.12-venv python3-pip

# Inisialisasi virtual environment di root repo
python3.12 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel
```

Pasang pustaka inti backend:
```bash
pip install fastapi uvicorn[standard] pynvml pyyaml websockets requests psutil
```

### 3.5 Runtime Chromium Browser untuk Kiosk
Pasang Chromium browser untuk menjalankan UI:

```bash
sudo apt-get install -y chromium-browser unclutter
```
*(Paket `unclutter` digunakan untuk menyembunyikan kursor mouse saat mode layar sentuh aktif).*

---

## 4. Kriteria Keberhasilan Setup Lingkungan
Sebelum melanjutkan ke tahap berikutnya, pastikan checklist ini terpenuhi:
- [ ] Perintah `nvidia-smi` berhasil mengeksekusi dan menampilkan GPU RTX 5060 8 GB.
- [ ] Perintah `docker run --rm --gpus all ... nvidia-smi` berhasil mengeksekusi tanpa error izin akses.
- [ ] Python venv aktif dengan modul `fastapi`, `uvicorn`, `pynvml`, dan `yaml` terimpor tanpa peringatan.
- [ ] Chromium dapat dipanggil dari terminal host.
