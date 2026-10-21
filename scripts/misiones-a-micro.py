#!/usr/bin/env python3
"""D111: convierte las misiones de consola de un capítulo (Java, C, C++…) en micro-misiones.

Toma cada «### Misión» con entrega de código y «#### Salida esperada» y la reemplaza por una «### Micro-misión»
con el mismo enunciado (Desafío + «Para superarla»), la misma entrada, salida y solución, y la recompensa de la
misión en denarios («monedas N») más «antes: <código de la misión>». Las micro-misiones nuevas van después de las
que ya tiene el nodo. La parte de historia (lugar, personajes, escena, Gheco sugiere, Al superarla e imagen) sale
de un JSON escrito a mano, una entrada por misión.

    python3 scripts/misiones-a-micro.py cursos/java/01-la-aduana-del-compilador.md scripts/java-micro/00-01.json [--apply]

El lenguaje sale del bloque de la solución de referencia («```java», «```c», «```cpp», «```python»).
"""
import json
import re
import sys
from pathlib import Path


def blocks(text: str) -> list[str]:
    return re.split(r'(?m)^(?=### )', text)


def section(block: str, name: str) -> str | None:
    m = re.search(rf'(?m)^#### {re.escape(name)}\n(.*?)(?=^#### |\Z)', block, re.S)
    return m.group(1).strip() if m else None


def fence(body: str | None) -> str | None:
    """El contenido del primer bloque de código («```java … ```»)."""
    if body is None:
        return None
    m = re.search(r'```[a-z]*\n(.*?)\n```', body, re.S)
    return m.group(1) if m else None


def fence_language(body: str | None) -> str:
    m = re.search(r'```([a-z+]*)\n', body or '')
    return m.group(1) if m and m.group(1) else 'java'


def skeleton(solution: str, language: str) -> str:
    """El código inicial: los import (o #include) y el main vacío."""
    if language == 'python':
        imports = [line for line in solution.splitlines() if line.startswith(('import ', 'from '))]
        return '\n'.join(imports + ([''] if imports else []) + ['# Escribí tu programa acá'])
    if language in ('c', 'cpp'):
        includes = [line for line in solution.splitlines() if line.startswith(('#include', 'using namespace'))]
        comment = '/* Escribí tu programa acá */' if language == 'c' else '// Escribí tu programa acá'
        main = 'int main(void)' if language == 'c' else 'int main()'
        return '\n'.join(includes + ([''] if includes else []) + [main, '{', f'    {comment}', '    return 0;', '}'])
    imports = [line for line in solution.splitlines() if line.startswith('import ')]
    m = re.search(r'public\s+class\s+(\w+)', solution)
    name = m.group(1) if m else 'Main'
    lines = imports + ([''] if imports else []) + [
        f'public class {name} {{',
        '    public static void main(String[] args) {',
        '        // Escribí tu programa acá',
        '    }',
        '}',
    ]
    return '\n'.join(lines)


def convert(block: str, code: str, story: dict) -> str:
    meta = re.search(r'```meta\n(.*?)```', block, re.S).group(1)
    coins = re.search(r'monedas:\s*(\d+)', meta)
    xp = re.search(r'xp:\s*(\d+)', meta)
    title = block.split('\n', 1)[0].split('·', 1)[1].strip()
    old_code = re.match(r'### Misión (\S+)', block).group(1)

    consigna = section(block, 'Consigna') or ''
    criteria = [line for line in (section(block, 'Criterio de aprobación') or '').splitlines()
                if line.strip().startswith('-') and 'salida' not in line.lower()]
    challenge = consigna + ('\n\n**Para superarla:**\n' + '\n'.join(criteria) if criteria else '')
    language = fence_language(section(block, 'Solución de referencia'))
    starter = story.get('inicial') or fence(section(block, 'Código inicial')) or skeleton(fence(section(block, 'Solución de referencia')), language)
    stdin = fence(section(block, 'Entrada de ejemplo'))
    expected = story.get('salida') or fence(section(block, 'Salida esperada'))
    solution = fence(section(block, 'Solución de referencia'))

    meta_lines = [f"lugar: {story['lugar']}", f"personajes: {story['personajes']}"]
    if story.get('criatura'):
        meta_lines.append(f"criatura: {story['criatura']}")
    meta_lines.append(f"recompensa: xp {xp.group(1) if xp else 10}, monedas {coins.group(1) if coins else 0}")
    meta_lines.append(f'antes: {old_code}')

    out = [f'### Micro-misión {code} · {title}', '', '```meta', *meta_lines, '```', '',
           '#### Escena', story['escena'], '', '#### Gheco sugiere', story['gheco'], '',
           '#### Desafío', challenge, '', '#### Código inicial', f'```{language}', starter, '```', '']
    if stdin is not None:
        out += ['#### Entrada', '```', stdin, '```', '']
    out += ['#### Salida esperada', '```', expected, '```', '', '#### Solución', f'```{language}', solution, '```', '',
            '#### Al superarla', story['exito'], '', '#### Imagen', *[f'- {line}' for line in story['imagen']], '', '']
    return '\n'.join(out)


def is_console(block: str) -> bool:
    if not block.startswith('### Misión '):
        return False
    meta = re.search(r'```meta\n(.*?)```', block, re.S).group(1)
    return 'entrega: codigo' in meta and '#### Salida esperada' in block


def main() -> None:
    path, story_path = Path(sys.argv[1]), Path(sys.argv[2])
    stories = json.loads(story_path.read_text())
    text = path.read_text()
    out, missing = [], []
    for node in re.split(r'(?m)^(?=## )', text):
        parts = blocks(node)
        steps = [b for b in parts if b.startswith('### Micro-misión ')]
        last = max((int(re.match(r'### Micro-misión \S+-P(\d+)', b).group(1)) for b in steps), default=0)
        node_code = re.match(r'## (\S+)', node).group(1) if node.startswith('## ') else None
        new, kept, inserted = [], [], False
        for block in parts:
            if is_console(block):
                code = re.match(r'### Misión (\S+)', block).group(1)
                if code not in stories:
                    missing.append(code)
                    kept.append(block)
                    continue
                last += 1
                new.append(convert(block, f'{node_code}-P{last}', stories[code]))
                continue
            kept.append(block)
        # Las nuevas, después de la última micro-misión (o antes de la primera misión o encargo).
        result = []
        for block in kept:
            if not inserted and new and re.match(r'### (Misión|Encargo|Prueba del sello|Soluciones)', block):
                result.extend(new)
                inserted = True
            result.append(block)
        if new and not inserted:
            result.extend(new)
        out.append(''.join(result))
    if missing:
        print('Sin historia:', ', '.join(missing))
    if '--apply' in sys.argv and not missing:
        path.write_text(''.join(out))
        print(f'{path}: listo.')
    elif '--apply' not in sys.argv:
        print(''.join(out)[:3000])


if __name__ == '__main__':
    main()
