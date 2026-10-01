# Escribir las pruebas de un curso (D73)

Ayudantes que se usaron para cargar las `#### Pruebas` de los cinco cursos (2026-10-01). Sirven igual para un curso nuevo. Se corren desde la carpeta del proyecto; el formato está en [docs/FORMATO-CURSO.md § 6](../../docs/FORMATO-CURSO.md).

1. **Listar** las prácticas que leen entrada y todavía no tienen pruebas, con su consigna, entrada y salida de ejemplo:
   ```bash
   php scripts/pruebas/listar-practicas.php cursos/cpp > /tmp/cpp.txt
   ```
2. **Escribir** las entradas de las pruebas en un archivo de texto (2 a 4 por práctica: el caso vacío, el borde, el dato inválido):
   ```
   @@ R01-N03-M2
   --- División por cero
   7 / 0
   --- Operación desconocida
   5 % 2
   ```
3. **Insertarlas** en los `.md`, con la salida vacía:
   ```bash
   python3 scripts/pruebas/insertar-pruebas.py cursos/cpp /tmp/pruebas.txt
   ```
4. **Completar las salidas** corriendo la solución de referencia (nunca a mano):
   ```bash
   php artisan app:course-tests cursos/cpp --fill
   ```
5. Si alguna prueba quedó **sin salida** (la solución no muestra nada o falla con esa entrada), cambiale la entrada o sacala:
   ```bash
   python3 scripts/pruebas/sacar-pruebas-vacias.py cursos/cpp
   ```
6. **Verificar** que todo coincida, revisar el diff y reimportar el curso:
   ```bash
   php artisan app:course-tests cursos/cpp
   php artisan app:import-course cursos/cpp     # revisar; con --apply guarda
   ```
