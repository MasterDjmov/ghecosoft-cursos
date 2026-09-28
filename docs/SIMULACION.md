# Súper test: simular un curso completo

Antes de abrir un curso a los alumnos (y cada vez que se carga uno nuevo), se corre una **simulación**:

- 5 alumnos se inscriben y el docente los aprueba (con sus monedas iniciales).
- Juegan día por día hasta abrir todo el árbol: entregan, se equivocan, rehacen, renuevan el abono y juntan comodines para las Sendas.
- Mientras tanto, el docente corrige: aprueba o pide rehacer según el código funcione.

Sirve para ver si el sistema falla en un recorrido real (economía, aperturas, jefes, insignias, fin del curso, abonos) y para ver cómo queda un alumno al final (árbol, CV, ranking, movimientos).

```bash
php artisan app:simulate-course python            # primera vez
php artisan app:simulate-course python --reset    # borra la simulación anterior y la repite
php artisan app:simulate-course c --days=90       # otro curso, con más días
```

**Solo en la base local.** El comando se niega en producción. Antes de correrlo conviene una copia de la base, porque escribe de verdad: usuarios, entregas, movimientos, avisos y fotos del ranking.

## Qué hace

La cursada arranca `--days` días atrás (60 por defecto) y avanza hasta hoy o hasta que terminan todos. El reloj se mueve de verdad, así que fechas, abonos de 30 días, renovaciones y tendencias del ranking quedan como en la vida real. Con la misma `--seed` sale siempre la misma historia.

| Alumno | Usuario / clave | Cómo juega |
|---|---|---|
| Valentina Ríos | `valen` / `Valen2026` | Casi no se equivoca y hace **todas** las optativas. Es la que se mira para ver el recorrido completo |
| Tomás Herrera | `tomi` / `Tomi2026` | Rápido y desprolijo (25 % de errores). Se inscribe por WhatsApp |
| Camila Sosa | `cami` / `Cami2026` | Constante, hace bastantes optativas |
| Mateo Quiroga | `mateo` / `Mateo2026` | Se equivoca mucho, falta seguido y tarda días en renovar el abono |
| Lucía Fernández | `lu` / `Lucia2026` | La crea el docente desde el admin (clave provisoria, ya inscripta) |

Los alumnos simulados usan emails `@simulacion.test`. Así `--reset` los encuentra y los borra.

**Cada día:**

1. **A la mañana, el docente** aprueba las inscripciones y renovaciones pendientes y corrige todas las entregas que llegaron:
   - Con **Python**, ejecuta el código con `python3` y la *Entrada de ejemplo*, igual que la consola del navegador. Si termina con error o la salida no coincide con la *Salida esperada*, pide rehacer con un comentario que dice qué línea no coincide o qué error apareció.
   - Con **C y C++**, compila con `gcc`/`g++` (`-Wall -Wextra`, como en la compu del alumno) y ejecuta igual: si no compila, se corta o la salida no coincide, pide rehacer con el primer error del compilador.
   - Con **otros lenguajes**, compara con la *Solución de referencia*.
   - Los **archivos** los revisa por su contenido.
2. **A la tarde, cada alumno** (algunos días no entra) hace varias acciones, en este orden:
   1. Entrega lo pendiente de los nodos abiertos: primero las obligatorias y después las optativas que "le gustan".
   2. Si no tiene nada para entregar, abre el siguiente nodo que puede pagar.
   3. Si le faltan comodines para una Senda, vuelve a hacer optativas.
   4. Con el abono vencido, pide la renovación.

   A veces se equivoca a propósito: un nombre mal escrito (`NameError`, o en C una variable sin declarar que no compila) o un `print`/`printf` de más. En el segundo intento se equivoca menos, y a veces le contesta al profe en el hilo de la entrega.
3. **A la noche** se guarda la foto diaria del ranking.

Todo pasa por los **mismos servicios que las pantallas**:

- `CreateNewUser` y `StudentAccounts` para las cuentas;
- `EnrollmentRequester` y `EnrollmentApprover` para inscripciones y renovaciones;
- `NodeUnlocker` para abrir nodos;
- `PracticeSubmitter` y `SubmissionReviewer` para entregar y corregir;
- `Ranking` para la foto diaria.

Si alguno falla o frena algo que debería poder hacerse, queda anotado.

## Qué informa

- **Una tabla por alumno:** nodos abiertos, prácticas aprobadas, entregas, pedidos de rehacer, renovaciones, XP, saldo de monedas y de comodines, si terminó el curso y en cuántos días. Si quedó **trabado**, dice en qué nodo y por qué.
- **Controles del sistema** (✓ / ✗):
  - Ningún saldo queda negativo.
  - Ninguna práctica se paga dos veces, aunque se rehaga.
  - La XP de cada alumno es la suma de su libro de movimientos.
  - Cada nodo abierto se pagó.
  - Nadie tiene un nodo abierto sin haber completado el anterior.
  - No hay prácticas aprobadas en nodos cerrados.
  - Cada jefe vencido dio su insignia.
  - Quien completó el tronco tiene el curso terminado (para el CV).
  - No hubo errores inesperados.
- **Errores inesperados:** cada excepción o freno del sistema, con fecha simulada, qué se intentaba hacer y el archivo y la línea.
- El usuario y la clave para entrar a ver el recorrido completo.

Si hay algún ✗ o algún error, el comando termina con código de error.

## Para un curso nuevo

1. Importarlo (`php artisan app:import-course cursos/<curso>/ --apply`) y publicarlo.
2. Correr `php artisan app:simulate-course <slug>`. Si ya hay alumnos simulados de otro curso, **se reutilizan**: se inscriben también en este (así se prueban cursos en paralelo y los movimientos por curso). `--reset` borra a todos los simulados y empieza de cero.
3. Revisar:
   - que nadie quede **trabado** (si pasa, suele ser la economía: las obligatorias no alcanzan para el próximo nodo, o faltan optativas para los comodines de una Senda);
   - que todos los controles den ✓;
   - que en Python los pedidos de rehacer sean solo los errores a propósito. Si una práctica correcta sale rechazada, su *Salida esperada* o su *Entrada de ejemplo* está mal.
4. Entrar como `valen` y recorrer el árbol, el CV, los movimientos y el ranking.
5. Si hacen falta cambios, corregir los `.md` del curso, reimportar y repetir.
