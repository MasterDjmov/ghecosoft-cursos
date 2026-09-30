<?php

namespace App\Http\Middleware;

use App\Services\SingleSession;
use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

/**
 * Sesión única para alumnos (D65). Al iniciar sesión (Login marca «claim»), esta sesión se queda con
 * la cuenta; en cada pedido se compara con la de la cuenta y, si otra entró después, esta queda afuera.
 * Una cuenta pausada por el docente no puede usar la plataforma.
 */
class EnsureSingleSession
{
    public function __construct(private readonly SingleSession $sessions) {}

    public function handle(Request $request, Closure $next): Response
    {
        $user = $request->user();
        if (! SingleSession::applies($user)) {
            return $next($request);
        }

        if ($user->blocked_at) {
            $this->sessions->rejectBlocked($request);

            return $this->out($request);
        }

        // Recién entró (o la cuenta todavía no tenía sesión registrada): esta es la sesión de la cuenta.
        if ($request->session()->pull('single_session_claim') || $user->session_token === null) {
            $this->sessions->claim($user, $request);

            return $next($request);
        }

        if (! $this->sessions->isCurrent($user, $request)) {
            $this->sessions->evict($user, $request);

            return $this->out($request);
        }

        return $next($request);
    }

    private function out(Request $request): Response
    {
        // Livewire: 419 hace que la página se recargue y ahí llega al login con el aviso.
        if ($request->hasHeader('X-Livewire') || $request->expectsJson()) {
            abort(419);
        }

        return redirect()->route('login');
    }
}
