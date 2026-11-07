#!/usr/bin/env python3
"""Arma las 8 direcciones de Serphira (S,SE,E,NE,N,NO,O,SO) desde sus hojas sobre magenta.
Stitch no siempre respeta el lado que se le pide: cada nivel dice qué figura va en cada dirección,
y las marcadas con «~» se espejan. También hace el bot apagado desde el nivel 1.
Uso: armar-serphira.py carpeta-con-serphira-nN.png carpeta-de-salida"""
import os, sys, tempfile
from PIL import Image, ImageOps, ImageEnhance
sys_argv, sys.argv = sys.argv, sys.argv[:1]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recortar
SRC, OUT = sys_argv[1:3]
LEVELS = {  # nivel: (alto, figuras de la hoja, dirección -> figura)
    'n1': (150, 8, ['0', '1', '2', '3', '4', '~3', '~2', '7']),
    'n2': (160, 5, ['0', '~1', '~2', '3', '4', '~3', '2', '1']),
    'n3': (170, 5, ['0', '1', '2', '3', '4', '~3', '~2', '~1']),
    'n4': (180, 5, ['0', '1', '2', '3', '4', '~3', '~2', '~1']),
    'n5': (190, 6, ['0', '1', '~2', '3', '5', '~3', '2', '~1']),
}
os.makedirs(OUT, exist_ok=True)
for name, (height, count, order) in LEVELS.items():
    with tempfile.TemporaryDirectory() as tmp:
        recortar.run(f'{SRC}/serphira-{name}.png', tmp, name, height, count)
        figs = {str(k): Image.open(f'{tmp}/{name}-{k}.webp').convert('RGBA') for k in range(count)}
        for d, ref in enumerate(order):
            fig = ImageOps.mirror(figs[ref[1:]]) if ref[0] == '~' else figs[ref]
            fig.save(f'{OUT}/{name}-{d}.webp', quality=88)
for d in range(8):
    fig = Image.open(f'{OUT}/n1-{d}.webp').convert('RGBA')
    alpha = fig.getchannel('A')
    off = ImageEnhance.Brightness(ImageOps.grayscale(fig.convert('RGB'))).enhance(.62).convert('RGBA')
    off.putalpha(alpha)
    off.save(f'{OUT}/off-{d}.webp', quality=88)
