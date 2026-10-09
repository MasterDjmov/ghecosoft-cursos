#!/usr/bin/env python3
"""Baja una escena de Stitch y la guarda como cursos/<curso>/escenas/<ID>.webp (1376×768).

Uso: python3 scripts/escenas/guardar.py cursos/c R01-N01-P1 <downloadUrl de Stitch>

También deja una vista chica en /tmp/escenas-vista/<ID>.jpg para revisarla rápido.
"""
import io
import sys
import urllib.request
from pathlib import Path

from PIL import Image

W, H = 1376, 768


def main():
    folder, sid, url = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
    url = url.split('=')[0] if '=s' in url else url
    data = urllib.request.urlopen(url + '=s1376', timeout=120).read()
    img = Image.open(io.BytesIO(data)).convert('RGB')
    if img.size != (W, H):  # recorte centrado a 16:9 y escala
        ratio = W / H
        w, h = img.size
        if w / h > ratio:
            nw = int(h * ratio)
            img = img.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
        else:
            nh = int(w / ratio)
            img = img.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
        img = img.resize((W, H), Image.LANCZOS)
    out = folder / 'escenas' / f'{sid}.webp'
    out.parent.mkdir(exist_ok=True)
    img.save(out, 'WEBP', quality=82, method=6)
    preview = Path('/tmp/escenas-vista') / f'{sid}.jpg'
    preview.parent.mkdir(exist_ok=True)
    img.resize((688, 384)).save(preview, 'JPEG', quality=80)
    print(f'{out} ({out.stat().st_size // 1024} KB) · vista: {preview}')


if __name__ == '__main__':
    main()
