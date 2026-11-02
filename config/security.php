<?php

/*
| Proxies de confianza. En producción el sitio está detrás de Cloudflare: sin
| esto Laravel ve la IP de Cloudflare en vez de la del alumno (los límites de
| intentos se compartirían entre todos) y no detecta bien el HTTPS.
|
| TRUSTED_PROXIES: "cloudflare" (los rangos de abajo), "*" (cualquiera: solo si
| el servidor no es accesible por fuera del proxy), una lista separada por comas
| o vacío (ninguno, como en desarrollo).
*/

return [
    'trusted_proxies' => env('TRUSTED_PROXIES'),

    /*
    | Solo por Cloudflare (CLOUDFLARE_ONLY=true): el servidor rechaza a quien le habla directo a su IP
    | (que se ve en mail., cpanel. y ftp.) en vez de pasar por Cloudflare y su protección. Se mira la IP
    | que entrega el servidor (REMOTE_ADDR), así que antes de dejarlo prendido hay que probar que el sitio
    | siga abriendo: si el hosting ya reemplaza esa IP por la del visitante, rechazaría a todos (DEPLOY.md § 9).
    */
    'cloudflare_only' => (bool) env('CLOUDFLARE_ONLY', false),

    // https://www.cloudflare.com/ips/ (revisar si Cloudflare los cambia).
    'cloudflare_ips' => [
        '173.245.48.0/20', '103.21.244.0/22', '103.22.200.0/22', '103.31.4.0/22',
        '141.101.64.0/18', '108.162.192.0/18', '190.93.240.0/20', '188.114.96.0/20',
        '197.234.240.0/22', '198.41.128.0/17', '162.158.0.0/15', '104.16.0.0/13',
        '104.24.0.0/14', '172.64.0.0/13', '131.0.72.0/22',
        '2400:cb00::/32', '2606:4700::/32', '2803:f800::/32', '2405:b500::/32',
        '2405:8100::/32', '2a06:98c0::/29', '2c0f:f248::/32',
    ],
];
