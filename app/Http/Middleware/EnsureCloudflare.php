<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\IpUtils;
use Symfony\Component\HttpFoundation\Response;

/**
 * Con CLOUDFLARE_ONLY prendido (config/security.php), solo se atiende lo que llega desde Cloudflare: quien
 * encuentra la IP real del servidor y le habla directo no se saltea su protección. No dice por qué.
 */
class EnsureCloudflare
{
    public function handle(Request $request, Closure $next): Response
    {
        if (config('security.cloudflare_only') && ! IpUtils::checkIp((string) $request->server('REMOTE_ADDR'), config('security.cloudflare_ips'))) {
            return response('Forbidden', 403, ['Content-Type' => 'text/plain']);
        }

        return $next($request);
    }
}
