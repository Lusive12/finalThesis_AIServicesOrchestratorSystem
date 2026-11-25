#!/usr/bin/env python3
"""Generator gambar teknis & diagram Smart Kiosk (SVG murni, tanpa dependensi).

Jalankan:  python3 gambar/generate.py
Semua dimensi fisik ada di blok PARAMETER di bawah. Dimensi layar/tiang/alas
masih ESTIMASI dari foto -- setelah unit asli diukur, ubah angkanya lalu
jalankan ulang skrip ini agar semua gambar ikut menyesuaikan.
"""
import html
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent

# ----------------------------------------------------------------- PARAMETER
# Layar + dudukan (estimasi dari foto, asumsi panel 32 inci) -- satuan mm
SCREEN_W, SCREEN_H, SCREEN_T = 430, 735, 40   # ukuran luar panel (potret)
BEZEL = 12
TOTAL_H = 1250                                # lantai -> tepi atas layar
BASE_W, BASE_D, BASE_T = 400, 450, 50         # alas
POLE_W, POLE_D = 60, 50                       # tiang
POLE_X = 40                                   # jarak tiang dari tepi belakang alas
SCREEN_X = 130                                # sisi belakang panel dari tepi belakang alas
# Mini PC ASRock DeskMeet (dari spesifikasi pabrikan)
PC_W, PC_D, PC_H = 168, 219, 218
PC_X = 100                                    # sisi belakang PC dari tepi belakang alas
# Periferal yang diusulkan
CAM_W, CAM_H, CAM_D = 30, 95, 30              # webcam dipasang potret
CAM_VFOV, CAM_HFOV, CAM_TILT = 70.0, 43.0, -5.0
BAR_W, BAR_H, BAR_D = 360, 60, 80             # soundbar
MIC_W, MIC_H = 120, 15
# Pengguna
USER_H, EYE_H = 1650, 1540
NEAR_D, FAR_D = 600, 1800                     # jarak dari muka layar
ZONE_A, ZONE_B = (400, 800), (1600, 2200)

SCREEN_BOTTOM = TOTAL_H - SCREEN_H
SCREEN_FACE = SCREEN_X + SCREEN_T
CAM_LENS_H = TOTAL_H + 60
TANGGAL = "30-09-2026"

# ------------------------------------------------------------------- GAYA
INK, MUTE, HAIR = "#1b1f24", "#5b6470", "#a3abb5"
DIM, ACC = "#0b5cad", "#c2410c"
PAPER, FILL, DARK = "#ffffff", "#f1f3f5", "#2b3038"
C_STT, C_LLM, C_TTS = "#2563eb", "#7c3aed", "#0d9488"
FONT = "Helvetica, Arial, sans-serif"


def _attrs(kw):
    return "".join(
        f' {k.replace("_", "-")}="{v}"' for k, v in kw.items() if v is not None
    )


class Svg:
    def __init__(self, w, h):
        self.w, self.h, self.el = w, h, []

    def raw(self, s):
        self.el.append(s)

    def rect(self, x, y, w, h, **kw):
        kw.setdefault("fill", "none")
        kw.setdefault("stroke", INK)
        kw.setdefault("stroke_width", 1.2)
        self.raw(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}"{_attrs(kw)}/>')

    def line(self, x1, y1, x2, y2, **kw):
        kw.setdefault("stroke", INK)
        kw.setdefault("stroke_width", 1.2)
        self.raw(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"{_attrs(kw)}/>')

    def poly(self, pts, closed=False, **kw):
        kw.setdefault("fill", "none")
        kw.setdefault("stroke", INK)
        kw.setdefault("stroke_width", 1.2)
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        tag = "polygon" if closed else "polyline"
        self.raw(f'<{tag} points="{p}"{_attrs(kw)}/>')

    def circle(self, cx, cy, r, **kw):
        kw.setdefault("fill", "none")
        kw.setdefault("stroke", INK)
        kw.setdefault("stroke_width", 1.2)
        self.raw(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}"{_attrs(kw)}/>')

    def ellipse(self, cx, cy, rx, ry, **kw):
        kw.setdefault("stroke", "none")
        self.raw(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}"{_attrs(kw)}/>')

    def text(self, x, y, s, size=12, anchor="start", weight=400, fill=INK, rotate=None, **kw):
        tr = f' transform="rotate({rotate} {x:.1f} {y:.1f})"' if rotate is not None else ""
        self.raw(
            f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" '
            f'font-weight="{weight}" fill="{fill}"{tr}{_attrs(kw)}>{html.escape(s, quote=False)}</text>'
        )

    def arrow(self, x, y, ang, size=7, fill=DIM):
        """Kepala panah; ujung di (x, y), mengarah ke sudut ang (radian)."""
        pts = [(x, y)]
        for d in (160, -160):
            a = ang + math.radians(d)
            pts.append((x + size * math.cos(a), y + size * math.sin(a)))
        self.poly(pts, closed=True, fill=fill, stroke="none")

    def dim_h(self, x1, x2, y, label, ext=None, size=11):
        if ext is not None:
            o = 4 if y > ext else -4
            for x in (x1, x2):
                self.line(x, ext, x, y + o, stroke=DIM, stroke_width=0.6)
        self.line(x1, y, x2, y, stroke=DIM, stroke_width=0.8)
        self.arrow(x1, y, math.pi)
        self.arrow(x2, y, 0)
        self.text((x1 + x2) / 2, y - 5, label, size=size, anchor="middle", fill=DIM, weight=600)

    def dim_v(self, x, y1, y2, label, ext=None, size=11):
        if ext is not None:
            o = 4 if x > ext else -4
            for y in (y1, y2):
                self.line(ext, y, x + o, y, stroke=DIM, stroke_width=0.6)
        self.line(x, y1, x, y2, stroke=DIM, stroke_width=0.8)
        top, bot = min(y1, y2), max(y1, y2)
        self.arrow(x, top, -math.pi / 2)
        self.arrow(x, bot, math.pi / 2)
        self.text(x - 5, (y1 + y2) / 2, label, size=size, anchor="middle", fill=DIM, weight=600, rotate=-90)

    def balloon(self, n, bx, by, tx, ty, r=11):
        d = math.hypot(tx - bx, ty - by) or 1
        self.line(bx + (tx - bx) * r / d, by + (ty - by) * r / d, tx, ty, stroke=ACC, stroke_width=0.9)
        self.circle(tx, ty, 2.2, fill=ACC, stroke="none")
        self.badge(n, bx, by, r)

    def badge(self, n, bx, by, r=11):
        self.circle(bx, by, r, fill=PAPER, stroke=ACC, stroke_width=1.4)
        self.text(bx, by + 4, str(n), size=11, anchor="middle", weight=700, fill=ACC)

    def flow(self, x1, y1, x2, y2, color=INK, dashed=False, both=False, width=1.4):
        ang = math.atan2(y2 - y1, x2 - x1)
        self.line(x1, y1, x2, y2, stroke=color, stroke_width=width,
                  stroke_dasharray="6 4" if dashed else None)
        self.arrow(x2, y2, ang, size=9, fill=color)
        if both:
            self.arrow(x1, y1, ang + math.pi, size=9, fill=color)

    def save(self, name):
        body = "\n".join(self.el)
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
            f'width="{self.w}" height="{self.h}" font-family="{FONT}">\n'
            '<defs>\n'
            '<pattern id="hatch" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            '<line x1="0" y1="0" x2="0" y2="7" stroke="#ffffff" stroke-width="3" stroke-opacity="0.38"/></pattern>\n'
            '</defs>\n'
            f'<rect width="{self.w}" height="{self.h}" fill="{PAPER}"/>\n{body}\n</svg>\n'
        )
        (OUT / name).write_text(svg, encoding="utf-8")
        print("tulis", OUT / name)


# ----------------------------------------------------------- ELEMEN BERSAMA
def frame(s):
    s.rect(10, 10, s.w - 20, s.h - 20, stroke_width=0.8)
    s.rect(20, 20, s.w - 40, s.h - 40, stroke_width=1.8)


def title_block(s, title, no, scale):
    x, y, w, h = s.w - 540, s.h - 130, 520, 110
    s.rect(x, y, w, h, fill=PAPER, stroke_width=1.8)
    s.line(x, y + 40, x + w, y + 40, stroke_width=0.8)
    s.line(x, y + 76, x + w, y + 76, stroke_width=0.8)
    s.line(x + 330, y, x + 330, y + 40, stroke_width=0.8)
    for cx in (x + 130, x + 270, x + 400):
        s.line(cx, y + 76, cx, y + h, stroke_width=0.8)
    s.text(x + 10, y + 15, "PROYEK", size=8, fill=MUTE)
    s.text(x + 10, y + 32, "Smart Kiosk Berbasis AI Lokal", size=13, weight=700)
    s.text(x + 340, y + 15, "NO. GAMBAR", size=8, fill=MUTE)
    s.text(x + 340, y + 32, no, size=13, weight=700)
    s.text(x + 10, y + 53, "JUDUL", size=8, fill=MUTE)
    s.text(x + 10, y + 69, title, size=13, weight=700)
    cells = [(x, "SKALA", scale), (x + 130, "SATUAN", "milimeter (mm)"),
             (x + 270, "TANGGAL", TANGGAL), (x + 400, "REVISI", "A — draf PoC")]
    for cx, k, v in cells:
        s.text(cx + 10, y + 89, k, size=8, fill=MUTE)
        s.text(cx + 10, y + 103, v, size=10.5, weight=600)


def floor(s, x1, x2, y):
    s.line(x1, y, x2, y, stroke_width=1.6)
    x = x1 + 6
    while x < x2:
        s.line(x, y + 1, x - 7, y + 9, stroke=HAIR, stroke_width=0.7)
        x += 12


def view_title(s, x, y, title, sub=None):
    s.text(x, y, title, size=14, weight=700, anchor="middle")
    w = len(title) * 4.4
    s.line(x - w, y + 5, x + w, y + 5, stroke_width=1)
    if sub:
        s.text(x, y + 21, sub, size=10.5, anchor="middle", fill=MUTE)


def person(s, X, Y, xc, k, facing=-1, arm_to=None, fill="#d7dce3"):
    """Siluet tampak samping. X, Y: fungsi mm -> px. xc: posisi tengah badan (mm)."""
    arm = "#bcc4ce"
    s.rect(X(xc - 60), Y(900), 120 * k, 900 * k, rx=45 * k, fill=fill, stroke="none")
    s.rect(X(xc - 95), Y(1430), 190 * k, 600 * k, rx=80 * k, fill=fill, stroke="none")
    s.rect(X(xc - 35), Y(1480), 70 * k, 90 * k, fill=fill, stroke="none")
    s.ellipse(X(xc + facing * 10), Y(USER_H - 115), 88 * k, 115 * k, fill=fill)
    sh = (xc + facing * 15, 1370)
    if arm_to:
        el = (xc + facing * 150, 1130)
        s.poly([(X(sh[0]), Y(sh[1])), (X(el[0]), Y(el[1])), (X(arm_to[0]), Y(arm_to[1]))],
               stroke=arm, stroke_width=50 * k, stroke_linecap="round", stroke_linejoin="round")
    else:
        s.line(X(sh[0]), Y(sh[1]), X(xc + facing * 25), Y(860), stroke=arm,
               stroke_width=50 * k, stroke_linecap="round")


def cam_rays(length_x):
    """Titik ujung sinar atas/bawah kamera (mm) pada jarak horizontal length_x dari lensa."""
    up = math.radians(CAM_TILT + CAM_VFOV / 2)
    dn = math.radians(CAM_TILT - CAM_VFOV / 2)
    return CAM_LENS_H + length_x * math.tan(up), CAM_LENS_H + length_x * math.tan(dn)


# ------------------------------------------------ SK-01  GAMBAR TEKNIS KIOSK
def sheet_kiosk():
    s = Svg(1600, 1130)
    frame(s)
    k, FL = 0.5, 935

    # ======================= TAMPAK DEPAN =======================
    CX = 335
    fx = lambda mm: CX + mm * k
    fy = lambda h: FL - h * k
    floor(s, 95, 565, FL)

    # alas + tiang
    s.rect(fx(-BASE_W / 2), fy(BASE_T), BASE_W * k, BASE_T * k, rx=8, fill=PAPER)
    s.rect(fx(-POLE_W / 2), fy(SCREEN_BOTTOM), POLE_W * k, (SCREEN_BOTTOM - BASE_T) * k, fill=FILL)
    # penutup PC (garis putus) + PC
    s.rect(fx(-PC_W / 2 - 12), fy(BASE_T + PC_H + 12), (PC_W + 24) * k, (PC_H + 12) * k,
           stroke=MUTE, stroke_width=0.9, stroke_dasharray="5 3", rx=4)
    px0, py0 = fx(-PC_W / 2), fy(BASE_T + PC_H)
    s.rect(px0, py0, PC_W * k, PC_H * k, fill="#454a52", rx=2)
    s.line(px0 + 26, py0, px0 + 26, py0 + PC_H * k, stroke="#7b828c", stroke_width=0.8)
    s.circle(px0 + 13, py0 + 16, 3, stroke="#c8ced6", stroke_width=1)
    for i in range(3):
        s.rect(px0 + 8, py0 + 44 + i * 11, 10, 5, stroke="#c8ced6", stroke_width=0.7)
    # soundbar
    bx, by = fx(-BAR_W / 2), fy(SCREEN_BOTTOM - 15)
    s.rect(bx, by, BAR_W * k, BAR_H * k, rx=6, fill="#e3e6ea")
    for i in range(1, 22):
        s.line(bx + i * 8 + 2, by + 7, bx + i * 8 + 2, by + BAR_H * k - 7, stroke=HAIR, stroke_width=0.8)
    # lampu LED opsional
    for sgn in (-1, 1):
        lx = fx(sgn * (SCREEN_W / 2 + 6)) - (9 if sgn < 0 else 0)
        s.rect(lx, fy(1180), 9, 600 * k, stroke=MUTE, stroke_width=0.9, stroke_dasharray="4 3", fill="#fff7d6")
    # layar
    s.rect(fx(-SCREEN_W / 2), fy(TOTAL_H), SCREEN_W * k, SCREEN_H * k, rx=7, fill=PAPER, stroke_width=1.5)
    s.rect(fx(-SCREEN_W / 2 + BEZEL), fy(TOTAL_H - BEZEL), (SCREEN_W - 2 * BEZEL) * k,
           (SCREEN_H - 2 * BEZEL) * k, rx=3, fill=DARK, stroke="none")
    s.text(CX, fy(920), "LAYAR SENTUH 32″", size=12, anchor="middle", fill="#e8ebef", weight=700)
    s.text(CX, fy(920) + 17, "potret · 1080 × 1920", size=10.5, anchor="middle", fill="#b9c0c9")
    s.text(CX, fy(920) + 33, "tata letak UI: lihat SK-02", size=9.5, anchor="middle", fill="#8e96a1")
    # kamera (potret) + mic array di tepi atas
    s.rect(fx(-CAM_W / 2), fy(TOTAL_H + 5 + CAM_H), CAM_W * k, CAM_H * k, rx=4, fill="#454a52")
    s.rect(fx(-20), fy(TOTAL_H + 5), 40 * k, 5 * k, fill="#454a52", stroke="none")
    s.circle(CX, fy(CAM_LENS_H), 4.5, fill="#9fd0ff", stroke="#e8ebef", stroke_width=1)
    mx = fx(70)
    s.rect(mx, fy(TOTAL_H + MIC_H), MIC_W * k, MIC_H * k, rx=3, fill="#454a52")
    for i in range(4):
        s.circle(mx + 9 + i * 14, fy(TOTAL_H + MIC_H / 2), 1.3, fill="#e8ebef", stroke="none")

    # dimensi tampak depan
    xl = fx(-SCREEN_W / 2) - 9
    s.dim_v(xl - 28, fy(0), fy(SCREEN_BOTTOM), str(SCREEN_BOTTOM), ext=xl + 6)
    s.dim_v(xl - 28, fy(SCREEN_BOTTOM), fy(TOTAL_H), str(SCREEN_H), ext=xl + 6)
    s.dim_v(xl - 66, fy(0), fy(TOTAL_H), str(TOTAL_H), ext=xl - 28)
    s.dim_v(xl - 104, fy(0), fy(TOTAL_H + 5 + CAM_H), str(TOTAL_H + 5 + CAM_H), ext=xl - 66)
    s.line(xl - 104, fy(TOTAL_H + 5 + CAM_H), fx(-CAM_W / 2) - 4, fy(TOTAL_H + 5 + CAM_H), stroke=DIM, stroke_width=0.6)
    ytop = fy(TOTAL_H + 5 + CAM_H) - 26
    s.dim_h(fx(-SCREEN_W / 2), fx(SCREEN_W / 2), ytop, str(SCREEN_W), ext=fy(TOTAL_H) - 3)
    s.dim_h(fx(-BASE_W / 2), fx(BASE_W / 2), FL + 30, str(BASE_W), ext=FL + 2)

    # balon tampak depan
    BXF = 525
    s.balloon(4, BXF, fy(1345), fx(15), fy(1335))
    s.balloon(5, BXF, fy(1262), fx(70 + MIC_W), fy(1258))
    s.balloon(7, BXF, fy(1080), fx(SCREEN_W / 2 + 14), fy(1080))
    s.balloon(1, BXF, fy(900), fx(SCREEN_W / 2 - 4), fy(900))
    s.balloon(6, BXF, fy(470), fx(BAR_W / 2 - 6), fy(470))
    s.balloon(2, BXF, fy(350), fx(POLE_W / 2 - 4), fy(350))
    s.balloon(3, BXF, fy(190), fx(PC_W / 2 - 6), fy(190))
    s.balloon(10, BXF, fy(100), fx(PC_W / 2 + 12), fy(100))
    view_title(s, CX, FL + 78, "TAMPAK DEPAN")

    # ======================= TAMPAK SAMPING =======================
    SX0 = 650
    sx = lambda mm: SX0 + mm * k
    floor(s, 585, 1105, FL)
    # pengguna + garis pandang + sinar kamera (di belakang objek lain)
    ux = SCREEN_FACE + NEAR_D
    lens = (SCREEN_FACE + 4, CAM_LENS_H)
    ray_len = 640
    hu, hd = cam_rays(ray_len)
    s.poly([(sx(lens[0]), fy(lens[1])), (sx(lens[0] + ray_len), fy(hu)), (sx(lens[0] + ray_len), fy(hd))],
           closed=True, fill=DIM, fill_opacity=0.06, stroke="none")
    person(s, sx, fy, ux, k, facing=-1, arm_to=(SCREEN_FACE + 8, 960))
    for hh in (hu, hd):
        s.line(sx(lens[0]), fy(lens[1]), sx(lens[0] + ray_len), fy(hh), stroke=DIM, stroke_width=0.8,
               stroke_dasharray="7 4")
    s.text(sx(lens[0] + 250), fy(CAM_LENS_H + 250 * math.tan(math.radians(CAM_TILT + CAM_VFOV / 2))) - 12,
           f"vFOV ≈ {CAM_VFOV:.0f}° (tilt {CAM_TILT:.0f}°)", size=10.5, fill=DIM, weight=600, anchor="middle",
           rotate=-(CAM_TILT + CAM_VFOV / 2))
    s.line(sx(ux - 70), fy(EYE_H), sx(SCREEN_FACE), fy(TOTAL_H - SCREEN_H / 2), stroke=MUTE, stroke_width=0.8,
           stroke_dasharray="2 4")
    # alas, tiang, engsel
    s.rect(sx(0), fy(BASE_T), BASE_D * k, BASE_T * k, rx=8, fill=PAPER)
    s.rect(sx(POLE_X), fy(960), POLE_D * k, (960 - BASE_T) * k, fill=FILL)
    s.rect(sx(POLE_X + POLE_D), fy(925), (SCREEN_X - POLE_X - POLE_D) * k, 80 * k, fill="#c9ced5")
    # jalur kabel (8) + kabel daya (9)
    s.poly([(sx(PC_X), fy(210)), (sx(POLE_X - 10), fy(210)), (sx(POLE_X - 10), fy(1000)), (sx(SCREEN_X), fy(1000))],
           stroke=ACC, stroke_width=1.6, stroke_dasharray="6 3")
    s.raw(f'<path d="M {sx(0):.1f} {fy(25):.1f} C {sx(-50):.1f} {fy(25):.1f}, {sx(-40):.1f} {fy(90):.1f}, '
          f'{sx(-95):.1f} {fy(95):.1f}" fill="none" stroke="{INK}" stroke-width="2.2"/>')
    s.rect(sx(-118), fy(107), 12, 12, fill="#454a52", rx=2)
    # soundbar, PC + penutup
    s.rect(sx(SCREEN_FACE - BAR_D), fy(SCREEN_BOTTOM - 15), BAR_D * k, BAR_H * k, rx=5, fill="#e3e6ea")
    s.rect(sx(PC_X - 8), fy(BASE_T + PC_H + 12), (PC_D + 20) * k, (PC_H + 12) * k, stroke=MUTE,
           stroke_width=0.9, stroke_dasharray="5 3", rx=4)
    qx, qy = sx(PC_X), fy(BASE_T + PC_H)
    s.rect(qx, qy, PC_D * k, PC_H * k, fill="#454a52", rx=2)
    for i in range(7):
        s.line(qx + 14, qy + 16 + i * 8, qx + PC_D * k - 26, qy + 16 + i * 8, stroke="#7b828c", stroke_width=0.8)
    s.text(qx + PC_D * k / 2, qy + 92, "GPU + PSU", size=9, anchor="middle", fill="#c8ced6")
    # layar (tampak samping) + kamera
    s.rect(sx(SCREEN_X), fy(TOTAL_H), SCREEN_T * k, SCREEN_H * k, rx=4, fill=PAPER, stroke_width=1.5)
    s.line(sx(SCREEN_FACE) - 3, fy(TOTAL_H - BEZEL), sx(SCREEN_FACE) - 3, fy(SCREEN_BOTTOM + BEZEL),
           stroke=DARK, stroke_width=3)
    s.rect(sx(SCREEN_X + 6), fy(TOTAL_H + 5 + CAM_H), CAM_D * k, CAM_H * k, rx=3, fill="#454a52")
    s.rect(sx(SCREEN_X + 6 + CAM_D), fy(CAM_LENS_H + 12), 4, 12, fill="#9fd0ff", stroke=INK, stroke_width=0.8)

    # dimensi tampak samping
    s.dim_h(sx(0), sx(BASE_D), FL + 30, str(BASE_D), ext=FL + 2)
    s.dim_h(sx(SCREEN_FACE), sx(ux), FL + 56, f"{NEAR_D} (jarak sentuh & bicara)", ext=FL + 30)
    xe = sx(ux) + 78
    s.dim_v(xe, fy(0), fy(EYE_H), f"≈ {EYE_H} (tinggi mata)", ext=sx(ux) + 40)
    s.dim_h(sx(PC_X), sx(PC_X + PC_D), fy(BASE_T + PC_H) - 22, str(PC_D), ext=fy(BASE_T + PC_H) - 8)
    s.dim_v(sx(PC_X + PC_D) + 34, fy(BASE_T), fy(BASE_T + PC_H), str(PC_H), ext=sx(PC_X + PC_D) + 8)
    s.text(sx(ux), fy(USER_H) - 10, f"pengguna ≈ {USER_H}", size=10.5, anchor="middle", fill=MUTE)
    s.text(sx(SCREEN_FACE + 345), fy(1335), "garis pandang", size=9.5, fill=MUTE, rotate=-51)

    # balon tampak samping
    BXS = 600
    s.balloon(4, sx(40), fy(1400), sx(SCREEN_X + 14), fy(1335))
    s.balloon(1, BXS, fy(1130), sx(SCREEN_X + 3), fy(1130))
    s.balloon(2, BXS, fy(700), sx(POLE_X + 8), fy(700))
    s.balloon(8, BXS, fy(520), sx(POLE_X - 10), fy(520))
    s.balloon(9, BXS, fy(190), sx(-60), fy(80))
    s.balloon(6, sx(300), fy(400), sx(SCREEN_FACE - 10), fy(455))
    s.balloon(3, sx(420), fy(330), sx(PC_X + PC_D - 30), fy(245))
    view_title(s, sx(330), FL + 98, "TAMPAK SAMPING", "pengguna pada jarak interaksi dekat")

    # ======================= KETERANGAN =======================
    LX, LY, LW = 1135, 42, 425
    s.text(LX, LY + 12, "KETERANGAN KOMPONEN", size=13, weight=700)
    s.line(LX, LY + 20, LX + LW, LY + 20, stroke_width=1.2)
    rows = [
        (1, "Layar sentuh 32″ potret — sudah ada", "1080 × 1920 · HDMI + USB sentuh dari PC (perlu diverifikasi)"),
        (2, "Tiang & alas — sudah ada", f"Alas ≈ {BASE_W} × {BASE_D} · tinggi total ≈ {TOTAL_H}"),
        (3, "Mini PC ASRock DeskMeet — sudah ada", "Ryzen 5 · 16 GB · RTX 5060 LP 8 GB · SSD 1 TB · PSU 500 W"),
        (4, "Kamera USB 1080p, dipasang potret", "VLM busana · try-on · photobooth · deteksi kehadiran"),
        (5, "Mic array USB far-field", "Beamforming + echo cancellation · masukan STT"),
        (6, "Speaker / soundbar", "Keluaran TTS · di bawah layar, terpisah dari mic"),
        (7, "Lampu LED pengisi (opsional)", "Pencahayaan konsisten untuk photobooth & try-on"),
        (8, "Jalur kabel HDMI + USB", "Di belakang tiang, dirapikan dengan klip / selongsong"),
        (9, "Kabel daya AC", "Satu kabel ke stopkontak · power strip di alas (PC + layar)"),
        (10, "Penutup PC berventilasi", "Plat berlubang / akrilik · celah udara ≥ 50 mm"),
    ]
    y = LY + 44
    for n, a, b in rows:
        s.badge(n, LX + 12, y)
        s.text(LX + 34, y - 2, a, size=11.5, weight=700)
        s.text(LX + 34, y + 13, b, size=10, fill=MUTE)
        y += 41
    # catatan
    NY = y + 8
    s.text(LX, NY, "CATATAN", size=13, weight=700)
    s.line(LX, NY + 8, LX + LW, NY + 8, stroke_width=1.2)
    notes = [
        "1. Dimensi layar, tiang, dan alas adalah ESTIMASI dari foto",
        "    (asumsi panel 32″). Ukur unit asli sebelum membuat dudukan.",
        f"2. Dimensi PC mengikuti spesifikasi DeskMeet: {PC_W} × {PC_D} × {PC_H}.",
        "3. Komponen 4–7 dan 10 belum ada pada unit (perlu pengadaan).",
        "4. Mic di atas dan speaker di bawah agar gema suara TTS",
        "    tidak masuk kembali ke STT.",
        "5. PC diletakkan di alas supaya titik berat rendah dan kiosk",
        "    tidak mudah terguling; pasang pengikat ke alas.",
        f"6. Pusat layar ≈ {TOTAL_H - SCREEN_H // 2} dari lantai — rendah untuk pengguna",
        "    berdiri. Tata letak UI menyesuaikan (SK-02).",
    ]
    for i, t in enumerate(notes):
        s.text(LX, NY + 28 + i * 16.5, t, size=10.5, fill=INK)

    title_block(s, "Gambar Teknis Kiosk — Tampak Depan & Samping", "SK-01", "≈ 1 : 8 (A3)")
    s.save("01-gambar-teknis-kiosk.svg")


# -------------------------------------- SK-02  ZONA INTERAKSI & TATA LETAK UI
def sheet_zona():
    s = Svg(1600, 1130)
    frame(s)
    z = 0.25
    EX0, EY = 120, 585
    ex = lambda mm: EX0 + mm * z
    ey = lambda h: EY - h * z
    XMAX, CEIL = 2560, 2100
    lens = (SCREEN_FACE + 4, CAM_LENS_H)
    up = math.tan(math.radians(CAM_TILT + CAM_VFOV / 2))
    dn = math.tan(math.radians(CAM_TILT - CAM_VFOV / 2))
    x_ceil = lens[0] + (CEIL - lens[1]) / up
    x_floor = lens[0] + (0 - lens[1]) / dn
    full_body = x_floor - SCREEN_FACE

    # ---------------- elevasi ----------------
    s.poly([(ex(lens[0]), ey(lens[1])), (ex(x_ceil), ey(CEIL)), (ex(XMAX), ey(CEIL)),
            (ex(XMAX), ey(0)), (ex(x_floor), ey(0))], closed=True, fill=DIM, fill_opacity=0.07, stroke="none")
    s.line(ex(lens[0]), ey(lens[1]), ex(x_ceil), ey(CEIL), stroke=DIM, stroke_width=0.9, stroke_dasharray="7 4")
    s.line(ex(lens[0]), ey(lens[1]), ex(x_floor), ey(0), stroke=DIM, stroke_width=0.9, stroke_dasharray="7 4")
    floor(s, 70, ex(XMAX) + 10, EY)
    # pita zona di lantai
    for (a, b), col in ((ZONE_A, ACC), (ZONE_B, DIM)):
        s.rect(ex(SCREEN_FACE + a), EY - 5, (b - a) * z, 10, fill=col, stroke="none", rx=2)
    person(s, ex, ey, SCREEN_FACE + NEAR_D, z, arm_to=(SCREEN_FACE + 8, 960))
    person(s, ex, ey, SCREEN_FACE + FAR_D, z)
    # kiosk ringkas
    s.rect(ex(0), ey(BASE_T), BASE_D * z, BASE_T * z, rx=3, fill=PAPER)
    s.rect(ex(POLE_X), ey(960), POLE_D * z, (960 - BASE_T) * z, fill=FILL)
    s.rect(ex(PC_X), ey(BASE_T + PC_H), PC_D * z, PC_H * z, fill="#454a52")
    s.rect(ex(SCREEN_X), ey(TOTAL_H), SCREEN_T * z, SCREEN_H * z, fill=PAPER, stroke_width=1.4)
    s.line(ex(SCREEN_FACE) - 1.5, ey(TOTAL_H - BEZEL), ex(SCREEN_FACE) - 1.5, ey(SCREEN_BOTTOM + BEZEL),
           stroke=DARK, stroke_width=2.5)
    s.rect(ex(SCREEN_X + 6), ey(TOTAL_H + 5 + CAM_H), CAM_D * z, CAM_H * z, fill="#454a52")
    # label
    s.text(ex(SCREEN_FACE + NEAR_D), ey(USER_H) - 12, "A", size=13, weight=700, anchor="middle", fill=ACC)
    s.text(ex(SCREEN_FACE + FAR_D), ey(USER_H) - 12, "B", size=13, weight=700, anchor="middle", fill=DIM)
    s.text(ex(1450), ey(1990), f"cakupan vertikal kamera ≈ {CAM_VFOV:.0f}° (kamera potret, tilt {CAM_TILT:.0f}°)",
           size=11, fill=DIM, weight=600)
    fb = f"{full_body / 1000:.1f} m".replace(".", ",")
    s.text(ex(SCREEN_FACE + FAR_D) + 34, EY - 42, "seluruh badan masuk", size=10, fill=DIM)
    s.text(ex(SCREEN_FACE + FAR_D) + 34, EY - 29, f"bingkai mulai ≈ {fb}", size=10, fill=DIM)
    s.dim_h(ex(SCREEN_FACE), ex(SCREEN_FACE + NEAR_D), EY + 34, str(NEAR_D), ext=EY + 8)
    s.dim_h(ex(SCREEN_FACE), ex(SCREEN_FACE + FAR_D), EY + 60, str(FAR_D), ext=EY + 34)
    s.dim_v(ex(0) - 28, ey(0), ey(CAM_LENS_H), f"{CAM_LENS_H} (lensa)", ext=ex(SCREEN_X))
    view_title(s, ex(1300), EY + 90, "ELEVASI — CAKUPAN KAMERA", "kamera menghadap pengguna; A = interaksi dekat, B = tangkap citra")

    # ---------------- denah ----------------
    zr = lambda zn: " – ".join(f"{v / 1000:.1f}".replace(".", ",") for v in zn)
    PY = 886
    py = lambda mm: PY + mm * z
    HALF = 640
    th = math.tan(math.radians(CAM_HFOV / 2))
    x_clip = lens[0] + HALF / th
    s.poly([(ex(lens[0]), PY), (ex(x_clip), py(-HALF)), (ex(XMAX), py(-HALF)), (ex(XMAX), py(HALF)),
            (ex(x_clip), py(HALF))], closed=True, fill=DIM, fill_opacity=0.07, stroke="none")
    for sg in (-1, 1):
        s.line(ex(lens[0]), PY, ex(x_clip), py(sg * HALF), stroke=DIM, stroke_width=0.9, stroke_dasharray="7 4")
    s.rect(ex(SCREEN_FACE + ZONE_A[0]), py(-330), (ZONE_A[1] - ZONE_A[0]) * z, 660 * z, rx=10,
           fill=ACC, fill_opacity=0.10, stroke=ACC, stroke_width=1, stroke_dasharray="6 4")
    s.rect(ex(SCREEN_FACE + ZONE_B[0]), py(-420), (ZONE_B[1] - ZONE_B[0]) * z, 840 * z, rx=10,
           fill=DIM, fill_opacity=0.10, stroke=DIM, stroke_width=1, stroke_dasharray="6 4")
    # jangkauan mic (busur)
    R = 1000
    a0 = math.radians(38)
    p1 = (ex(lens[0] + R * math.cos(a0)), py(-R * math.sin(a0)))
    p2 = (ex(lens[0] + R * math.cos(a0)), py(R * math.sin(a0)))
    s.raw(f'<path d="M {p1[0]:.1f} {p1[1]:.1f} A {R * z:.1f} {R * z:.1f} 0 0 1 {p2[0]:.1f} {p2[1]:.1f}" '
          f'fill="none" stroke="{MUTE}" stroke-width="0.9" stroke-dasharray="3 4"/>')
    s.text(p1[0] + 8, p1[1] - 2, "jangkauan mic array ≈ 1 m", size=10, fill=MUTE)
    # kiosk dari atas
    s.rect(ex(0), py(-BASE_W / 2), BASE_D * z, BASE_W * z, rx=8, fill=PAPER)
    s.rect(ex(POLE_X), py(-POLE_W / 2), POLE_D * z, POLE_W * z, fill=FILL)
    s.rect(ex(PC_X), py(-PC_W / 2), PC_D * z, PC_W * z, fill="#454a52")
    s.rect(ex(SCREEN_X), py(-SCREEN_W / 2), SCREEN_T * z, SCREEN_W * z, fill=PAPER, stroke_width=1.4)
    s.line(ex(SCREEN_FACE) - 1.5, py(-SCREEN_W / 2 + BEZEL), ex(SCREEN_FACE) - 1.5, py(SCREEN_W / 2 - BEZEL),
           stroke=DARK, stroke_width=2.5)
    # orang dari atas
    for d in (NEAR_D, FAR_D):
        cx = ex(SCREEN_FACE + d)
        s.ellipse(cx, PY, 115 * z, 230 * z, fill="#d7dce3")
        s.circle(cx - 3, PY, 90 * z, fill="#bcc4ce", stroke="none")
    s.text(ex(SCREEN_FACE + sum(ZONE_A) / 2), py(-330) - 8, "ZONA A · sentuh & suara", size=11, weight=700,
           anchor="middle", fill=ACC)
    s.text(ex(SCREEN_FACE + sum(ZONE_A) / 2), py(330) + 16, zr(ZONE_A) + " m", size=10.5, anchor="middle", fill=ACC)
    s.text(ex(SCREEN_FACE + sum(ZONE_B) / 2), py(-420) - 8, "ZONA B · tangkap citra seluruh badan", size=11,
           weight=700, anchor="middle", fill=DIM)
    s.text(ex(SCREEN_FACE + sum(ZONE_B) / 2), py(420) + 16, zr(ZONE_B) + " m · stiker lantai “berdiri di sini”",
           size=10.5, anchor="middle", fill=DIM)
    s.text(ex(2350), py(-HALF) + 16, f"hFOV ≈ {CAM_HFOV:.0f}°", size=10.5, fill=DIM, weight=600)
    view_title(s, ex(1300), 1084, "DENAH — ZONA INTERAKSI")

    # ---------------- detail UI ----------------
    UX, UY, u = 880, 84, 0.3
    UW, UH = 1080 * u, 1920 * u
    s.text(UX + UW / 2, UY - 22, "DETAIL — TATA LETAK UI (1080 × 1920)", size=14, weight=700, anchor="middle")
    s.rect(UX - 7, UY - 7, UW + 14, UH + 14, rx=10, fill=PAPER, stroke_width=1.5)
    s.rect(UX, UY, UW, UH, rx=3, fill="#f7f8fa", stroke=HAIR, stroke_width=0.8)
    uy = lambda p: UY + p * u
    bands = [90, 800, 1040, 1240, 1660]
    for b in bands:
        s.line(UX, uy(b), UX + UW, uy(b), stroke=HAIR, stroke_width=0.8)
    # bilah status
    s.rect(UX + 10, uy(22), 58, 15, rx=7.5, fill=DARK, stroke="none")
    s.text(UX + 39, uy(22) + 11, "ID | EN", size=9, anchor="middle", fill=PAPER, weight=700)
    s.circle(UX + UW - 18, uy(45), 4, fill="#16a34a", stroke="none")
    s.text(UX + UW - 28, uy(45) + 3.5, "siap", size=9, anchor="end", fill=MUTE)
    # avatar
    ax, ay = UX + UW / 2, uy(400)
    s.circle(ax, ay - 20, 42, fill="#d7dce3", stroke="none")
    s.raw(f'<path d="M {ax - 88:.1f} {uy(800):.1f} C {ax - 88:.1f} {ay + 30:.1f}, {ax + 88:.1f} {ay + 30:.1f}, '
          f'{ax + 88:.1f} {uy(800):.1f} Z" fill="#d7dce3"/>')
    s.text(ax, uy(150), "AVATAR DIGITAL", size=11, weight=700, anchor="middle", fill=MUTE)
    # transkrip
    s.rect(UX + 14, uy(822), 170, 22, rx=8, fill="#e3e6ea", stroke="none")
    s.text(UX + 22, uy(822) + 15, "“Di mana ruang dosen?”", size=9.5, fill=INK)
    s.rect(UX + 70, uy(822) + 30, UW - 84, 30, rx=8, fill=DARK, stroke="none")
    s.text(UX + 78, uy(822) + 43, "Ruang dosen ada di lantai 2,", size=9.5, fill=PAPER)
    s.text(UX + 78, uy(822) + 55, "sebelah kanan tangga…", size=9.5, fill=PAPER)
    # tombol mic
    mcx, mcy = UX + UW / 2, uy(1140)
    s.circle(mcx, mcy, 22, fill=ACC, stroke="none")
    s.rect(mcx - 4.5, mcy - 12, 9, 16, rx=4.5, fill=PAPER, stroke="none")
    s.raw(f'<path d="M {mcx - 9:.1f} {mcy - 1:.1f} a 9 9 0 0 0 18 0" fill="none" stroke="{PAPER}" stroke-width="1.8"/>')
    s.line(mcx, mcy + 8, mcx, mcy + 13, stroke=PAPER, stroke_width=1.8)
    s.text(mcx + 34, mcy + 4, "Tekan & bicara", size=10, fill=MUTE)
    # menu 2x2
    tiles = ["Informasi", "Rekomendasi Busana", "Virtual Try-On", "AI Photobooth"]
    tw, th_ = (UW - 42) / 2, (uy(1660) - uy(1240) - 40) / 2
    for i, t in enumerate(tiles):
        tx = UX + 14 + (i % 2) * (tw + 14)
        ty = uy(1240) + 13 + (i // 2) * (th_ + 14)
        s.rect(tx, ty, tw, th_, rx=8, fill=PAPER, stroke=INK, stroke_width=1)
        s.text(tx + tw / 2, ty + th_ / 2 + 4, t, size=10, weight=700, anchor="middle")
    s.text(UX + UW / 2, uy(1780), "Pemberitahuan privasi · logo · QR unduh hasil", size=9, anchor="middle", fill=MUTE)
    # tinggi fisik tiap batas (kiri)
    mm_per_px = (SCREEN_H - 2 * BEZEL) / 1920
    top_mm = TOTAL_H - BEZEL
    for b in [0] + bands + [1920]:
        h = top_mm - b * mm_per_px
        s.line(UX - 7, uy(b), UX - 20, uy(b), stroke=DIM, stroke_width=0.7)
        s.text(UX - 24, uy(b) + 3.5, f"{h:.0f}", size=9.5, anchor="end", fill=DIM, weight=600)
    s.text(UX - 66, UY + UH / 2, "tinggi dari lantai (mm)", size=10, anchor="middle", fill=DIM, rotate=-90)
    # anotasi (kanan)
    AXR = UX + UW + 40
    ann = [
        ("A", 45, "Bilah status", "Bahasa ID/EN · mode aktif · status model", "Rendy"),
        ("B", 445, "Avatar digital", "Lip-sync & ekspresi dari audio TTS, dekat garis mata", "Gung"),
        ("C", 920, "Transkrip & jawaban", "Hasil STT dan jawaban LLM yang di-stream", "Ferdie"),
        ("D", 1140, "Tombol mic", "Push-to-talk / VAD · pemicu prefetch LLM", "Rendy"),
        ("E", 1450, "Menu layanan", "Informasi · Busana · Try-On · Photobooth", "Ferdie · Ria · Erdi · Deva"),
        ("F", 1790, "Area non-interaktif", "Terlalu rendah untuk disentuh sambil berdiri", "—"),
    ]
    for tag, p, a, b, who in ann:
        yy = uy(p)
        s.line(UX + UW + 7, yy, AXR - 12, yy, stroke=ACC, stroke_width=0.9)
        s.badge(tag, AXR, yy)
        s.text(AXR + 20, yy - 4, a, size=11.5, weight=700)
        s.text(AXR + 20, yy + 10, b, size=10, fill=MUTE)
        s.text(AXR + 20, yy + 23, f"TA: {who}", size=9.5, fill=ACC, weight=600)

    # catatan desain
    NX, NY = 850, 724
    s.text(NX, NY, "CATATAN DESAIN", size=13, weight=700)
    s.line(NX, NY + 8, NX + 700, NY + 8, stroke_width=1.2)
    notes = [
        f"1. Kamera dipasang potret (diputar 90°) agar bidang pandang vertikal ≈ {CAM_VFOV:.0f}°; seluruh badan pengguna",
        f"    tertangkap mulai jarak ≈ {fb}. Beri stiker lantai pada zona B.",
        "2. Zona A dipakai untuk percakapan dan sentuhan; zona B untuk rekomendasi busana, try-on, dan photobooth.",
        "    UI memandu pengguna mundur ke zona B (hitung mundur + pratinjau kamera).",
        "3. Layar relatif rendah: avatar dan teks ditaruh di bagian atas (dekat garis mata), kontrol sentuh",
        "    di tengah, bagian bawah tanpa tombol. Seluruh kontrol berada < 1220 mm (terjangkau kursi roda).",
        "4. Saat try-on video, pengguna berdiri di zona B dan tidak dapat menjangkau layar: tampilan layar penuh,",
        "    kendali lewat suara, gestur, atau pewaktu (lihat SK-05).",
        "5. Jika tinggi tiang dapat diatur, naikkan layar ± 150–200 mm lalu perbarui parameter di generate.py.",
        "6. Semua tinggi pada detail UI dihitung dari dimensi estimasi — bukan hasil ukur.",
    ]
    for i, t in enumerate(notes):
        s.text(NX, NY + 28 + i * 17, t, size=10.5)

    title_block(s, "Zona Interaksi, Cakupan Kamera & Tata Letak UI", "SK-02", "1 : 16 (A3) · UI 0,3×")
    s.save("02-zona-interaksi-dan-ui.svg")


# ------------------------------------------------ SK-03  ARSITEKTUR SISTEM
def box(s, x, y, w, h, title, lines=(), who=None, fill=PAPER, top=None, tsize=12.5):
    s.rect(x, y, w, h, rx=7, fill=fill, stroke_width=1.2)
    if top:
        s.raw(f'<path d="M {x + 1:.1f} {y + 8:.1f} a 7 7 0 0 1 7 -7 h {w - 16:.1f} a 7 7 0 0 1 7 7 z" fill="{top}"/>')
    ty = y + (26 if top else 22)
    s.text(x + w / 2, ty, title, size=tsize, weight=700, anchor="middle")
    for i, t in enumerate(lines):
        s.text(x + w / 2, ty + 18 + i * 15, t, size=10.5, anchor="middle", fill=MUTE)
    if who:
        pw = len(who) * 5.6 + 14
        s.rect(x + w - pw - 8, y + h - 24, pw, 17, rx=8.5, fill=ACC, stroke="none")
        s.text(x + w - 8 - pw / 2, y + h - 12, who, size=9.5, weight=700, anchor="middle", fill=PAPER)


def sheet_arsitektur():
    s = Svg(1600, 1060)
    frame(s)
    s.text(60, 62, "ARSITEKTUR SISTEM SMART KIOSK", size=20, weight=700)
    s.text(60, 82, "Satu mesin, banyak proses: tiap model adalah layanan terpisah yang dimuat dan dilepas oleh orkestrator.",
           size=12, fill=MUTE)
    # legenda
    s.flow(1090, 58, 1150, 58)
    s.text(1160, 62, "aliran data (audio, teks, citra)", size=11)
    s.flow(1090, 80, 1150, 80, color=ACC, dashed=True)
    s.text(1160, 84, "kendali load / unload / prefetch", size=11)

    # baris I/O
    io = [("Layar sentuh 32″", "HDMI (video) + USB (sentuh)"), ("Kamera USB", "1080p, dipasang potret"),
          ("Mic array USB", "beamforming + AEC"), ("Speaker", "USB / jack 3,5 mm")]
    for i, (a, b) in enumerate(io):
        x = 80 + i * 234
        box(s, x, 112, 218, 60, a, [b], fill=FILL)
        s.flow(x + 109, 172, x + 109, 214, both=True)
    s.text(1022, 146, "PERANGKAT I/O", size=11, weight=700, fill=MUTE)

    box(s, 80, 214, 920, 70, "KIOSK UI — Chromium mode kiosk (web app potret 1080 × 1920)",
        ["Avatar · transkrip · menu layanan · pratinjau kamera · tampilan hasil"], who="Rendy")
    box(s, 1060, 214, 460, 70, "Admin & Monitoring", ["SSH via Tailscale · dasbor latensi & VRAM"], fill=FILL)
    s.flow(540, 284, 540, 326, both=True)
    s.text(552, 310, "WebSocket / HTTP (localhost)", size=10.5, fill=MUTE)

    box(s, 80, 326, 920, 70, "API GATEWAY — FastAPI (REST + WebSocket)",
        ["Streaming audio & token · routing ke layanan · manajemen sesi"], who="Rendy")
    box(s, 1060, 326, 330, 70, "Basis Pengetahuan (RAG)", ["Dokumen informasi layanan · embedding di CPU"], fill=FILL)
    s.flow(1000, 361, 1060, 361, both=True)
    s.flow(540, 396, 540, 438, both=True)
    s.flow(1460, 284, 1460, 438, color=MUTE, dashed=True)
    s.text(1452, 365, "metrik", size=10.5, fill=MUTE, anchor="end")

    # orkestrator
    s.rect(80, 438, 1440, 186, rx=9, fill="#fff4ec", stroke=ACC, stroke_width=1.8)
    s.text(100, 462, "ORKESTRATOR — kontribusi utama TA Rendy", size=13.5, weight=700, fill=ACC)
    subs = [
        ("Session & Mode Manager", ["Mode: idle · percakapan · busana ·", "try-on video · photobooth", "Satu mode GPU berat pada satu waktu"]),
        ("Pipeline Percakapan", ["VAD → STT → LLM → TTS → Avatar", "Streaming per kalimat", "Batal / sela (barge-in)"]),
        ("GPU Memory Manager", ["Registry model: disk → RAM → VRAM", "Penjadwal load/unload · prefetch", "Eviction (LRU / prediksi giliran)"]),
        ("VRAM Monitor & Metrics", ["NVML: VRAM terpakai & puncak", "Latensi per tahap & waktu swap", "Log eksperimen strategi (a)–(d)"]),
    ]
    for i, (a, ls) in enumerate(subs):
        box(s, 100 + i * 352, 476, 336, 130, a, ls)

    # layanan
    svc = [
        ("STT", ["faster-whisper", "Large v3 Turbo", "vs Qwen3-ASR", "VRAM ≈ 1,5–2,5 GB"], "Ferdie", C_STT),
        ("LLM", ["Gemma 3 / Qwen3 4B", "kuantisasi Q4", "llama.cpp / Ollama", "VRAM ≈ 3–4 GB"], "Ferdie", C_LLM),
        ("TTS", ["Piper (CPU) vs", "OpenAudio S1-mini", "bahasa ID + EN", "VRAM 0 / ≈ 2–4 GB"], "Ferdie", C_TTS),
        ("Avatar", ["Lip-sync real-time", "digerakkan audio TTS", "jalan bersama TTS", "VRAM ≈ 2–4 GB"], "Gung", "#64748b"),
        ("Rekomendasi Busana", ["VLM menganalisis citra,", "lalu difusi membuat", "beberapa gambar 2D", "VRAM ≈ 3–5 → 6–8 GB"], "Ria", "#64748b"),
        ("Try-On Video", ["Video-to-video real-time", "(mirip Decart AI)", "eksklusif & terus-menerus", "VRAM ≈ 6–8 GB"], "Erdi", "#64748b"),
        ("AI Photobooth", ["Image generation", "identity-preserving", "mode eksklusif", "VRAM ≈ 6–8 GB"], "Deva", "#64748b"),
    ]
    for i, (a, ls, who, col) in enumerate(svc):
        x = 80 + i * 208
        box(s, x, 676, 192, 150, a, ls, who=who, top=col)
        s.flow(x + 76, 624, x + 76, 676, both=True)
        s.flow(x + 116, 624, x + 116, 676, color=ACC, dashed=True)
    s.text(80, 850, "LAYANAN MODEL — satu proses per model (isolasi VRAM, isolasi dependensi CUDA, crash tidak merambat). "
           "Angka VRAM = estimasi awal, diukur ulang pada PoC.", size=11, fill=MUTE)

    # sumber daya
    s.rect(80, 876, 720, 84, rx=7, fill=DARK, stroke="none")
    s.text(100, 903, "GPU — Gigabyte RTX 5060 Low Profile · 8 GB VRAM", size=13, weight=700, fill=PAPER)
    s.text(100, 922, "Blackwell · CUDA 12.8+ · PCIe ×8", size=10.5, fill="#b9c0c9")
    segs = [("STT", 1.5, C_STT), ("LLM", 3.3, C_LLM), ("TTS", 3.0, C_TTS)]
    gx, gw = 100, 680
    s.rect(gx, 932, gw, 16, rx=3, fill="#454a52", stroke="none")
    cur = gx
    for name, gb, col in segs:
        w = gw * gb / 8
        s.rect(cur, 932, w - 2, 16, rx=3, fill=col, stroke="none")
        s.text(cur + w / 2, 944, f"{name} {gb:g} GB".replace(".", ","), size=9.5, anchor="middle", fill=PAPER, weight=700)
        cur += w
    s.text(cur + 4, 944, "sisa", size=9, fill="#b9c0c9")
    box(s, 816, 876, 344, 84, "RAM 16 GB (→ 32 GB)", ["Cache bobot / pinned memory", "untuk swap cepat RAM ↔ VRAM"], fill=FILL)
    box(s, 1176, 876, 344, 84, "SSD 1 TB", ["Penyimpanan model", "(GGUF, safetensors, CTranslate2)"], fill=FILL)
    s.text(80, 986, "Tiga model percakapan saja sudah ≈ 7,8 GB dari 8 GB; ditambah avatar, VLM, dan diffusion total jauh melebihi VRAM "
           "→ model harus bergiliran.", size=11, fill=MUTE)
    s.text(80, 1024, "SK-03 · Arsitektur sistem · rev. A (draf PoC) · " + TANGGAL, size=10, fill=MUTE)
    s.save("03-arsitektur-sistem.svg")


# ------------------------------------------------ SK-04  TIMELINE VRAM
def sheet_timeline():
    s = Svg(1600, 960)
    frame(s)
    s.text(60, 62, "TIMELINE SATU GILIRAN PERCAKAPAN — LOAD NAIF vs PREFETCH", size=20, weight=700)
    s.text(60, 82, "Ilustrasi konsep, bukan hasil ukur. Asumsi: STT 1,5 GB · LLM 3,3 GB · TTS 3,0 GB; pengguna berbicara selama 3 detik.",
           size=12, fill=MUTE)
    X0, PS = 250, 108
    tx = lambda t: X0 + t * PS
    TMAX = 11.6
    LH = 30

    def seg(y, t1, t2, col, kind, label=None):
        w = (t2 - t1) * PS
        if kind == "idle":
            s.rect(tx(t1), y, w, LH, fill=col, fill_opacity=0.18, stroke=col, stroke_width=0.8, stroke_dasharray="3 3", rx=3)
        else:
            s.rect(tx(t1), y, w, LH, fill=col, stroke="none", rx=3)
            if kind == "load":
                s.rect(tx(t1), y, w, LH, fill="url(#hatch)", stroke="none", rx=3)
        if label:
            inside = w > len(label) * 5.6 + 8
            s.text(tx(t1) + w / 2 if inside else tx(t2) + 5, y + LH / 2 + 4, label, size=10,
                   anchor="middle" if inside else "start", weight=700,
                   fill=PAPER if inside and kind != "idle" else col)

    def panel(y0, title, sub, lanes, vram, t_end, t_audio):
        s.text(60, y0, title, size=14.5, weight=700)
        s.text(60, y0 + 18, sub, size=11, fill=MUTE)
        names = ["Pengguna", "STT", "LLM", "TTS"]
        ys = [y0 + 40 + i * 42 for i in range(4)]
        for nm, y in zip(names, ys):
            s.text(X0 - 14, y + LH / 2 + 4, nm, size=12, weight=700, anchor="end")
            s.line(X0, y + LH + 6, tx(TMAX), y + LH + 6, stroke="#e3e6ea", stroke_width=0.8)
        vy0 = ys[3] + LH + 26
        VH = 80
        vyy = lambda gb: vy0 + VH - gb * VH / 8
        ay = vy0 + VH
        top = ys[0] - 8
        s.rect(X0, vy0, (TMAX) * PS, VH, fill="#f7f8fa", stroke="none")
        for t, col in ((t_end, INK), (t_audio, ACC)):
            s.line(tx(t), top, tx(t), ay, stroke=col, stroke_width=1.1, stroke_dasharray="4 3")
        seg(ys[0], 0, 3.0, "#8b95a1", "run", "berbicara")
        for li, items in enumerate(lanes):
            for it in items:
                seg(ys[li + 1], *it)
        # grafik VRAM
        s.text(X0 - 14, vy0 + VH / 2 + 4, "VRAM terpakai", size=12, weight=700, anchor="end")
        pts = [(tx(0), vyy(0))]
        for i, (t, gb) in enumerate(vram):
            pts.append((tx(t), pts[-1][1]))
            pts.append((tx(t), vyy(gb)))
        pts.append((tx(TMAX), pts[-1][1]))
        area = pts + [(tx(TMAX), vyy(0))]
        s.poly(area, closed=True, fill="#64748b", fill_opacity=0.22, stroke="none")
        s.poly(pts, stroke="#475569", stroke_width=1.8)
        s.line(X0, vyy(8), tx(TMAX), vyy(8), stroke="#b91c1c", stroke_width=1.2, stroke_dasharray="6 4")
        s.text(tx(TMAX) + 6, vyy(8) + 4, "8 GB", size=10.5, fill="#b91c1c", weight=700)
        for j, (t, gb) in enumerate(vram):
            t2 = vram[j + 1][0] if j + 1 < len(vram) else TMAX
            if gb > 0 and (t2 - t) > 0.55:
                s.text((tx(t) + tx(t2)) / 2, vyy(gb) - 5, f"{gb:.1f} GB".replace(".", ","), size=10, anchor="middle",
                       fill="#334155", weight=700)
        # sumbu waktu
        s.line(X0, ay, tx(TMAX), ay, stroke_width=1)
        for t in range(0, 12):
            s.line(tx(t), ay, tx(t), ay + 5, stroke_width=1)
            s.text(tx(t), ay + 18, f"{t} s", size=10, anchor="middle", fill=MUTE)
        # penanda
        s.text(tx(t_end) - 5, top + 3, "akhir ucapan", size=10, anchor="end", fill=INK)
        s.text(tx(t_audio) + 5, top + 3, "audio pertama", size=10, fill=ACC, weight=700)
        ly = ay + 38
        s.line(tx(t_end), ly, tx(t_audio), ly, stroke=ACC, stroke_width=2)
        s.arrow(tx(t_end), ly, math.pi, size=8, fill=ACC)
        s.arrow(tx(t_audio), ly, 0, size=8, fill=ACC)
        s.text(tx(t_audio) + 12, ly + 4, f"latensi respons ≈ {t_audio - t_end:.1f} s".replace(".", ","), size=12.5,
               weight=700, fill=ACC)

    # --- strategi (b)
    panel(128, "Strategi (b) — load/unload naif dari disk",
          "Tiap model baru dimuat setelah model sebelumnya selesai; LLM menunggu sampai seluruh jawaban jadi sebelum TTS dimuat.",
          [
              [(3.0, 4.5, C_STT, "load", "muat"), (4.5, 4.9, C_STT, "run", "STT")],
              [(4.9, 6.9, C_LLM, "load", "muat dari disk"), (6.9, 9.0, C_LLM, "run", "generate")],
              [(9.0, 10.5, C_TTS, "load", "muat dari disk"), (10.5, TMAX, C_TTS, "run", "sintesis")],
          ],
          [(3.0, 1.5), (4.9, 3.3), (9.0, 3.0)], 3.0, 10.8)

    # --- strategi (d)
    panel(528, "Strategi (d) — prefetch + swap lewat pinned memory",
          "LLM ditarik ke VRAM saat pengguna mulai bicara; TTS ditarik saat LLM mulai men-stream; STT ditukar keluar lalu masuk lagi setelah LLM selesai.",
          [
              [(0.0, 0.2, C_STT, "idle", None), (0.2, 3.3, C_STT, "run", "STT streaming + VAD"),
               (5.4, 5.7, C_STT, "load", None), (5.7, TMAX, C_STT, "idle", "siaga untuk giliran berikutnya")],
              [(0.3, 0.7, C_LLM, "load", None), (0.7, 3.3, C_LLM, "idle", "siaga di VRAM (prefetch)"),
               (3.3, 5.4, C_LLM, "run", "generate (stream)")],
              [(3.3, 3.7, C_TTS, "load", None), (3.7, 3.8, C_TTS, "idle", None), (3.8, 8.2, C_TTS, "run", "sintesis + putar per kalimat")],
          ],
          [(0.0, 1.5), (0.3, 4.8), (3.3, 6.3), (5.4, 4.5), (8.2, 1.5)], 3.0, 4.1)

    # legenda
    ly = 912
    s.text(60, ly + 4, "Legenda:", size=11, weight=700)
    lx = 130
    for col, kind, lab in (("#64748b", "load", "muat / swap-in"), ("#64748b", "run", "inferensi"),
                           ("#64748b", "idle", "siaga di VRAM")):
        if kind == "idle":
            s.rect(lx, ly - 9, 34, 16, fill=col, fill_opacity=0.18, stroke=col, stroke_width=0.8, stroke_dasharray="3 3", rx=3)
        else:
            s.rect(lx, ly - 9, 34, 16, fill=col, stroke="none", rx=3)
            if kind == "load":
                s.rect(lx, ly - 9, 34, 16, fill="url(#hatch)", stroke="none", rx=3)
        s.text(lx + 42, ly + 4, lab, size=11)
        lx += 170
    for col, lab in ((C_STT, "STT"), (C_LLM, "LLM"), (C_TTS, "TTS")):
        s.rect(lx, ly - 9, 16, 16, fill=col, stroke="none", rx=3)
        s.text(lx + 22, ly + 4, lab, size=11)
        lx += 70
    s.text(s.w - 60, ly + 4, "SK-04 · rev. A (draf PoC) · " + TANGGAL, size=10, fill=MUTE, anchor="end")
    s.save("04-timeline-vram.svg")


# ------------------------------------------------ SK-05  TAMPILAN PER MODE
def fperson(s, cx, top, h, shirt, pants, skin="#c9cfd7", op=1.0):
    """Siluet tampak depan; h = tinggi badan dalam px."""
    s.raw(f'<g opacity="{op}">')
    for dx in (-0.115, 0.015):
        s.rect(cx + dx * h, top + 0.50 * h, 0.10 * h, 0.47 * h, rx=0.03 * h, fill=pants, stroke="none")
    for sg in (-1, 1):
        s.line(cx + sg * 0.145 * h, top + 0.20 * h, cx + sg * 0.185 * h, top + 0.46 * h, stroke=shirt,
               stroke_width=0.055 * h, stroke_linecap="round")
    s.rect(cx - 0.13 * h, top + 0.155 * h, 0.26 * h, 0.37 * h, rx=0.045 * h, fill=shirt, stroke="none")
    s.circle(cx, top + 0.075 * h, 0.065 * h, fill=skin, stroke="none")
    s.raw('</g>')


def pill(s, x, y, label):
    pw = len(label) * 5.6 + 16
    s.rect(x, y, pw, 17, rx=8.5, fill=ACC, stroke="none")
    s.text(x + pw / 2, y + 12, label, size=9.5, weight=700, anchor="middle", fill=PAPER)


def sheet_tampilan():
    s = Svg(1600, 1000)
    frame(s)
    s.text(60, 62, "TAMPILAN LAYAR PER MODE", size=20, weight=700)
    s.text(60, 82, "Apa yang dilihat pengguna pada tiap layanan. Sketsa tata letak untuk layar potret 1080 × 1920, bukan desain akhir.",
           size=12, fill=MUTE)
    W, H, Y = 270, 480, 128
    xs = [70, 450, 830, 1210]
    GAR = ["#2563eb", "#0d9488", "#c2410c", "#7c3aed"]

    def screen(x, dark=False):
        s.rect(x - 7, Y - 7, W + 14, H + 14, rx=10, fill=PAPER, stroke_width=1.5)
        s.rect(x, Y, W, H, rx=3, fill=DARK if dark else "#f7f8fa", stroke=HAIR, stroke_width=0.8)

    # ---- (a) percakapan
    x = xs[0]; cx = x + W / 2
    screen(x)
    s.rect(x + 10, Y + 10, 58, 15, rx=7.5, fill=DARK, stroke="none")
    s.text(x + 39, Y + 21, "ID | EN", size=9, anchor="middle", fill=PAPER, weight=700)
    s.circle(cx, Y + 130, 46, fill="#d7dce3", stroke="none")
    s.raw(f'<path d="M {cx - 92:.1f} {Y + 262:.1f} C {cx - 92:.1f} {Y + 176:.1f}, {cx + 92:.1f} {Y + 176:.1f}, '
          f'{cx + 92:.1f} {Y + 262:.1f} Z" fill="#d7dce3"/>')
    s.raw(f'<path d="M {cx - 14:.1f} {Y + 146:.1f} q 14 10 28 0" fill="none" stroke="{MUTE}" stroke-width="2" stroke-linecap="round"/>')
    s.line(x, Y + 262, x + W, Y + 262, stroke=HAIR, stroke_width=0.8)
    s.rect(x + 14, Y + 276, 160, 22, rx=8, fill="#e3e6ea", stroke="none")
    s.text(x + 22, Y + 291, "“Di mana ruang dosen?”", size=9.5)
    s.rect(x + 60, Y + 306, W - 74, 34, rx=8, fill=DARK, stroke="none")
    s.text(x + 68, Y + 320, "Ruang dosen ada di lantai 2,", size=9.5, fill=PAPER)
    s.text(x + 68, Y + 333, "sebelah kanan tangga…", size=9.5, fill=PAPER)
    s.circle(cx, Y + 408, 24, fill=ACC, stroke="none")
    s.rect(cx - 5, Y + 395, 10, 17, rx=5, fill=PAPER, stroke="none")
    s.raw(f'<path d="M {cx - 10:.1f} {Y + 407:.1f} a 10 10 0 0 0 20 0" fill="none" stroke="{PAPER}" stroke-width="1.8"/>')
    s.line(cx, Y + 417, cx, Y + 422, stroke=PAPER, stroke_width=1.8)
    s.text(cx, Y + 456, "Tekan & bicara", size=10, anchor="middle", fill=MUTE)

    # ---- (b) rekomendasi busana: beberapa gambar 2D
    x = xs[1]
    screen(x)
    s.text(x + 14, Y + 28, "Busana yang cocok untuk Anda", size=11.5, weight=700)
    s.rect(x + 14, Y + 42, 62, 94, rx=5, fill="#e3e6ea", stroke=HAIR, stroke_width=0.8)
    fperson(s, x + 45, Y + 49, 82, "#9aa3ad", "#6b7480")
    s.text(x + 45, Y + 148, "foto asli", size=8.5, anchor="middle", fill=MUTE)
    s.text(x + 90, Y + 58, "Analisis VLM", size=10, weight=700)
    for i, ln in enumerate(["• bentuk tubuh & warna kulit", "• busana yang sedang dipakai", "• saran: kasual, warna hangat"]):
        s.text(x + 90, Y + 76 + i * 15, ln, size=9.5, fill=MUTE)
    cw, ch = 114, 132
    for i in range(4):
        gx = x + 14 + (i % 2) * (cw + 14)
        gy = Y + 160 + (i // 2) * (ch + 10)
        if i < 3:
            s.rect(gx, gy, cw, ch, rx=6, fill=PAPER, stroke=HAIR, stroke_width=0.9)
            fperson(s, gx + cw / 2, gy + 8, 100, GAR[i], ["#1e293b", "#a8a29e", "#334155"][i])
            s.text(gx + cw / 2, gy + ch - 7, f"Opsi {i + 1}", size=9, weight=700, anchor="middle")
        else:
            s.rect(gx, gy, cw, ch, rx=6, fill="#f1f3f5", stroke=HAIR, stroke_width=0.9, stroke_dasharray="4 3")
            s.circle(gx + cw / 2, gy + 54, 13, stroke=HAIR, stroke_width=3)
            s.raw(f'<path d="M {gx + cw / 2:.1f} {gy + 41:.1f} a 13 13 0 0 1 13 13" fill="none" stroke="{ACC}" stroke-width="3" stroke-linecap="round"/>')
            s.text(gx + cw / 2, gy + 90, "membuat gambar…", size=9, anchor="middle", fill=MUTE)
    s.text(x + 14, Y + 456, "3 dari 4 gambar selesai", size=9, fill=MUTE)
    s.rect(x + 14, Y + 463, W - 28, 5, rx=2.5, fill="#e3e6ea", stroke="none")
    s.rect(x + 14, Y + 463, (W - 28) * 0.75, 5, rx=2.5, fill=ACC, stroke="none")

    # ---- (c) try-on video real-time
    x = xs[2]; cx = x + W / 2
    screen(x, dark=True)
    fperson(s, cx - 20, Y + 62, 318, GAR[2], "#64748b", skin="#d9b99b", op=0.16)
    fperson(s, cx + 17, Y + 62, 318, GAR[2], "#64748b", skin="#d9b99b", op=0.16)
    fperson(s, cx, Y + 62, 318, GAR[2], "#94a3b8", skin="#d9b99b")
    s.rect(x + 12, Y + 12, 52, 18, rx=4, fill="#dc2626", stroke="none")
    s.circle(x + 22, Y + 21, 3, fill=PAPER, stroke="none")
    s.text(x + 29, Y + 25, "LIVE", size=9.5, weight=700, fill=PAPER)
    s.text(x + W - 12, Y + 25, "video real-time", size=9.5, anchor="end", fill="#b9c0c9")
    for i in range(4):
        tx_ = x + 32 + i * 54
        s.rect(tx_, Y + 398, 44, 44, rx=6, fill=GAR[(i + 2) % 4], stroke=PAPER if i == 0 else "none",
               stroke_width=2.5)
    s.text(cx, Y + 462, "Ucapkan “berikutnya” untuk ganti busana", size=9.5, anchor="middle", fill="#e8ebef")

    # ---- (d) photobooth
    x = xs[3]; cx = x + W / 2
    screen(x)
    s.text(x + 14, Y + 28, "AI Photobooth", size=11.5, weight=700)
    s.rect(x + 35, Y + 44, 200, 250, rx=6, fill="#fde7d3", stroke=INK, stroke_width=1)
    s.circle(x + 80, Y + 90, 26, fill="#fbbf77", stroke="none")
    s.circle(x + 200, Y + 250, 40, fill="#f9c9a0", stroke="none")
    s.circle(cx, Y + 150, 44, fill="#8b5e3c", stroke="none")
    s.raw(f'<path d="M {cx - 86:.1f} {Y + 293:.1f} C {cx - 86:.1f} {Y + 196:.1f}, {cx + 86:.1f} {Y + 196:.1f}, '
          f'{cx + 86:.1f} {Y + 293:.1f} Z" fill="{GAR[3]}"/>')
    for i, c in enumerate(["Kartun", "Lukisan", "Astronaut"]):
        px = x + 22 + i * 78
        s.rect(px, Y + 306, 70, 20, rx=10, fill=DARK if i == 0 else PAPER, stroke=INK, stroke_width=0.9)
        s.text(px + 35, Y + 320, c, size=9.5, anchor="middle", fill=PAPER if i == 0 else INK, weight=600)
    qx, qy, qc = cx - 40, Y + 344, 80 / 9
    s.rect(qx - 5, qy - 5, 90, 90, fill=PAPER, stroke=HAIR, stroke_width=0.8)
    for r in range(9):
        for c in range(9):
            corner = (r < 3 and c < 3) or (r < 3 and c > 5) or (r > 5 and c < 3)
            if corner or (r * 7 + c * 5 + r * c) % 3 == 0:
                s.rect(qx + c * qc, qy + r * qc, qc, qc, fill=INK, stroke="none")
    s.text(cx, Y + 456, "Pindai untuk mengunduh", size=9.5, anchor="middle", fill=MUTE)

    # ---- keterangan
    caps = [
        ("Percakapan informasi", "Ferdie · Gung",
         ["Keluaran: suara, teks, dan avatar yang berbicara.", "Posisi: zona A (dekat layar).",
          "GPU: STT → LLM → TTS bergiliran;", "avatar aktif bersama TTS."]),
        ("Rekomendasi busana", "Ria",
         ["Keluaran: beberapa gambar 2D foto pengguna", "memakai busana yang cocok untuknya.",
          "Posisi: difoto di zona B, melihat hasil di zona A.", "GPU: VLM dahulu, lalu ditukar dengan difusi gambar."]),
        ("Virtual try-on video", "Erdi",
         ["Keluaran: video bergerak real-time yang mengikuti", "gerakan pengguna (mirip Decart AI).",
          "Posisi: zona B; layar tidak terjangkau tangan.", "GPU: eksklusif dan terus-menerus selama sesi."]),
        ("AI photobooth", "Deva",
         ["Keluaran: foto bergaya dengan wajah tetap", "dikenali, plus kode QR untuk mengunduh.",
          "Posisi: difoto di zona B.", "GPU: eksklusif per foto."]),
    ]
    for x, (ttl, who, lines) in zip(xs, caps):
        cy = Y + H + 40
        s.text(x - 7, cy, ttl, size=14, weight=700)
        pill(s, x - 7, cy + 10, who)
        for i, ln in enumerate(lines):
            s.text(x - 7, cy + 50 + i * 16, ln, size=10.5, fill=MUTE if i else INK)

    s.rect(60, 826, 1480, 84, rx=8, fill="#fff4ec", stroke=ACC, stroke_width=1.2)
    s.text(80, 852, "Alur gabungan yang diusulkan", size=12.5, weight=700, fill=ACC)
    s.text(80, 873, "Ria dan Erdi memakai katalog busana yang sama. Layanan Ria memilih busana yang cocok dan menampilkannya sebagai gambar diam; "
           "pengguna mengetuk salah satu,", size=11)
    s.text(80, 891, "lalu layanan Erdi menampilkan busana itu sebagai video bergerak. Perbedaan keduanya: Ria menjawab “busana apa yang cocok”, "
           "Erdi menjawab “seperti apa saat saya bergerak”.", size=11)
    s.text(60, 952, "SK-05 · Tampilan layar per mode · rev. A (draf PoC) · " + TANGGAL, size=10, fill=MUTE)
    s.save("05-tampilan-per-mode.svg")


if __name__ == "__main__":
    sheet_kiosk()
    sheet_zona()
    sheet_arsitektur()
    sheet_timeline()
    sheet_tampilan()
