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
        # Por archivo, cuando la región tiene su propio lugar.
        'ambientes': {
            '03-las-minas.md': 'en una mina subterránea de piedra volcánica, con vías, vagonetas, vetas de cristal cian y faroles',
            '04-el-archivo.md': 'en un archivo subterráneo de piedra, con estantes de hierro altísimos, libros encadenados, cajas de fichas y faroles',
            '06-senda-forja-viva.md': 'en una sala de forja subterránea detrás de una puerta de vidrio negro, donde formas de luz cian y naranja se mueven sobre superficies que brillan como pantallas',
            '07-senda-automatas.md': 'en un taller subterráneo de piedra volcánica lleno de autómatas de latón, engranajes, cables, perillas y lucecitas',
        },
        'chars': [
            # (patrón en el texto, nombre, pantallas, aclaración de tamaño)
            (r'(?<!que )\bKira\b', 'Kira', ['14393643890262141765', '14393643890262141939'], ''),
            (r'Ferrum', 'Maese Ferrum', ['10337375498659242332', '10337375498659242906'],
             'Maese Ferrum es HUMANO y NO es un enano. Copiá las proporciones de su imagen de referencia de cuerpo entero: un hombre de unos dos metros, de unas siete cabezas de alto, con piernas largas (la mitad de su altura) y torso ancho (al lado de Kira, le saca una cabeza y media y es mucho más ancho).'),
            (r'Tiz[oó]n', 'Tizón', ['39f0163ef1c4420981621687c35f4e02', 'efeb92bd8d4f4de58e0f3de8f5ffba7e'],
             'Tizón es un ENANO joven, mucho más bajo que Kira: su cabeza le llega a Kira al hombro (piernas cortas, cuerpo ancho; parados sobre el mismo suelo). Tiene cara ancha y redonda y orejas HUMANAS, chicas y redondeadas arriba, como en su referencia (nada de orejas de elfo ni de duende: la parte de arriba de la oreja es una curva redonda, sin punta).'),
            (r'Chispa', 'Chispa', ['f16d155319584836bac46bb188e095f4', '5178cab1b35a43e086faf1d31c715e61'],
             'Chispa es humano, alto y flaco: más alto que Kira.'),
            (r'Hulda', 'Hulda', ['ce52b8c5b55941a78f0b76e1ab7f44ef', '8423b67a3d2f47a68ee4ca91a5bb77c5'],
             'Hulda es una MUJER (sin barba) ENANA fornida, mucho más baja que Kira: con el casco puesto, su cabeza le llega a Kira al hombro (piernas cortas, cuerpo ancho; paradas sobre el mismo suelo). Lleva UN solo pico.'),
            (r'[Aa]rchivero', 'el Archivero', ['0be226861a8f4a8d8e583a582464fb19', '0fc92e97cf90409b8cd34f93e5450941'],
             'El Archivero es un ENANO muy viejo, mucho más bajo que Kira: su cabeza le llega a Kira al hombro (encorvado, de piernas cortas).'),
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
    'cpp': {
        'project': '14674491267148198305',
        'region': 'La Ciudadela de los Artífices',
        'ambiente': 'en una ciudadela de relojeros e inventores, con torres de bronce, engranajes enormes, chispas eléctricas cian y talleres llenos de piezas',
        'ambientes': {
            '04-la-gran-biblioteca.md': 'en una biblioteca enorme con cúpula de bronce, estantes altísimos, cajas de piezas ordenadas y escaleras con engranajes',
            '05-el-taller-del-juego.md': 'en un taller de juegos mecánicos de la ciudadela, con tableros, autómatas chicos, engranajes y luces cian',
            '06-los-vitrales.md': 'en la torre más alta de la ciudadela, con vitrales de colores, engranajes de bronce y arcos eléctricos cian',
            '07-senda-linterna-magica.md': 'en una sala oscura de proyección de la ciudadela, con una linterna mágica, vidrios pintados, haces de luz de colores y engranajes',
        },
        'chars': [
            # Solo el cuerpo entero: los circulares de este proyecto llevan el nombre escrito y Stitch lo copiaría.
            # Bron y Gheco se generaron en este proyecto el 2026-10-11 desde sus fichas y sus imágenes (no estaban subidos).
            (r'\bBron\b', 'Bron', ['36fd6421d03b45329e15255c57bf1d96'], 'Bron es un mecánico grandote de 24 años, alto y ancho, con una llave inglesa cian al hombro.'),
            (r'Gheco|gecko', 'Gheco', ['8b96c262b47549dbb5a441fb463377a5'], 'Gheco es un gecko chiquito, del tamaño de una mano.'),
            (r'\bTesla\b', 'Tesla', ['17568498787211306263'], 'Tesla es un muchacho de estatura mediana (1,75 m), delgado, de pelo en punta y visor cian.'),
            (r'\bLima\b', 'Lima', ['3741430dea15423a86d24bbd54d5c72f'], 'Lima es una chica chiquita (1,52 m), mucho más baja que los demás, con dos rodetes y una lupa de relojera en un ojo.'),
            (r'Maestra Art[ií]fice|[Ii]nspectora', 'la Maestra Artífice', ['4954292303660227400'], 'La Maestra Artífice es una mujer alta (1,72 m), delgada y erguida.'),
            (r'\bLyn\b', 'Lyn', ['bf450970bfd946e4b5f1d4fb29929adf'], 'Lyn es alta (1,74 m), atlética, de piernas de corredora, con UNA trenza rubia oscura.'),
            (r'\bOto\b', 'Oto', ['0dfaf599086548f48aeb6035b93e7ae7'], 'Oto es un cocinero grandote (1,90 m) y panzón, pelado, con un bigote enorme y gorro de cocinero.'),
            (r'Aut[oó]mata de Lat[oó]n', 'el Autómata de Latón', ['878a7317ad314d8b8d737f66e4a1a7fa'], ''),
            (r'Quimera', 'la Quimera de la Arena', ['1aeae621b76a4c9980a77db77057bb6c'], ''),
            (r'M[ií]mico', 'el Mímico del Bestiario', ['6098c0d9ddbe400b8440afc77b3c2b2f'], ''),
            (r'Kraken', 'el Kraken de los Contenedores', ['b3be0c4e051d41f8a974c672c19436f0'], ''),
            (r'Minotauro', 'el Minotauro del Laberinto', ['8fc81d5252ff497ea4ef620899035c67'], ''),
            (r'G[aá]rgola', 'la Gárgola de los Vitrales', ['5d77586f65474573b8727664c878f8ee'], ''),
            (r'Espectro', 'el Espectro de la Linterna', ['45d69362e68640d6ab6f9714fd564c2b'], ''),
        ],
    },
    'php': {
        'project': '12272294721581088244',
        'region': 'El Puerto de los Mensajeros',
        'ambiente': 'en un puerto de noche con muelles de madera, barcos, grúas, faroles, gaviotas y una torre con una campana, con luces violetas y cian',
        'ambientes': {
            '02-el-astillero-de-los-moldes.md': 'en un astillero del puerto, con galpones de madera, moldes de barcos colgados de las paredes, cascos a medio armar y faroles',
            '03-la-oficina-de-correos.md': 'en una oficina de correos dentro de una torre, con tubos de bronce que bajan del techo, casilleros de cartas, mostradores y lámparas violetas',
            '04-la-bodega-del-puerto.md': 'en una bodega de piedra bajo la torre del puerto, con galerías de estanterías llenas de fichas ordenadas, faroles cian y agua que se filtra',
            '05-el-faro.md': 'en un faro alto en la punta del muelle, con una escalera de caracol, palancas de bronce y una lámpara enorme, de noche junto al mar',
            '06-senda-de-la-arena.md': 'en una arena circular de arena rodeada de gradas, junto al puerto, con antorchas y un reloj de arena gigante',
            '07-senda-de-la-ciudadela.md': 'en una fortaleza de piedra clara sobre una colina junto al puerto, con salas ordenadas, estandartes lisos y faroles',
            '08-senda-de-los-mensajes-veloces.md': 'en un palomar de piedra junto al mar, con cientos de palomas mensajeras que entran y salen',
            '09-senda-del-escaparate.md': 'en una calle de tiendas del puerto con vidrieras de madera iluminadas, de noche',
        },
        'chars': [
            # Generados en este proyecto el 2026-10-11 (Nilo y Elefa desde sus imágenes oficiales; el resto, desde sus fichas).
            (r'\bNilo\b', 'Nilo', ['3defe2e1780843e09e4c04400943f0b8'], 'Nilo es un muchacho de 17 años, de estatura mediana (1,70 m) y delgado, con gorra de mensajero y bufanda violeta.'),
            (r'\bElefa\b', 'Elefa', ['ede888afd1934fa6a2d4853f2f4ef6b1'], 'Elefa es una elefanta enorme (2,60 m) erguida en dos patas, con armadura: le saca casi un metro a una persona.'),
            (r'Gheco|gecko', 'Gheco', ['bce6aece6b9c43939e86fd2b757679ad'], 'Gheco es un gecko chiquito, del tamaño de una mano.'),
            (r'\bIara\b', 'Iara', ['5d09d4c2cd01468999e671616ec88913'], 'Iara es bajita (1,58 m): más baja que Nilo.'),
            (r'Ferm[ií]n|[Bb]odeguero', 'Fermín', ['fc1a64872e8e420ab4ca98a70c73800a'], 'Fermín es un anciano bajo y encorvado.'),
            (r'\bMarea\b|[Ff]arera', 'Marea', ['15758130c92349e88c7ca83c931fcae1'], 'Marea es una mujer alta (1,78 m) y fuerte: más alta que Nilo.'),
            (r'\bPico\b', 'Pico', ['3ddf2b48417d4bab8a5ef77b03ce4227'], 'Pico es una gaviota del tamaño de una gaviota real.'),
            (r'Sirena', 'la Sirena de los Tipos Débiles', ['c71b98ffb0bd4bc88ef712de0201884e'], ''),
            (r'G[oó]lem', 'el Gólem del Astillero', ['52cd0909808b46eea669353b03637714'], ''),
            (r'Gorgona', 'la Gorgona de los Formularios', ['14106957d3df4712bde2186067dece71'], ''),
            (r'Serpiente Marina', 'la Serpiente Marina de las Tablas', ['aac39a769d40417dbbbfd635d747c363'], ''),
            (r'Drag[oó]n del Faro', 'el Dragón del Faro', ['21bb239895d8460c9bfe93d2ea25d0b9'], ''),
            (r'Campe[oó]n Eterno', 'el Campeón Eterno', ['2a4dfe1f32224ac787f4af1606dbfc94'], ''),
            (r'Grifo', 'el Grifo de los Registros', ['c6db8bca36764764b7f36f1ec7f33751'], ''),
            (r'\bOrca\b', 'la Orca de los Mensajes', ['df4d58f03c7f4e7f9606b7015c18b890'], ''),
            (r'Hipocampo', 'el Hipocampo de las Vidrieras', ['ba8ec9a0f5044116baa84f06f72ed9d4'], ''),
        ],
    },
    'html': {
        'project': '9229721314509917104',
        'region': 'Los Talleres de los Vitrales',
        'ambiente': 'en un taller de vitralistas con ventanales de colores, ríos de plomo fundido, hornos y mesas llenas de bocetos y vidrios',
        'chars': [
            (r'\bIris\b', 'Iris', ['16228314456252100662', '16228314456252101368'],
             'Iris lleva UNA SOLA trenza gruesa, de costado, que le cae sobre un hombro (nunca dos trenzas), pelo castaño cobrizo con mechones de colores dentro de la trenza, anteojos redondos.'),
            (r'Tesela', 'Tesela', ['1156350282938354434', '1156350282938353708'],
             'Tesela e Iris son casi de la misma altura (Tesela apenas unos centímetros más alta).'),
            (r'Gheco|gecko', 'Gheco', ['11514129442070458985'], 'Gheco es un gecko chiquito, del tamaño de una mano.'),
            # Subidos el 2026-10-10. Solo el cuerpo entero: los circulares llevan el nombre escrito y Stitch lo copiaría.
            (r'\bNora\b', 'Nora', ['e01c853235f1406f8ae015a41a3ddb13'],
             'Nora es ciega y alta, más alta que Iris; lleva túnica gris perla y un bastón blanco.'),
            (r'\bTeo\b', 'Teo', ['21a330a7f37f44ae88efae1965f5261c'],
             'Teo es un chico flaco y bajo para su edad, apenas más bajo que Iris, de pelo negro enrulado.'),
            (r'[ÁA]mbar\b', 'Ámbar', ['75ef2e33ad354037aab45fcd703d2d9e'],
             'Ámbar es una señora mayor, baja y redonda, más baja que Iris.'),
            (r'[Ss]lime', 'el Slime de las Etiquetas Huérfanas', ['66e80ef80f2647688427bfdec056c871'], ''),
            (r'[Oo]gro', 'el Ogro de la Cascada', ['ba4b3f1b293f43f4baa369df6491ff00'], ''),
            (r'[Oo]rco', 'el Orco del Desborde', ['7a8f59387a2545509da51e5bce46317f'], ''),
            (r'[Dd]rag[oó]n', 'el Dragón de los Talleres', ['6f9f122674eb41fa91eef6ca0a8a494c'], ''),
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


def missing_refs(course: str, scene: dict) -> list:
    """Personajes de la escena que todavía no tienen sus imágenes en Stitch."""
    return [c[1] for c in REFS[course]['chars'] if not c[2] and re.search(c[0], scene['imagen'])]


def prompt(course: str, scene: dict) -> dict:
    cfg = REFS[course]
    found = [c for c in cfg['chars'] if re.search(c[0], scene['imagen'])]
    screens, notes = [], []
    has_kira = any(c[1] == 'Kira' for c in found)
    has_iris = any(c[1] == 'Iris' for c in found)
    for _, name, ids, note in found:
        screens += ids
        if note and not has_kira and ' (al lado de Kira' in note:  # sin Kira, sin la comparación (la haría aparecer)
            note = note.split(' (al lado de Kira')[0] + '.'
        if note and not has_kira:  # sin Kira, el tamaño se dice sin compararla
            note = re.sub(r', mucho más baj.*?\)\.', ', de baja estatura.', note) if ', mucho más baj' in note else note.replace('le llega a Kira al hombro', 'es de baja estatura (enano), mucho menor que un humano').replace('más alto que Kira', 'más alto que un humano promedio')
        if note and not has_iris:  # en HTML, la comparación es con Iris
            note = re.sub(r',? (apenas )?más (alt|baj)[oa] que Iris', '', note)
        if note and ('Kira' not in note or has_kira) and ('Iris' not in note or has_iris):
            notes.append(note)
    if len(screens) > MAX_REFS or len(found) >= 3:  # se quedan los cuerpos enteros (con 3+, Stitch arma viñetas si no)
        screens = [c[2][0] for c in found][:MAX_REFS]
    names = [c[1] for c in found]
    who = ', '.join(names[:-1]) + (' y ' if len(names) > 1 else '') + names[-1] if names else ''
    text = (
        'Generá una IMAGEN NUEVA de escena (no modifiques las imágenes seleccionadas: son referencias de cómo se ven los personajes). '
        + (f'Usá las referencias para que {who} ' + ('tengan' if len(names) > 1 else 'tenga') + ' exactamente su aspecto: misma cara, pelo, ropa, colores y proporciones.' if who else '')
        # Ni el lugar ni la región van con nombre: Stitch los escribe en un cartel. Se describe el ambiente.
        + f'\n\nLa escena ({cfg.get("ambientes", {}).get(scene["file"], cfg["ambiente"])}):\n'
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
    if '--next' in sys.argv:  # el pedido de la primera pendiente cuyos personajes ya tienen referencia
        ready = [s for s in pending if not missing_refs(course, s)]
        if not ready:
            print('Todas hechas.' if not pending else f'Faltan {len(pending)}, todas con personajes sin referencia.')
            return
        sys.argv += ['--prompt', ready[0]['id']]
        print(ready[0]['id'])
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
        miss = missing_refs(course, s)
        print(f'  {s["id"]:14} {s["title"]}' + (f'  (sin referencia: {", ".join(miss)})' if miss else ''))


if __name__ == '__main__':
    main()
