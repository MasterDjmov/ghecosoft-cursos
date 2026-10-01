#!/usr/bin/env python3
"""Saca las pruebas cuya salida quedó vacía después de --fill (la solución no muestra nada con esa entrada,
o falla con ella): una salida vacía no se puede guardar.

  python3 scripts/pruebas/sacar-pruebas-vacias.py cursos/cpp
"""
import glob, re, sys
n = 0
for p in glob.glob(sys.argv[1] + '/*.md'):
    s = open(p, encoding='utf-8').read()
    new, k = re.subn(r'\n##### [^\n]*\n```entrada\n(?:[^`][^\n]*\n|\n)*?```\n```salida\n```\n', '\n', s)
    if k:
        n += k
        open(p, 'w', encoding='utf-8').write(new)
print('sacadas:', n)
