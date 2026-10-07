<?php

namespace App\Http\Middleware;

use App\Support\Maintenance;
use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Symfony\Component\HttpFoundation\Response;

/**
 * Plataforma en mantenimiento (D86): a quien no es administrador se le cierra la sesión y vuelve al login,
 * que muestra el aviso. Las páginas públicas (inicio, CV) se siguen viendo.
 */
class EnsurePlatformOpen
{
    public function handle(Request $request, Closure $next): Response
    {
        $user = $request->user();
        if ($user === null || Maintenance::letsIn($user)) {
            return $next($request);
        }

        Auth::guard('web')->logout();
        $request->session()->invalidate();
        $request->session()->regenerateToken();
        $request->session()->flash('status', Maintenance::message());

        // Livewire: 419 hace que la página se recargue y ahí llega al login con el aviso.
        if ($request->hasHeader('X-Livewire') || $request->expectsJson()) {
            abort(419);
        }

        return redirect()->route('login');
    }
}
