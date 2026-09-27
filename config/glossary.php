<?php

/*
| Valores por defecto del diccionario narrativo. Se usan cuando la clave no
| está cargada ni en el curso ni en el general (admin → Diccionario).
| gender: 'f' | 'm' (para artículos: "la escama", "el rubí").
*/

return [
    'world.name' => ['singular' => 'el Mundo del Código', 'gender' => 'm'],
    'coin.course' => ['singular' => 'moneda', 'plural' => 'monedas', 'gender' => 'f'],
    'coin.wildcard' => ['singular' => 'comodín', 'plural' => 'comodines', 'gender' => 'm'],
    'xp' => ['singular' => 'experiencia', 'plural' => 'experiencia', 'gender' => 'f'],
    'xp.short' => ['singular' => 'XP', 'plural' => 'XP', 'gender' => 'f'],
    'node' => ['singular' => 'nodo', 'plural' => 'nodos', 'gender' => 'm'],
    'node.root' => ['singular' => 'nodo raíz', 'plural' => 'nodos raíz', 'gender' => 'm'],
    'node.boss' => ['singular' => 'jefe', 'plural' => 'jefes', 'gender' => 'm'],
    'practice' => ['singular' => 'práctica', 'plural' => 'prácticas', 'gender' => 'f'],
    'level' => ['singular' => 'nivel', 'plural' => 'niveles', 'gender' => 'm'],
];
