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
| C++ | 37 de 163 | En curso (2026-10-11): R00 y R01 completas, R02 hasta `R02-N02-P2`. Bron y Gheco no estaban subidos: se generaron en el proyecto de C++ desde sus fichas y sus imágenes oficiales (`REFS['cpp']`). |
| PHP | 36 de 213 | En curso (2026-10-13): la Clase 0 y R01 hasta `R01-N08-P4`; sigue `R01-N09-P1`. Para rehacer si sobra cuota: `R01-N08-P4` (las cajas no quedaron una dentro de la otra). Gheco a veces sale más grande que una mano y algún número de objetos no coincide (3 cajones en vez de 4): se dejaron cuando no cambia la escena. Historia, personajes y mapa en el proyecto de PHP (`REFS['php']`, docs/historias/php.md). Ojo: una corrección con `edit_screens` puede redibujar la escena entera (la de Elefa en el mostrador perdió la gorra de Nilo al arreglarle la bufanda): mirar cada versión. |

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
