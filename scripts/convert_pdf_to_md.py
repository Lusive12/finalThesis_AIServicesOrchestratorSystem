#!/usr/bin/env python3
"""Script untuk mengekstrak isi PDF (teks lengkap, struktur, tabel, dan gambar)
menjadi format Markdown yang ramah AI, hemat konteks token, dan lengkap tanpa simplifikasi.
"""

import sys
import os
from pathlib import Path
import pymupdf  # PyMuPDF

ROOT_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT_DIR / "docs"
OUT_DIR = DOCS_DIR / "extracted_materials"
IMG_DIR = OUT_DIR / "images"

OUT_DIR.mkdir(parents=True, exist_ok=True)
IMG_DIR.mkdir(parents=True, exist_ok=True)

def process_pdf(pdf_path: Path):
    doc = pymupdf.open(pdf_path)
    base_name = pdf_path.stem
    md_file = OUT_DIR / f"{base_name}.md"
    
    print(f"\n[+] Memproses: {pdf_path.name} ({len(doc)} halaman)...")
    
    md_lines = []
    md_lines.append(f"# Ekstraksi Komprehensif Dokumen: `{pdf_path.name}`\n")
    md_lines.append(f"> **Sumber Asli:** `{pdf_path}`  ")
    md_lines.append(f"> **Jumlah Halaman:** {len(doc)}  ")
    md_lines.append(f"> **Tujuan:** Digest representasi teks lengkap, tabel, dan gambar untuk referensi AI tugas akhir tanpa memangkas detail teknis.\n")
    md_lines.append("---\n")
    
    img_counter = 0
    
    for page_idx in range(len(doc)):
        page = doc[page_idx]
        page_num = page_idx + 1
        
        md_lines.append(f"\n## --- Halaman {page_num} ---\n")
        
        # Ekstrak gambar di halaman ini
        image_list = page.get_images(full=True)
        if image_list:
            for img_info in image_list:
                xref = img_info[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                # Filter gambar kecil/icon (kurang dari 2KB)
                if len(image_bytes) < 2048:
                    continue
                    
                img_counter += 1
                img_filename = f"{base_name}_p{page_num}_img{img_counter}.{image_ext}"
                img_save_path = IMG_DIR / img_filename
                
                with open(img_save_path, "wb") as f_img:
                    f_img.write(image_bytes)
                
                rel_path = f"images/{img_filename}"
                md_lines.append(f"\n![Gambar Halaman {page_num} ({img_filename})]({rel_path})\n")
                print(f"    Ekstrak gambar: {img_filename} ({len(image_bytes)} bytes)")
        
        # Ekstrak teks halaman
        text = page.get_text("text")
        if text.strip():
            md_lines.append(text)
        else:
            md_lines.append("*(Halaman tidak memuat teks selectable / halaman kosong)*")
            
    with open(md_file, "w", encoding="utf-8") as f_md:
        f_md.write("\n".join(md_lines))
        
    print(f"[OK] File Markdown berhasil dibuat: {md_file} ({md_file.stat().st_size} bytes)")
    return md_file

if __name__ == "__main__":
    pdf_files = list(DOCS_DIR.glob("*.pdf"))
    for pdf_path in pdf_files:
        process_pdf(pdf_path)
