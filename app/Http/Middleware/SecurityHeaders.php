<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

/**
 * Cabeceras de seguridad para todas las páginas: no se puede meter la plataforma
 * en un iframe ajeno, el navegador no adivina tipos de archivo y no se filtran
 * URLs completas a otros sitios. Una respuesta que ya trae la suya la conserva.
 */
class SecurityHeaders
{
    public function handle(Request $request, Closure $next): Response
    {
        $response = $next($request);

        $headers = [
            'X-Content-Type-Options' => 'nosniff',
            'X-Frame-Options' => 'SAMEORIGIN',
            'Referrer-Policy' => 'strict-origin-when-cross-origin',
            // El micrófono, solo para la propia plataforma: el extra «Decilo en voz alta» de inglés (D106, INGLES.md
            // § 4 bis). Va en todas las páginas porque wire:navigate conserva la cabecera de la primera que se cargó.
            // Los iframes del código del alumno (sandbox sin permisos) y los sitios ajenos siguen sin él, y el navegador
            // igual le pide permiso a quien lo usa.
            'Permissions-Policy' => 'camera=(), microphone=(self), geolocation=(), payment=(), usb=()',
        ];

        // Con HTTPS, el navegador no vuelve a entrar por HTTP durante un año.
        if ($request->isSecure()) {
            $headers['Strict-Transport-Security'] = 'max-age=31536000';
        }

        foreach ($headers as $name => $value) {
            if (! $response->headers->has($name)) {
                $response->headers->set($name, $value);
            }
        }

        return $response;
    }
}
