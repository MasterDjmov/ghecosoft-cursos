#!/usr/bin/env python3
"""D111: corre la solución de cada micro-misión de Java (con su entrada) y la compara con la salida esperada.

    python3 scripts/java-micro/probar.py cursos/java/01-la-aduana-del-compilador.md [--todas]

Sin --todas, solo las que vienen de una misión («antes:»). Necesita `java` (17 o más) en la compu.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def section(block: str, name: str) -> str | None:
    m = re.search(rf'(?m)^#### {re.escape(name)}\n(.*?)(?=^#### |\Z)', block, re.S)
    if not m:
        return None
    code = re.search(r'```[a-z]*\n(.*?)\n```', m.group(1), re.S)
    return code.group(1) if code else None


def main() -> None:
    ok = bad = 0
    for path in sys.argv[1:]:
        if path.startswith('--'):
            continue
        text = Path(path).read_text()
        for block in re.split(r'(?m)^(?=### )', text):
            if not block.startswith('### Micro-misión ') or ('--todas' not in sys.argv and 'antes:' not in block):
                continue
            code = block.split()[2]
            solution, expected = section(block, 'Solución'), section(block, 'Salida esperada')
            if not solution or expected is None or not solution.lstrip().startswith(('public', 'import', '//', 'class', 'record', 'enum', 'interface')):
                continue
            name = (re.search(r'public\s+(?:final\s+)?class\s+(\w+)', solution) or re.search(r'class\s+(\w+)', solution)).group(1)
            with tempfile.TemporaryDirectory() as tmp:
                source = Path(tmp) / f'{name}.java'
                source.write_text(solution)
                run = subprocess.run(['java', str(source)], input=section(block, 'Entrada') or '', capture_output=True, text=True, timeout=30, cwd=tmp)
            got = run.stdout.rstrip()
            if got == expected.rstrip():
                ok += 1
            else:
                bad += 1
                print(f'✗ {code}\n--- esperada\n{expected}\n--- obtenida\n{got}\n{run.stderr[:500]}')
    print(f'{ok} bien, {bad} mal')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
