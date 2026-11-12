"""Vectoriza el icono dibujado por un niño (nota negra con trazos rosas) y genera icons/icon.svg
(y en /tmp las versiones cuadrada y maskable de las que salen icon-180.png e icon-maskable-512.png). Uso: python vectorizar_icono.py foto.jpg
Requisitos: pip install opencv-python numpy
El recorte está ajustado a la foto concreta (primer plano de la nota, 1659x2212).
Separa dos tintas: negro (poco color y oscuro) y rosa (saturado, tono rosa); cada una se pinta
con el color de la app: negro #1d1d1b y rosa #e07bb5 (color 6 de los instrumentos).
"""
import sys, cv2, numpy as np
src = sys.argv[1] if len(sys.argv) > 1 else 'nota.jpg'
c = cv2.imread(src)[560:1560, 330:1290]
hsv = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)
H, S, V = hsv[..., 0].astype(int), hsv[..., 1].astype(int), hsv[..., 2].astype(float)
bg = cv2.GaussianBlur(cv2.dilate(V.astype(np.uint8), np.ones((45, 45), np.uint8)), (0, 0), 15).astype(float)
Vn = np.clip(V / bg * 255, 0, 255)                   # brillo relativo al papel (quita sombras)
black = ((Vn < 120) & (S < 110)).astype(np.uint8) * 255
pink = ((S > 60) & ((H > 150) | (H < 8)) & (Vn > 70)).astype(np.uint8) * 255

def clean(m, close=5, min_area=1500):
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((close, close), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    k, lab, st, _ = cv2.connectedComponentsWithStats(m)
    keep = np.zeros_like(m)
    for i in range(1, k):
        if st[i][4] >= min_area: keep[lab == i] = 255   # quita motas
    m = cv2.resize(keep, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    m = cv2.GaussianBlur(m, (0, 0), 3); _, m = cv2.threshold(m, 127, 255, cv2.THRESH_BINARY)
    return m
black, pink = clean(black), clean(pink)
pink[black > 0] = 0                                   # el negro va por encima
ys, xs = np.nonzero(black | pink); x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
side = max(x1 - x0, y1 - y0)

def paths(m, color, size, pad):
    # coloca el dibujo centrado en un cuadrado de 'size' con margen 'pad' (proporción)
    s = size * (1 - 2 * pad) / side
    ox = size / 2 - (x0 + x1) / 2 * s; oy = size / 2 - (y0 + y1) / 2 * s
    cs, _ = cv2.findContours(m, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    d = ''
    for cc in cs:
        cc = cv2.approxPolyDP(cc, 1.5, True).reshape(-1, 2)
        if len(cc) < 3: continue
        d += 'M' + ' L'.join(f'{px*s+ox:.1f} {py*s+oy:.1f}' for px, py in cc) + 'Z'
    return f'<path fill="{color}" d="{d}"/>'

def svg(rounded, pad):
    bgr = f'<rect width="512" height="512" rx="{112 if rounded else 0}" fill="#ffffff"/>'
    body = paths(pink, '#e07bb5', 512, pad) + paths(black, '#1d1d1b', 512, pad)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" fill-rule="evenodd">{bgr}{body}</svg>\n'

open('icon.svg', 'w').write(svg(True, 0.12))            # pestaña y Android "any"
open("/tmp/icon-square.svg", "w").write(svg(False, 0.12))    # iPhone/iPad (el sistema redondea): se usa para icon-180.png
open("/tmp/icon-maskable.svg", "w").write(svg(False, 0.22))  # Android recorta en círculo: más margen; se usa para icon-maskable-512.png
print('listo', side)
