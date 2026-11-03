#!/usr/bin/env python3
"""Tapa algo chico de una escena rellenándolo con lo que lo rodea (difusión, sin OpenCV ni numpy).

Uso: python3 scripts/escenas/tapar.py ESCENA.webp X0 Y0 X1 Y1 oscuro|claro UMBRAL

- oscuro UMBRAL: rellena lo que tiene luminancia < UMBRAL dentro de la caja (las letras que Stitch escribe en un
  papel o un cartel, por ejemplo con UMBRAL 85 en un papel en penumbra).
- claro UMBRAL: rellena lo que tiene luminancia > UMBRAL (una franja de piel entre la chaqueta y el cinturón).

Las coordenadas son de la imagen de 1376×768. Pisa la escena y deja una vista en /tmp/escenas-vista/<nombre>.jpg.
"""
import random
import sys
from pathlib import Path

from PIL import Image, ImageFilter


def main():
    path = Path(sys.argv[1])
    x0, y0, x1, y1 = map(int, sys.argv[2:6])
    mode, threshold = sys.argv[6], int(sys.argv[7])
    im = Image.open(path).convert('RGB')
    pad = 6
    box = (x0 - pad, y0 - pad, x1 + pad, y1 + pad)
    reg = im.crop(box)
    w, h = reg.size
    lum = reg.convert('L').load()

    mask = Image.new('L', (w, h), 0)
    mp = mask.load()
    for y in range(pad, h - pad):
        for x in range(pad, w - pad):
            if (lum[x, y] < threshold) if mode == 'oscuro' else (lum[x, y] > threshold):
                mp[x, y] = 255
    mp = mask.filter(ImageFilter.MaxFilter(5)).load()

    px = [[list(reg.getpixel((x, y))) for x in range(w)] for y in range(h)]
    hole = [(x, y) for y in range(1, h - 1) for x in range(1, w - 1) if mp[x, y]]
    for _ in range(400):
        for x, y in hole:
            a, b, c, d = px[y][x - 1], px[y][x + 1], px[y - 1][x], px[y + 1][x]
            px[y][x] = [(a[i] + b[i] + c[i] + d[i]) / 4 for i in range(3)]

    random.seed(1)
    out = reg.load()
    for x, y in hole:
        grain = random.gauss(0, 3)
        out[x, y] = tuple(max(0, min(255, int(px[y][x][i] + grain))) for i in range(3))
    im.paste(reg, box[:2])
    im.save(path, 'WEBP', quality=88)

    view = Path('/tmp/escenas-vista') / f'{path.stem}.jpg'
    view.parent.mkdir(exist_ok=True)
    im.resize((688, 384)).save(view)
    print(f'{path} · {len(hole)} puntos tapados · vista: {view}')


if __name__ == '__main__':
    main()
