<?php

/*
| Parámetros del juego que no dependen de cada práctica (GAMIFICACION.md).
*/

return [
    // XP extra al aprobar la última obligatoria de un nodo (se paga una sola vez).
    'node_completed_xp' => 20,

    // XP extra al vencer a un jefe (además de la del nodo completo) y su insignia.
    'boss_defeated_xp' => 50,

    // El oro de las micro-misiones (D89). Cada jugador recibe, una sola vez, el de todas las que ya superó
    // (`Heroes::settleGold`), así que prenderlo tarde no hace perder nada.
    'gold_enabled' => env('GAME_GOLD_ENABLED', true),

    // Los ítems y lo que «se abre» de las micro-misiones (D90: la mochila ya existe). Apagado, no se muestran
    // ni se dan; al prenderlo, a cada jugador se le acredita lo de las que ya superó (`Inventory::settleItems`).
    'inventory_enabled' => env('GAME_INVENTORY_ENABLED', true),

    // El protagonista de cada curso base, por lenguaje (D84 § 1). Sus 6 aspectos van en
    // public/img/protagonistas/<slug>/1.webp … 6.webp (solo cosméticos, sin bonos).
    'protagonists' => [
        'python' => [
            'name' => 'Mia',
            'slug' => 'mia',
            'title' => 'Aprendiz de maga',
            // La tienda del mundo (D90).
            'shop' => ['name' => 'El puesto de Baldo', 'keeper' => 'Baldo', 'portrait' => 'img/personajes/baldo.webp', 'figure' => 'img/personajes/baldo-cuerpo.webp',
                'greeting' => '—¡Pasá, pasá! Todo lo que necesitás para el camino, a precio de amigo. Bueno… casi.'],
            'looks' => [
                1 => 'Lectora de Runas',
                2 => 'Aprendiz de coletas',
                3 => 'Exploradora del Visor',
                4 => 'Escriba Rúnica',
                5 => 'Voz del Valle',
                6 => 'Hechicera de la Espiral',
            ],
        ],
    ],

    // Días antes del vencimiento en que se avisa "tu abono vence pronto".
    'subscription_warning_days' => 5,
];
