# Ideas para mejorar la gamificación (revisar antes de subir a producción)

Análisis del 2026-09-28, conversado con el docente. Es una **lista para decidir**, no un plan cerrado: antes de codear cualquiera de estas ideas, se elige, se diseña en un `.md` y se anota la decisión en [PLAN.md](PLAN.md).

Referencia: *larioja-aprende* (API + web, para inicial, primaria y secundaria) tiene duelos, un laberinto programable, práctica libre, insignias automáticas por criterios y rankings por aula. Esta plataforma es más dinámica (árbol, economía, historia, código real), pero le falta la sensación de juego inmediato que aquella sí tiene.

## Lo que ya funciona bien (no perderlo)

- **El árbol como eje.** Abrir nodos con monedas propias da la sensación de conquista, y la espiral (D47) lo hace ver como un mapa de juego.
- **La historia integrada.** Héroe con nombre, mentor, criaturas por tipo de error y jefes con insignia, todo desde el diccionario. Sirve para cualquier curso (D39).
- **Las Sendas.** Dejan elegir qué estudiar después del tronco.
- **Una economía sólida.** Libro de movimientos único, verificado por el súper test ([SIMULACION.md](SIMULACION.md)).
- **Un CV que sirve afuera** (con link propio y código opcional, D51).
- **La devolución humana del docente**, que vale más que un «incorrecto» automático.

## Problemas detectados

1. **Entregar y esperar un día corta el ritmo.** El navegador ya sabe si la salida coincide («✓ Coincide») y hoy eso no da nada.
2. **Corregir no escala.** El súper test con 5 alumnos generó unas 650 correcciones; con 30 alumnos serían unas 4000 por curso. El docente queda como cuello de botella.
3. **Las monedas solo sirven para abrir nodos.** Al terminar, los alumnos simulados quedaron con 72 escamas y hasta 29 comodines sin nada en qué gastarlos.
4. **No hay retos cortos.** Todas las misiones son programas completos, y la Prueba del sello, sin puntaje, no se siente como un juego.
5. **El ranking premia al que tiene más tiempo.** Al que va último lo desmotiva.
6. **Casi no hay juego entre alumnos.** No hay duelos, cooperación ni metas de la comisión.
7. **Solo dan insignia los jefes.** No hay logros por hábitos (primera entrega sin errores, días seguidos, ayudar a un compañero).

## Abanico de mejoras

### A. Respuesta inmediata

| Idea | Qué es | Impacto | Esfuerzo |
|---|---|---|---|
| Comprobación instantánea | Al coincidir la salida, el alumno gana al instante una parte (por ejemplo, la XP); el docente confirma las monedas después | Muy alto | Medio |
| Pruebas ocultas | Varias entradas por misión, ejecutadas en el navegador («3 de 4 pruebas pasadas») | Muy alto | Medio |
| Autoaprobación opcional | El docente elige, práctica por práctica, cuáles se aprueban solas; revisa a mano solo los jefes y las de diseño | Muy alto para el docente | Bajo, sobre lo anterior |
| Jefe con barra de vida | Cada prueba superada es un golpe al jefe, con la barra bajando en pantalla | Alto | Medio |

⚠️ Lo que corre en el navegador se puede trampear desde las herramientas del navegador. La autoaprobación va solo en misiones que pagan poco; los jefes y los proyectos los revisa siempre el docente. Además, hoy «corrección automática» figura **fuera de alcance** en CLAUDE.md: si se hace, primero hay que cambiar esa decisión.

### B. Algo en qué gastar las monedas

| Idea | Qué es |
|---|---|
| Pistas pagas | La primera es gratis; la segunda cuesta 2 monedas; «ver un fragmento de la solución» cuesta más |
| Cosméticos | Aspectos del héroe, marcos del CV, títulos («Domador de la Hidra»), colores del geco |
| Tienda de comodines | Un «perdón» que renueva un día de racha, o doble XP en la próxima misión |

Todo gasto pasa por el `Ledger`, como cualquier movimiento.

### C. Retos cortos (ideas de larioja-aprende adaptadas)

| Idea | Qué es |
|---|---|
| «¿Qué imprime?» | Ver un código y elegir la salida. Entrena la lectura de código |
| Ordenar líneas | Las líneas de un programa mezcladas, para ordenarlas |
| Cazar el bug | Un programa con un error, para encontrar la línea |
| Duelos | Estos retos, cronometrados, contra un compañero o un bot. Se juegan por turnos, no hace falta que sea en vivo |
| Prueba del sello con puntaje | La misma autoevaluación, como mini-juego que da XP |

### D. Ritmo y comunidad

| Idea | Qué es |
|---|---|
| Liga semanal | Todos arrancan de cero cada semana, así el que va último igual puede ganar. Se calcula en cada pedido, sin cron |
| Desafío de la semana | Un reto con su propio mini-ranking |
| Logros automáticos | Insignias por hábitos, calculadas en cada pedido (como los criterios de larioja-aprende) |
| Meta de la comisión | «Entre todos, 200 misiones esta semana» abre un cofre para todos. Aprovecha `companion.guild` |
| Revisión entre pares | Comentar el código de otro da comodines |
| Rachas suaves | Días seguidos con recompensa, con comodines para no perderla. Sin castigos |

### E. Más «juego»

- **Tortuga o canvas en Pyodide:** programar dibujos o mover un personaje en una grilla, como el laberinto de larioja-aprende. Ideal para la Clase 0.
- **Taller libre:** editor para probar cosas, guardar fragmentos y compartirlos.
- **Eventos temporales:** «Semana de la Hidra: doble XP en jefes». Se calculan por fecha, sin cron.

### F. Para el docente

- **Tablero de «dónde se traban»:** qué misiones reciben más pedidos de rehacer, que suelen ser consignas poco claras.
- **Aviso de «alumno en riesgo»:** hace días que no entra, o se le vence el abono.
- **Comentarios guardados:** respuestas frecuentes para corregir con un clic.

## Recomendación (orden sugerido)

1. **Comprobación instantánea con pruebas ocultas y autoaprobación opcional (A).** Resuelve a la vez el ritmo del alumno y la carga del docente.
2. **Pistas pagas y cosméticos (B).** Le da sentido a la economía de punta a punta, y cuesta poco.
3. **Logros automáticos y liga semanal (D).** Recupera lo mejor de larioja-aprende y mantiene enganchado al que va atrás.
4. **Retos cortos y duelos (C).** Lo más «juego», para días con poco tiempo.

## Antes de subir a producción

- [ ] Decidir cuáles de estas ideas entran **antes** del lanzamiento y cuáles quedan para después.
- [ ] Si entra la corrección automática (A), cambiar «fuera de alcance» en CLAUDE.md y anotar la decisión en PLAN.
- [ ] Cada idea elegida lleva su diseño en `.md`, sus tests y una nueva corrida del súper test (`app:simulate-course`), para ver que la economía sigue cerrando.
