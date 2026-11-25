# INDEKS & PANDUAN PENCERNAAN DOKUMEN PDF (AI DIGEST INDEX)

Direktori ini (`docs/extracted_materials/`) memuat hasil konversi dan ekstraksi komprehensif dari setiap berkas PDF di repositori. Setiap PDF dipecah menjadi berkas Markdown (`.md`) tersendiri yang mempertahankan teks lengkap tanpa simplifikasi, mengekstrak diagram/foto asli, dan memetakan relevansinya dengan Tugas Akhir Rendy.

---

## 1. Daftar Dokumen & Aset yang Tersedia

### 1.1 Dokumen Proposal Tugas Akhir Rendy Lexxy K (ITS)
- **PDF Asli:** `docs/5024231007_Rendy Lexxy K_Draft_DIKUMPULIN.pdf` (27 Halaman)
- **Teks Lengkap Terperinci (Raw Digest):** [5024231007_Rendy Lexxy K_Draft_DIKUMPULIN.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/extracted_materials/5024231007_Rendy%20Lexxy%20K_Draft_DIKUMPULIN.md)
- **Analisis & Peta Perubahan Arsitektur:** [DRAFT_SKRIPSI_RENDY_ANALYSIS.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/extracted_materials/DRAFT_SKRIPSI_RENDY_ANALYSIS.md)
- **Aset Gambar:**
  - `images/5024231007_Rendy Lexxy K_Draft_DIKUMPULIN_p1_img1.png` (Logo ITS Resolusi Tinggi)

---

### 1.2 Dokumen Jurnal Ilmiah: Adaptive GPU Resource Allocation
- **PDF Asli:** `docs/Adaptive_GPU_Resource_Allocation_for_Multi-Agent_Collaborative_Reasoning_in_Serverless_Environments.pdf` (6 Halaman)
- **Penulis:** Guilin Zhang, Wulan Guo, Ziqi Tan (George Washington University, USA)
- **Teks Lengkap Terperinci (Raw Digest):** [Adaptive_GPU_Resource_Allocation_for_Multi-Agent_Collaborative_Reasoning_in_Serverless_Environments.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/extracted_materials/Adaptive_GPU_Resource_Allocation_for_Multi-Agent_Collaborative_Reasoning_in_Serverless_Environments.md)
- **Analisis & Relevansi Tugas Akhir:** [PAPER_ADAPTIVE_GPU_ALLOCATION_ANALYSIS.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/extracted_materials/PAPER_ADAPTIVE_GPU_ALLOCATION_ANALYSIS.md)
- **Aset Gambar & Diagram Asli:**
  - `images/Adaptive_GPU_Resource_Allocation_for_Multi-Agent_Collaborative_Reasoning_in_Serverless_Environments_p4_img1.jpeg` (Arsitektur Framework Multi-Agent & Resource Engine)
  - `images/Adaptive_GPU_Resource_Allocation_for_Multi-Agent_Collaborative_Reasoning_in_Serverless_Environments_p5_img2.png` (Grafik Throughput & Latensi)
  - `images/Adaptive_GPU_Resource_Allocation_for_Multi-Agent_Collaborative_Reasoning_in_Serverless_Environments_p5_img3.png` (Grafik Pemanfaatan GPU)

---

## 2. Skrip Ekstraksi Otomatis untuk PDF Masa Depan

Setiap kali Anda mengunggah berkas PDF baru ke folder `docs/`, Anda atau AI dapat langsung menjalankan:
```bash
python scripts/convert_pdf_to_md.py
```
Skrip ini akan secara otomatis:
1. Membaca setiap halaman PDF dan mengekstrak teks lengkap dengan struktur heading.
2. Mengekstrak seluruh diagram, grafik, atau foto beresolusi tinggi ke dalam folder `docs/extracted_materials/images/`.
3. Menghasilkan file `.md` yang siap dibaca oleh AI tanpa menghabiskan banyak token/credit.
