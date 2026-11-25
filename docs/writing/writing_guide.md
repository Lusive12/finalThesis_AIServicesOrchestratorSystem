# writing_guide.md — Panduan Penulisan Skripsi & Integritas Sitasi

> **Lokasi:** `docs/writing/writing_guide.md`  
> **Fungsi:** Standar tata bahasa formal skripsi, pola paragraf argumen teknis, format sitasi IEEE, dan integritas referensi akademik.  
> **Kapan AI membaca:** Saat menyusun, merevisi, atau memformat naskah laporan skripsi (Bab I–V).

---

## 1. Identitas Proyek & Batas Ruang Lingkup

1. **Judul Resmi:** Gunakan judul persis yang telah disetujui:  
   *“Sistem Orkestrasi Layanan AI Berbasis Microservices pada Sistem Smart Kiosk”*  
   *(Microservices-Based AI Service Orchestration System for Smart Kiosks)*.  
   **Dilarang** menambahkan kata *“Rancang Bangun”*.
2. **Fokus Kontribusi:** Kontribusi utama adalah **resource-aware service orchestration**: arsitektur microservices, API gateway, registry layanan, pengelolaan siklus hidup model (*lifecycle management*), mekanisme transisi mode, dan evaluasi trade-off performa vs memori pada perangkat edge dengan 1 GPU fisik lokal (NVIDIA RTX 5060 8 GB VRAM).
3. **Bukan Kontribusi:** Penelitian ini **tidak** melatih foundation model baru dari awal (*from scratch*), **tidak** memodifikasi driver kernel NVIDIA, dan **tidak** menjanjikan pemartisian keras VRAM pada tingkat perangkat keras.
4. **Pembedaan Status:** Pisahkan secara tegas antara **rencana/desain arsitektur**, **fitur yang telah diimplementasikan**, dan **hasil pengukuran terverifikasi**. Angka target PoC (misal 100 giliran percakapan tanpa OOM, VRAM $\le 7,5$ GB) adalah target penerimaan, bukan kesimpulan sebelum diuji.

---

## 2. Pedoman Penulisan Ilmiah (Academic Writing Rules)

### 2.1 Tata Bahasa & Gaya Penulisan
- Gunakan **Bahasa Indonesia formal ragam ilmiah** yang lugas, padat, dan objektif.
- Hindari kata pengisi (*filler words*) seperti: *"tentunya"*, *"sangat penting"*, *"di era modern ini"*, *"seiring berkembangnya teknologi"*.
- Hindari repetisi konjungsi di awal paragraf seperti *"Selain itu"* atau *"Oleh karena itu"*.
- Hindari klaim superlatif tanpa data pembanding: jangan gunakan kata *"optimal"*, *"efisien"*, *"real-time"*, atau *"stabil"* kecuali didefinisikan dengan tolok ukur kuantitatif dan didukung data pengujian.
- Gunakan sudut pandang orang ketiga pasif (hindari *"penulis"*, *"kami"*, *"saya"*).

### 2.2 Pola Paragraf Argumen Teknis
Setiap paragraf penjelasan rasionalisasi atau pembahasan hasil harus mengikuti pola 4 tahap:
1. **Pernyataan Inti (*Claim*):** Paparkan inti argumen atau temuan secara jelas.
2. **Bukti (*Evidence*):** Sajikan data eksperimen, referensi literatur primer, atau standar teknis resmi.
3. **Analisis / Penalaran (*Reasoning*):** Jelaskan mengapa data tersebut terjadi dan bagaimana korelasinya dengan keterbatasan sistem (misal batas VRAM/PCIe).
4. **Keterkaitan (*Connection*):** Hubungkan dengan rumusan masalah atau implikasi perancangan tahap berikutnya.

### 2.3 Disiplin Sitasi & Integritas Referensi
- Gunakan format sitasi numerik standar **IEEE** (contoh: `[1]`, `[2]–[4]`).
- Sitasi diletakkan langsung setelah klaim teknis yang relevan.
- **Integritas Wajib:** Dilarang keras mengarang sumber, nama penulis, jurnal, DOI, atau nomor halaman. Semua rujukan harus dapat dilacak pada basis data ilmiah (IEEE Xplore, ACM DL, ScienceDirect, arXiv resmi).
- Berkas referensi BibTeX berada di `docs/bab3_latex/references.bib`.
