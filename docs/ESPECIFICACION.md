# Especificación funcional — GhecoSoft-Code

> Fuente de verdad del **qué**. Reescrita el 2026-09-27 a partir de la conversación registrada en [GAMIFICACION.md](GAMIFICACION.md).
> El **cómo** está en [PLAN.md](PLAN.md). La forma del árbol, en [ARBOL-HABILIDADES.md](ARBOL-HABILIDADES.md). La marca y los colores, en [IDENTIDAD-VISUAL.md](IDENTIDAD-VISUAL.md).

## 1. Qué es

Plataforma de cursos de programación **gamificada** de un docente (Python, C, C++, Java, web…), para secundaria, terciario, universidad y particulares.

- No es "te activo el curso y ves todo". El alumno avanza por un **árbol de habilidades** que sigue la historia del curso.
- Cada parte del árbol se abre con **monedas**, y las monedas se ganan con **prácticas aprobadas** por el docente.
- Así el docente se asegura de que el alumno lea, intente y entregue.
- **Primer curso: Python.** Todo se diseña y se prueba con él.

## 2. Stack y hosting

| Pieza | Elección |
|---|---|
| Backend | Laravel (última estable) + Livewire (última estable), starter kit oficial de Livewire |
| Estilos | Tailwind CSS con Vite |
| Base | MariaDB |
| Editor | CodeMirror 6 (Vite) |
| Python en el navegador | Pyodide en un Web Worker con timeout de 5 s. **Nunca** se ejecuta código de alumnos en el servidor |
| Árbol | `force-graph` en modo radial (vista gráfica) + vista en lista |
| Tests | Pest |

**Hosting:** cPanel/CloudLinux (servidor `mate`).
- PHP 8.3, MariaDB y Node 20. Node se usa solo para compilar, por SSH.
- Sin workers (`QUEUE_CONNECTION=sync`) y **sin cron obligatorio**: todo vencimiento se calcula en cada request.
- Archivos privados (comprobantes, entregas, apuntes, autorizaciones) en `storage/app/private`, servidos solo por controladores con autorización.

## 3. Roles

- **admin**: el docente. Se crea con seeder y con `php artisan app:create-admin`.
- **alumno**: se registra solo.
- El login acepta **usuario o email** + contraseña.

## 4. Conceptos del juego

| Concepto | Qué es |
|---|---|
| **Curso** | Un lenguaje o tema. Es un **mundo/isla** en el mapa y tiene **su árbol** |
| **Nodo raíz** | Centro del árbol, con el **logo del curso**. Es una "clase 0" (instalar, presentarse, primer programa). Abrirlo = entrar al curso |
| **Rama** | Un bloque del curso (Fundamentos, Objetos…). Sale del raíz hacia afuera |
| **Nodo** | Un tema (Comentarios, Variables, Control…). Tiene explicación, ejemplo, recursos y **hojas** |
| **Hoja / práctica** | Un ejercicio del nodo. **Obligatoria** u **optativa** |
| **Nodo jefe (boss)** | Cierra cada rama: proyecto integrador con XP extra e insignia |
| **Extras** | Nodos optativos en un anillo exterior o en un árbol "Extras" |
| **Moneda del curso** | Solo sirve en su curso (ícono con el logo) |
| **Moneda comodín** | Se gana con optativas; abre extras de cualquier curso con raíz abierto y abono vigente. **Nunca abre un raíz** |
| **XP** | Nunca baja. Define nivel/rango, ranking y CV |
| **Abono** | Plazo **por curso** (30 días por defecto) para **avanzar** |

## 5. Reglas de negocio

1. **Registro:** la cuenta nueva arranca con **0 monedas**.
2. **Ingreso a un curso:**
   - el alumno pide inscripción (comprobante de pago jpg/png/pdf ≤ 5 MB, o "Contactar al profe" por WhatsApp);
   - el docente da la clase inicial y **aprueba**;
   - al aprobar: se acreditan las **monedas del curso** por el precio del raíz (10 por defecto, configurable por curso) y empieza el **abono** (30 días por defecto, configurable por curso);
   - **el alumno abre el raíz él mismo.**
3. **Abrir el nodo siguiente** exige **las dos cosas**:
   - todas las **obligatorias del nodo anterior aprobadas**;
   - pagar su **precio** en monedas del curso.

   Tener ahorro no permite saltearse prácticas.
4. **Extras:** se abren con **comodines** (o con el tipo que diga el nodo). Solo en cursos con raíz abierto y abono vigente.
5. **Recompensas:** cada práctica aprobada paga un **monto fijo** de monedas (del curso si es obligatoria, comodín si es optativa) y de XP.
   - No hay notas: solo **Aprobada** o **Rehacer**.
   - Intentos ilimitados. Reentregar o entregar tarde **paga igual**.
   - Completar un nodo y vencer un jefe dan XP extra; el jefe da además una insignia.
6. **Prácticas sin entrega** (instalar, leer): se marcan como completadas; pagan solo si el docente les puso recompensa (por defecto, 0).
   - **Todas** las prácticas tienen "Marcar como completada", que es la marca personal del alumno.
7. **Abono:**
   - **Vigente:** puede abrir nodos y entregar prácticas.
   - **Vencido:** no abre **ni entrega** nada de ese curso, pero **sigue viendo y repasando** todo lo que abrió, para siempre.
   - **Renovar** (mismo circuito de pago y aprobación) solo extiende el plazo; no da monedas.
   - Se guardan los **días de cursada**.
8. **Avance libre:** no hay liberación por fecha ni tope por comisión.
9. **Comisiones:** son opcionales, un **grupo** (horario, modalidad, filtro de la bandeja). Las clases suelen ser individuales.
10. **Ajustes manuales:** el docente puede dar o quitar monedas o XP con **motivo obligatorio**. Queda en el libro de movimientos.
11. **Toda moneda y todo XP** se registra como **movimiento**. El saldo es la suma de los movimientos.
12. **Menores de 18:** el alumno sube una **nota de autorización** firmada (docente, alumno y adulto responsable). Hasta que el docente la aprueba, no puede tener CV público ni aparecer en el ranking global.
13. **CV y ranking:**
    - **Top ten por curso**, visible entre compañeros; cada uno elige si figura con su nombre o con un apodo.
    - **CV público** en su propio link (`/cv/nombre-apellido-xxxxxx`, nunca el usuario de login; el alumno puede generar uno nuevo y, si quiere, pedir un código de 6 cifras para verlo), solo si el alumno tilda "Compartir mi CV públicamente" (apagado por defecto; lo puede apagar cuando quiera). Se descarga en PDF.
    - El CV **nunca** muestra código ni comentarios.
14. **DNI:** opcional, lo carga el alumno en *Mi cuenta*.
15. **Seguridad:** un alumno **nunca** ve nodos que no abrió, cursos cuyo raíz no abrió ni entregas de otros. Todo cubierto por Policies y tests Pest.

## 6. Pantallas del alumno

Estilo: [IDENTIDAD-VISUAL.md](IDENTIDAD-VISUAL.md) (oscuro "DevLevel Obsidian", grilla de puntos, paneles de vidrio). Responsive.

1. **Registro / Login:**
   - registro con nombre, apellido, usuario, email y contraseña (mín. 8, mayúscula, minúscula y número, con medidor de seguridad);
   - login con usuario o email.
2. **Mapa de mundos** (inicio): cada curso es una isla con su progreso (`x/y`) y su estado:
   - **abierto:** botón "Entrar";
   - **abono vencido:** "Renovar";
   - **sin abrir:** "Ver curso".

   Arriba: saldo de monedas por tipo, nivel y XP.
3. **Detalle de curso** (sin abrir): descripción, comisiones abiertas, "Solicitar inscripción" (con comprobante) y "Contactar al profe". Muestra el estado de la solicitud pendiente. Con monedas del curso, botón **"Abrir el curso"**.
4. **Árbol del curso**, con dos vistas:
   - **gráfica** (radial, logo al centro, estados con color, animaciones);
   - **lista por rama**, por defecto en celular.

   Tiene panel de referencias y filtros. Al tocar un nodo "listo para abrir", muestra el precio y el botón **Abrir**.
5. **Nodo:**
   - explicación (markdown);
   - ejemplo con "Copiar" y **"Ejecutar"** si es Python, con la salida esperada;
   - recursos;
   - **hojas**, cada una con su consigna, editor CodeMirror con "Ejecutar" (y entrada estándar), subida de archivo, **Entregar**, historial y **hilo de comentarios**;
   - navegación al nodo anterior y al siguiente.
6. **Mi cuenta:**
   - datos personales, usuario, DNI opcional, fecha de nacimiento;
   - contraseña y avatar;
   - **privacidad** (CV público, nombre o apodo en el ranking);
   - **autorización de menor**;
   - **movimientos** de monedas y XP.
7. **Ranking** del curso y **CV** propio (vista previa del público).

## 7. Pantallas del admin

1. **Inicio:** solicitudes pendientes, entregas por corregir, alumnos con abono vigente, autorizaciones pendientes.
2. **Solicitudes:** filtro, vista del comprobante, **Aprobar** (acredita monedas y abre el abono, o renueva) o **Rechazar** con nota.
3. **Alumnos:** buscador y detalle con cursos, abonos, saldos, movimientos, **ajuste manual**, entregas y autorización.
4. **Cursos:**
   - datos del curso, precio del raíz y días de abono;
   - **editor del árbol**: ramas, nodos (raíz, tema, jefe, extra) y hojas, con **"+ Nueva hoja"**, orden por arrastre, precios y recompensas;
   - duplicar nodo o curso.
5. **Bandeja de entregas:** "Sin corregir" por defecto, ver y ejecutar código, **Aprobar / Rehacer** con comentario, "siguiente sin corregir".
6. **Diccionario narrativo:** nombres, género, íconos e historia por clave, general o por curso ([GAMIFICACION.md](GAMIFICACION.md) § 8).
7. **Insignias y niveles.**
8. **Configuración:** WhatsApp, mensaje prearmado, nombre y logo.

## 8. Notificaciones (base de datos + mail si hay SMTP)

- **Admin:** nueva solicitud, nueva entrega, nueva autorización.
- **Alumno:** solicitud aprobada o rechazada, entrega aprobada o rehacer (con las monedas ganadas), comentario nuevo, abono por vencer (aviso al entrar) y vencido.

## 9. Fuera de alcance (por ahora)

- Pagos online, certificados, foros, cuestionarios y corrección automáticos.
- Ejecución de C, C++ o Java: se deja la interfaz `CodeRunner` para un servicio externo.
- Cuentas de observador y la conexión con La Rioja Aprende.
- Tienda de cosméticos, pistas y eventos (se agregan después, con comodines).

## 10. Forma de trabajo

- Por fases ([PLAN.md](PLAN.md) § 9), **frenando al final de cada una** para que el docente pruebe.
- Commits chicos.
- Interfaz en **español rioplatense**, código en inglés.
