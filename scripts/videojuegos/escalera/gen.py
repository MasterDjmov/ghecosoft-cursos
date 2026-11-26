"""Reescribe R02-N02 en adelante de cursos/videojuegos/02-la-cancha-de-las-paletas.md desde las plantillas (R02-N01 queda como está).

    python3 scripts/videojuegos/escalera/gen.py n02 n03 n04 n05 n06 n07
    node scripts/videojuegos/probar-curso.mjs cursos/videojuegos/02-la-cancha-de-las-paletas.md --fill

Ojo: el .md es la fuente; si se corrigió algo a mano en el .md, pasarlo a la plantilla antes de regenerar.
"""
import importlib
import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import motor

F = __import__('os').path.join(__file__.rsplit('/', 4)[0], 'cursos/videojuegos/02-la-cancha-de-las-paletas.md')
mods = sys.argv[1:] or ['n02']
text = open(F).read()
cut = text.find('\n## R02-N02 ')
head = text if cut == -1 else text[:cut + 1]
nodes = [motor.node(importlib.import_module(m).NODO) for m in mods]
open(F, 'w').write(head.rstrip('\n') + '\n\n' + '\n\n'.join(nodes) + '\n')
print('ok', mods)
