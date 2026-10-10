#!/usr/bin/env python3
"""Baja dos o más versiones de una escena y arma una hoja para elegir: /tmp/escenas-vista/comparar.jpg (1, 2, …)."""
import io
import sys
import urllib.request

from PIL import Image, ImageDraw

urls = sys.argv[1:]
ims = [Image.open(io.BytesIO(urllib.request.urlopen(u.split('=s')[0] + '=s688', timeout=120).read())).convert('RGB').resize((688, 384)) for u in urls]
sheet = Image.new('RGB', (688, 384 * len(ims)))
for i, im in enumerate(ims):
    sheet.paste(im, (0, 384 * i))
    ImageDraw.Draw(sheet).text((8, 384 * i + 8), str(i + 1), fill=(255, 255, 0))
sheet.save('/tmp/escenas-vista/comparar.jpg', quality=80)
