# Catálogo de temas del universo

Los temas con los que se marcan los nodos de todos los cursos (`temas:` lo que el nodo **enseña**, `usa:` lo que da por sabido; ver `docs/FORMATO-CURSO.md` § 5). Es una lista **ideal**: incluye temas que todavía ningún curso enseña, para que el mapa del universo (*Admin → Universo*) muestre qué falta.

Reglas:
- Cada familia empieza con `## clave · Título` y su `alcance`:
  - **lenguaje**: cada lenguaje lo enseña a su manera (bucles en C y en Python no son contenido repetido). Sirve para ver qué le falta a cada curso.
  - **compartido**: el contenido se puede reusar entre cursos (HTML, SQL, algoritmos…). Si dos cursos lo enseñan, es contenido repetido; y un curso nuevo de esa familia se arma con lo que ya existe.
- Cada tema: `- familia.clave · Título · qué abarca`. Las claves no se cambian (los cursos las usan); se agregan temas nuevos donde corresponda.
- Dentro de cada familia, los temas van **de lo básico a lo avanzado**: es el orden en que se arma un curso nuevo.

## prog · Fundamentos de programación
alcance: lenguaje

- prog.entorno · Hola mundo y el entorno · instalar, escribir, compilar o ejecutar el primer programa, leer los errores
- prog.salida · Mostrar datos · imprimir texto y valores con formato
- prog.entrada · Leer datos · leer del teclado, convertir lo leído
- prog.variables · Variables, tipos y conversiones · tipos básicos, constantes, conversiones
- prog.operadores · Operadores y expresiones · aritméticos, lógicos, de comparación, precedencia
- prog.bits · Operadores de bits · binario, hexadecimal, máscaras y banderas
- prog.cadenas · Textos · buscar, cortar, reemplazar, partir, formatear
- prog.condicionales · Decisiones · if, switch, match, ternario
- prog.bucles · Bucles · while, for, do, break, continue, acumuladores
- prog.funciones · Funciones · parámetros, retorno, sobrecarga, valores por defecto
- prog.alcance · Alcance y vida de las variables · local, global, static
- prog.recursion · Recursión · casos base, recursión sobre estructuras
- prog.referencias · Valor, referencia y mutabilidad · alias, copias, referencias
- prog.enums · Enumeraciones · listas cerradas de valores
- prog.matematica-azar · Matemática y azar · biblioteca matemática, números al azar con semilla
- prog.fechas · Fechas y horas · crear, formatear y calcular fechas
- prog.modulos · Varios archivos, módulos y paquetes · separar el programa, importar, espacios de nombres
- prog.argumentos · Argumentos de la línea de comandos · argv, opciones, mensaje de uso
- prog.menu · Programas de consola con menú · bucle de menú, estado del programa, salida prolija

## col · Colecciones
alcance: lenguaje

- col.arrays · Arrays · tamaño fijo, recorrer, pasar a funciones
- col.matrices · Matrices · filas y columnas, grillas y mapas
- col.listas · Listas que crecen · vector, ArrayList, list, array dinámico
- col.registros · Registros y tuplas · struct, tupla, agrupar datos
- col.mapas · Diccionarios · clave-valor, contar, anidar
- col.conjuntos · Conjuntos · sin repetidos, operaciones de conjuntos
- col.pilas-colas · Pilas, colas y colas con prioridad · stack, queue, deque, heap

## poo · Objetos
alcance: lenguaje

- poo.clases · Clases y objetos · atributos, métodos, crear objetos
- poo.constructores · Constructores y destructores · estado válido desde el inicio
- poo.encapsulamiento · Encapsulamiento · privados, invariantes, getters que validan
- poo.static · Miembros de clase · static, constantes de clase
- poo.herencia · Herencia · extends, super, redefinir métodos
- poo.polimorfismo · Polimorfismo · ligadura dinámica, colecciones de distintos tipos
- poo.abstractas · Clases abstractas · métodos abstractos, plantillas de comportamiento
- poo.interfaces · Interfaces · contratos, implementar varias
- poo.composicion · Composición y delegación · "tiene un", preferir composición
- poo.operadores · Operadores y métodos especiales · sobrecarga de operadores, __str__, toString
- poo.records · Datos inmutables · record, dataclass, readonly, jerarquías cerradas
- poo.genericos · Genéricos y plantillas · código que sirve para cualquier tipo

## mem · Memoria
alcance: lenguaje

- mem.punteros · Punteros · direcciones, &, *, NULL, punteros y arrays
- mem.dinamica · Memoria dinámica · pila y montón, malloc/free, new/delete
- mem.punteros-funcion · Punteros a función · callbacks, tablas de acciones
- mem.raii · RAII · adquirir en el constructor, soltar en el destructor
- mem.smart-pointers · Punteros inteligentes · unique_ptr, shared_ptr, weak_ptr
- mem.movimiento · Copias y movimientos · constructor de copia y de movimiento

## err · Errores y validación
alcance: lenguaje

- err.validacion · Validar la entrada · volver a preguntar, no cortar el programa
- err.excepciones · Excepciones · lanzar, atrapar, excepciones propias, limpiar recursos
- err.opcionales · Valores que pueden faltar · optional, null seguro

## func · Programación funcional
alcance: lenguaje

- func.lambdas · Lambdas · funciones sin nombre, capturas
- func.orden-superior · Funciones como valores · map, filter, reduce, callbacks, functores
- func.closures · Closures · funciones que recuerdan su entorno
- func.iteradores · Iteradores y generadores · iterar a mano, yield, perezosos
- func.streams · Streams y ranges · cadenas de operaciones sobre colecciones
- func.decoradores · Decoradores · envolver funciones

## arch · Archivos
alcance: lenguaje

- arch.texto · Archivos de texto · abrir, leer, escribir, línea por línea
- arch.csv · CSV · leer y escribir planillas
- arch.json · JSON · guardar y cargar datos estructurados
- arch.binarios · Archivos binarios · registros, acceso directo
- arch.config · Configuración · .properties, .env, .ini
- arch.rutas · Rutas y carpetas · crear, listar, borrar

## conc · Concurrencia
alcance: lenguaje

- conc.hilos · Hilos y tareas · crear tareas, repartir trabajo
- conc.sincronizacion · Sincronización · datos compartidos, candados, atómicos
- conc.async · Asincronía · async/await, corrutinas
- conc.ui-hilo · Tareas largas en una interfaz · no congelar la ventana

## cal · Calidad y herramientas
alcance: lenguaje

- cal.depuracion · Depuración · depurador, sanitizadores, método para buscar errores
- cal.pruebas · Pruebas automáticas · assert, frameworks de pruebas, casos límite
- cal.logging · Logs y manejo de errores de la aplicación · registrar, niveles
- cal.tipos · Tipos estrictos · anotaciones de tipos, strict_types, chequeo estático
- cal.documentacion · Documentación del código · Javadoc, docstrings
- cal.rendimiento · Medir y optimizar · medir tiempos, perfilar
- cal.build · Compilar y dependencias · Makefile, CMake, Maven, Composer, pip

## herr · Herramientas del programador
alcance: compartido

- herr.compilacion · Compilar y enlazar · qué hace el compilador, advertencias, enlazador
- herr.terminal · La terminal · comandos básicos, rutas, redirecciones
- herr.git · Git · commits, ramas, GitHub

## diseno · Diseño de software
alcance: compartido

- diseno.uml · Diagramas UML · clases, relaciones, secuencia
- diseno.maquina-estados · Máquinas de estados · estados, transiciones
- diseno.capas · Capas y MVC · modelo, vista, controlador, DAO, repositorios
- diseno.inyeccion · Inyección de dependencias · recibir las piezas, contenedor
- diseno.patrones · Patrones de diseño · estrategia, fábrica, observador

## alg · Algoritmos y estructuras de datos
alcance: compartido

- alg.complejidad · Complejidad · contar operaciones, O grande
- alg.busqueda · Búsqueda · lineal, binaria
- alg.ordenamiento · Ordenamiento · burbuja, inserción, quicksort, ordenar con criterio
- alg.listas-enlazadas · Listas enlazadas · nodos, insertar, quitar
- alg.arboles · Árboles · binarios de búsqueda, recorridos
- alg.hash · Tablas hash · funciones hash, colisiones
- alg.grafos · Grafos y caminos · BFS, DFS, Dijkstra, A*
- alg.dinamica · Programación dinámica · memoización, tablas
- alg.ia-juegos · IA para juegos · minimax, poda alfa-beta, aprendizaje por refuerzo

## sql · Bases de datos
alcance: compartido

- sql.modelo · Tablas y restricciones · tipos, clave primaria, foránea, NOT NULL, UNIQUE
- sql.abm · Altas, bajas y modificaciones · INSERT, UPDATE, DELETE
- sql.consultas · Consultas · SELECT, WHERE, ORDER BY, agregados, GROUP BY
- sql.joins · Relaciones y JOIN · uno a muchos, muchos a muchos, los JOIN
- sql.normalizacion · Normalización · no repetir datos, formas normales
- sql.indices · Índices · cuándo y cómo indexar
- sql.transacciones · Transacciones · ACID, commit, rollback, concurrencia
- sql.avanzado · Vistas, funciones, procedimientos y triggers · lógica en la base
- sql.desde-codigo · SQL desde un programa · conectar, consultas preparadas (PDO, JDBC, sqlite3)
- sql.inyeccion · Inyección SQL · el ataque y cómo evitarlo
- sql.orm · ORM · Eloquent, JPA, mapear clases a tablas

## html · HTML
alcance: compartido

- html.estructura · Estructura de una página · doctype, head, body, etiquetas y atributos
- html.texto · Texto, enlaces e imágenes · títulos, párrafos, enlaces, imágenes
- html.semantica · HTML semántico y accesible · header, nav, main, footer, textos alternativos
- html.listas-tablas · Listas y tablas · ul, ol, tablas accesibles
- html.formularios · Formularios · campos, etiquetas, validación del navegador
- html.multimedia · Multimedia · audio, video, iframes, canvas

## css · CSS
alcance: compartido

- css.selectores · Selectores y cascada · selectores, especificidad, herencia
- css.caja · Colores, texto y el modelo de caja · colores, tipografía, margin, padding, border
- css.flexbox · Flexbox · filas y columnas flexibles
- css.grid · Grid · grillas, áreas, grillas que se adaptan
- css.responsive · Diseño adaptable · mobile first, @media
- css.animaciones · Transiciones y animaciones · transition, keyframes
- css.frameworks · Frameworks de CSS · Tailwind, Bootstrap

## js · JavaScript
alcance: compartido

- js.fundamentos · JavaScript básico · variables, funciones, objetos, arrays
- js.dom · El DOM · buscar y modificar elementos
- js.eventos · Eventos · clicks, teclado, formularios
- js.fetch · fetch y asincronía · promesas, async/await, pedir datos a una API
- js.formularios · Formularios con JavaScript · enviar con fetch, mostrar errores
- js.modulos · Módulos · import, export, empaquetadores
- js.almacenamiento · Guardar en el navegador · localStorage, sessionStorage
- js.canvas · Dibujar con canvas · 2D, animación con requestAnimationFrame
- js.typescript · TypeScript · tipos sobre JavaScript
- js.frameworks · Frameworks de interfaz · React, Vue, Alpine

## web · Desarrollo web del lado del servidor
alcance: compartido

- web.http · Cómo funciona la web · pedido-respuesta, verbos, códigos, encabezados
- web.servidor · Páginas dinámicas · servidor local, mezclar código y HTML
- web.formularios · Formularios del lado del servidor · GET, POST, validar en el servidor
- web.sesiones · Sesiones y cookies · recordar entre pedidos
- web.auth · Login y contraseñas · hash, iniciar y cerrar sesión, páginas protegidas
- web.seguridad · Seguridad web · XSS, CSRF, validar del lado del servidor
- web.subidas · Subir archivos · multipart, validar el tipo real
- web.plantillas · Plantillas y layouts · separar lógica de presentación
- web.mvc · MVC y router · controlador frontal, rutas, controladores
- web.api-rest · APIs REST y JSON · recursos, verbos, códigos, DTO, validación
- web.despliegue · Subir a producción · hosting, dominio, HTTPS, variables de entorno

## fw · Frameworks
alcance: compartido

- fw.laravel · Laravel · rutas, Blade, Eloquent, migraciones
- fw.spring · Spring Boot · contenedor, REST, JPA
- fw.flask · Flask o Django · web con Python
- fw.express · Express · web con Node.js

## juegos · Videojuegos
alcance: compartido

- juegos.bucle · El bucle de juego · entrada, actualizar, dibujar, delta time
- juegos.entrada · Teclado y mouse · eventos y estado del teclado, movimiento
- juegos.sprites · Sprites y animación · imágenes, animar por tiempo
- juegos.colisiones · Colisiones · rectángulos (AABB), resolver eje por eje
- juegos.estados · Estados y escenas · menú, jugando, pausa, fin
- juegos.camara · Cámara y mapas de baldosas · mundos más grandes que la pantalla
- juegos.ia · Enemigos con comportamiento · perseguir, patrullar, decidir
- juegos.turnos · Juegos por turnos · combate, dados, reglas
- juegos.guardado · Guardar partidas y récords · archivos o base de datos
- juegos.sonido · Sonido · efectos y música
- juegos.fisica · Física simple · gravedad, saltos, rebotes

## graf · Bibliotecas gráficas y de juegos
alcance: compartido

- graf.pygame · pygame · ventana, dibujo y juegos con Python
- graf.sdl · SDL · ventana, render y juegos con C y C++
- graf.sfml · SFML · juegos 2D con C++
- graf.opengl · OpenGL · gráficos 3D, shaders
- graf.raylib · raylib · juegos simples en C
- graf.phaser · Phaser · juegos en el navegador
- graf.wasm · WebAssembly · llevar C/C++ al navegador

## gui · Aplicaciones de escritorio
alcance: compartido

- gui.eventos · Interfaces dirigidas por eventos · el bucle de eventos, señales, listeners
- gui.componentes · Componentes · botones, campos, listas, opciones
- gui.layouts · Layouts · ordenar la ventana sin posiciones fijas
- gui.menus-dialogos · Menús y diálogos · barras de menú, atajos, diálogos
- gui.tablas-arboles · Tablas y árboles · modelos de datos en la interfaz
- gui.modelo-vista · Modelo-vista · separar los datos de su presentación
- gui.dibujo · Dibujar en una ventana · pintar a mano, animar con un timer
- gui.qt · Qt · aplicaciones de escritorio con C++
- gui.swing · Swing · aplicaciones de escritorio con Java
- gui.tkinter · Tkinter · aplicaciones de escritorio con Python

## hw · Hardware y Arduino
alcance: compartido

- hw.arduino · Arduino · setup y loop, pines, millis
- hw.entradas · Botones, perillas y PWM · digital, analógico, rebote
- hw.serie · Puerto serie · protocolos de texto entre la placa y la compu
- hw.sensores · Sensores y actuadores · distancia, temperatura, motores

## datos · Ciencia de datos e IA
alcance: compartido

- datos.pandas · Análisis de datos · cargar, filtrar, agrupar
- datos.graficos · Gráficos de datos · matplotlib y afines
- datos.numpy · Cálculo numérico · arrays numéricos
- datos.ml · Aprendizaje automático · modelos simples, entrenar y evaluar
