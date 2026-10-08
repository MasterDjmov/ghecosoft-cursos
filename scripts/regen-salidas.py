#!/usr/bin/env python3
"""Compila y ejecuta todo el código de un curso de C o C++ (los ejemplos de los nodos y las soluciones de
referencia de las prácticas, con su entrada de ejemplo y sus pruebas) y compara lo que sale con lo que dice el .md.

    scripts/regen-salidas.py cursos/cpp [--only=R02] [--apply]

Sin --apply solo informa las diferencias; con --apply reescribe las salidas en el .md. Es el complemento de
`php artisan app:course-tests` (que revisa solo las prácticas): sirve, por ejemplo, después de renombrar a un
personaje en todos los ejemplos. Se saltea el código que usa Qt, SDL o Arduino, y el que no tiene `main`.
Cada ejecución corre en una carpeta vacía nueva, como en el navegador.
"""
import os
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

FENCE = re.compile(r'^```(\w*)\s*$')


def blocks(lines):
    """(inicio, fin, lenguaje) de cada bloque ``` (inicio y fin son las líneas de las cercas)."""
    out, i = [], 0
    while i < len(lines):
        m = FENCE.match(lines[i])
        if m:
            j = i + 1
            while j < len(lines) and lines[j].rstrip() != '```':
                j += 1
            out.append((i, j, m.group(1)))
            i = j + 1
        else:
            i += 1
    return out


def skip(code):
    return 'int main' not in code or re.search(r'#include\s*<(Q\w+|SDL|Arduino)', code) or 'void setup()' in code


def run(code, stdin, lang, cache={}):
    key = (code, lang)
    if key not in cache:
        tmp = tempfile.mkdtemp(prefix='regen-')
        # Un proyecto de varios archivos viene separado con «// ===== Nombre.h =====».
        parts = re.split(r'^(?://|/\*) ===== (\S+) =====(?: \*/)?\s*$', code, flags=re.M)
        files = dict(zip(parts[1::2], parts[2::2])) if len(parts) > 1 else {'main.' + ('c' if lang == 'c' else 'cpp'): code}
        for name, text in files.items():
            Path(tmp, name).write_text(text)
        # Rutas relativas, como en la compu del alumno (__FILE__ da «main.c», no la carpeta temporal).
        sources = [n for n in files if n.endswith(('.c', '.cpp'))]
        cmd = ['gcc', '-std=c11', *sources, '-lm'] if lang == 'c' else ['g++', '-std=c++20', *sources]
        r = subprocess.run(cmd + ['-o', 'prog'], capture_output=True, text=True, cwd=tmp)
        cache[key] = os.path.join(tmp, 'prog') if r.returncode == 0 else 'ERROR: ' + r.stderr[:300]
    prog = cache[key]
    if prog.startswith('ERROR'):
        return prog
    with tempfile.TemporaryDirectory() as cwd:
        try:
            r = subprocess.run([prog], input=stdin, capture_output=True, text=True, timeout=10, cwd=cwd)
        except subprocess.TimeoutExpired:
            return 'ERROR: se pasó de tiempo'
    return r.stdout.rstrip('\n')


def norm(text):
    # Como la plataforma (LocalCodeRunner::normalize): sin los espacios del final de cada renglón ni los saltos
    # de línea de las puntas. Al reescribir, en cambio, se guarda la salida exacta del programa.
    return '\n'.join(l.rstrip() for l in text.split('\n')).strip('\n')


def process(path, lang, only, apply):
    lines = path.read_text().split('\n')
    bl = blocks(lines)
    heading_of = {}  # línea de inicio del bloque → (título ###, título ####, título #####, código de unidad)
    h3 = h4 = h5 = ''
    unit = ''
    inside = {n for (s, e, _) in bl for n in range(s, e + 1)}
    starts = {s for (s, _, _) in bl}
    for n, line in enumerate(lines):
        if n in starts:
            heading_of[n] = (h3, h4, h5, unit)
        if n in inside:
            continue
        if line.startswith('## '):
            unit = line[3:].split(' ·')[0]
            h3 = h4 = h5 = ''
        elif line.startswith('### '):
            h3, h4, h5 = line[4:], '', ''
        elif line.startswith('#### '):
            h4, h5 = line[5:], ''
        elif line.startswith('##### '):
            h5 = line[6:]

    # Arma las tareas: (código, entrada, bloque de salida esperada, nombre)
    tasks = []
    node_code = node_in = None
    prac = {}
    for (s, e, kind) in bl:
        h3, h4, h5, unit = heading_of[s]
        body = '\n'.join(lines[s + 1:e])
        if only and not unit.startswith(only):
            continue
        if h3 == 'Código de ejemplo' and kind in ('cpp', 'c'):
            # Un ejemplo de varios archivos trae cada uno en su bloque, con el nombre arriba: `Torre.h`
            label = next((l for l in reversed(lines[:s]) if l.strip()), '')
            m = re.fullmatch(r'`([\w.]+\.(?:h|hpp|c|cpp))`', label.strip())
            if m:
                prev = node_code if node_code and node_code.startswith('// =====') else ''
                node_code, node_in = prev + f'// ===== {m.group(1)} =====\n' + body + '\n', ''
            else:
                node_code, node_in = body, ''
        elif h3 == 'Entrada de ejemplo' and node_code is not None:
            node_in = body
        elif h3 == 'Salida esperada' and node_code is not None:
            tasks.append((node_code, node_in, (s, e), f'{unit} ejemplo'))
            node_code = None
        elif h3.startswith(('Misión', 'Encargo')):
            key = h3.split(' ·')[0]
            p = prac.setdefault(key, {'tests': []})
            if h4 == 'Entrada de ejemplo':
                p['in'] = body
            elif h4 == 'Salida esperada':
                p['out'] = (s, e)
            elif h4 == 'Solución de referencia' and kind in ('cpp', 'c'):
                p['code'] = body
            elif h4 == 'Pruebas' and kind == 'entrada':
                p['tests'].append([body, None, h5])
            elif h4 == 'Pruebas' and kind == 'salida' and p['tests']:
                p['tests'][-1][1] = (s, e)
    for key, p in prac.items():
        if 'code' not in p:
            continue
        if 'out' in p:
            tasks.append((p['code'], p.get('in', ''), p['out'], f'{key} ejemplo'))
        for (stdin, out, name) in p['tests']:
            if out:
                tasks.append((p['code'], stdin, out, f'{key} «{name}»'))

    # Compila y ejecuta en paralelo (cada caso en su carpeta); después compara en orden.
    todo = [t for t in tasks if not skip(t[0])]
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as pool:
        list(pool.map(lambda code: run(code, '', lang), {t[0] for t in todo}))  # compila cada código una vez
        results = list(pool.map(lambda t: run(t[0], t[1] + '\n' if t[1].strip() else t[1], lang), todo))
    changes, bad = {}, 0
    for (code, stdin, (s, e), name), got in zip(todo, results):
        if got.startswith('ERROR'):
            print(f'  {path.name} {name}: {got}')
            bad += 1
            continue
        want = norm('\n'.join(lines[s + 1:e]))
        if norm(got) != want:
            bad += 1
            print(f'  {path.name} {name}: distinta')
            for a, b in zip(want.split('\n') + [''] * 50, got.split('\n') + [''] * 50):
                if a != b:
                    print(f'      esperaba «{a}»\n      salió    «{b}»')
                    break
            changes[(s, e)] = got
    if apply and changes:
        for (s, e), got in sorted(changes.items(), reverse=True):
            lines[s + 1:e] = got.split('\n') if got else []
        path.write_text('\n'.join(lines))
    return len(tasks), bad


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    only = next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--only=')), '')
    apply = '--apply' in sys.argv
    folder = Path(args[0])
    lang = 'c' if folder.name == 'c' else 'cpp'
    total = bad = 0
    for f in sorted(folder.glob('*.md')):
        t, b = process(f, lang, only, apply)
        total, bad = total + t, bad + b
    print(f'{total} casos, {bad} distintos' + (' (reescritos)' if apply and bad else ''))


if __name__ == '__main__':
    main()
