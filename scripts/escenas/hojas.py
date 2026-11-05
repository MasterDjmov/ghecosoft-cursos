#!/usr/bin/env python3
"""Hojas de personaje: 8 ángulos de cada personaje, una por proyecto de Stitch (Stitch solo toma referencias del mismo proyecto).

Uso:
  python3 scripts/escenas/hojas.py                     resumen por proyecto
  python3 scripts/escenas/hojas.py --next N [PROY]     las próximas N que faltan, con su pedido (JSON)
  python3 scripts/escenas/hojas.py --ok PROY NOMBRE SCREEN ARCHIVO.txt
                                                       guarda la hoja revisada y la anota; desde ahí pendientes.py la usa

Lo aprobado queda en referencias/hojas.json y las copias en referencias/<proyecto>/. Ver docs/ESCENAS.md.
"""
import base64
import importlib.util
import io
import json
import re
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
MANIFEST = HERE / 'referencias' / 'hojas.json'
BEASTS = r'^(el|la) (Slime|Ogro|Orco|Dragón|Goblin|Fantasma|ogro|troll|Troll|Polilla|Ratón|Herrumbre|Gran Pato|Gólem|Araña|Sanguijuela|Salamandra|Autómata|Quimera|Mímico|Kraken|Minotauro|Gárgola|Espectro|Sirena|Gorgona|Serpiente|Grifo|Orca|Hipocampo|Leviatán|Centinela|Borrón|Guardián)|^(Gheco|Axón|Eco|Pico|Bengala|Ébano|Saeta)$'
# En estos proyectos la referencia de Gheco es regenerada y distinta: subir la oficial antes de hacerle su hoja (docs/ESCENAS.md).
SKIP = {('14674491267148198305', 'Gheco'), ('12272294721581088244', 'Gheco')}
COMMON = 'Copiá fielmente su diseño, cara, colores, ropa, accesorios y proporciones, sin rediseñarlo ni embellecerlo. Es UN SOLO personaje repetido. Fondo azul noche oscuro liso, sin grilla, sin piso y sin decorado. Formato 16:9 (1376×768). Ocho figuras separadas, sin tocarse, del mismo tamaño, cuerpo entero, en dos filas de cuatro.'
PERSON = 'Fila de arriba, de pie en postura neutra: 1) de frente; 2) tres cuartos; 3) de perfil; 4) de espaldas. Fila de abajo: 5) caminando, con su objeto característico si tiene; 6) sentado; 7) señalando algo con la mano, hablando; 8) primer plano de la cabeza en tres cuartos, para ver bien la cara y el pelo. En TODAS, la misma ropa, opaca y cerrada, sin escote ni panza al aire y sin agregar prendas.'
BEAST = 'Fila de arriba, en postura neutra: 1) de frente; 2) tres cuartos; 3) de perfil; 4) de espaldas. Fila de abajo: 5) en movimiento; 6) quieto, descansando; 7) amenazando o en acción, con cara expresiva; 8) primer plano de la cabeza. En TODAS, la misma forma, el mismo cuerpo, los mismos colores y detalles. Aspecto apto para alumnos chicos, sin sangre.'
END = 'Solo dibujo: sin letras, números, rótulos, flechas, líneas de guía ni runas. Imagen limpia.'


def refs():
    spec = importlib.util.spec_from_file_location('pendientes', HERE / 'pendientes.py')
    module = importlib.util.module_from_spec(spec)
    sys.dont_write_bytecode = True
    spec.loader.exec_module(module)
    return module.REFS, module.ORIGINAL_IDS


def manifest():
    return json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}


def inventory():
    table, originals = refs()
    out = {}
    for cfg in table.values():
        for char in cfg['chars']:
            key = (cfg['project'], char[1])
            if key not in out and key not in SKIP:
                out[key] = {'project': cfg['project'], 'name': char[1], 'ids': originals.get(key, char[2])[:2], 'note': char[3]}
    return out


def request(item):
    beast = re.search(BEASTS, item['name'])
    note = f" {item['note']}" if item['note'] else ''
    text = (
        f'Generá una IMAGEN NUEVA: hoja de personaje (model sheet) de EXACTAMENTE este personaje, {item["name"]}, el de la imagen seleccionada.{note} '
        f'{COMMON} {BEAST if beast else PERSON} {END}'
    )
    return {'project': item['project'], 'name': item['name'], 'selectedScreenIds': item['ids'], 'prompt': text}


def main():
    args = sys.argv[1:]
    done = manifest()
    items = inventory()
    pending = [i for k, i in items.items() if k[1] not in done.get(k[0], {})]
    if args[:1] == ['--ok']:
        project, name, screen, source = args[1:5]
        image = Image.open(io.BytesIO(base64.b64decode(json.loads(Path(source).read_text())['image']))).convert('RGB')
        slug = re.sub(r'[^a-z0-9]+', '-', name.lower().translate(str.maketrans('áéíóúñ', 'aeioun'))).strip('-')
        target = HERE / 'referencias' / project / f'{slug}.webp'
        target.parent.mkdir(parents=True, exist_ok=True)
        image.save(target, quality=90)
        done.setdefault(project, {})[name] = screen
        MANIFEST.write_text(json.dumps(done, ensure_ascii=False, indent=1) + '\n')
        print(f'{name}: {target} · faltan {len(pending) - (1 if (project, name) in items and name not in done.get(project, {}) else 0)}')
    elif args[:1] == ['--next']:
        chosen = [i for i in pending if len(args) < 3 or i['project'] == args[2]][:int(args[1])]
        print(json.dumps([request(i) for i in chosen], ensure_ascii=False, indent=1))
    else:
        for project in dict.fromkeys(k[0] for k in items):
            total = sum(1 for k in items if k[0] == project)
            print(project, f'{len(done.get(project, {}))} de {total}')
        print('faltan', len(pending))


if __name__ == '__main__':
    main()
