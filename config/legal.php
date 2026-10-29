<?php

/*
 * D112: datos de las páginas legales (Términos, Privacidad, arrepentimiento y baja).
 * Al cambiar un texto que el alumno acepta, subir la versión: queda guardada en cada cuenta.
 */
return [
    'version' => '2026-10-29',
    'owner' => env('LEGAL_OWNER', 'GhecoSoft-Code'),
    'owner_id' => env('LEGAL_OWNER_ID'), // CUIT del titular, si se quiere mostrar
    'email' => env('LEGAL_EMAIL', 'contacto@lariojaclick.ar'),
    'city' => 'La Rioja, Argentina',
    'withdrawal_days' => 10,
];
