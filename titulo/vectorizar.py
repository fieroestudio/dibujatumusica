"""Vectoriza el título escrito a mano (titulo/original.jpg) y genera titulo.svg.
Uso: python vectorizar.py original.jpg
Requisitos: pip install opencv-python numpy
Las cajas de cada letra (x en píxeles del recorte) están ajustadas a esta foto concreta.
"""
import sys, cv2, numpy as np
src = sys.argv[1] if len(sys.argv) > 1 else 'original.jpg'
im = cv2.imread(src)
crop = im[700:1020, 120:2140]                      # franja donde está el texto
g = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
# brillo del papel (máximo local) para compensar sombras, luego umbral
bg = cv2.GaussianBlur(cv2.dilate(g, np.ones((45, 45), np.uint8)), (0, 0), 15)
n = np.clip(g.astype(np.float32) / bg * 255, 0, 255).astype(np.uint8)
_, m = cv2.threshold(n, 170, 255, cv2.THRESH_BINARY_INV)
m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
# suavizar bordes
m2 = cv2.resize(m, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
m2 = cv2.GaussianBlur(m2, (0, 0), 1.6); _, m2 = cv2.threshold(m2, 120, 255, cv2.THRESH_BINARY)
boxes = [('D',20,135),('I',170,240),('B',355,475),('U',476,590),('J',665,770),('A',775,862),
         ('T',935,1038),('Ü',1038,1156),('M',1205,1322),('U',1350,1447),('S',1475,1578),('I',1638,1716),('C',1772,1872),('A',1898,2008)]
letters = []
for ch, x0, x1 in boxes:
    sub = m2[:, x0*2:x1*2].copy()
    k, lab, st, _ = cv2.connectedComponentsWithStats(sub)
    keep = np.zeros_like(sub)
    for i in range(1, k):
        if st[i][4] > 150: keep[lab == i] = 255     # quita motas
    ys, xs = np.nonzero(keep)
    letters.append((ch, keep, xs.min(), xs.max(), ys.min(), ys.max()))
gap, wgap = 26, 80                                   # espacio entre letras y entre palabras
words = [[0,1,2,3,4,5], [6,7], [8,9,10,11,12,13]]     # DIBUJA / TU / MUSICA
cols = ['#efa52f','#4a6fd6','#de5b3c','#e07bb5','#2f9a72','#7d63d1','#4fb3d9','#a77b54']
x = 0; paths = []; ci = 0
top = min(l[4] for l in letters); bot = max(l[5] for l in letters)
for w in words:
    for li in w:
        ch, keep, xa, xb, ya, yb = letters[li]
        cs, _ = cv2.findContours(keep, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
        d = ''
        for c in cs:
            c = cv2.approxPolyDP(c, 1.0, True).reshape(-1, 2)
            if len(c) < 3: continue
            d += 'M' + ' L'.join(f'{px-xa+x:.0f} {py-top:.0f}' for px, py in c) + 'Z'
        paths.append(f'<path fill="{cols[ci % len(cols)]}" d="{d}"/>'); ci += 1
        x += (xb - xa) + gap
    x += wgap - gap
W = x - wgap + gap; H = bot - top + 4
svg = f'<svg class="hand" viewBox="0 0 {W} {H}" fill-rule="evenodd" role="img" aria-label="Dibuja tu música">' + ''.join(paths) + '</svg>'
open('titulo.svg', 'w').write(svg)
print('titulo.svg', W, H)
