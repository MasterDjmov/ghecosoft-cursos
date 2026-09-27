<?php

/*
| Límites de subida (en KB para las reglas "max" de validación) y extensiones
| permitidas. Se valida mime y extensión; el archivo se guarda con nombre UUID.
*/

return [
    // Logos de curso e íconos (disco público).
    'image' => [
        'max_kb' => 2048,
        'mimes' => ['png', 'jpg', 'jpeg', 'webp'],
    ],

    // Comprobantes de pago (disco privado).
    'receipt' => [
        'max_kb' => 5120,
        'mimes' => ['jpg', 'jpeg', 'png', 'pdf'],
    ],

    // Recursos de un nodo (disco privado, se sirven por controlador).
    'resource' => [
        'max_kb' => 20480,
        'mimes' => ['pdf', 'zip', 'txt', 'py', 'c', 'cpp', 'h', 'java', 'js', 'html', 'css', 'sql', 'md', 'png', 'jpg', 'jpeg', 'webp', 'docx', 'xlsx', 'pptx', 'odt', 'ods', 'odp'],
    ],
];
