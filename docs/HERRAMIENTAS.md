# Herramientas (D120)

Lugares para practicar lo que se quiera sin instalar nada. Es práctica personal: no cuenta para el curso y no guarda nada en el servidor.

## Qué hay

| En el menú | Cómo corre | Se habilita con |
|---|---|---|
| Practicar Python, C, C++, C#, PHP, HTML y CSS | En el navegador, con los mismos ejecutores de los cursos | El abono vigente de un curso de ese lenguaje |
| Practicar SQL | SQLite en el navegador, con la base vacía en cada ejecución | El abono vigente de un curso de PHP o de Java (los que usan SQL) |
| Practicar Java | En la compu del alumno, con el Ejecutor de Java abierto | El abono vigente de un curso de Java |
| La caja de la Feria (JavaScript) y Gólem 8086 | En el navegador, como antes | Sus reglas de siempre (`useJsTool`, `useAsmTool`) |
| Ejecutor de Java | Es la página para instalarlo | Quien cursa o pidió un curso de Java, aunque el abono no esté vigente (D85) |

El administrador y el docente las tienen todas. Se calcula en cada request; con el abono vencido se cierra la herramienta y sale del menú. La Clase 0 no las habilita.

## Qué hace cada página

- **Tarjeta del menú:** `<x-tools-card>`, con lo que da `App\Support\PracticeTools::menu()`. Si no hay ninguna, no se muestra.
- **Editor:** `<x-code-runner>` con `keep` y `autocomplete`. Solo en las Herramientas: en las clases y las micro-misiones no hay sugerencias, porque ahí se aprende a escribir las palabras.
- **Lo escrito:** queda en el `localStorage` de ese navegador, por usuario y por lenguaje. «Restaurar» vuelve al ejemplo.
- **Sugerencias:** `resources/js/editor/completions.js`. Son palabras del lenguaje, estructuras que se completan con Tab y las palabras que ya están en el programa. **No entienden el código:** no saben los métodos de una variable ni marcan errores.
- **Ventana flotante:** `resources/js/tool-window.js`. Se mueve, cambia de tamaño, se achica y se abre como página. Sigue corriendo mientras se navega, porque vive fuera del `<body>` que reemplaza `wire:navigate`, y se recuerda al recargar. Hay una sola: abrir otra herramienta reemplaza la que estaba. En el celular ocupa toda la pantalla y no se arrastra.

## Sumar un lenguaje

Si el lenguaje ya corre en `<x-code-runner>`, alcanza con agregarlo a `PracticeTools::TOOLS` (con su ejemplo, sus avisos y los cursos que lo habilitan) y a `LISTS` en `completions.js`.

## Para más adelante

- **Sugerencias que entiendan el código** (por ejemplo, los métodos de una variable). Para C# se podría usar Roslyn, que ya corre en el navegador; para Python, Jedi con Pyodide. Cada lenguaje es un trabajo aparte.
- **Varios archivos por programa** y bajar el programa como archivo. Hoy se copia con «Copiar».
