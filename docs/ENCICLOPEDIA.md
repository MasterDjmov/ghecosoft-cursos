# La Gran Enciclopedia del Código (D104)

Un lugar donde el alumno consulta **todo el universo**: quién es cada personaje, qué criaturas hay, qué ítems existen y **dónde se consiguen**, las monturas, las monedas y los reinos. Sirve para leer por gusto y para buscar: «¿dónde se consigue el Monóculo de Cristal?» → «HTML y CSS, al vencer al Ogro de la Cascada (R02)».

Referencia visual: `publicidad/logos cursos/` (la portada de la enciclopedia con Gheco señalando las 8 tarjetas).

## 1. Decisiones (charla con el docente, 2026-10-11)

| Pregunta | Decisión |
|---|---|
| ¿Qué ve de lo que no descubrió? | **Silueta y pista**, como un Pokédex: lo no descubierto aparece en sombra, con el nombre y dónde se consigue, pero sin su historia. |
| ¿Qué cursos abarca? | **Todo el universo** (los cursos publicados), aunque no esté inscripto: así ve que algo se consigue en otro curso y le da ganas de cursarlo. |
| ¿Y el Grimorio? | **Queda como está** y la enciclopedia tiene una tarjeta «Hechizos & Sintaxis» que lleva a él. |
| ¿La portada? | La **imagen de la biblioteca** del docente (`publicidad/logos cursos/enciclopedia.jpeg` → `public/img/enciclopedia/portada.webp`): sus 8 tarjetas pintadas son los botones; en el celular, una grilla debajo. La portada ocupa todo el ancho. De fondo, en todas las pantallas, va **la biblioteca limpia** (`publicidad/logos cursos/fondo_enciclopedia.jpeg` → `public/img/enciclopedia/fondo-biblioteca.webp`, sin letras) en toda el área, con una capa oscura para que se lea. |
| ¿Da algo? | **No, por ahora es solo para leer.** |
| ¿Quién la ve? | **Todos los alumnos**, también los que solo prueban la Clase 0: es para que se motiven. |
| ¿Cómo se ve cada elemento? | Al hacer click, **en un modal**, como los ítems de la mochila. |

## 2. Las 8 secciones y de dónde sale cada una

Nada se escribe dos veces: la enciclopedia **lee** lo que ya existe.

| Sección | Qué muestra | Fuente | Descubierto cuando… |
|---|---|---|---|
| **Clases / Lenguajes** | cada curso: logo, mundo, líder, moneda, protagonista, cuántos nodos | `courses` + Diccionario | siempre visible (es la puerta de entrada) |
| **Maestros** (líderes, guías y compañía) | retrato, cuerpo entero, rol, personalidad, frase, le gusta, relaciones, primera aparición | `docs/historias/PERSONAJES.md` (`CharacterSheets`) | abrió el nodo de su «Primera aparición» (o el raíz del curso, si no la tiene) |
| **Bestiario** | criaturas y jefes: qué error de programación representan, cómo se los vence, qué dejan al caer | PERSONAJES.md + nodos jefe + `config('game')` (criaturas de cada lugar) | lo vio (abrió el nodo o lo cruzó en una expedición); «vencido» al completar el jefe |
| **Monturas** | cada especie, su imagen y cómo se consigue | `config('game.mounts')` | la tiene o la tuvo |
| **Monedas** | moneda de cada curso, el comodín y el oro: imagen y cómo se gana | `currencies` + Diccionario | está inscripto en ese curso (el comodín y el oro, siempre) |
| **Artefactos** | los ítems: imagen, rareza, atributos, descripción y **dónde se consigue** | `items` + micro-misiones que lo dan + tienda de cada mundo + recetas del taller + botín | lo tuvo alguna vez (`item_movements`) |
| **Reinos / Mapas** | cada mundo con su fondo, su líder y los lugares de las expediciones | Diccionario (`world.region`) + `config('game')` | abrió el raíz de ese curso |
| **Hechizos & Sintaxis** | lleva al Grimorio | `student.grimoire` | (lo que ya hace el Grimorio) |

### «Dónde se consigue» (lo más útil para el alumno)
Se arma solo, con todos los orígenes que tenga cada cosa:
- **Micro-misión:** «HTML y CSS · R02-N03, micro-misión 2» (el `item` de `node_steps`).
- **Jefe:** «al vencer al Ogro de la Cascada (HTML, R02)».
- **Tienda:** «en el carro de Chispa (C), 40 de oro, desde el nivel 3».
- **Taller:** «se fabrica con 2 × Vidrio y 1 × Plomo».
- **Expedición:** «botín raro en la Cueva del Troll (Python)».
- **Personajes:** «aparece en C, R01-N02».

Si el curso no lo tiene abierto, el lugar se muestra igual (es la pista), pero sin el enlace.

## 3. Silueta y pista: qué se oculta

| | Descubierto | No descubierto |
|---|---|---|
| Imagen | a color | **silueta** (la misma imagen en negro con brillo, por CSS) |
| Nombre | sí | sí |
| Dónde se consigue | sí | sí |
| Historia, frase, relaciones, atributos | sí | «???» |

Como en Mis Crónicas (D80), **el texto de lo no descubierto no sale del servidor**: no basta con taparlo por CSS.

## 4. Pantallas

- **Portada** (`/enciclopedia`): la escena de la biblioteca con las 8 tarjetas y un contador por sección («Bestiario 12 / 48»).
- **Sección** (`/enciclopedia/bestiario`…): una grilla de tarjetas con filtro por curso y buscador por nombre.
- **Ficha**: se abre en un panel al costado (en el celular, a pantalla completa) con la imagen grande y todo lo de arriba.
- En el menú del alumno: **Enciclopedia**, cerca de Mis Crónicas y el Grimorio. Las fichas de personajes de otras pantallas (la compañía en el nodo, la tienda) pueden enlazar a su ficha.

## 5. Lo que hay que preparar (contenido)

1. **Imágenes.** En la plataforma hay 20 imágenes de personajes; en `publicidad/logos cursos/personajes/` hay unas 290, ordenadas por mundo y por personaje (`Nora/Nora.jpeg` y `Nora/circular_nora.jpeg`). Un comando `app:encyclopedia-images carpeta/ [--apply]` las cargaría por el nombre de la carpeta (como `app:glossary-portraits`), convertidas a webp. Las monturas, de `monturas/`.
2. **Primera aparición.** De las 63 fichas de PERSONAJES.md, 25 dicen dónde aparecen. Hay que completar el resto con el formato «Curso, R01-N02» para saber cuándo se descubren y para la pista.
3. **Qué se muestra de cada ficha.** Al alumno van rol, personalidad, le gusta, defecto, frase y relaciones. No van las líneas pensadas para generar imágenes (altura, ropa, color) ni las notas para el docente.

## 6. Etapas

1. **Portada y Maestros + Bestiario** (lo que más contenido tiene), con la silueta y la pista, y el comando de imágenes.
2. **Artefactos** con «dónde se consigue» y **Monedas**.
3. **Monturas** y **Reinos / Mapas**.
4. Enlaces desde el resto de la plataforma a cada ficha.

## 7. Cómo quedó la etapa 1 (2026-10-11)

- **Pantalla:** `/enciclopedia` (`App\Livewire\Student\Encyclopedia`), en el menú del alumno, grupo Juego. Maestros y Bestiario con filtro por mundo y buscador; un solo modal que se llena con la ficha elegida.
- **Datos:** `App\Support\Encyclopedia` lee las fichas de PERSONAJES.md. Una ficha con «Qué es» o «Qué error representa» va al Bestiario; las demás, a Maestros. El mundo sale del lenguaje entre paréntesis de su sección («Las Forjas de Hierro (C)») y el de un protagonista, de `config('game.protagonists')`.
- **Cuándo se descubre:** al abrir el nodo de su «Primera aparición» (`R01-N02`, o `R01` = cualquier nodo de esa rama; «Clase 0» = el raíz). Una criatura sin primera aparición toma el código de su «Rol» y, si es una rama, el **jefe** de esa rama; queda «vencida» al completar ese nodo. Sin código, el raíz del curso. Los protagonistas, los guías y el bestiario común se ven siempre; el staff ve todo.
- **Qué se muestra:** rol, qué es, qué error representa, cómo se lo vence, qué explica, edad, personalidad, le gusta, defecto, objeto, frase, cómo habla y relaciones (`Encyclopedia::FIELDS`), sin los enlaces a los .md.
- **Bestiario común:** las 7 criaturas de todos los mundos se sumaron a PERSONAJES.md («El bestiario común»).
- **Imágenes:** `python3 scripts/enciclopedia/imagenes.py "<carpeta de personajes>" [--force]` deja el retrato (320 px) y el cuerpo entero en `public/img/enciclopedia/<slug>.webp` y `<slug>-cuerpo.webp` (van en git y suben con el deploy). Une cada carpeta con su ficha por el nombre, dentro de su mundo; al final dice qué carpetas y qué fichas quedaron sin pareja. Con un personaje nuevo: su carpeta con `circular_<nombre>.jpeg` y el cuerpo entero, y volver a correrlo.
- **Falta imagen:** la maestra del Gremio de Artífices (Python).
