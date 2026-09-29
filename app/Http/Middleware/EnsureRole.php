<?php

namespace App\Http\Middleware;

use App\Enums\Role;
use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

/** Uso: ->middleware('role:admin') */
class EnsureRole
{
    public function handle(Request $request, Closure $next, string $role): Response
    {
        if ($request->user()?->role === Role::from($role)) {
            return $next($request);
        }

        // Quien abre una dirección que no es para su rol (un marcador a /admin, un link viejo)
        // vuelve a su inicio en vez de ver un 403. Fuera de una página común, sigue el 403.
        abort_if($request->user() === null || ! $request->isMethod('GET') || $request->expectsJson(), 403);

        return redirect()->route('home');
    }
}
