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
| C | ver el script | Referencias completas en Stitch: Kira, Ferrum, Gheco, Tizón, Chispa, Hulda, el Archivero y los 7 jefes. |
| HTML | 10 de prueba | Referencias: Iris, Tesela, Gheco. |
| C++ | 0 | Faltan en Stitch Bron, Gheco, Lima, Oto, Lyn (están en `~/stitch-subir/`). |

**Para rehacer (C):** toda la tanda de prueba salió con el Ferrum viejo («enano») o sin referencias, así que se
sacó de `escenas/` y volvió a quedar pendiente: `R00-N01-P1`, `R00-N01-P2`, `R01-N03-P2`, `R01-N06-P1` (además tenía
números flotando), `R02-N03-P1`, `R03-N05-P4`, `R05-N01-P1`, `R02-N06-P2` (faltaba Chispa), `R01-N10-P1` (el Gólem) y
`R05-N04-P3` (el Dragón). Quedan buenas `R00-N01-P3` y `R00-N01-P4` (Tizón).

**Próximo paso (2026-10-10):** el docente vuelve a probar Stitch (se había agotado la cuota). Seguir con la primera
pendiente que da el script, de a una, y revisar cada escena contra las referencias antes de guardarla.
