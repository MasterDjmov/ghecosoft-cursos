<?php

namespace App\Http\Middleware;

use App\Enums\Role;
use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

/** Uso: ->middleware('role:admin') o, para varios roles, ->middleware('role:admin,teacher') */
class EnsureRole
{
    public function handle(Request $request, Closure $next, string ...$roles): Response
    {
        if (in_array($request->user()?->role, array_map(fn ($role) => Role::from($role), $roles), true)) {
            return $next($request);
        }

        // Quien abre una dirección que no es para su rol (un marcador a /admin, un link viejo)
        // vuelve a su inicio en vez de ver un 403. Fuera de una página común, sigue el 403.
        abort_if($request->user() === null || ! $request->isMethod('GET') || $request->expectsJson(), 403);

        return redirect()->route('home');
    }
}
