# Micro-misiones: el generador

Las micro-misiones de Python (ramas 2 y 3 y las Sendas) se escriben como datos en estos `.py` y se pasan al formato del importador (FORMATO-CURSO.md § 6 bis). **La salida esperada nunca se escribe a mano**: sale de ejecutar cada solución, y se comprueba que el código inicial **no** dé ya esa salida.

- `python3 check.py s01.py -v` — ejecuta cada solución y muestra su salida (las de numpy y pandas necesitan un Python con esos paquetes).
- `python3 to_course.py s01.py s02.py` — las inserta (o reescribe) en `cursos/python/`, antes de las prácticas de cada nodo.
- Después: `php artisan app:import-course cursos/python --apply` y probarlas en el navegador (Pyodide), que es donde las corre el alumno.

**Estado:** `r02.py` y `r03.py` ya están en el curso. `s01.py` (Arena, 17) y `s02.py` (Reino, 18) están escritas y verificadas en Python, **sin insertar todavía**: falta correrlas en el navegador y revisarlas.

## Java

`genjava.py` hace lo mismo con el JDK de la compu (`java Archivo.java`, como el ejecutor del alumno): `python3 genjava.py java_r01.py [--apply]`. `java_r01.py` tiene la Clase 0 y R01-N01 a N05; `java_r01b.py`, R01-N06 a N09 (el Centinela); `java_r02a.py` y `java_r02b.py`, la Academia (R02); `java_r03.py`, los Archivos (R03: JUnit imitado con Java puro, porque el ejecutor corre un solo archivo sin librerías). `java_r04.py`, las Corrientes (R04, concurrencia determinista) y `java_r05.py`, la Torre (R05: Spring imitado con Java puro); `java_s02.py` y `java_s03_s04.py`, el Palacio, el Arcade y el Puerto. La Bóveda (`java_s01.py`) mezcla Java y SQL: se genera con `python3 gensql.py java_s01.py [--apply]`, que corre las de SQL con SQLite y el mismo formato que el ejecutor del navegador (D97). Ojo con `printf("%,d")` y los decimales: dependen del idioma de la compu; usá `%d` o `Locale.US`. En el modo de un solo archivo, la clase con el `main` va primero y las demás, sin `public`, debajo. Cada nodo usa solo lo que ya se enseñó: nada de bucles antes de N06 ni de arrays antes de N07.

## C

`genc.py` compila cada solución con `gcc -std=c11 -Wall -Wextra` y la ejecuta: `python3 genc.py c_r01.py [--apply] [--json casos.json]`. Rechaza las soluciones con advertencias y lo que en el navegador da distinto (D98: ahí C corre en wasm32, donde `long` y los punteros miden 4 bytes y `rand()` da otra secuencia): nada de `%p`, `sizeof(long)`, `sizeof` de punteros ni `rand()` (para azar, una semilla y una cuenta propia). Con `--json` deja los casos para probarlos en Chrome con el Clang del navegador. Cada nodo usa solo lo que ya se enseñó.

## C++

`gencpp.py` hace lo mismo con `g++ -std=c++20 -Wall -Wextra`: `python3 gencpp.py cpp_r01.py [--apply] [--json casos.json]`. En el navegador (D100) C++ corre con libc++ y en la compu del alumno con libstdc++ (o la de su compilador), así que además de lo de C rechaza las distribuciones de `<random>` (para azar, `std::mt19937` crudo y `gen() % n`, que da igual en todas), `random_device`, `typeid` y `std::hash`, y pide revisar a mano los `unordered_*` (`orden_libre=True` si nunca se muestra su orden). Las salidas van sin tildes. `cpp_r01.py` y `cpp_r01b.py` tienen la Clase 0 y los Cimientos; `cpp_r02.py` a `cpp_r05.py`, una rama cada uno; `cpp_r06.py`, los Vitrales (Qt) y la Senda de la Linterna (SDL3), que prueban la lógica sin ventana. Son 163, todas verificadas también en el navegador.

`browser-check.mjs` prueba los casos de `--json` con el Clang del navegador (Chrome sin ventana, el admin local y el ejecutor del ejemplo de un nodo): `node browser-check.mjs casos.json --nodo=/cursos/cpp/nodos/ID`. Sirve igual para C.

