#!/usr/bin/env python3
"""Baja una escena de Stitch y la guarda como cursos/<curso>/escenas/<ID>.webp (1376×768).

Uso: python3 scripts/escenas/guardar.py cursos/c R01-N01-P1 <downloadUrl de Stitch>

Si Stitch devuelve un enlace de stitch.googleapis.com (pide credenciales), bajar la imagen con la herramienta
`download_file` y pasar en lugar del enlace el archivo .txt donde quedó su respuesta (JSON con la imagen en base64).

También deja una vista chica en /tmp/escenas-vista/<ID>.jpg para revisarla rápido.
"""
import base64
import io
import json
import sys
import urllib.request
from pathlib import Path

from PIL import Image

W, H = 1376, 768


def sin_franjas(img):
    """Saca las franjas negras de arriba y de abajo que a veces agrega Stitch (filas casi negras enteras)."""
    gris = img.convert('L')
    w, h = gris.size
    px = gris.load()

    def negra(y):
        return sum(px[x, y] for x in range(0, w, 8)) / len(range(0, w, 8)) < 10

    arriba = next((y for y in range(h // 6) if not negra(y)), 0)
    abajo = next((y for y in range(h - 1, h - h // 6, -1) if not negra(y)), h - 1)
    return img.crop((0, arriba, w, abajo + 1)) if arriba or abajo < h - 1 else img


def main():
    folder, sid, url = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
    if Path(url).is_file():  # respuesta de download_file
        data = base64.b64decode(json.loads(Path(url).read_text())['image'])
    else:
        url = url.split('=')[0] if '=s' in url else url
        data = urllib.request.urlopen(url + '=s1376', timeout=120).read()
    img = Image.open(io.BytesIO(data)).convert('RGB')
    img = sin_franjas(img)
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
