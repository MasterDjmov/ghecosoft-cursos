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
            // Las expediciones del mundo (D91): se abren al completar `opens_after`; cada lugar, al completar su nodo.
            // x e y: dónde está en el mapa (porcentaje del ancho y del alto).
            'expeditions' => [
                'opens_after' => 'R01-N05',
                'map' => 'img/mundos/valle/mapa.webp',
                'places' => [
                    ['code' => 'aldea-del-script', 'name' => 'Aldea del Script', 'node' => 'R00-N01', 'level' => 1, 'creatures' => ['slime'], 'x' => 18, 'y' => 87,
                        'text' => 'Los callejones de la Aldea, donde los slimes se esconden entre comillas sin cerrar.'],
                    ['code' => 'el-mercado', 'name' => 'El Mercado', 'node' => 'R01-N01', 'level' => 2, 'creatures' => ['goblin', 'slime'], 'x' => 22, 'y' => 72,
                        'text' => 'Entre los toldos verdes, los goblins mezclan monedas con letras.'],
                    ['code' => 'casa-de-los-copistas', 'name' => 'Casa de los Copistas', 'node' => 'R01-N03', 'level' => 3, 'creatures' => ['slime', 'esqueleto'], 'x' => 29, 'y' => 84,
                        'text' => 'Carteles torcidos, tinta derramada y algún nombre sin cuerpo.'],
                    ['code' => 'puente-del-juicio', 'name' => 'Puente del Juicio', 'node' => 'R01-N02', 'level' => 3, 'creatures' => ['goblin', 'esqueleto'], 'x' => 53, 'y' => 75,
                        'text' => 'La piedra negra del puente; abajo, el río y lo que se esconde en él.'],
                    ['code' => 'laberinto-de-las-siete-salas', 'name' => 'Laberinto de las Siete Salas', 'node' => 'R01-N04', 'level' => 4, 'creatures' => ['esqueleto', 'orco'], 'x' => 36, 'y' => 64,
                        'text' => 'Siete salas que cambian de lugar. Los orcos piden puertas que no están.'],
                    ['code' => 'posada-de-la-serpiente', 'name' => 'Caminos de la Posada', 'node' => 'R01-N05', 'level' => 5, 'creatures' => ['orco', 'goblin'], 'x' => 61, 'y' => 91,
                        'text' => 'Los caminos que salen de la Posada, de noche.'],
                    ['code' => 'ermita-del-bestiario', 'name' => 'Ermita del Bestiario', 'node' => 'R01-N06', 'level' => 5, 'creatures' => ['orco', 'esqueleto'], 'x' => 12, 'y' => 45,
                        'text' => 'El bosque de la Ermita: cada criatura, con su página en el Bestiario.'],
                    ['code' => 'cueva-del-troll', 'name' => 'Cueva del Troll', 'node' => 'R01-N07', 'level' => 6, 'creatures' => ['troll', 'orco'], 'x' => 41, 'y' => 92,
                        'text' => 'Bajo el puente viejo. Dos nombres, una sola lista.'],
                    ['code' => 'cueva-de-los-ecos', 'name' => 'Cueva de los Ecos', 'node' => 'R01-N09', 'level' => 7, 'creatures' => ['esqueleto', 'troll'], 'x' => 26, 'y' => 58,
                        'text' => 'Lo que se grita adentro, adentro se queda.'],
                    ['code' => 'terrazas-de-las-funciones', 'name' => 'Terrazas de las Funciones', 'node' => 'R01-N08', 'level' => 7, 'creatures' => ['ogro', 'orco'], 'x' => 44, 'y' => 30,
                        'text' => 'Escalones de piedra y cascadas; los ogros hacen otra cosa de la que dicen.'],
                    ['code' => 'casa-de-los-tomos', 'name' => 'Casa de los Tomos', 'node' => 'R01-N10', 'level' => 8, 'creatures' => ['ogro', 'troll'], 'x' => 44, 'y' => 46,
                        'text' => 'Estantes hasta el techo. Algo se mueve entre los tomos viejos.'],
                    ['code' => 'paso-de-la-hidra', 'name' => 'Paso de la Hidra', 'node' => 'R01-N11', 'level' => 9, 'creatures' => ['ogro', 'troll', 'dragon'], 'x' => 54, 'y' => 35,
                        'text' => 'Donde cayó la Hidra todavía quedan cabezas sueltas.'],
                    // Acto II: el Bastión de las Escamas (R02).
                    ['code' => 'gran-biblioteca', 'name' => 'La Gran Biblioteca', 'node' => 'R02-N01', 'level' => 10, 'creatures' => ['orco', 'esqueleto', 'troll'], 'x' => 66, 'y' => 40,
                        'text' => 'Pasillos de estantes infinitos, donde algunos moldes se escaparon solos.'],
                    ['code' => 'sotano-del-bastion', 'name' => 'El Sótano del Bastión', 'node' => 'R02-N03', 'level' => 11, 'creatures' => ['slime', 'troll', 'ogro'], 'x' => 72, 'y' => 48,
                        'text' => 'Goteras, pergaminos húmedos y errores que nadie atrapó.'],
                    ['code' => 'la-boveda', 'name' => 'La Bóveda', 'node' => 'R02-N05', 'level' => 12, 'creatures' => ['ogro', 'troll', 'dragon'], 'x' => 61, 'y' => 47,
                        'text' => 'Donde cayó el Archivista todavía vuelan hojas corruptas.'],
                    // Acto III: la Gran Ciudadela y la Torre del Reloj (R03).
                    ['code' => 'torre-del-reloj', 'name' => 'Los pisos de la Torre', 'node' => 'R03-N01', 'level' => 13, 'creatures' => ['orco', 'ogro', 'troll'], 'x' => 76, 'y' => 31,
                        'text' => 'Del portal del primer piso todavía salen enemigos, de a uno.'],
                    ['code' => 'gremio-de-artifices', 'name' => 'El Gremio de Artífices', 'node' => 'R03-N04', 'level' => 14, 'creatures' => ['ogro', 'troll', 'dragon'], 'x' => 90, 'y' => 23,
                        'text' => 'Talleres llenos de piezas sin probar. Algunas muerden.'],
                    ['code' => 'cima-del-reloj', 'name' => 'La cima del Reloj', 'node' => 'R03-N07', 'level' => 15, 'creatures' => ['troll', 'dragon'], 'x' => 82, 'y' => 13,
                        'text' => 'Bajo las auroras, los engranajes del Gólem siguen girando solos.'],
                ],
            ],
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

    // Las criaturas de las expediciones (D91), al nivel 1: vida, ataque, defensa y destreza. Crecen con el
    // nivel del lugar. `material`: el código del ítem que pueden dejar.
    'creatures' => [
        'slime' => ['hp' => 22, 'attack' => 5, 'defense' => 0, 'dexterity' => 3, 'material' => 'baba-de-slime'],
        'goblin' => ['hp' => 28, 'attack' => 7, 'defense' => 1, 'dexterity' => 7, 'material' => 'diente-de-goblin'],
        'esqueleto' => ['hp' => 32, 'attack' => 8, 'defense' => 2, 'dexterity' => 5, 'material' => 'hueso-de-esqueleto'],
        'orco' => ['hp' => 42, 'attack' => 9, 'defense' => 3, 'dexterity' => 4, 'material' => 'colmillo-de-orco'],
        'troll' => ['hp' => 50, 'attack' => 9, 'defense' => 3, 'dexterity' => 2, 'material' => 'musgo-de-troll'],
        'ogro' => ['hp' => 54, 'attack' => 10, 'defense' => 3, 'dexterity' => 3, 'material' => 'garra-de-ogro'],
        'dragon' => ['hp' => 80, 'attack' => 12, 'defense' => 4, 'dexterity' => 5, 'material' => null],
    ],

    // Expediciones (D91, JUEGO.md § 6 y § 8): minutos y oro base de cada largo, cuántas criaturas, el tope diario
    // y el botín (probabilidad de ítem por rareza; a las `pity` expediciones sin raro, cae uno).
    'expedition' => [
        'lengths' => [
            'short' => ['label' => 'Corta', 'minutes' => 5, 'gold' => 15, 'enemies' => [1, 2]],
            'medium' => ['label' => 'Media', 'minutes' => 15, 'gold' => 40, 'enemies' => [2, 3]],
            'long' => ['label' => 'Larga', 'minutes' => 30, 'gold' => 80, 'enemies' => [3, 4]],
        ],
        // Cada cuántos minutos se vuelven a sortear las 3 del momento (se calcula al mirar, sin cron).
        'refresh_minutes' => 30,
        'per_day' => 6,
        'drops' => ['common' => 20, 'rare' => 5, 'epic' => 1],
        'pity' => 15,
        // Para probar en local: 60 = cada minuto dura un segundo. En producción, 1.
        'speed' => (int) env('GAME_EXPEDITION_SPEED', 1),
    ],

    // Monturas (JUEGO.md § 6): la especie es cosmética; el nivel acorta las expediciones.
    'mounts' => [
        'species' => ['algoritmia' => 'Algoritmia', 'archivald' => 'Archivald', 'auragryph' => 'AuraGryph', 'copperpug' => 'CopperPug',
            'cristal' => 'Cristal', 'draco-bit' => 'Draco-Bit', 'gran-apex' => 'Gran Apex', 'pixelshell' => 'PixelShell', 'serphira' => 'Serphira',
            'titan' => 'Titán', 'vitral' => 'Vitral', 'vitrox' => 'Vitrox', 'voltcat' => 'VoltCat', 'voltio' => 'Voltio'],
        'levels' => [
            1 => ['reduction' => 10, 'price' => 300, 'min_level' => 3],
            2 => ['reduction' => 20, 'price' => 1500, 'min_level' => 8],
            3 => ['reduction' => 30, 'price' => 4000, 'min_level' => 15],
            4 => ['reduction' => 40, 'price' => 8000, 'min_level' => 22],
            5 => ['reduction' => 50, 'price' => 15000, 'min_level' => 30],
        ],
    ],

    // Días antes del vencimiento en que se avisa "tu abono vence pronto".
    'subscription_warning_days' => 5,
];
