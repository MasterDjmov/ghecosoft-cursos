# Micro-misiones: el generador

Las micro-misiones de Python (ramas 2 y 3 y las Sendas) se escriben como datos en estos `.py` y se pasan al formato del importador (FORMATO-CURSO.md § 6 bis). **La salida esperada nunca se escribe a mano**: sale de ejecutar cada solución, y se comprueba que el código inicial **no** dé ya esa salida.

- `python3 check.py s01.py -v` — ejecuta cada solución y muestra su salida (las de numpy y pandas necesitan un Python con esos paquetes).
- `python3 to_course.py s01.py s02.py` — las inserta (o reescribe) en `cursos/python/`, antes de las prácticas de cada nodo.
- Después: `php artisan app:import-course cursos/python --apply` y probarlas en el navegador (Pyodide), que es donde las corre el alumno.

**Estado:** `r02.py` y `r03.py` ya están en el curso. `s01.py` (Arena, 17) y `s02.py` (Reino, 18) están escritas y verificadas en Python, **sin insertar todavía**: falta correrlas en el navegador y revisarlas.

## Java

`genjava.py` hace lo mismo con el JDK de la compu (`java Archivo.java`, como el ejecutor del alumno): `python3 genjava.py java_r01.py [--apply]`. `java_r01.py` tiene la Clase 0 y R01-N01 a N05; `java_r01b.py`, R01-N06 a N09 (el Centinela); `java_r02a.py` y `java_r02b.py`, la Academia (R02); `java_r03.py`, los Archivos (R03: JUnit imitado con Java puro, porque el ejecutor corre un solo archivo sin librerías). `java_r04.py`, las Corrientes (R04, concurrencia determinista) y `java_r05.py`, la Torre (R05: Spring imitado con Java puro); `java_s02.py` y `java_s03_s04.py`, el Palacio, el Arcade y el Puerto. La Bóveda (`java_s01.py`) mezcla Java y SQL: se genera con `python3 gensql.py java_s01.py [--apply]`, que corre las de SQL con SQLite y el mismo formato que el ejecutor del navegador (D97). Ojo con `printf("%,d")` y los decimales: dependen del idioma de la compu; usá `%d` o `Locale.US`. En el modo de un solo archivo, la clase con el `main` va primero y las demás, sin `public`, debajo. Cada nodo usa solo lo que ya se enseñó: nada de bucles antes de N06 ni de arrays antes de N07.
