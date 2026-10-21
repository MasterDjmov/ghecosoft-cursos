#!/usr/bin/env python3
"""D111: corre con el PHP 8.3 del navegador simulado (el `php()` de scripts/micro-misiones/genphp.py: misma zona
horaria, mismos avisos, carpeta vacía nueva) la solución de cada micro-misión de PHP que vino de una misión (las que
tienen «antes:»; con --todas, todas) y la compara con su salida esperada. También revisa que el código inicial NO dé
ya esa salida y que la solución dé lo mismo dos veces.

    python3 scripts/php-micro/probar.py cursos/php/0*.md [--todas]
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'micro-misiones'))
from genphp import php  # noqa: E402


def section(block, name):
    m = re.search(rf'(?m)^#### {re.escape(name)}\n(.*?)(?=^#### |\Z)', block, re.S)
    return m.group(1) if m else None


def fence(body):
    if body is None:
        return None
    m = re.search(r'```[a-z]*\n(.*?)\n```', body, re.S)
    return m.group(1) if m else None


def norm(text):
    return '\n'.join(line.rstrip() for line in text.replace('\r', '').strip('\n').split('\n'))


def main():
    every = '--todas' in sys.argv
    ok, bad = 0, []
    for path in [a for a in sys.argv[1:] if not a.startswith('--')]:
        for block in re.split(r'(?m)^(?=### )', open(path, encoding='utf-8').read()):
            head = re.match(r'### Micro-misión (\S+) · (.*)', block)
            if not head:
                continue
            meta = re.search(r'```meta\n(.*?)```', block, re.S).group(1)
            if not every and not re.search(r'(?m)^antes:', meta):
                continue
            solution, expected = fence(section(block, 'Solución')), fence(section(block, 'Salida esperada'))
            if solution is None or expected is None:
                continue
            stdin = fence(section(block, 'Entrada')) or ''
            _, out, err = php(solution, stdin)
            label = f'{head.group(1)} · {head.group(2)}'
            if norm(out) != norm(expected):
                bad.append(f'{label}: la salida no coincide {err[:200]}')
            elif norm(php(solution, stdin)[1]) != norm(out):
                bad.append(f'{label}: da distinto cada vez')
            elif norm(php(fence(section(block, "Código inicial")) or '', stdin)[1]) == norm(expected):
                bad.append(f'{label}: el código inicial ya da la salida esperada')
            else:
                ok += 1
    print(f'{ok} bien, {len(bad)} mal')
    for line in bad:
        print('  ' + line)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
