#!/usr/bin/env python3
"""Imágenes de la Enciclopedia (D104): toma las carpetas de personajes del docente y deja, por cada ficha de
docs/historias/PERSONAJES.md, su retrato y su cuerpo entero en webp en public/img/enciclopedia/<slug>.webp y
<slug>-cuerpo.webp (el slug es el de Str::slug del nombre de la ficha sin la aclaración final entre paréntesis).

Cada personaje tiene su carpeta (dentro de la de su mundo o suelta). En la carpeta, el retrato es la imagen
cuadrada (mejor si se llama circular_…, circulo_… o logo_…) y el cuerpo entero, la vertical; las de WhatsApp
son avatares y no se usan. La carpeta se une con la ficha por las palabras del nombre, dentro de su mundo.

    python3 scripts/enciclopedia/imagenes.py "/home/djmov/Programas/LaRiojaClick-Aprende/publicidad/logos cursos/personajes" [--force]
"""
import re
import sys
import unicodedata
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SHEETS = ROOT / 'docs/historias/PERSONAJES.md'
OUT = ROOT / 'public/img/enciclopedia'
PORTRAIT = 320
FIGURE_HEIGHT = 900

# Carpetas cuyo nombre no alcanza para encontrar la ficha.
ALIASES = {'asistente-gheco': 'gheco', 'heroe-mujer': 'la-heroina', 'heroe-varon': 'el-heroe', 'maesse-ferrum': 'maese-ferrum', 'arania': 'la-arana-de-las-direcciones'}
# Carpetas que no son fichas (avatares del héroe, copias).
SKIP = {'kira2'}
STOP = {'el', 'la', 'los', 'las', 'de', 'del', 'y', 'jefe', 'r01', 'r02', 'r03', 'r04', 'java', 'final'}


def slug(text: str) -> str:
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', text).strip('-')


def words(text: str) -> set[str]:
    return {w for w in slug(text).split('-') if w and w not in STOP}


def sheets() -> list[tuple[str, str]]:
    """(nombre de la ficha, sección)."""
    section, out = '', []
    for line in SHEETS.read_text().splitlines():
        if m := re.match(r'^## (?:\d+\.\s*)?(.+)$', line):
            section = m.group(1).strip()
        elif m := re.match(r'^### (.+)$', line):
            # Sin las marcas («*(falta la imagen)*») ni la aclaración del final («(jefe de R02)»).
            name = re.sub(r'\s*\*\(.*?\)\*\s*', ' ', m.group(1)).strip()
            out.append((re.sub(r'\s*\([^)]*\)$', '', name).strip(), section))
    return out


def is_world(section: str) -> bool:
    """La sección de un mundo dice su lenguaje entre paréntesis: «Las Forjas de Hierro (C)»."""
    return bool(re.search(r'\((Python|C|C\+\+|HTML y CSS|Java|PHP)\)$', section))


def find_sheet(folder: Path, base: Path, all_sheets):
    key = slug(folder.name)
    if key in SKIP:
        return None
    by_slug = {slug(name): name for name, _ in all_sheets}
    if key in ALIASES and ALIASES[key] in by_slug:
        return by_slug[ALIASES[key]]
    world = folder.parent.name if folder.parent != base else None
    common = [(n, s) for n, s in all_sheets if not is_world(s)]
    own = [(n, s) for n, s in all_sheets if world and is_world(s) and (words(world) <= words(s) or words(s) <= words(world))]
    # En la carpeta de un mundo, primero sus fichas; si no está, las comunes (un protagonista puede estar guardado ahí).
    for candidates in ([own, common] if world else [common]):
        hits = [n for n, _ in candidates if words(folder.name) and words(folder.name) <= words(n)]
        if hits:
            break
    if len(hits) == 1:
        return hits[0]
    exact = [n for n in hits if words(n) == words(folder.name)]
    return exact[0] if len(exact) == 1 else None


def pick(folder: Path):
    files = [f for f in folder.iterdir() if f.suffix.lower() in ('.jpg', '.jpeg', '.png', '.webp') and not f.name.lower().startswith('whatsapp')]
    portrait = figure = None
    for f in sorted(files, key=lambda f: (not re.match(r'(circular|circulo|logo)_', f.name.lower()), f.name)):
        with Image.open(f) as im:
            w, h = im.size
        if h > w * 1.15 and figure is None:
            figure = f
        elif portrait is None and (abs(w - h) <= w * 0.08 or re.match(r'(circular|circulo|logo)_', f.name.lower())):
            portrait = f
    return portrait, figure


def save(src: Path, dest: Path, figure: bool, force: bool) -> bool:
    if dest.exists() and not force:
        return False
    with Image.open(src) as im:
        im = im.convert('RGB')
        if figure:
            im.thumbnail((FIGURE_HEIGHT * 2, FIGURE_HEIGHT))
        else:
            im = im.resize((PORTRAIT, PORTRAIT), Image.LANCZOS)
        im.save(dest, 'WEBP', quality=82, method=6)
    return True


def save_bust(src: Path, dest: Path, force: bool) -> bool:
    if dest.exists() and not force:
        return False
    with Image.open(src) as im:
        w, h = im.size
        side = int(w * 0.55)
        left = (w - side) // 2
        top = int(h * 0.01)
        im.convert('RGB').crop((left, top, left + side, top + side)).resize((PORTRAIT, PORTRAIT), Image.LANCZOS).save(dest, 'WEBP', quality=82, method=6)
    return True


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    force = '--force' in sys.argv
    if not args:
        sys.exit(__doc__)
    base = Path(args[0])
    OUT.mkdir(parents=True, exist_ok=True)
    all_sheets = sheets()
    done, unmatched = set(), []
    folders = [d for d in base.iterdir() if d.is_dir()]
    # Las carpetas de mundo tienen subcarpetas: se recorren las de adentro.
    folders = [sub for d in folders for sub in ([x for x in d.iterdir() if x.is_dir()] or [d])]
    for folder in sorted(folders):
        name = find_sheet(folder, base, all_sheets)
        if not name:
            if slug(folder.name) not in SKIP:
                unmatched.append(str(folder.relative_to(base)))
            continue
        portrait, figure = pick(folder)
        key = slug(name)
        wrote = []
        if portrait and save(portrait, OUT / f'{key}.webp', False, force):
            wrote.append('retrato')
        elif not portrait and figure and save_bust(figure, OUT / f'{key}.webp', force):
            # Sin retrato (los héroes del jugador solo tienen avatares enmarcados): cabeza y hombros del cuerpo entero.
            wrote.append('retrato recortado del cuerpo entero')
            portrait = figure
        if figure and save(figure, OUT / f'{key}-cuerpo.webp', True, force):
            wrote.append('cuerpo')
        done.add(name)
        print(f'{folder.relative_to(base)} → {name}: {", ".join(wrote) or "ya estaba"}'
              + ('' if portrait else ' (sin retrato)') + ('' if figure else ' (sin cuerpo entero)'))
    print('\nCarpetas sin ficha:', ', '.join(unmatched) or 'ninguna')
    print('Fichas sin carpeta:', ', '.join(n for n, _ in all_sheets if n not in done) or 'ninguna')


if __name__ == '__main__':
    main()
