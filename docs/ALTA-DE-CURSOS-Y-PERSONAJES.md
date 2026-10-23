# Alta de cursos, personajes e historias: dónde va cada cosa

Pedido del docente (2026-10-14): cada vez que se suma **un curso, un personaje (principal, secundario o enemigo), una criatura, una montura, un ítem o un tramo de historia**, se revisa esta lista entera. Así no hay que salir a buscar después dónde faltó agregarlo (pasó con los ítems de PHP sin imagen, con Ada sin retrato en la enciclopedia y con las monedas de inglés).

Se vienen **JavaScript, React Native y Laravel**: cada uno trae su región, su héroe, su líder, su gente, sus jefes y su moneda, y todo eso pasa por esta lista.

> Regla: el trabajo no está terminado hasta que cada fila que aplica esté hecha o anotada como pendiente en el .md del curso (con el motivo).

---

## 1. Un curso nuevo

| Dónde | Qué | Archivo o comando |
|---|---|---|
| Lenguaje | el `case` del enum, `label()`, extensión, si el alumno puede ejecutar | `app/Enums/Language.php` |
| Contenido | la carpeta del curso en el formato del importador; temas en `cursos/temas.md` | `cursos/<slug>/`, [FORMATO-CURSO.md](FORMATO-CURSO.md) |
| Pruebas de las prácticas | salidas de referencia | `php artisan app:course-tests cursos/<slug> --fill` |
| Seeder y deploy | que el seeder local lo importe; `scripts/deploy.sh --cursos` lo reimporte | `database/seeders/`, `scripts/deploy.sh` |
| Landing | logo, moneda, «destacado», Próximamente/Avisame | `LandingController` (`IMAGES`), `CourseCatalog`, *Admin → Cursos* |
| Universo | color del curso en el mapa 3D | `app/Support/UniverseGraph.php` |
| Enciclopedia | la región en `WORLDS` (si no, sus personajes no se agrupan) | `app/Support/Encyclopedia.php` |
| Monedas | logo de la moneda y su texto en la enciclopedia | `EncyclopediaItems` |
| Ejecutores y entregas | listas de lenguajes con casos y ejecución local | `SubmissionCases::LANGUAGES`, `LocalCodeRunner`, `components/code-runner` |
| Historia | `docs/historias/<slug>.md` + fichas en `PERSONAJES.md` + `NOVELA-GRAFICA.md` + `HISTORIA-BRIEF.md` si cambia el sistema | `docs/historias/` |
| Mis Crónicas | el libro del curso y su pieza del portal | `Support\Chronicles`, [CRONICAS.md](CRONICAS.md) |
| Simulación | correr el súper test antes de abrirlo | `php artisan app:simulate-course <slug>` |
| **Inglés** | **su temporada en las Crónicas en Inglés (Primaria y Secundaria)**, ver § 4 | [INGLES.md](INGLES.md) § 8 |
| CLAUDE.md | la carpeta del curso en «Documentos» | `CLAUDE.md` |

## 2. Un personaje nuevo (héroe, líder, secundario o jefe)

| Dónde | Qué | Archivo o comando |
|---|---|---|
| Ficha | aspecto, edad, rol, frase (manda sobre todo lo demás) | `docs/historias/PERSONAJES.md` |
| Imágenes en Stitch | cuerpo entero (+ circular si va al diccionario); su ID en las referencias de escenas | `scripts/escenas/pendientes.py` (`REFS`/`chars`) |
| Copia del docente | en la carpeta de personajes | `publicidad/logos cursos/personajes/<curso>/` |
| Diccionario general | retrato | `php artisan app:glossary-portraits carpeta/ --apply` |
| Enciclopedia | retrato y cuerpo (`<slug>.webp`, `<slug>-cuerpo.webp`), silueta y pista | `public/img/enciclopedia/`, `scripts/enciclopedia/imagenes.py` |
| Mis Crónicas | figura de cuerpo entero | `app:glossary-portraits --figuras` |
| Landing | si aparece en la portada | `LandingController::IMAGES`, `public/img/personajes/` |
| Si es **protagonista** | `config/game.php` → `protagonists`: nombre, 6 aspectos (`public/img/protagonistas/<slug>/1..6.webp`), tienda, expediciones y mapa | `Heroes`, `config/game.php` |
| Si **atiende una tienda** | `shop` con `portrait` y `figure` | `config/game.php` |
| Si es **jefe o criatura** | bestiario (enciclopedia), `creatures` si va a las expediciones, su material | `config/game.php`, `GameItems` |
| **Inglés** | **sale en su temporada de inglés**, con su forma de hablar | § 4 |

## 3. Juego: ítems, monturas, recetas, expediciones

| Dónde | Qué | Archivo o comando |
|---|---|---|
| Ítems | catálogo del curso **y** su pedido de imagen | `GameItems::CATALOG` y `::PROMPTS` |
| Imágenes de ítems | **siempre**, en el mismo commit o la misma tanda (Stitch: hojas 3×3, «CERO texto», recortadas) | `php artisan app:item-images carpeta/ --apply` en local **y en producción** |
| Segunda vida | si el ítem la da | `Item::SECOND_LIFE` |
| Recetas del taller | que todo ítem de receta tenga imagen | `config('game.recipes')`, `Crafting` |
| Monturas | especie en `mounts.species` + `public/img/monturas/<especie>/n1..n5.webp` | `config/game.php`, `Stables` |
| Expediciones | lugares, mapa `public/img/mundos/<región>/mapa.webp`, criaturas | `config/game.php` |
| Mochila | sale sola (una solapa por curso con abono o con ítems) | `Livewire/Student/Inventory` |

Para saber qué falta en producción:

```bash
ssh ghecosoft-prod 'cd ~/gamificado.lariojaclick.ar && php artisan tinker --execute "echo App\Models\Item::whereNull(\"image_path\")->pluck(\"code\")->implode(\", \");"'
```

## 4. Inglés: cada curso nuevo es una temporada nueva

Las Crónicas en Inglés recorren **todas** las regiones ([INGLES.md](INGLES.md) § 8). Cuando entra un curso nuevo (JS, React Native, Laravel…):
- sus personajes (héroe, líder, gente del lugar, jefes) tienen **su reparto en inglés**: aparecen en una **temporada nueva** de Primaria y de Secundaria, con episodios de tronco y ramas;
- la gramática de esa temporada se elige según dónde encaje en el recorrido (la tabla de INGLES.md § 8);
- sus escenas sirven para el inglés: cuantas más escenas tenga el curso, más barata es su temporada;
- sus criaturas pasan a ser errores de inglés como las demás (historias/ingles.md § 2);
- si algún personaje nuevo se cruza con Ada, va en su ficha;
- **la regla del tiempo** ([historias/ingles.md](historias/ingles.md) § 3 bis): en Primaria la Ada de 11 vive la región en presente y cada héroe la conoce una vez; en Secundaria la Ada de 15 la **reescribe cuatro años después** (pasado, presente perfecto, estilo indirecto) y no comparte escena con el héroe en su momento: en sus portadas sale sola y el héroe, como recuerdo; si hace falta alguien grande en presente, se crea otro personaje;
- **las portadas** (una por episodio, tronco y ramas, en las dos edades de Ada) se hacen en el proyecto de Stitch de esa región, recreando antes ahí las hojas de Ada niña y de 15 (ver ESCENAS.md, fila de las Forjas); si al curso le faltan escenas para los episodios, se generan.

## 5. Una historia o escena nueva

- El texto en `docs/historias/<slug>.md` y, si toca a otros cursos, en `NOVELA-GRAFICA.md`.
- Las escenas en `cursos/<slug>/escenas/` y el conteo en [ESCENAS.md](ESCENAS.md).
- Si suma un objeto que gana el héroe, va a `GameItems` (con imagen).
- Si suma un personaje, § 2.
- Si se puede contar en inglés, se anota en la temporada de esa región.
