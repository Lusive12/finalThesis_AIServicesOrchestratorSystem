# 01_HARDWARE_AUDIT_M0.md — Prosedur Audit Perangkat Keras dan Periferal (Milestone M0)

> **Bagian dari:** [implementation.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/implementation.md)  
> **Tahap:** Milestone M0 (Verifikasi Lingkungan Fisik & Audit Kiosk)  
> **Target:** Mini PC ASRock DeskMeet + Layar Sentuh 32 Inci + Sensor USB

---

## 1. Tujuan Dokumen
Menyediakan instruksi langkah-demi-langkah dan perintah shell untuk memverifikasi spesifikasi fisik perangkat keras kios cerdas sebelum model AI dan orkestrator dijalankan. Hasil audit dicatat sebagai data empiris awal di [DECISIONS.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/DECISIONS.md) dan [CHECKPOINT.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/CHECKPOINT.md).

---

## 2. Prosedur Audit Perangkat Keras Utama

### 2.1 Audit Motherboard, CPU, dan PCIe Bus
Pastikan bandwidth bus PCIe mencukupi untuk transfer Host-to-Device (H2D) pada Strategi (c) dan (d):

```bash
# Periksa model motherboard & BIOS
sudo dmidecode -t baseboard | grep -E "Manufacturer|Product Name|Version"

# Periksa rincian CPU (AMD Ryzen 5)
lscpu | grep -E "Model name|Socket|Thread|Core|CPU max MHz"

# Periksa status jalur PCIe GPU NVIDIA (pastikan PCIe Gen 4 x8 atau x16)
sudo lspci -vv -s $(lspci | grep -i nvidia | head -n 1 | awk '{print $1}') | grep -E "LnkCap|LnkSta"
```

### 2.2 Audit Memori Host RAM dan Penyimpanan NVMe
```bash
# Periksa tipe RAM (DDR5) dan kecepatan transfer
sudo dmidecode -t memory | grep -E "Size|Type:|Speed:|Manufacturer"

# Periksa kapasitas dan sisa ruang SSD NVMe
lsblk -d -o NAME,SIZE,TYPE,MODEL
df -h /
```

### 2.3 Audit GPU dan Konsumsi VRAM Baseline (Idle)
Sebelum proses AI apa pun dijalankan, ukur konsumsi VRAM dasar yang dipakai oleh window manager / X11 / GNOME:

```bash
# Tampilkan rincian GPU, driver, dan VRAM idle
nvidia-smi --query-gpu=name,driver_version,memory.total,memory.used,memory.free --format=csv

# Periksa proses apa saja yang menggunakan VRAM
nvidia-smi pmon -c 1
```
*Catatan: Nilai $V_{\text{idle}}$ ini adalah batas bawah pemakaian VRAM sistem (biasanya sekitar 200–500 MB untuk desktop Linux).*

---

## 3. Prosedur Audit Periferal Interaksi Kiosk

### 3.1 Layar Sentuh 32 Inci (Portrait 1080x1920)
Verifikasi apakah controller layar sentuh dikenali sebagai perangkat input sentuhan:

```bash
# Deteksi perangkat pointer/touch USB
lsusb
xinput list

# Uji penangkapan event koordinat sentuh layar (tekan layar untuk melihat event)
sudo evtest /dev/input/eventX  # Ganti X sesuai nomor node touch controller
```

Untuk memastikan rotasi potret pada X11 / Wayland:
```bash
# Verifikasi resolusi layar saat ini
xrandr --current

# Jika orientasi masih landscape, putar ke portrait (kanan):
xrandr --output HDMI-1 --rotate right
```

### 3.2 Kamera USB 1080p
```bash
# Deteksi perangkat video UVC
v4l2-ctl --list-devices

# Periksa format resolusi yang didukung webcam
v4l2-ctl -d /dev/video0 --list-formats-ext
```

### 3.3 Mikrofon Array USB & Speaker
```bash
# Periksa kartu suara masukan (mikrofon)
arecord -l

# Periksa kartu suara keluaran (speaker)
aplay -l

# Uji rekaman audio singkat (3 detik)
arecord -d 3 -f cd -t wav /tmp/test_mic.wav
aplay /tmp/test_mic.wav
```

---

## 4. Templat Pencatatan Hasil Audit M0

Simpan hasil pengujian ke dalam log atau masukkan ke [DECISIONS.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/DECISIONS.md) dengan format berikut:

```markdown
### Log Audit Hardware M0:
- Tanggal Audit: [YYYY-MM-DD]
- Motherboard: ASRock DeskMeet X600 (BIOS vX.XX)
- CPU: AMD Ryzen 5 [XXXX] (X Cores, X Threads)
- RAM: 16 GB DDR5 @ [XXXX] MT/s
- GPU: NVIDIA GeForce RTX 5060 (8192 MiB VRAM)
- Driver NVIDIA: [550.XX] | CUDA: [12.X]
- PCIe Link: Gen 4 x8 (Speed 16 GT/s)
- VRAM Idle Sistem: [XXX] MiB
- Layar: 1080x1920 Portrait Touch OK
- Kamera: /dev/video0 1080p @ 30fps OK
- Audio Mic/Speaker: ALSA Card [X] OK
```

---

## 5. Kriteria Keberhasilan Milestone M0
- [ ] Seluruh perintah diagnostic berjalan tanpa segmentation fault atau missing devices.
- [ ] $V_{\text{idle}}$ tercatat dan di bawah 800 MB (memberikan sisa ruang $\ge 7,2$ GB untuk orkestrator dan model AI).
- [ ] Periferal layar sentuh, kamera, mikrofon, dan speaker merespons dengan benar.
