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
   enorme, más alto que Kira** (no enano); enanos son Tizón, Hulda y el Archivero.
4. La imagen se baja con `get_screen` (URL de `screenshot.downloadUrl` + `=s1376`), se pasa a WebP 1376×768 y se
   guarda como `cursos/<curso>/escenas/<ID>.webp`. Se mira: si un personaje salió distinto, se borra y se pide de nuevo.
5. Cada tanto, commit (`content(c): escenas …`). Al terminar: `php artisan app:import-course cursos/c --apply` en local
   y, para producción, `git push && scripts/deploy.sh --cursos`.

Las referencias de cada curso (ids de pantallas de Stitch) están en `REFS` dentro de `scripts/escenas/pendientes.py`.
**Cuota:** Stitch tiene un límite de generaciones. Si responde «Resource has been exhausted (e.g. check quota)», no
insistir: se espera (al día siguiente) y se sigue con la primera pendiente. Pedirlas **de a una**: en paralelo se
gasta la cuota enseguida. El 2026-10-09 se cortó después de `R00-N01-P4` (siguiente: `R00-N01-P5`).

Si una llamada a Stitch se corta por tiempo, la pantalla igual puede aparecer: buscarla con `get_screen` no sirve sin el
id, así que se vuelve a pedir.

## Estado

| Curso | Hechas | Notas |
|---|---|---|
| C | ver el script | Referencias completas en Stitch: Kira, Ferrum, Gheco, Tizón, Chispa, Hulda, el Archivero y los 7 jefes. |
| HTML | 10 de prueba | Referencias: Iris, Tesela, Gheco. |
| C++ | 0 | Faltan en Stitch Bron, Gheco, Lima, Oto, Lyn (están en `~/stitch-subir/`). |

De la tanda de prueba de C se rehicieron con referencias `R02-N06-P2` (faltaba Chispa), `R01-N10-P1` (el Gólem) y
`R05-N04-P3` (el Dragón).
