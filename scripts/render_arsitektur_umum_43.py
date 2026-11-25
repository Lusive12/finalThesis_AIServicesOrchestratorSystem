import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

OUT_DIR = Path("assets/diagrams")
OUT_DIR.mkdir(parents=True, exist_ok=True)
out_file = OUT_DIR / "bab3_01_arsitektur_umum.png"

# Setup Canvas 4:3 (Width: 16, Height: 12) -> High-Res 2400x1800 at 200 DPI
fig, ax = plt.subplots(figsize=(16, 12), dpi=200)
fig.patch.set_facecolor('#F8FAFC')
ax.set_facecolor('#F8FAFC')
ax.set_xlim(0, 16)
ax.set_ylim(0, 12)
ax.axis('off')

# Main Header & Subtitle
ax.text(8.0, 11.45, "DIAGRAM ARSITEKTUR UMUM SISTEM SMART KIOSK",
        fontsize=21, fontweight='bold', color='#0F172A', ha='center', va='center', family='sans-serif')
ax.text(8.0, 11.05, "Integrasi Multi-Layanan AI, Alur Kerja Antar-Modul, dan Pencatatan Metrik Kinerja (Format 4:3)",
        fontsize=12, color='#475569', ha='center', va='center', family='sans-serif')

def draw_subgraph(ax, x, y, w, h, title, bg_color, border_color):
    """Draw a container box with header banner"""
    box = patches.FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0,rounding_size=0.18",
                                linewidth=1.6, edgecolor=border_color,
                                facecolor=bg_color, zorder=1)
    ax.add_patch(box)
    
    # Title Banner
    banner_h = 0.52
    banner = patches.FancyBboxPatch((x, y + h - banner_h), w, banner_h,
                                   boxstyle="round,pad=0,rounding_size=0.18",
                                   linewidth=0, facecolor=border_color, zorder=2)
    ax.add_patch(banner)
    
    sq = patches.Rectangle((x, y + h - banner_h), w, 0.2,
                           linewidth=0, facecolor=border_color, zorder=2)
    ax.add_patch(sq)
    
    ax.text(x + w/2, y + h - banner_h/2, title,
            fontsize=12, fontweight='bold', color='white', ha='center', va='center', family='sans-serif', zorder=3)

def draw_node(ax, x, y, w, h, text, shape="rect", bg_color="#FFFFFF", border_color="#1E293B", text_color="#0F172A", fontsize=10.5):
    """Draw an individual process block"""
    rounding = (h / 2.0) if shape == "pill" else 0.12
    box = patches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                boxstyle=f"round,pad=0,rounding_size={rounding}",
                                linewidth=1.4, edgecolor=border_color,
                                facecolor=bg_color, zorder=4)
    ax.add_patch(box)
    
    ax.text(x, y, text, fontsize=fontsize, fontweight='bold', color=text_color,
            ha='center', va='center', family='sans-serif', zorder=5, multialignment='center')

def draw_arrow(ax, p1, p2, text=None, text_offset=(0, 0), bidirectional=False, rad=0.0, color='#334155'):
    """Draw connection arrow"""
    arrow_style = "<->" if bidirectional else "->"
    conn_style = f"arc3,rad={rad}" if rad != 0.0 else "arc3"
    
    arrow = patches.FancyArrowPatch(p1, p2,
                                   arrowstyle=arrow_style,
                                   connectionstyle=conn_style,
                                   mutation_scale=15,
                                   linewidth=2.0,
                                   edgecolor=color,
                                   zorder=6)
    ax.add_patch(arrow)
    
    if text:
        mid_x = (p1[0] + p2[0]) / 2 + text_offset[0]
        mid_y = (p1[1] + p2[1]) / 2 + text_offset[1]
        ax.text(mid_x, mid_y, text, fontsize=9.5, fontweight='bold', color='#1E293B',
                ha='center', va='center', family='sans-serif', zorder=7,
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#CBD5E1", lw=1))

# ==============================================================================
# SUBGRAPH POSITIONS (2 x 3 Balanced Grid in 4:3 Ratio)
# ==============================================================================

# ----------------- TOP ROW -----------------
# 1. Input Pengguna (Top-Left)
draw_subgraph(ax, 0.6, 6.0, 4.4, 4.6, "1. Input Pengguna", "#F8FAFC", "#475569")
draw_node(ax, 2.8, 9.2, 3.6, 0.9, "Pengguna Kiosk", shape="pill", bg_color="#F1F5F9", border_color="#334155")
draw_node(ax, 2.8, 7.3, 3.6, 0.9, "Sentuhan / Suara / Kamera", shape="rect", bg_color="#F1F5F9", border_color="#334155")
draw_arrow(ax, (2.8, 8.75), (2.8, 7.75))

# 2. UI/UX Chromium Kiosk (Top-Center)
draw_subgraph(ax, 5.6, 6.0, 4.8, 4.6, "2. UI/UX Chromium Kiosk", "#FEFCE8", "#CA8A04")
draw_node(ax, 8.0, 7.3, 4.2, 0.9, "Tampilan Layar Potret 9:16", shape="rect", bg_color="#FEF9C3", border_color="#CA8A04")
draw_node(ax, 8.0, 9.2, 4.2, 0.9, "Kirim Permintaan Aksi\nPengguna", shape="rect", bg_color="#FEF9C3", border_color="#CA8A04")
draw_arrow(ax, (8.0, 7.75), (8.0, 8.75))

# Connect Input -> UI/UX: Sentuhan/Suara/Kamera -> Tampilan Layar Potret 9:16 (Straight Horizontal)
draw_arrow(ax, (4.6, 7.3), (5.9, 7.3))

# 3. Orchestrator (Top-Right)
draw_subgraph(ax, 11.0, 6.0, 4.4, 4.6, "3. Orchestrator", "#F0F9FF", "#0284C7")
draw_node(ax, 13.2, 9.2, 3.8, 0.75, "API Gateway", shape="rect", bg_color="#E0F2FE", border_color="#0284C7")
draw_node(ax, 13.2, 8.0, 3.8, 0.75, "Routing dan Seleksi Layanan", shape="rect", bg_color="#E0F2FE", border_color="#0284C7")
draw_node(ax, 13.2, 6.75, 3.8, 0.85, "Manajer Siklus Hidup\nModel AI", shape="rect", bg_color="#E0F2FE", border_color="#0284C7")
draw_arrow(ax, (13.2, 8.82), (13.2, 8.38))
draw_arrow(ax, (13.2, 7.62), (13.2, 7.18))

# Connect UI/UX -> Orchestrator: Kirim Permintaan Aksi -> API Gateway (Straight Horizontal)
draw_arrow(ax, (10.1, 9.2), (11.3, 9.2))

# ----------------- BOTTOM ROW -----------------
# 4. Resource Management (Bottom-Right, directly below Orchestrator)
draw_subgraph(ax, 11.0, 0.9, 4.4, 4.6, "4. Resource Management", "#FAF5FF", "#9333EA")
draw_node(ax, 13.2, 4.1, 3.8, 0.85, "Eksekusi Strategi\nMemori GPU", shape="rect", bg_color="#F3E8FF", border_color="#9333EA")
draw_node(ax, 13.2, 2.1, 3.8, 0.85, "Pemantauan VRAM dan\nRAM via NVML", shape="rect", bg_color="#F3E8FF", border_color="#9333EA")
draw_arrow(ax, (13.2, 3.67), (13.2, 2.53), bidirectional=True)

# Orchestrator <-> Resource Management: Manajer Siklus Hidup <-> Eksekusi Strategi (Straight Vertical)
draw_arrow(ax, (13.2, 6.32), (13.2, 4.53), bidirectional=True)

# 5. Eksekusi Model AI (Bottom-Center)
draw_subgraph(ax, 5.6, 0.9, 4.8, 4.6, "5. Eksekusi Model AI", "#F0FDF4", "#16A34A")
draw_node(ax, 8.0, 3.1, 4.2, 1.2, "Inferensi Model AI\npada GPU Lokal", shape="rect", bg_color="#DCFCE7", border_color="#16A34A")

# Orchestrator -> Eksekusi Model AI: Manajer Siklus Hidup -> Inferensi Model AI
draw_arrow(ax, (11.3, 6.75), (9.8, 3.7), rad=0.15)

# 6. Output dan Evaluasi (Bottom-Left)
draw_subgraph(ax, 0.6, 0.9, 4.4, 4.6, "6. Output dan Evaluasi", "#FFF1F2", "#DC2626")
draw_node(ax, 2.8, 4.1, 3.8, 0.85, "Hasil Respons ke UI Kiosk", shape="rect", bg_color="#FEF9C3", border_color="#CA8A04")
draw_node(ax, 2.8, 2.1, 3.8, 0.85, "Pencatatan 5 Metrik\nEvaluasi Kinerja", shape="rect", bg_color="#FEE2E2", border_color="#DC2626")

# Eksekusi Model AI -> Hasil Respons ke UI Kiosk
draw_arrow(ax, (5.9, 3.1), (4.7, 4.1), rad=0.15)

# Pemantauan VRAM/RAM via NVML -> Pencatatan 5 Metrik Evaluasi Kinerja (Straight Horizontal across bottom)
draw_arrow(ax, (11.3, 2.1), (4.7, 2.1), color='#475569')

# Footer Caption
ax.text(8.0, 0.42, "*Diagram Arsitektur Umum Sistem: Hubungan menyeluruh dari input pengguna, orkestrasi microservices, manajemen memori GPU, hingga evaluasi empiris.",
        fontsize=10, fontstyle='italic', color='#64748B', ha='center', va='center', family='sans-serif')

plt.tight_layout()
plt.savefig(out_file, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
print(f"Berhasil membuat diagram 4:3 resolusi tinggi: {out_file} ({out_file.stat().st_size} bytes)")
