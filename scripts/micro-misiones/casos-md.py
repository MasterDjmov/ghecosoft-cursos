#!/usr/bin/env python3
"""Saca de los .md de un curso los casos de sus micro-misiones (solución, entrada y salida esperada) para
probarlos en el navegador con browser-check.mjs. Sin --todas, solo las que vienen de una misión («antes:», D111).

    python3 scripts/micro-misiones/casos-md.py cursos/c/0[0-5]*.md [--todas] > /tmp/casos.json
"""
import json
import re
import sys
from pathlib import Path


def section(block: str, name: str) -> str | None:
    m = re.search(rf'(?m)^#### {re.escape(name)}\n(.*?)(?=^#### |\Z)', block, re.S)
    if not m:
        return None
    code = re.search(r'```[a-z+]*\n(.*?)\n```', m.group(1), re.S)
    return code.group(1) if code else None


cases = []
for path in (a for a in sys.argv[1:] if not a.startswith('--')):
    for block in re.split(r'(?m)^(?=### )', Path(path).read_text()):
        if not block.startswith('### Micro-misión ') or ('--todas' not in sys.argv and 'antes:' not in block):
            continue
        solution, expected = section(block, 'Solución'), section(block, 'Salida esperada')
        if solution and expected is not None:
            cases.append({'name': block.split()[2], 'code': solution, 'stdin': section(block, 'Entrada') or '', 'expected': expected})
json.dump(cases, sys.stdout, ensure_ascii=False)
