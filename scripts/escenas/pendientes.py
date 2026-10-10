#!/usr/bin/env python3
"""Lista las micro-misiones de un curso que todavía no tienen su escena en cursos/<curso>/escenas/.

Uso: python3 scripts/escenas/pendientes.py cursos/c [--json] [--prompt ID]

El progreso es la carpeta escenas/: una escena está hecha cuando existe escenas/<ID>.webp.
Con --prompt arma el pedido para Stitch (edit_screens) de esa micro-misión, con las referencias
de los personajes que aparecen (ver docs/ESCENAS.md).
"""
import json
import re
import sys
from pathlib import Path

# Referencias en Stitch por curso: nombre → (proyecto, [pantallas]). Cuerpo entero + circular.
REFS = {
    'c': {
        'project': '12453694413360128121',
        'region': 'Las Forjas de Hierro',
        'ambiente': 'en una ciudad-forja subterránea de piedra volcánica, con fraguas, lava y circuitos encendidos',
        'chars': [
            # (patrón en el texto, nombre, pantallas, aclaración de tamaño)
            (r'(?<!que )\bKira\b', 'Kira', ['14393643890262141765', '14393643890262141939'], ''),
            (r'Ferrum', 'Maese Ferrum', ['10337375498659242332', '10337375498659242906'],
             'Maese Ferrum es HUMANO y NO es un enano. Copiá las proporciones de su imagen de referencia de cuerpo entero: un hombre de unos dos metros, de unas siete cabezas de alto, con piernas largas (la mitad de su altura) y torso ancho (al lado de Kira, le saca una cabeza y media y es mucho más ancho).'),
            (r'Tiz[oó]n', 'Tizón', ['39f0163ef1c4420981621687c35f4e02', 'efeb92bd8d4f4de58e0f3de8f5ffba7e'],
             'Tizón es un enano joven: le llega a Kira al hombro.'),
            (r'Chispa', 'Chispa', ['f16d155319584836bac46bb188e095f4', '5178cab1b35a43e086faf1d31c715e61'],
             'Chispa es humano, alto y flaco: más alto que Kira.'),
            (r'Hulda', 'Hulda', ['ce52b8c5b55941a78f0b76e1ab7f44ef', '8423b67a3d2f47a68ee4ca91a5bb77c5'],
             'Hulda es una enana: le llega a Kira a la cintura.'),
            (r'Archivero', 'el Archivero', ['0be226861a8f4a8d8e583a582464fb19', '0fc92e97cf90409b8cd34f93e5450941'],
             'El Archivero es un enano muy viejo y encorvado: más bajo que Ferrum.'),
            (r'G[oó]lem', 'el Gólem de Escoria', ['2283b769ea444726bb504ca2d9c1d97f', '9baac98214ae432cbe4fafe2213e869a'], ''),
            (r'Ara[ñn]a', 'la Araña de las Direcciones', ['7a392ac74b964aa8a3932661c7031056', '7793569acd504ae9a3e211b944ade966'], ''),
            (r'Sanguijuela', 'la Sanguijuela de las Minas', ['f617f9cd0f3c4beb99d914c938de1461', 'a7a2f337ac9840319ca3bfd2f32ffaef'], ''),
            (r'Guardi[aá]n del Archivo', 'el Guardián del Archivo', ['aa13eb15fc834c2fbcdba627bf463772', 'eb43c11139924e9a9f7242be9d3c098e'], ''),
            (r'Drag[oó]n', 'el Dragón bajo la Montaña', ['1beb2b13ac2740e39ec873e25f0a9d2a', '05f46ee7ccb54ec5b3521163315fe841'], ''),
            (r'Salamandra', 'la Salamandra del Horno', ['f00b5bd8e0b541fd925273a2f23e8a1e', 'f94717f4f0ea4451a188eeb0c6077d24'], ''),
            (r'Aut[oó]mata Guardi[aá]n', 'el Autómata Guardián', ['be394c154b3544cd84a0f6cb5304046d', 'ae330b94011143dd97df7dab07894b9c'], ''),
            (r'Gheco|gecko', 'Gheco', ['7475890398726357700'], 'Gheco es un gecko chiquito, del tamaño de una mano.'),
        ],
    },
}

MAX_REFS = 8  # más de esto y Stitch empieza a mezclar personajes

HEAD = re.compile(r'^### (?:Micro-misión|Misión|Encargo|Jefe) (\S+) · (.+)$')


def scenes(folder: Path):
    for md in sorted(folder.glob('*.md')):
        lines = md.read_text(encoding='utf-8').splitlines()
        current = None
        for i, line in enumerate(lines):
            m = HEAD.match(line)
            if m:
                current = {'id': m.group(1), 'title': m.group(2).strip(), 'file': md.name, 'lugar': '', 'imagen': ''}
                continue
            if line.startswith('### '):
                current = None
            if current is None:
                continue
            if line.startswith('lugar:'):
                current['lugar'] = line.split(':', 1)[1].strip()
            if line.strip() == '#### Imagen':
                body = []
                for nxt in lines[i + 1:]:
                    if nxt.startswith('#'):
                        break
                    body.append(nxt)
                current['imagen'] = '\n'.join(body).strip()
                yield current
                current = None


def done(folder: Path, sid: str) -> bool:
    return any((folder / 'escenas' / f'{sid}.{ext}').exists() for ext in ('webp', 'jpg', 'jpeg', 'png'))


def prompt(course: str, scene: dict) -> dict:
    cfg = REFS[course]
    found = [c for c in cfg['chars'] if re.search(c[0], scene['imagen'])]
    screens, notes = [], []
    has_kira = any(c[1] == 'Kira' for c in found)
    for _, name, ids, note in found:
        screens += ids
        if note and not has_kira and ' (al lado de Kira' in note:  # sin Kira, sin la comparación (la haría aparecer)
            note = note.split(' (al lado de Kira')[0] + '.'
        if note and ('Kira' not in note or has_kira):
            notes.append(note)
    if len(screens) > MAX_REFS:  # se quedan los cuerpos enteros
        screens = [c[2][0] for c in found][:MAX_REFS]
    names = [c[1] for c in found]
    who = ', '.join(names[:-1]) + (' y ' if len(names) > 1 else '') + names[-1] if names else ''
    text = (
        'Generá una IMAGEN NUEVA de escena (no modifiques las imágenes seleccionadas: son referencias de cómo se ven los personajes). '
        + (f'Usá las referencias para que {who} ' + ('tengan' if len(names) > 1 else 'tenga') + ' exactamente su aspecto: misma cara, pelo, ropa, colores y proporciones.' if who else '')
        # Ni el lugar ni la región van con nombre: Stitch los escribe en un cartel. Se describe el ambiente.
        + f'\n\nLa escena ({cfg["ambiente"]}):\n'
        + scene['imagen']
        + ('\n\nTamaños: ' + ' '.join(notes) if notes else '')
        + '\n\nEstilo: anime/cómic cyber-arcana, 16:9 horizontal (1376×768), de noche, con luz propia. Sin texto de ningún tipo: ni letras, ni números, ni carteles, ni títulos, ni rótulos con el nombre del lugar.'
    )
    if not has_kira:  # la descripción de Ferrum la nombra: sin Kira en la escena, se saca
        text = text.replace(', más alto y ancho que Kira', '')
    return {'projectId': cfg['project'], 'selectedScreenIds': screens, 'prompt': text}


def main():
    folder = Path(sys.argv[1])
    course = folder.name
    all_scenes = list(scenes(folder))
    pending = [s for s in all_scenes if not done(folder, s['id'])]
    if '--next' in sys.argv:  # el pedido de la primera pendiente
        if not pending:
            print('Todas hechas.')
            return
        sys.argv += ['--prompt', pending[0]['id']]
        print(pending[0]['id'])
    if '--prompt' in sys.argv:
        sid = sys.argv[sys.argv.index('--prompt') + 1]
        scene = next(s for s in all_scenes if s['id'] == sid)
        print(json.dumps(prompt(course, scene), ensure_ascii=False, indent=1))
        return
    if '--json' in sys.argv:
        print(json.dumps(pending, ensure_ascii=False, indent=1))
        return
    print(f'{course}: {len(all_scenes) - len(pending)} de {len(all_scenes)} escenas hechas, faltan {len(pending)}')
    for s in pending:
        print(f'  {s["id"]:14} {s["title"]}')


if __name__ == '__main__':
    main()
