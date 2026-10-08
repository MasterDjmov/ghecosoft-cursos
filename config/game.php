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
        // Java (docs/historias/java.md). La tienda del Imperio, cuando haya ítems del Imperio.
        // Ojo: al reordenar el curso (R04 y R05 nuevas, D92 de java.md), revisar los nodos de los lugares del final.
        'java' => [
            'name' => 'Zed',
            'slug' => 'zed',
            'title' => 'Ladrón del Puerto',
            // Baldo, el mercader ambulante, también pone su puesto en el Imperio (aparece en R01-N04).
            'shop' => ['name' => 'El puesto de Baldo en el Imperio', 'keeper' => 'Baldo', 'portrait' => 'img/personajes/baldo.webp', 'figure' => 'img/personajes/baldo-cuerpo.webp',
                'greeting' => '—¡Zed! Sabía que ibas a terminar acá. Te tengo justo lo que necesitás para la Aduana… a precio imperial, eso sí.'],
            'expeditions' => [
                'opens_after' => 'R01-N05',
                'map' => 'img/mundos/imperio/mapa.webp',
                'places' => [
                    ['code' => 'aduana-del-compilador', 'name' => 'La Aduana del Compilador', 'node' => 'R00-N01', 'level' => 1, 'creatures' => ['slime'], 'x' => 22, 'y' => 76,
                        'text' => 'La muralla y sus portones: los slimes se esconden en los pergaminos rechazados.'],
                    ['code' => 'camino-de-las-caravanas', 'name' => 'El camino de las caravanas', 'node' => 'R01-N02', 'level' => 2, 'creatures' => ['slime', 'goblin'], 'x' => 13, 'y' => 92,
                        'text' => 'Carretas que esperan para entrar, con mercadería mal declarada.'],
                    ['code' => 'muelles-del-rio', 'name' => 'Los muelles del Río', 'node' => 'R01-N04', 'level' => 3, 'creatures' => ['goblin', 'esqueleto'], 'x' => 44, 'y' => 70,
                        'text' => 'Cajones sin etiqueta y nombres que no existen en ningún registro.'],
                    ['code' => 'posada-del-bytecode', 'name' => 'La Posada del Bytecode', 'node' => 'R01-N05', 'level' => 4, 'creatures' => ['goblin', 'orco'], 'x' => 75, 'y' => 66,
                        'text' => 'De noche, los viajeros piden lo que no está en el menú.'],
                    ['code' => 'encrucijada-de-los-denarios', 'name' => 'La Encrucijada de los Denarios', 'node' => 'R01-N09', 'level' => 5, 'creatures' => ['orco', 'esqueleto'], 'x' => 41, 'y' => 58,
                        'text' => 'La plaza de la fuente: todos los caminos del Imperio pasan por acá.'],
                    ['code' => 'academia-de-los-moldes', 'name' => 'La Academia de los Moldes', 'node' => 'R02-N01', 'level' => 6, 'creatures' => ['esqueleto', 'troll'], 'x' => 22, 'y' => 44,
                        'text' => 'Moldes rotos de los que salen criaturas a medio hacer.'],
                    ['code' => 'jardines-polimorficos', 'name' => 'Los Jardines Polimórficos', 'node' => 'R02-N06', 'level' => 7, 'creatures' => ['troll', 'ogro'], 'x' => 58, 'y' => 38,
                        'text' => 'Cada planta responde distinto a la misma orden. Algunas muerden.'],
                    ['code' => 'archivos-imperiales', 'name' => 'Los Archivos Imperiales', 'node' => 'R03-N01', 'level' => 8, 'creatures' => ['troll', 'ogro'], 'x' => 73, 'y' => 46,
                        'text' => 'Salas de estantes donde a veces lo que buscás es null.'],
                    ['code' => 'rio-de-la-capital', 'name' => 'El Río de la Capital', 'node' => 'R03-N04', 'level' => 9, 'creatures' => ['ogro', 'orco'], 'x' => 52, 'y' => 54,
                        'text' => 'Las barcazas bajan cargadas; no todas llegan a destino.'],
                    ['code' => 'la-represa', 'name' => 'La Represa', 'node' => 'R03-N08', 'level' => 10, 'creatures' => ['ogro', 'troll', 'dragon'], 'x' => 66, 'y' => 82,
                        'text' => 'Donde el río se traba, algo enorme se mueve bajo el agua.'],
                    ['code' => 'boveda-imperial', 'name' => 'La Bóveda Imperial', 'node' => 'R04-N01', 'level' => 11, 'creatures' => ['troll', 'ogro', 'dragon'], 'x' => 86, 'y' => 26,
                        'text' => 'Tablas huérfanas y registros sin dueño, en lo alto del acantilado.'],
                    ['code' => 'torre-del-arquitecto', 'name' => 'La Torre del Arquitecto', 'node' => 'R05-N01', 'level' => 13, 'creatures' => ['ogro', 'dragon'], 'x' => 30, 'y' => 20,
                        'text' => 'La torre más alta del Imperio. Arriba, una ventana espera su vidrio.'],
                ],
            ],
            'looks' => [
                1 => 'Ladrón del Visor',
                2 => 'Saqueador de Coleta',
                3 => 'Máscara de Humo',
                4 => 'Sombra de Capucha',
                5 => 'Sonrisa Torcida',
                6 => 'Veterano del Puerto',
            ],
        ],
        // C (docs/historias/c.md): la tienda (el carro de Chispa) y las expediciones de las Forjas se suman
        // cuando estén la imagen de Chispa y el mapa.
        'c' => [
            'name' => 'Kira',
            'slug' => 'kira',
            'title' => 'Aprendiz de espadachina',
            // Las Forjas (docs/historias/c.md): los lugares siguen el recorrido de Kira, de la Boca de la Forja a la Montaña.
            'expeditions' => [
                'opens_after' => 'R01-N05',
                'map' => 'img/mundos/forjas/mapa.webp',
                'places' => [
                    ['code' => 'boca-de-la-forja', 'name' => 'La Boca de la Forja', 'node' => 'R00-N01', 'level' => 1, 'creatures' => ['slime'], 'x' => 12, 'y' => 81,
                        'text' => 'El portón que se abre tirando, no empujando. Al costado, un vitral apagado.'],
                    ['code' => 'deposito-de-cajones', 'name' => 'El Depósito de Cajones', 'node' => 'R01-N01', 'level' => 2, 'creatures' => ['slime', 'goblin'], 'x' => 28, 'y' => 83,
                        'text' => 'Cajones de 255 clavos: el que mete uno más los vacía todos.'],
                    ['code' => 'cruce-de-los-operadores', 'name' => 'El Cruce de los Operadores', 'node' => 'R01-N02', 'level' => 3, 'creatures' => ['goblin'], 'x' => 40, 'y' => 68,
                        'text' => 'El puente sobre la lava, con carteles que apuntan a todos lados.'],
                    ['code' => 'posada-del-byte', 'name' => 'La Posada del Byte', 'node' => 'R01-N05', 'level' => 4, 'creatures' => ['goblin', 'esqueleto'], 'x' => 54, 'y' => 70,
                        'text' => 'Cerveza medida al mililitro: Tizón ya se quejó de la espuma.'],
                    ['code' => 'forja-de-maese-ferrum', 'name' => 'La Forja de Maese Ferrum', 'node' => 'R01-N10', 'level' => 5, 'creatures' => ['esqueleto', 'orco'], 'x' => 50, 'y' => 26,
                        'text' => 'La escoria de toda la Forja se amontona detrás de los hornos. A veces se mueve.'],
                    ['code' => 'pasillos-numerados', 'name' => 'Los Pasillos Numerados', 'node' => 'R02-N01', 'level' => 6, 'creatures' => ['orco'], 'x' => 24, 'y' => 38,
                        'text' => 'Puertas del 0 en adelante. La que está después de la última no debería abrirse.'],
                    ['code' => 'aldea-del-puntero-nulo', 'name' => 'La Aldea del Puntero Nulo', 'node' => 'R02-N04', 'level' => 7, 'creatures' => ['orco', 'ogro'], 'x' => 14, 'y' => 66,
                        'text' => 'Un cartel que no apunta a ningún lado. Quien lo sigue, no vuelve.'],
                    ['code' => 'minas-de-silicio', 'name' => 'Las Minas de Silicio', 'node' => 'R03-N01', 'level' => 8, 'creatures' => ['ogro', 'troll'], 'x' => 65, 'y' => 61,
                        'text' => 'Hulda cuenta cada vagoneta. Las que nadie devuelve, se pierden en la galería.'],
                    ['code' => 'galeria-de-la-sanguijuela', 'name' => 'La Galería de la Sanguijuela', 'node' => 'R03-N06', 'level' => 9, 'creatures' => ['troll'], 'x' => 68, 'y' => 90,
                        'text' => 'Un túnel que se traga lo que nadie liberó.'],
                    ['code' => 'archivo-de-la-forja', 'name' => 'El Archivo de la Forja', 'node' => 'R04-N01', 'level' => 10, 'creatures' => ['troll', 'ogro'], 'x' => 79, 'y' => 36,
                        'text' => 'Libros que alguien abrió y nunca cerró. Algo los hojea de noche.'],
                    ['code' => 'boveda-de-los-registros', 'name' => 'La Bóveda de los Registros', 'node' => 'R04-N06', 'level' => 11, 'creatures' => ['ogro', 'dragon'], 'x' => 91, 'y' => 40,
                        'text' => 'Cajas selladas con fichas de baja. Nada se tira, todo se marca.'],
                    ['code' => 'montana-del-dragon', 'name' => 'La Montaña del Dragón', 'node' => 'R05-N01', 'level' => 12, 'creatures' => ['ogro', 'dragon'], 'x' => 90, 'y' => 28,
                        'text' => 'La fragua más honda. Desde abajo se oye roncar al fuego.'],
                ],
            ],
            'looks' => [
                1 => 'Espadachina del Visor',
                2 => 'Sombra Enmascarada',
                3 => 'Coleta de Acero',
                4 => 'Trenzas Rúnicas',
                5 => 'Hija de la Fragua',
                6 => 'Escarcha Arcana',
            ],
        ],
        // C++ (docs/historias/cpp.md): la tienda y las expediciones de la Ciudadela se suman cuando estén sus imágenes y el mapa.
        'cpp' => [
            'name' => 'Bron',
            'slug' => 'bron',
            'title' => 'Mecánico de la Ciudadela',
            'looks' => [
                1 => 'Mecánico del Monóculo',
                2 => 'Antiparras de Taller',
                3 => 'Máscara de Vapor',
                4 => 'Medio Autómata',
                5 => 'Fuego de Caldera',
                6 => 'Gran Ingeniero del Bastión',
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
        'dragon' => ['hp' => 80, 'attack' => 12, 'defense' => 4, 'dexterity' => 5, 'material' => 'escama-de-dragon'],
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

    // El taller (crafteo, D93): recetas fijas por código de ítem. `needs`: ingredientes (código → cantidad; un
    // ítem de la receta, como la Pluma de la Copista, se mejora); `gives`: el resultado y cuántos; `minutes`: lo
    // que tarda (se calcula al mirar, sin cron); `min_level`: nivel del jugador. Las recetas que mezclan mundos
    // se suman cuando cada mundo tenga sus materiales.
    'recipes' => [
        ['code' => 'pocion-de-baba', 'gives' => ['pocion-de-curacion' => 2], 'needs' => ['baba-de-slime' => 3], 'minutes' => 5, 'min_level' => 1],
        ['code' => 'pocion-grande-de-musgo', 'gives' => ['pocion-grande' => 1], 'needs' => ['pocion-de-curacion' => 2, 'musgo-de-troll' => 1], 'minutes' => 5, 'min_level' => 6],
        ['code' => 'anillo-de-colmillos', 'gives' => ['anillo-de-colmillos' => 1], 'needs' => ['anillo-del-bucle' => 1, 'colmillo-de-orco' => 5], 'minutes' => 10, 'min_level' => 5],
        ['code' => 'pluma-del-juicio', 'gives' => ['pluma-del-juicio' => 1], 'needs' => ['pluma-de-la-copista' => 1, 'diente-de-goblin' => 4, 'hueso-de-esqueleto' => 3], 'minutes' => 15, 'min_level' => 5],
        ['code' => 'capa-de-musgo', 'gives' => ['capa-de-musgo' => 1], 'needs' => ['capa-del-valle' => 1, 'musgo-de-troll' => 3, 'baba-de-slime' => 4], 'minutes' => 15, 'min_level' => 6],
        ['code' => 'baculo-de-la-garra', 'gives' => ['baculo-de-la-garra' => 1], 'needs' => ['baculo-del-interprete' => 1, 'garra-de-ogro' => 4, 'escama-de-dragon' => 2], 'minutes' => 30, 'min_level' => 10],
        // El Imperio (Java): los mismos materiales, con los ítems del puesto de Baldo.
        ['code' => 'cafe-fuerte-doble', 'gives' => ['cafe-fuerte' => 2], 'needs' => ['baba-de-slime' => 3], 'minutes' => 5, 'min_level' => 1],
        ['code' => 'taza-encantada', 'gives' => ['taza-encantada' => 1], 'needs' => ['taza-de-cafe' => 1, 'colmillo-de-orco' => 5], 'minutes' => 10, 'min_level' => 5],
        ['code' => 'sello-dentado', 'gives' => ['sello-dentado' => 1], 'needs' => ['baston-del-aduanero' => 1, 'diente-de-goblin' => 4, 'hueso-de-esqueleto' => 3], 'minutes' => 15, 'min_level' => 5],
        ['code' => 'chaqueta-forrada', 'gives' => ['chaqueta-forrada' => 1], 'needs' => ['chaqueta-de-la-aduana' => 1, 'musgo-de-troll' => 3, 'baba-de-slime' => 4], 'minutes' => 15, 'min_level' => 6],
        ['code' => 'estoque-de-la-garra', 'gives' => ['estoque-de-la-garra' => 1], 'needs' => ['estoque-del-casting' => 1, 'garra-de-ogro' => 4, 'escama-de-dragon' => 2], 'minutes' => 30, 'min_level' => 10],
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
