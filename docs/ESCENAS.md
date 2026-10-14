# Escenas de las micro-misiones (Stitch)

Cada micro-misión, misión y encargo tiene un `#### Imagen` en su .md: el pedido de la escena. La imagen se carga
sola desde `cursos/<curso>/escenas/<ID>.webp` al importar el curso (FORMATO-CURSO § 6).

**El progreso es la carpeta `escenas/`**: una escena está hecha cuando existe su archivo. Para ver cuánto falta:

```
python3 scripts/escenas/pendientes.py cursos/c
```

## Cómo se generan sin alterar los personajes

1. Los personajes ya están dibujados en el proyecto de Stitch del curso (cuerpo entero 896×1200 + circular 1024×1024).
   Son las **referencias**: nunca se editan ni se regeneran.
2. Cada escena se pide con `edit_screens` (MCP de Stitch) **seleccionando las referencias** de los personajes que
   aparecen y con el pedido «Generá una IMAGEN NUEVA… no modifiques las imágenes seleccionadas». Stitch crea una
   pantalla nueva y deja las referencias como estaban (probado: las referencias no cambian).
3. El pedido exacto lo arma el script: `python3 scripts/escenas/pendientes.py cursos/c --prompt R01-N01-P1`
   (proyecto, pantallas de referencia y texto, con los tamaños). Las descripciones de los `#### Imagen` tienen que
   cuadrar con las referencias: si no, Stitch duda entre el texto y la imagen. En C, Maese Ferrum es un **herrero
   enorme, más alto que Kira** (no enano); enanos son Tizón, Hulda y el Archivero. Ojo: Stitch reescribe el pedido
   por su cuenta y lo vuelve «dwarven blacksmith» (de piernas cortas): por eso el texto dice «humano, NO es enano, de
   unos dos metros». Mirar las proporciones contra la referencia de cuerpo entero antes de guardar.
4. La imagen se baja con `get_screen` (URL de `screenshot.downloadUrl` + `=s1376`), se pasa a WebP 1376×768 y se
   guarda como `cursos/<curso>/escenas/<ID>.webp`. Se mira: si un personaje salió distinto, se borra y se pide de nuevo.
5. Cada tanto, commit (`content(c): escenas …`). Al terminar: `php artisan app:import-course cursos/c --apply` en local
   y, para producción, `git push && scripts/deploy.sh --cursos`.

**Sin carteles:** si el pedido nombra el lugar («La boca de la Forja»), Stitch lo escribe en un cartel; por eso el
script no lo pasa. Si igual aparece un rótulo chico, se puede tapar con la textura de al lado (como en `R00-N01-P2`) o
pedir de nuevo. Cuando Stitch devuelve dos pantallas, la segunda es una corrección suya: mirar las dos.

Las referencias de cada curso (ids de pantallas de Stitch) están en `REFS` dentro de `scripts/escenas/pendientes.py`.
**Cuota:** Stitch tiene un límite de generaciones. Si responde «Resource has been exhausted (e.g. check quota)», no
insistir: se espera (al día siguiente) y se sigue con la primera pendiente. Pedirlas **de a una**: en paralelo se
gasta la cuota enseguida. El 2026-10-09 se cortó después de `R00-N01-P4`.

Si una llamada a Stitch se corta por tiempo, la pantalla igual puede aparecer: buscarla con `get_screen` no sirve sin el
id, así que se vuelve a pedir.

## Estado

| Curso | Hechas | Notas |
|---|---|---|
| C | 161 de 161 | Completo (2026-10-10). |
| HTML | 100 de 100 | Completo (2026-10-11). Tesla y Ofidia (visitas) se dibujaron por descripción: no tienen referencia en el proyecto de HTML. |
| C++ | 45 de 163 | En curso (2026-10-11): R00 y R01 completas, R02 hasta `R02-N02-P2`; más 8 sueltas hechas para la temporada de la Ciudadela (2026-10-14: `R02-N02-P3`, `R05-N01-P1` a `P3`, `R06-N05-P1` a `P4`). Bron y Gheco no estaban subidos: se generaron en el proyecto de C++ desde sus fichas y sus imágenes oficiales (`REFS['cpp']`). |
| PHP | 59 de 213 | En curso: la Clase 0 y R01 completos (2026-10-13), más 18 sueltas de R03–R05 hechas para la temporada del Puerto (2026-10-14, fila de abajo); sigue `R02-N01-P1`. La Sirena ya está descrita con blusa cerrada en los .md y en PERSONAJES.md. Ojo: a veces sale un segundo Gheco o una cola cian suelta; pedir «UN SOLO Gheco». Para rehacer si sobra cuota: `R01-N08-P4` (las cajas no quedaron una dentro de la otra). Gheco a veces sale más grande que una mano y algún número de objetos no coincide (3 cajones en vez de 4): se dejaron cuando no cambia la escena. Historia, personajes y mapa en el proyecto de PHP (`REFS['php']`, docs/historias/php.md). Ojo: una corrección con `edit_screens` puede redibujar la escena entera (la de Elefa en el mostrador perdió la gorra de Nilo al arreglarle la bufanda): mirar cada versión. |
| Inglés · Forjas (temporada 2) | 24 de 24 | Completo (2026-10-14): una portada por episodio, tronco y ramas, `FORJAS-01` a `FORJAS-12` (Ada niña) y `FORJAS-S01` a `FORJAS-S12` (Ada de 15), en `cursos/ingles/escenas/`; las misiones reusan las de C. Hechas en el **proyecto de C** (`12453694413360128121`): Stitch solo toma referencias del mismo proyecto, así que primero se recrearon las hojas de Ada niña (`4eb59d68037844c09f3cf2aafdd77cd4`) y de Ada de 15 (`a94bdbb01fe44e2eb49eea421419838c`) con Eco y el Borrón desde sus fichas, y después cada portada con la hoja + el personaje de la región. **Cada temporada nueva repite esto en el proyecto de su región.** De a una llamada (dos en paralelo ya se cortan); para pasar una escena de Ada niña a Ada de 15, «como la segunda, pero con Ada de 15 de la primera» con la portada de Primaria como referencia sale a la primera. Ojo: a veces le saca las cejas o el pelo a quien no corresponde, o escribe un título: revisar cada una. |
| Inglés · Puerto (temporada 3) | 24 de 24 | Completo (2026-10-14): `PUERTO-01` a `PUERTO-12` (Ada niña) y `PUERTO-S01` a `PUERTO-S12` (Ada de 15) en `cursos/ingles/escenas/`, hechas en el **proyecto de PHP** con las hojas de Ada recreadas ahí (niña `fd32dbcd41874f3ebedd1802bb364b76`, de 15 `ec1abd3a409d48b58277a0408b62d043`). Para las de Secundaria anduvo mejor el pedido **corto** «como la segunda, con Ada de 15 y Eco joven de la primera» (los largos se cortan por tiempo). Ojo: la Sirena salió sin mangas en una (corregida: blusa cerrada con mangas y cuello alto), en otra quedaron dos Ecos y en otra un título y palabras en el agua. De paso se hicieron **18 escenas de PHP** (R01-N10-P3/P4, R03-N04, R04-N01, R04-N02-P1, R04-N07, R05-N06-P3, R05-N07, R05-N08-P2) que usan el curso y la temporada; usar la escena anterior como única referencia (con los personajes ya dibujados) es lo que menos se corta. |
| Inglés · Ciudadela (temporada 4) | 19 de 24 | En curso (2026-10-14): `CIUDADELA-01` a `12` (Ada niña) y `CIUDADELA-S01` a `S07` (Ada de 15) en `cursos/ingles/escenas/`, hechas en el **proyecto de C++** (`14674491267148198305`) con las hojas de Ada recreadas ahí (niña `d78c472031ae4da8b564180cc607e12b`, de 15 `888fedb546b049779bc0758f69293c42`; la primera hoja dibujó al Borrón como un gato: pedir «mancha sin patas, orejas ni cola»). **Faltan `S08` a `S12`**: Stitch se quedó sin cuota; los IDs de las portadas de Primaria para pasarlas a Ada de 15 están en `pendientes.py`. Ojo: una portada que parte de otra escena arrastra lo de esa escena (la cocina salió inundada por usar la portada del comedor como referencia; se rehízo desde la escena seca de C++).
| Inglés · ramas de los Talleres | 10 de 10 | Completo (2026-10-14): portadas `NUEVA-06` a `NUEVA-08` (Ada niña con Teo, Nora y Ámbar) y `NUEVA-S06` a `NUEVA-S08` (Ada de 15), más `AMBAR-1` a `AMBAR-4` (Ámbar y su carretilla con Teo, Iris, Tesela y Nora; las usan los dos cursos), en el proyecto de HTML. La carretilla salió igual en todas usando la portada `NUEVA-08` (`33161fc524a2455cb00cc91ba060b8ff`) como referencia; ojo, copia también a Eco de esa portada: pedir «sin pájaro» y revisar. Pasar a Ada de 15 con «como la segunda, pero con Ada de 15 de la primera» a veces la deja del tamaño de la nena: corregirla después con «más alta, su cabeza llega al hombro de…». |
| Inglés (piloto) | 10 de 10 | Completo (2026-10-14): Primaria con Ada niña (`NUEVA-01` a `NUEVA-05`) y Secundaria con Ada de 15, Eco joven y el Gran Borrón (`NUEVA-S01` a `NUEVA-S05`); antes, las portadas de Ada y Eco `NUEVA-01` a `NUEVA-05` en `cursos/ingles/escenas/` (historias/ingles-piloto.md). Las misiones reusan las de HTML. Proyecto de HTML con `REFS['ingles']`; salieron todas al primer intento con pedidos cortos y «UN SOLO Eco». Con 3 referencias Stitch se corta por tiempo seguido: pedir de a una y, si se corta, repetir con un pedido más corto. |

**Tamaños que funcionan** (ya están en el script): Ferrum «HUMANO, NO enano, siete cabezas, piernas largas»;
Tizón y Hulda «ENANO/A, su cabeza le llega a Kira al hombro»; Tizón «orejas HUMANAS… la parte de arriba es una
curva redonda, sin punta» (si no, Stitch le pone orejas de elfo); Hulda «MUJER, sin barba, UN solo pico».
Con 3+ personajes, mandar solo las referencias de cuerpo entero y pedir «una sola ilustración, sin viñetas»
(si no, a veces arma viñetas con nombres). Si sale una franja de texto abajo, pedir de nuevo con «la ilustración
ocupa todo el cuadro, sin franjas ni recuadros». Números o letras chicos en la escena se tapan con PIL
(como en `R03-N05-P2`). Iris: «UNA SOLA trenza gruesa, de costado» (si no, le pone dos). Con dos personajes iguales en tipo (Iris y Tesela), mandar solo los cuerpos enteros y decir «exactamente dos personas» (una vez salieron dos Teselas). Plaquitas, etiquetas y carteles: pedirlos «lisos, con un dibujito (estrella, llave, sol), sin letras» (si no, escribe palabras). Los líderes del mundo son Ofidia, Maese Ferrum, Tesla, Kaffa, Elefa y Tesela: no son todas mujeres.

**Próximo paso:** seguir C++ desde la primera pendiente (`python3 scripts/escenas/pendientes.py cursos/cpp --next`). Al terminar: `php artisan app:import-course cursos/cpp --apply` y deploy con `--cursos`.

**Lecciones de C++:**
- **Pedidos cortos.** Stitch reescribe y alarga el pedido por su cuenta; con uno largo se corta por tiempo. Con 2–4 líneas («IMAGEN NUEVA 16:9… Bron y Lima como en las referencias. …») anda y respeta igual a los personajes.
- **Stitch escribe sus propias restricciones dentro de la imagen.** En libros abiertos, papeles y esferas de medidores puso «NO LETTERS», «NO DIGITS». Evitarlos: libros **cerrados**, papeles con **solo un dibujo** o un sello, y en vez de manómetros, **tubos de vidrio con luz** o **lucecitas**. Pizarrones: barras, engranajes o dibujitos de tiza.
- Lo que el `#### Imagen` pide con números o letras (precios, «7/2», «a, b, c», «xxoxx») se traduce a algo visual: banderines de colores, puntitos llenos y vacíos, barras ordenadas.
- Parchar texto con PIL (mediana o reemplazo de píxeles) deja manchas: mejor regenerar.
- **No nombrar el contenido de bolsas, frascos o botellas** («harina», «sal», «aceite»): Stitch les pone la etiqueta escrita («Flour», «Salt»), y si se le pide que no, escribe «NO». Describirlos por cómo se ven (bolsas de tela blanca empolvadas, bolsitas grises) y cambiar botellas por **cántaros de barro** (PHP `R01-N07-P2`, tres intentos).
