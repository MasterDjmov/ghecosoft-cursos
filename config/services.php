<?php

return [

    /*
    |--------------------------------------------------------------------------
    | Third Party Services
    |--------------------------------------------------------------------------
    |
    | This file is for storing the credentials for third party services such
    | as Resend, Postmark, AWS, and more. This file provides the de facto
    | location for this type of information, allowing packages to have
    | a conventional file to locate the various service credentials.
    |
    */

    'postmark' => [
        'key' => env('POSTMARK_API_KEY'),
    ],

    'resend' => [
        'key' => env('RESEND_API_KEY'),
    ],

    'ses' => [
        'key' => env('AWS_ACCESS_KEY_ID'),
        'secret' => env('AWS_SECRET_ACCESS_KEY'),
        'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    ],

    'slack' => [
        'notifications' => [
            'bot_user_oauth_token' => env('SLACK_BOT_USER_OAUTH_TOKEN'),
            'channel' => env('SLACK_BOT_USER_DEFAULT_CHANNEL'),
        ],
    ],

    // Python en el navegador (D5): se descarga del CDN la primera vez que se ejecuta algo.
    'pyodide' => [
        'url' => env('PYODIDE_URL', 'https://cdn.jsdelivr.net/pyodide/v0.29.5/full/'),
        'timeout_ms' => 5000,
    ],

    // Ejecutor local de Java del docente (D69): scripts/JavaRunner.java, en su compu.
    'java_runner' => [
        'url' => env('JAVA_RUNNER_URL', 'http://127.0.0.1:17017'),
    ],

    // Avisos al WhatsApp del docente con CallMeBot (gratis, uso personal): sin las dos variables, no se manda nada.
    // Se activa mandándole «I allow callmebot to send me messages» al número del bot (callmebot.com).
    'callmebot' => [
        'phone' => env('CALLMEBOT_PHONE'),
        'apikey' => env('CALLMEBOT_APIKEY'),
    ],

];
