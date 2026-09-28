<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;
use Illuminate\Validation\ValidationException;
use Symfony\Component\HttpFoundation\Response;

/**
 * Límite de intentos para los formularios de cuenta (login, olvidé mi clave,
 * nueva clave, confirmar clave). Lo que falla se muestra como error del
 * formulario, no como una página 429.
 *
 * El login además tiene el límite de Fortify: 5 intentos fallidos por minuto
 * para el mismo usuario desde la misma IP. Este suma el tope por IP, que frena
 * probar muchos usuarios distintos.
 */
class ThrottleAuthForms
{
    /** Ruta => [campo del error, intentos, ventana en segundos, por usuario logueado]. */
    private const LIMITS = [
        'login.store' => ['login', 20, 60, false],
        'passkey.login' => ['login', 20, 60, false],
        'password.email' => ['email', 5, 600, false],
        'password.update' => ['email', 10, 600, false],
        'password.confirm.store' => ['password', 5, 60, true],
    ];

    public function handle(Request $request, Closure $next): Response
    {
        $limit = self::LIMITS[$request->route()?->getName()] ?? null;

        if (! $limit || ! $request->isMethod('post')) {
            return $next($request);
        }

        [$field, $attempts, $seconds, $perUser] = $limit;
        $key = 'auth-form:'.$request->route()->getName().':'.($perUser ? 'user:'.$request->user()?->id : 'ip:'.$request->ip());

        if (RateLimiter::tooManyAttempts($key, $attempts)) {
            throw ValidationException::withMessages([
                $field => __('auth.throttle', ['seconds' => RateLimiter::availableIn($key)]),
            ]);
        }
        RateLimiter::hit($key, $seconds);

        return $next($request);
    }
}
