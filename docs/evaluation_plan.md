# evaluation_plan.md — Rencana Evaluasi & Milestone Bab IV

> **Lokasi:** `docs/evaluation_plan.md`  
> **Fungsi:** Perencanaan pengujian, tahapan milestone evaluasi, dan pemetaan data empiris ke naskah Bab IV Tugas Akhir.  
> **Kapan AI membaca:** Saat menyusun eksperimen, menganalisis data benchmark, atau menulis naskah Bab IV.

---

## 1. Tujuan Evaluasi

Membuktikan secara kuantitatif efektivitas sistem orkestrasi microservices dan membandingkan performa 4 strategi pengelolaan siklus hidup model AI pada GPU lokal NVIDIA RTX 5060 (8 GB VRAM) dengan tolok ukur:
1. Menjaga alokasi memori fisik GPU aman: $V_{\text{peak}} \le 7,5\text{ GB}$.
2. Meminimalkan waktu swap dan transisi: $T_{\text{swap}} < 1,0\text{ s}$ (Strategi C/D).
3. Menjaga total latensi interaksi tetap wajar bagi pengguna kiosk: $T_{\text{e2e}} \le 2,0\text{ s}$ (percakapan).
4. Menjamin ketahanan sesi: $SR \ge 99\%$ (100 giliran berturut-turut & uji stabilitas hingga 8 jam tanpa crash OOM).

---

## 2. Pemetaan Eksperimen ke Struktur Bab IV Skripsi

| Subbab Bab IV | Fokus Evaluasi | Sumber Data & Skrip | Rujukan Metrik |
|---|---|---|---|
| **4.1 Lingkungan Pengujian Aktual** | Hasil audit fisik hardware Mini PC, driver NVIDIA, CUDA, idle VRAM ($V_{\text{idle}}$), dan konfigurasi baseline | `experiments/m0_hardware_audit.py` $\rightarrow$ `results/*_audit/` | $V_{\text{idle}}$, PCIe bandwidth |
| **4.2 Karakteristik Baseline Model AI** | Konsumsi memori mandiri, load time, dan waktu inferensi murni ($T_{\text{infer}}$) masing-masing model (STT, LLM, TTS, Visual) | `experiments/m1_model_baseline.py` $\rightarrow$ `results/*_baseline/` | $T_{\text{infer}}$, Load time, Standalone $V_{\text{peak}}$ |
| **4.3 Komparasi 4 Strategi Pengelolaan GPU** | Perbandingan kinerja Strategi (a) All-Resident, (b) Naive, (c) Pinned Swap, dan (d) Prefetch pada workload seragam | `experiments/run_benchmark.py` $\rightarrow$ `results/*_strategy_comp/` | $T_{\text{swap}}$, $T_{\text{e2e}}$, $V_{\text{peak}}$ |
| **4.4 Evaluasi Transisi Mode Eksklusif** | Waktu pembersihan VRAM (barrier verification) saat berpindah dari percakapan ke mode Try-On / Photobooth dan kembali pulih | `experiments/m3_transition_eval.py` $\rightarrow$ `results/*_transitions/` | Barrier time, OOM avoidance |
| **4.5 Uji Daya Tahan & Stabilitas Sistem** | Uji 100 giliran percakapan berulang dan uji ketahanan sesi jangka panjang tanpa memori bocor | `experiments/m4_stability_test.py` $\rightarrow$ `results/*_stability/` | Stability Rate ($SR$), VRAM Drift Rate |
| **4.6 Pembahasan Trade-off Rekayasa** | Analisis komprehensif trade-off antara efisiensi memori, latensi, dan kompleksitas orkestrasi | Agregasi seluruh data empiris | Sintesis temuan ilmiah |

---

## 3. Protokol & Kriteria Pengujian Ilmiah

1. **Jumlah Sampel Minimum:** Setiap kondisi pengujian wajib diulang minimal **10 kali ($N \ge 10$)** untuk menghasilkan signifikansi statistik.
2. **Pemisahan Cache:** Pengujian wajib memisahkan data *Cold Run* (inisialisasi awal / tanpa page-cache) dan *Warm Run* (data tersimpan di page-cache atau Host RAM).
3. **Statistik Deskriptif:** Data yang disajikan dalam tabel naskah skripsi Bab IV wajib mencakup:
   - Rata-rata (*Mean*)
   - Median
   - Simpangan Baku (*Standard Deviation*)
   - Nilai Minimum dan Maksimum
4. **Integritas Bukti:** Hanya hasil eksperimen berstatus `SUCCESS` dengan metadata lengkap (`meta.json` berisi git commit, SHA-256 input, parameter run) yang sah dikutip ke dalam naskah Bab IV.
