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
    'mentor.name' => ['group' => 'world', 'label' => 'Mentor o guía (nombre, retrato y presentación)', 'singular' => 'el profe', 'gender' => 'm'],

    // Economía
    'coin.course' => ['group' => 'economy', 'label' => 'Moneda del curso (se gana con obligatorias)', 'singular' => 'moneda', 'plural' => 'monedas', 'gender' => 'f'],
    'coin.wildcard' => ['group' => 'economy', 'label' => 'Moneda comodín (se gana con optativas, abre extras)', 'singular' => 'comodín', 'plural' => 'comodines', 'gender' => 'm'],
    'xp' => ['group' => 'economy', 'label' => 'Experiencia', 'singular' => 'experiencia', 'plural' => 'experiencia', 'gender' => 'f'],
    'xp.short' => ['group' => 'economy', 'label' => 'Abreviatura de la experiencia', 'singular' => 'XP', 'plural' => 'XP', 'gender' => 'f'],

    // Progreso
    'level' => ['group' => 'progress', 'label' => 'Nivel o rango (palabra genérica)', 'singular' => 'nivel', 'plural' => 'niveles', 'gender' => 'm'],
    'branch' => ['group' => 'progress', 'label' => 'Rama o bloque del árbol', 'singular' => 'rama', 'plural' => 'ramas', 'gender' => 'f'],
    'node' => ['group' => 'progress', 'label' => 'Nodo (un tema del árbol)', 'singular' => 'nodo', 'plural' => 'nodos', 'gender' => 'm'],
    'node.root' => ['group' => 'progress', 'label' => 'Nodo raíz (la clase 0, entrada al curso)', 'singular' => 'nodo raíz', 'plural' => 'nodos raíz', 'gender' => 'm'],
    'node.boss' => ['group' => 'progress', 'label' => 'Nodo jefe (cierra cada rama)', 'singular' => 'jefe', 'plural' => 'jefes', 'gender' => 'm'],
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

    // Bestiario (errores habituales)
    'beast.slime' => ['group' => 'bestiary', 'label' => 'Bestia: slime', 'singular' => 'slime', 'plural' => 'slimes', 'gender' => 'm'],
    'beast.goblin' => ['group' => 'bestiary', 'label' => 'Bestia: goblin', 'singular' => 'goblin', 'plural' => 'goblins', 'gender' => 'm'],
    'beast.skeleton' => ['group' => 'bestiary', 'label' => 'Bestia: esqueleto', 'singular' => 'esqueleto', 'plural' => 'esqueletos', 'gender' => 'm'],
    'beast.orc' => ['group' => 'bestiary', 'label' => 'Bestia: orco', 'singular' => 'orco', 'plural' => 'orcos', 'gender' => 'm'],
    'beast.ogre' => ['group' => 'bestiary', 'label' => 'Bestia: ogro', 'singular' => 'ogro', 'plural' => 'ogros', 'gender' => 'm'],
    'beast.troll' => ['group' => 'bestiary', 'label' => 'Bestia: troll', 'singular' => 'troll', 'plural' => 'trolls', 'gender' => 'm'],
    'beast.dragon' => ['group' => 'bestiary', 'label' => 'Bestia: dragón', 'singular' => 'dragón', 'plural' => 'dragones', 'gender' => 'm'],
];
