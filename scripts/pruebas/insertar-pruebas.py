#!/usr/bin/env python3
"""Inserta «#### Pruebas» al final de cada práctica listada, con las salidas vacías (D73).
Después: php artisan app:course-tests cursos/cpp --fill  (las completa con la solución de referencia).

  python3 scripts/pruebas/insertar-pruebas.py cursos/cpp /tmp/pruebas.txt

Formato de pruebas.txt (una práctica que ya tiene pruebas no se toca):
  @@ R01-N02-M1
  --- Nombre de la prueba
  líneas de la entrada
  --- Otra prueba
  ...
"""
import glob, re, sys

folder, spec = sys.argv[1], sys.argv[2]
tests = {}
code = None
for line in open(spec, encoding='utf-8').read().split('\n'):
    if line.startswith('@@ '):
        code = line[3:].strip().upper(); tests[code] = []
    elif line.startswith('--- '):
        tests[code].append([line[4:].strip(), []])
    elif code and tests[code]:
        tests[code][-1][1].append(line)
for c in tests:
    for t in tests[c]:
        while t[1] and t[1][-1].strip() == '':
            t[1].pop()

PRACTICE = re.compile(r'^###\s+(Misi[oó]n|Encargo|Pr[aá]ctica|Desaf[ií]o)\s+(\S+)', re.I)
done = set()

def block(c):
    out = ['#### Pruebas', '']
    for name, lines in tests[c]:
        out += ['##### ' + name, '```entrada', *lines, '```', '```salida', '```', '']
    return out

for path in sorted(glob.glob(folder + '/*.md')):
    lines = open(path, encoding='utf-8').read().split('\n')
    out, current, fence, has_tests = [], None, None, False

    def close():
        global current
        if current in tests and current not in done:
            if has_tests:
                print('ya tiene pruebas:', current); done.add(current); return
            while out and out[-1].strip() == '':
                out.pop()
            out.extend([''] + block(current))
            done.add(current)

    for line in lines:
        if fence:
            out.append(line)
            if re.match(r'^\s*' + re.escape(fence) + r'\s*$', line):
                fence = None
            continue
        m = re.match(r'^\s*(```+|~~~+)', line)
        if m:
            fence = m.group(1); out.append(line); continue
        h = re.match(r'^(#{1,3})\s', line)
        if h:
            close()
            pm = PRACTICE.match(line)
            current = pm.group(2).upper() if pm else None
            has_tests = False
        elif re.match(r'^####\s+Pruebas\s*$', line):
            has_tests = True
        out.append(line)
    close()
    text = '\n'.join(out)
    if text != '\n'.join(lines):
        open(path, 'w', encoding='utf-8').write(text)

missing = set(tests) - done
print('insertadas:', len(done), '| no encontradas:', sorted(missing))
