"""Escribe las micro-misiones de la escalera de juegos desde las plantillas por nodo.

    python3 scripts/videojuegos/escalera/gen.py n02 n03 n04 n05 n06 n07       (R02: reescribe desde R02-N02; N01 queda)
    python3 scripts/videojuegos/escalera/gen.py r03 n01 n02 n03 n04 n05 n06 n07   (R03: el archivo entero)
    node scripts/videojuegos/probar-curso.mjs cursos/videojuegos --only=R03 --fill

Ojo: el .md es la fuente; si se corrigió algo a mano en el .md, pasarlo a la plantilla antes de regenerar.
"""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE.rsplit('/', 3)[0]
sys.path.insert(0, HERE)
import motor

args = sys.argv[1:]
if args and args[0].startswith('r0'):
    rama = args.pop(0)
    sys.path.insert(0, os.path.join(HERE, rama))
    cabecera = importlib.import_module('cabecera')
    F = os.path.join(ROOT, 'cursos/videojuegos', cabecera.ARCHIVO)
    head = motor.para(cabecera.RAMA)
else:
    rama = 'r02'
    F = os.path.join(ROOT, 'cursos/videojuegos/02-la-cancha-de-las-paletas.md')
    text = open(F).read()
    cut = text.find('\n## R02-N02 ')
    head = (text if cut == -1 else text[:cut + 1]).rstrip('\n')
mods = args or ['n02']
nodes = [motor.node(importlib.import_module(m).NODO) for m in mods]
open(F, 'w').write(head + '\n\n' + '\n\n'.join(nodes) + '\n')
print('ok', rama, mods)
