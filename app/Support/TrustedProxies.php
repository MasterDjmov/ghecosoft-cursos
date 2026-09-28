<?php

namespace App\Support;

use Illuminate\Http\Middleware\TrustProxies;

/**
 * Detrás de Cloudflare: la IP real del alumno y el HTTPS vienen en X-Forwarded-*,
 * y solo se les cree si el pedido llega desde un proxy de confianza
 * (config/security.php, TRUSTED_PROXIES).
 */
class TrustedProxies
{
    public static function apply(): void
    {
        $proxies = config('security.trusted_proxies');

        if (! $proxies) {
            return;
        }

        TrustProxies::at(match ($proxies) {
            'cloudflare' => config('security.cloudflare_ips'),
            '*' => '*',
            default => array_map('trim', explode(',', $proxies)),
        });
    }
}
