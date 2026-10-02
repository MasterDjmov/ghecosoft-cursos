<?php

/*
| Catálogo del diccionario narrativo (GAMIFICACION.md § 8).
|
| Cada clave trae su valor por defecto, que se usa cuando no está cargada ni
| en el curso ni en el general (admin → Diccionario).
| - group: para filtrar en el admin.
| - label: qué es, para que el docente sepa qué está editando.
| - gender: 'f' | 'm' (para artículos: "la escama", "el rubí").
|
| Los nombres de los niveles usan claves dinámicas "level.{número}" (se editan
| desde Niveles) y el docente puede crear claves propias desde el admin.
*/

return [
    // Mundo
    'world.name' => ['group' => 'world', 'label' => 'Nombre del mundo (reemplaza a «Codexia»)', 'singular' => 'el Mundo del Código', 'gender' => 'm'],
    'world.region' => ['group' => 'world', 'label' => 'Nombre de la región o isla de un curso', 'singular' => 'región', 'plural' => 'regiones', 'gender' => 'f'],
    'hero.name' => ['group' => 'world', 'label' => 'Héroe por defecto (hasta que el alumno elija el suyo; en los textos: {heroe})', 'singular' => 'Kira', 'gender' => 'f'],
    'mentor.name' => ['group' => 'world', 'label' => 'Mentor o guía (nombre, retrato y presentación)', 'singular' => 'el profe', 'gender' => 'm'],

    // Compañía: cada personaje presenta una sección fija del nodo (D37). Iguales en todos los cursos salvo que un curso los cambie.
    'companion.theory' => ['group' => 'companions', 'label' => 'Quien da la explicación teórica del nodo', 'singular' => 'Mia', 'gender' => 'f'],
    'companion.uses' => ['group' => 'companions', 'label' => 'Quien cuenta "¿para qué sirve?" (usos reales)', 'singular' => 'Bron', 'gender' => 'm'],
    'companion.errors' => ['group' => 'companions', 'label' => 'Quien muestra los errores habituales y las trampas', 'singular' => 'Zed', 'gender' => 'm'],
    'companion.guild' => ['group' => 'companions', 'label' => 'Quien da los encargos del mundo real (optativas)', 'singular' => 'el Gremio', 'gender' => 'm'],

    // Economía
    'coin.course' => ['group' => 'economy', 'label' => 'Moneda del curso (se gana con obligatorias)', 'singular' => 'moneda', 'plural' => 'monedas', 'gender' => 'f'],
    'coin.wildcard' => ['group' => 'economy', 'label' => 'Moneda comodín (se gana con optativas, abre extras)', 'singular' => 'comodín', 'plural' => 'comodines', 'gender' => 'm'],
    'xp' => ['group' => 'economy', 'label' => 'Experiencia', 'singular' => 'experiencia', 'plural' => 'experiencia', 'gender' => 'f'],
    'xp.short' => ['group' => 'economy', 'label' => 'Abreviatura de la experiencia', 'singular' => 'XP', 'plural' => 'XP', 'gender' => 'f'],

    // Progreso
    'level' => ['group' => 'progress', 'label' => 'Nivel o rango (palabra genérica)', 'singular' => 'nivel', 'plural' => 'niveles', 'gender' => 'm'],
    'branch' => ['group' => 'progress', 'label' => 'Rama o bloque del árbol', 'singular' => 'rama', 'plural' => 'ramas', 'gender' => 'f'],
    'branch.path' => ['group' => 'progress', 'label' => 'Senda (rama de especialización optativa)', 'singular' => 'senda', 'plural' => 'sendas', 'gender' => 'f'],
    'node' => ['group' => 'progress', 'label' => 'Nodo (un tema del árbol)', 'singular' => 'nodo', 'plural' => 'nodos', 'gender' => 'm'],
    'node.root' => ['group' => 'progress', 'label' => 'Nodo raíz (la clase 0, entrada al curso)', 'singular' => 'nodo raíz', 'plural' => 'nodos raíz', 'gender' => 'm'],
    'node.boss' => ['group' => 'progress', 'label' => 'Nodo jefe (cierra cada rama)', 'singular' => 'jefe', 'plural' => 'jefes', 'gender' => 'm'],
    'node.window' => ['group' => 'progress', 'label' => 'Nodo ventana (prueba un campo; de ahí brota una Senda)', 'singular' => 'ventana', 'plural' => 'ventanas', 'gender' => 'f'],
    'node.extra' => ['group' => 'progress', 'label' => 'Nodo extra (optativo)', 'singular' => 'extra', 'plural' => 'extras', 'gender' => 'm'],
    'practice' => ['group' => 'progress', 'label' => 'Hoja o práctica', 'singular' => 'práctica', 'plural' => 'prácticas', 'gender' => 'f'],
    'badge' => ['group' => 'progress', 'label' => 'Insignia', 'singular' => 'insignia', 'plural' => 'insignias', 'gender' => 'f'],

    // Estados de un nodo
    'state.locked' => ['group' => 'states', 'label' => 'Nodo bloqueado', 'singular' => 'Bloqueado', 'gender' => 'm'],
    'state.available' => ['group' => 'states', 'label' => 'Nodo listo para abrir', 'singular' => 'Listo para abrir', 'gender' => 'm'],
    'state.unlocked' => ['group' => 'states', 'label' => 'Nodo abierto', 'singular' => 'Abierto', 'gender' => 'm'],
    'state.completed' => ['group' => 'states', 'label' => 'Nodo completado', 'singular' => 'Completado', 'gender' => 'm'],

    // Historia (el texto largo va en "Historia")
    'story.course_intro' => ['group' => 'story', 'label' => 'Crónica de entrada al curso', 'singular' => 'Bienvenida', 'gender' => 'f'],
    'story.branch_completed' => ['group' => 'story', 'label' => 'Mensaje al completar una rama', 'singular' => '¡Rama completada!', 'gender' => 'f'],
    'story.course_completed' => ['group' => 'story', 'label' => 'Mensaje al completar el curso', 'singular' => '¡Curso completado!', 'gender' => 'm'],
    // Mis Crónicas (D80): el prólogo del libro (para todos) y las frases de aliento de lo bloqueado (una por línea).
    'story.prologue' => ['group' => 'story', 'label' => 'Prólogo de Mis Crónicas (lo ven todos)', 'singular' => 'El mundo que vive en tu mente', 'gender' => 'm',
        'lore' => "Hay un mundo que no aparece en ningún mapa, {heroe}. No está al otro lado del mar ni detrás de las montañas: está **adentro de la cabeza de quien programa**. Se enciende la primera vez que alguien escribe una instrucción y la ve cobrar vida en la pantalla.\n\nLo llaman **{mundo}**. Sus regiones no se recorren a pie: se llega a ellas por **portales**, y cada portal es una lengua. Algunos huelen a bosque y a serpiente; otros, a hierro recién forjado; otros brillan como vidrio de colores. Nadie los conoce todos. Nadie terminó nunca de recorrerlo, porque cada puerta que se abre deja ver otras dos.\n\nPor eso, en este mundo, lo que aprendés no se pierde: **cada rama que crece en tu árbol se toca con otra**. Lo que te enseñe una región te va a servir en la siguiente, y en la otra, y en la que todavía no existe.\n\nEsta noche, un portal se abrió para vos. Del otro lado te espera **Gheco**, un gecko de escamas cian que conoce todos los caminos porque trepa por las paredes entre un mundo y otro. —Tranquila, tranquilo —te dice—. Nadie llega sabiendo. **Se llega aprendiendo.**"],
    'story.portal_piece' => ['group' => 'story', 'label' => 'Pieza del misterio del portal (se lee al terminar el curso)', 'singular' => 'Una pieza del portal', 'gender' => 'f'],
    'story.locked_hints' => ['group' => 'story', 'label' => 'Frases de aliento de Mis Crónicas (una por línea)', 'singular' => 'Frases de aliento', 'gender' => 'f',
        'lore' => "La historia no se escribe sola: la escribís vos, misión a misión.\n¿Qué habrá del otro lado de esta puerta?\n{mentor} te está esperando unas páginas más adelante.\nCada hoja que aprobás es una página más de tu historia.\nKira tampoco sabía cómo seguía. Por eso siguió.\nNadie llega sabiendo: se llega aprendiendo."],

    // Bestiario (errores habituales)
    'beast.slime' => ['group' => 'bestiary', 'label' => 'Bestia: slime', 'singular' => 'slime', 'plural' => 'slimes', 'gender' => 'm'],
    'beast.goblin' => ['group' => 'bestiary', 'label' => 'Bestia: goblin', 'singular' => 'goblin', 'plural' => 'goblins', 'gender' => 'm'],
    'beast.skeleton' => ['group' => 'bestiary', 'label' => 'Bestia: esqueleto', 'singular' => 'esqueleto', 'plural' => 'esqueletos', 'gender' => 'm'],
    'beast.orc' => ['group' => 'bestiary', 'label' => 'Bestia: orco', 'singular' => 'orco', 'plural' => 'orcos', 'gender' => 'm'],
    'beast.ogre' => ['group' => 'bestiary', 'label' => 'Bestia: ogro', 'singular' => 'ogro', 'plural' => 'ogros', 'gender' => 'm'],
    'beast.troll' => ['group' => 'bestiary', 'label' => 'Bestia: troll', 'singular' => 'troll', 'plural' => 'trolls', 'gender' => 'm'],
    'beast.dragon' => ['group' => 'bestiary', 'label' => 'Bestia: dragón', 'singular' => 'dragón', 'plural' => 'dragones', 'gender' => 'm'],
];
