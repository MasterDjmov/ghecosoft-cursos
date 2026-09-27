<?php

/*
| Parámetros del juego que no dependen de cada práctica (GAMIFICACION.md).
*/

return [
    // XP extra al aprobar la última obligatoria de un nodo (se paga una sola vez).
    'node_completed_xp' => 20,

    // XP extra al vencer a un jefe (además de la del nodo completo) y su insignia.
    'boss_defeated_xp' => 50,

    // Días antes del vencimiento en que se avisa "tu abono vence pronto".
    'subscription_warning_days' => 5,
];
