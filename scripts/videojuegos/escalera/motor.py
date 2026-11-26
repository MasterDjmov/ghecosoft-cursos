"""Motor de las micro-misiones de Pong (R02): una plantilla en C por nodo con bloques marcados.

    //@ n1: acá: lo que tiene que agregar
    ...líneas nuevas...
    //@ else
    ...líneas viejas (opcional)...
    //@ end

Para la micro-misión k: los bloques de las anteriores van con lo nuevo; los de la k, con el comentario «/* acá… */»
y lo viejo (inicial) o con lo nuevo (solución); los de las siguientes, con lo viejo.
"""
import re
import textwrap

ORDER = ['n1', 'n2', 'n3', 'n4']


def render(template, done, target=None, solved=False):
    out = []
    lines = textwrap.dedent(template).strip('\n').split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r'^(\s*)//@ (n\d)(\+?)(?::\s*(.*))?$', line)
        if not m:
            out.append(line)
            i += 1
            continue
        indent, name, early, comment = m.group(1), m.group(2), m.group(3) == '+', m.group(4)
        new, old, part = [], [], 'new'
        i += 1
        while not re.match(r'^\s*//@ end\s*$', lines[i]):
            if re.match(r'^\s*//@ else\s*$', lines[i]):
                part = 'old'
            else:
                (new if part == 'new' else old).append(lines[i])
            i += 1
        i += 1
        if name in done or (name == target and (solved or early)):
            out.extend(new)
        else:
            if name == target and comment:
                out.append(f'{indent}/* {comment} */')
            out.extend(old)
    return '\n'.join(out)


def mission_codes(template, k):
    """(inicial, solución) de la micro-misión k (1..4)."""
    done = set(ORDER[:k - 1])
    target = ORDER[k - 1]
    return render(template, done, target, False), render(template, done, target, True)


def full(template):
    return render(template, set(ORDER))


def block(lang, text):
    return f'```{lang}\n{textwrap.dedent(text).strip()}\n```'


def para(t):
    return textwrap.dedent(t).strip()


def mission(code, k, m, template):
    starter, solution = mission_codes(template, k)
    meta = [f"lugar: {m.get('lugar', 'La Cancha de las Paletas')}", f"personajes: {m.get('personajes', 'Kira, Gheco, Arcadia')}"]
    if m.get('criatura'):
        meta.append(f"criatura: {m['criatura']}")
    meta.append(f"carta: {m['carta']}")
    meta.append('recompensa: ' + m.get('recompensa', 'xp 10, oro 10' if k == 1 else 'xp 10, monedas 4'))
    if m.get('item'):
        meta.append(f"item: {m['item']}")
    parts = [f"### Micro-misión {code}-P{k} · {m['titulo']}", block('meta', '\n'.join(meta)),
             '#### Escena\n' + para(m['escena']), '#### Gheco sugiere\n' + para(m['gheco']),
             '#### Desafío\n' + para(m['desafio']),
             '#### Pasos\n' + '\n'.join(f'{n}. {p}' for n, p in enumerate(m['pasos'], 1)),
             '#### Código inicial\n' + block('c', starter),
             '#### Eventos\n' + block('', m['eventos']), '#### Estado\n' + block('', m['estado']),
             '#### Salida esperada',
             '#### Solución\n' + block('c', solution),
             '#### Al superarla\n' + para(m['superarla']),
             '#### Imagen\n' + '\n'.join(f'- {x}' for x in m['imagen'])]
    return '\n\n'.join(parts)


def node(n):
    meta = [f"tipo: {n.get('tipo', 'tema')}", f"criatura: {n['criatura']}", f"padre: {n['padre']}", 'precio: 10']
    for key in ('insignia', 'insignia_descripcion', 'temas', 'usa'):
        if n.get(key):
            meta.append(f'{key}: {n[key]}')
    parts = [f"## {n['codigo']} · {n['titulo']}", block('meta', '\n'.join(meta)),
             '### Crónica\n\n' + para(n['cronica']), '### Objetivos\n\n' + para(n['objetivos']),
             '### Antes de empezar\n\n' + para(n['antes']), '### Explicación\n\n' + para(n['explicacion']),
             '### Código de ejemplo\n\n' + block('c', full(n['plantilla'])),
             '### ¿Para qué sirve?\n\n' + para(n['para_que']), '### Errores habituales\n\n' + para(n['errores'])]
    parts += [mission(n['codigo'], k, m, n['plantilla']) for k, m in enumerate(n['misiones'], 1)]
    return '\n\n'.join(parts)
