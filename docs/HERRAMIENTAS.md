# Herramientas (D120)

Lugares para practicar lo que se quiera sin instalar nada. Es práctica personal: no cuenta para el curso y no guarda nada en el servidor.

## Qué hay

| En el menú | Cómo corre | Se habilita con |
|---|---|---|
| Practicar Python, C, C++, C#, PHP, HTML y CSS | En el navegador, con los mismos ejecutores de los cursos | El abono vigente de un curso de ese lenguaje |
| Practicar SQL | SQLite en el navegador, con la base vacía en cada ejecución | El abono vigente de un curso de PHP o de Java (los que usan SQL) |
| Practicar Java | En la compu del alumno, con el Ejecutor de Java abierto | El abono vigente de un curso de Java |
| La caja de la Feria (JavaScript) y Gólem 8086 | En el navegador, como antes | Sus reglas de siempre (`useJsTool`, `useAsmTool`) |
| Calculadora y Tabla ASCII | En el navegador, sin guardar nada en el servidor | Todos los que iniciaron sesión, con o sin abono |
| Ejecutor de Java | Es la página para instalarlo | Quien cursa o pidió un curso de Java, aunque el abono no esté vigente (D85) |

El administrador y el docente las tienen todas. Se calcula en cada request; con el abono vencido se cierra la herramienta y sale del menú. La Clase 0 no las habilita.

## Qué hace cada página

- **Tarjeta del menú:** `<x-tools-card>`, con lo que da `App\Support\PracticeTools::menu()`. Si no hay ninguna, no se muestra.
- **Editor:** `<x-code-runner>` con `keep` y `autocomplete`. Solo en las Herramientas: en las clases y las micro-misiones no hay sugerencias, porque ahí se aprende a escribir las palabras.
- **Lo escrito:** queda en el `localStorage` de ese navegador, por usuario y por lenguaje. «Restaurar» vuelve al ejemplo.
- **Sugerencias:** `resources/js/editor/completions.js`. Son palabras del lenguaje, estructuras que se completan con Tab y las palabras que ya están en el programa. **No entienden el código:** no saben los métodos de una variable ni marcan errores.
- **Ventanas flotantes:** `resources/js/tool-window.js`. Se mueven, cambian de tamaño, se achican y quedan por encima de la página (tocar una la trae adelante). Siguen corriendo mientras se navega, porque viven fuera del `<body>` que reemplaza `wire:navigate`, y se recuerdan al recargar. Puede haber una por herramienta a la vez. En el celular ocupan toda la pantalla, no se arrastran y las achicadas se apilan abajo.

## Calculadora y Tabla ASCII

Son de consulta y para todos (`PracticeTools::utilities()`). En el menú, un clic abre su ventana o trae la que estaba; el **+** abre otra, hasta 3 de cada una (`limit`), por ejemplo para llevar sumas parciales. Solo se cierran con la cruz: no tienen «Abrir como página» y Esc no las cierra. Cada ventana recuerda lo suyo en el navegador (`tool-instance:usuario:ventana`) y lo olvida al cerrarse. También se abren como página, con Ctrl + clic o desde el enlace directo.

- **Calculadora** (`resources/js/tools/calculator.js`, la cuenta en `calculator-core.js`): analizador propio, nunca `eval`. Simple: `+ − × ÷ mod % √ x² π`, paréntesis y lo hecho arriba. Programador: enteros exactos de 8 a 64 bits; escribe en HEX, DEC, OCT o BIN y muestra las cuatro, con signo y el carácter; bits que se tocan; `AND OR XOR NOT << >>` (escriben su símbolo, el de C) y complemento a dos. La cuenta se hace sin tope y se recorta al final, como un registro, y avisa si no entró.
- **Tabla** (`resources/js/tools/ascii.js`, los datos en `ascii-data.js`): ASCII de 0 a 127, Windows 850, Linux y Unicode, y DOS 437. Copia el símbolo, DEC, HEX, OCT, BIN, código, HTML o UTF-8. Los de control se copian como código (`\n`) o en hexa (`0x1B`). Busca en todas por carácter, número, `0x41`, `41h`, `U+00F1` o nombre. Unicode muestra los grupos útiles para programar; otro carácter se encuentra por su código o pegándolo.

**Qué tabla usar.** Depende del lenguaje además del sistema; la guía está en cada pestaña. Probado: Python, Java, JavaScript, C#, PHP y C en Linux con sus programas reales; Python, C, C++, C#, PHP, JavaScript y el Gólem en los ejecutores de la plataforma (el Gólem usa la 437 y C y C++ se comportan como en Linux, con UTF-8). **Falta probar la 850 en una consola real de Windows.**

Pruebas: `node scripts/herramientas/probar.mjs` (la cuenta y las tablas) y `node scripts/herramientas/probar-ventanas.mjs` (las ventanas en Chrome, con la plataforma local en el puerto 8123).

## Sumar un lenguaje

Si el lenguaje ya corre en `<x-code-runner>`, alcanza con agregarlo a `PracticeTools::TOOLS` (con su ejemplo, sus avisos y los cursos que lo habilitan) y a `LISTS` en `completions.js`.

## Para más adelante

- **Sugerencias que entiendan el código** (por ejemplo, los métodos de una variable). Para C# se podría usar Roslyn, que ya corre en el navegador; para Python, Jedi con Pyodide. Cada lenguaje es un trabajo aparte.
- **Varios archivos por programa** y bajar el programa como archivo. Hoy se copia con «Copiar».
