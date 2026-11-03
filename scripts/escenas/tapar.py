#!/usr/bin/env python3
"""Tapa algo chico de una escena rellenándolo con lo que lo rodea (difusión, sin OpenCV ni numpy).

Uso: python3 scripts/escenas/tapar.py ESCENA.webp X0 Y0 X1 Y1 oscuro|claro UMBRAL

- oscuro UMBRAL: rellena lo que tiene luminancia < UMBRAL dentro de la caja (las letras que Stitch escribe en un
  papel o un cartel, por ejemplo con UMBRAL 85 en un papel en penumbra).
- claro UMBRAL: rellena lo que tiene luminancia > UMBRAL (una franja de piel entre la chaqueta y el cinturón).
- piel BRILLO: pinta lo que tiene color de piel (cálido: rojo > azul) como una remera oscura de ese BRILLO (24 va bien
  debajo de la chaqueta de Nima): sirve con piel morena, que no se separa por luminancia. Dejar afuera de la caja manos,
  papeles y el cinturón (el verde no se toca).

Las coordenadas son de la imagen de 1376×768. Pisa la escena y deja una vista en /tmp/escenas-vista/<nombre>.jpg.
"""
import random
import sys
from pathlib import Path

from PIL import Image, ImageFilter


def remera(im, box, brillo):
    """Pinta la piel de la caja como tela oscura, con pliegues suaves, y la difumina un poco."""
    x0, y0, x1, y1 = box
    px = im.load()
    mask = Image.new('L', im.size, 0)
    m = mask.load()
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b = px[x, y]
            if r - b > 14 and r >= g and r > 40 and g < 150:
                m[x, y] = 255
    m = mask.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3)).load()
    random.seed(3)
    n = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if m[x, y]:
                base = brillo + (6 if (x // 23) % 2 else 0) + int(6 * (y - y0) / max(1, y1 - y0)) + random.randint(-2, 2)
                px[x, y] = (base, base + 1, base + 4)
                n += 1
    soft = im.filter(ImageFilter.GaussianBlur(2)).load()
    for y in range(y0, y1):
        for x in range(x0, x1):
            if m[x, y]:
                px[x, y] = soft[x, y]
    return n


def main():
    path = Path(sys.argv[1])
    x0, y0, x1, y1 = map(int, sys.argv[2:6])
    mode, threshold = sys.argv[6], int(sys.argv[7])
    im = Image.open(path).convert('RGB')
    if mode == 'piel':
        n = remera(im, (x0, y0, x1, y1), threshold)
        im.save(path, 'WEBP', quality=88)
        view = Path('/tmp/escenas-vista') / f'{path.stem}.jpg'
        view.parent.mkdir(exist_ok=True)
        im.resize((688, 384)).save(view)
        print(f'{path} · {n} puntos de piel pintados como remera · vista: {view}')
        return
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
