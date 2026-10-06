# La compañía de héroes (D83, reemplazada)

> **Reemplazada por [JUEGO.md](JUEGO.md) (D84, 2026-10-06).** Queda como historia de la charla.

Conversado con el docente el 2026-10-04, tomando ideas de Tanoth, MapleStory, Lineage 2 y Shiba Wars. **Estado:** diseño, sin programar.

**El problema:** el alumno entrega código, pero no ve qué gana con eso. Las monedas abren nodos, pero no *tiene* nada propio. **La idea:** que su código construya a sus héroes. Cada misión aprobada les deja algo —un atributo, un ítem, una victoria— que se ve en una ficha y crece con lo que aprende. Siempre escribiendo código.

## 1. La compañía: un héroe por curso, inventario común

- La cuenta del alumno es su **compañía**. **Cada curso base que empieza le suma un héroe** de esa cultura: un aprendiz del Valle (Python), un enano de las Forjas (C), un artífice de la Ciudadela (C++), un ciudadano del Imperio (Java), un marinero del Puerto (PHP), un artesano de los Talleres (HTML), y los que vengan (JavaScript, TypeScript…).
- Cada héroe tiene **su retrato** (unas 5 caras por curso, que prepara el docente; solo cosmético), **su nombre** y **sus atributos**.
- El **inventario es de la compañía**: la poción que consiguió en Python se usa en C; la espada que forjó en C se la pasa al héroe de Python.
- **Solo los cursos base tienen héroe.** Los cursos y Sendas *accesorios* (SDL3, SFML, OpenGL, Qt, Arduino, Phaser, Laravel, Spring…) se abren según lo aprendido en los base y dan **misiones especiales**, no un héroe nuevo.

## 2. El Alfa: crear el primer héroe

El Alfa no es de ningún curso: es **el balcón de los portales**, donde llega todo el mundo. Lo recibe **Gheco**. Es un formulario de juego (no código, todavía no eligió lenguaje) y es inmediato:

1. **Elegir el retrato.**
2. **Ponerle nombre.**
3. **Repartir los puntos**: 24 puntos entre **Fuerza, Destreza, Inteligencia y Suerte**, cada uno entre 4 y 12, como el creador de personajes de MapleStory (con un botón de tirada al azar, opcional). **Queda para siempre**, salvo con un Pergamino del Reinicio.
4. **Elegir el equipo inicial** de un catálogo chico: una espada entre tres y hasta 5 pociones.

Lo hace cualquiera que se registre, aunque no haya pagado nada (como la Clase 0 de prueba): sirve para «chusmear» las razas. **Los alumnos que ya cursan lo tienen que completar** la primera vez que entren después del cambio, como una actualización de juego: la plataforma los lleva al Alfa y les marca en rojo lo que falta.

Cuando empieza un curso base nuevo, lo primero es **«Sumá un héroe a tu compañía»**: retrato, nombre y puntos de ese héroe.

## 3. La ficha la escribe el código (el camino 2)

- La primera misión de la Clase 0 de cada curso base es **«Tu ficha en {lenguaje}»**: el alumno escribe a su héroe en código (sus variables, con los valores que eligió) y el programa **imprime la ficha** en un formato fijo al final de la salida:
  ```
  FICHA nombre=Kira fuerza=12 destreza=4 inteligencia=4 suerte=4
  ```
- Las misiones siguientes **cambian la ficha con lo que programan**, con la misma línea: `FICHA +pocion_vida=1`, `FICHA +daño=7`, `FICHA victoria=slime`.
- Al **aprobar** el docente, la plataforma lee esa línea de la salida que el alumno ejecutó (en su navegador; el código nunca corre en el servidor), **la valida** (rangos, máximos, ítems que existen) y la aplica. Si no valida, no se aplica y se avisa por qué.
- Ejemplos de progresión: variables (la ficha) → operadores (el daño con su fuerza y su espada) → `if` (si cosechó hierbas, prepara una poción) → bucles (recorrer el bosque) → funciones (la primera pelea: `atacar()`, `defender()`, turnos, contra un slime).
- **Ninguna misión traba a otra**: el nombre no depende del equipo, el equipo no depende de la montura.

## 4. Las recorridas diarias (rutinas aprobadas que se repiten)

Algunas misiones enseñan a escribir una **rutina repetible**: recorrer el terreno, cosechar, pelear en una zona. **El docente la aprueba una vez** y desde entonces el alumno la puede **ejecutar todos los días**, sin volver a entregarla:

1. Toca *Salir a recorrer* en su terreno.
2. **El mundo tira los dados en el servidor** y le da al programa una entrada: las tiradas y la tabla de botín (`5 tiradas: 37 82 5 64 91`).
3. Su rutina aprobada (no se puede editar) corre **en su navegador** con esa entrada e imprime lo que encontró.
4. La plataforma ya sabe qué tenía que salir (las tiradas son suyas y la tabla es declarativa): **si coincide, le da el botín al instante**. Si no, no cae nada y le dice por qué.

- **Temporizador** como en Tanoth: unos minutos entre recorridas y un máximo por día. **Una montura** baja el tiempo.
- **El grimorio**: cada rutina aprobada queda en su *Grimorio de hechizos*, con su código, para releerla y ver cómo la hizo; y el historial de lo que le dio.
- **Crece con el curso**: con el tiempo la rutina queda corta; nuevas misiones enseñan rutinas mejores (más tiradas, una mochila con listas, combinar materiales con funciones, la tabla con diccionarios), que el alumno escribe, **envía a aprobar** y recién entonces puede repetir.
- Excepción a la regla «corrección automática fuera de alcance»: **solo la repetición de una rutina ya aprobada**. Las misiones del curso las sigue corrigiendo el docente.
- Las recorridas dan **ítems**, nunca monedas del curso ni aperturas de nodos.

## 5. Los artesanos (HTML y CSS)

Los héroes de los Talleres **no recorren: fabrican**. Sus misiones producen objetos que se ven: el **estandarte** de la compañía, la **portada del grimorio**, el **cartel** del terreno. Quedan en la ficha y en el perfil, dibujados en la misma caja aislada de la vista previa (D76).

## 6. Ítems, Pergamino del Reinicio y diamantes

- **Catálogo inicial** (inspirado en la base de Lineage 2 que tiene el docente, con nombres propios): armas (espada de principiante, daga, espada a dos manos, con sus atributos), pociones (vida chica: cura 50; maná chica: cura 20; antídoto), materiales de cosecha, monturas.
- **Pergamino del Reinicio**: permite repartir de nuevo los puntos de un héroe. Se consigue como premio de un jefe, de un encargo del Gremio o con diamantes.
- **Diamantes**: los da el Alfa y algunos logros; se gastan en cosas **cosméticas o de comodidad** (retratos, marcos, una montura, un pergamino), nunca en aprobaciones ni nodos.

## 7. Las incursiones entre lenguajes (más adelante)

Jefes especiales **fuera de los árboles** que solo se vencen juntando héroes de varios cursos, como en Shiba Wars: por ejemplo, una interfaz en HTML y CSS que lee con PHP de la base de datos y resuelve una pelea en JavaScript. Es un proyecto real de varios lenguajes.

## 8. Lo que hay que resolver

- **La ejecución del alumno**: las recorridas y «Tu ficha» corren en su navegador. Hoy solo Python; C, C++ y PHP necesitan habilitar para el alumno los ejecutores que ya usa el docente (con avisos claros). **Java** hoy solo corre en la compu del docente: sus recorridas quedan pendientes de una solución.
- **Los atributos en las peleas**: cómo pesan Fuerza, Destreza, Inteligencia y Suerte en las misiones de lucha (dentro del código del alumno) sin romper la economía.
- **Las imágenes**: los retratos por curso, los ítems y las monturas.

## 9. Etapas

1. **El Alfa y la compañía**: crear el héroe (retrato, nombre, puntos, equipo inicial), el inventario común y la ficha visible; obligatorio para todos.
2. **Las misiones que escriben la ficha** (`FICHA …`): «Tu ficha en {lenguaje}» y las siguientes, curso base por curso base, empezando por Python.
3. **Las recorridas**: el terreno, las tiradas del mundo, las rutinas aprobadas, el temporizador y el grimorio.
4. **Monturas, Pergamino del Reinicio, diamantes y los artesanos de HTML.**
5. **Las incursiones entre lenguajes.**
