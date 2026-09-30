<?php

namespace App\Listeners;

use App\Services\SingleSession;
use Illuminate\Auth\Events\Login;

/** Al iniciar sesión (con clave, passkey o "recordarme"), la próxima vuelta del middleware la registra como la sesión de la cuenta (D65). */
class ClaimSingleSession
{
    public function handle(Login $event): void
    {
        if (SingleSession::applies($event->user) && app()->bound('session.store')) {
            session()->put('single_session_claim', true);
        }
    }
}
