<?php

/*
| Parámetros del juego que no dependen de cada práctica (GAMIFICACION.md).
*/

return [
    // XP extra al aprobar la última obligatoria de un nodo (se paga una sola vez).
    'node_completed_xp' => 20,

    // XP extra al vencer a un jefe (además de la del nodo completo) y su insignia.
    'boss_defeated_xp' => 50,

    // El oro, los ítems y lo que «se abre» de las micro-misiones (D84 etapa 4). Mientras esté apagado no se
    // muestran: no existen todavía. Al prenderlo, a cada jugador se le acredita lo de las que ya superó.
    'inventory_enabled' => env('GAME_INVENTORY_ENABLED', false),

    // Días antes del vencimiento en que se avisa "tu abono vence pronto".
    'subscription_warning_days' => 5,
];
