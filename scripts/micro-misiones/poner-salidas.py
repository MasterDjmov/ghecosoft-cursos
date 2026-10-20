#!/usr/bin/env python3
"""Escribe como «Salida esperada» de algunas micro-misiones lo que dio el navegador (browser-check.mjs --salidas).
Solo para las que dan distinto a propósito (rand(), sizeof(long) en wasm32: D98); las demás tienen que coincidir.

    python3 scripts/micro-misiones/poner-salidas.py salidas.json R01-N01-P7,R01-N09-P5 cursos/c/01-templar-el-metal.md
"""
import json
import re
import sys
from pathlib import Path

outputs = json.loads(Path(sys.argv[1]).read_text())
codes = sys.argv[2].split(',')
done = set()
for path in map(Path, sys.argv[3:]):
    parts = re.split(r'(?m)^(?=### )', path.read_text())
    for i, block in enumerate(parts):
        m = re.match(r'### Micro-misión (\S+)', block)
        if m and m.group(1) in codes:
            parts[i] = re.sub(r'(#### Salida esperada\n```\n).*?(\n```)', lambda x: x.group(1) + outputs[m.group(1)] + x.group(2), block, count=1, flags=re.S)
            done.add(m.group(1))
    path.write_text(''.join(parts))
missing = set(codes) - done
print('listo:', len(done), '| no encontradas:', ', '.join(sorted(missing)) or '-')
