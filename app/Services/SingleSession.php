<?php

namespace App\Services;

use App\Models\User;
use App\Notifications\PlatformNotification;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;

/**
 * Sesión única para alumnos (D65): al entrar, la sesión se queda con la cuenta y las demás se
 * cierran en su próximo pedido. Si pasa seguido (EVICTIONS_TO_WARN en 24 h), se avisa al docente,
 * que decide si pausa la cuenta. El docente no tiene esta regla.
 */
class SingleSession
{
    public const EVICTIONS_TO_WARN = 3;

    public const SESSION_KEY = 'single_session_token';

    /** Aviso que ve en el login quien quedó afuera (se guarda en la sesión, no como flash, para que llegue). */
    public const NOTICE_KEY = 'auth_notice';

    public static function applies(?User $user): bool
    {
        // Solo alumnos: el administrador y los docentes (D72) pueden tener varias sesiones.
        return $user !== null && $user->isStudent();
    }

    /** Esta sesión pasa a ser la de la cuenta (las otras quedan afuera). */
    public function claim(User $user, Request $request): void
    {
        $token = Str::random(40);
        $user->forceFill(['session_token' => $token])->saveQuietly();
        $request->session()->put(self::SESSION_KEY, $token);
    }

    public function isCurrent(User $user, Request $request): bool
    {
        return $user->session_token !== null
            && hash_equals($user->session_token, (string) $request->session()->get(self::SESSION_KEY));
    }

    /** La cuenta se abrió en otro lado: se cierra esta sesión, se anota y, si se repite, se avisa. */
    public function evict(User $user, Request $request): void
    {
        DB::table('session_evictions')->insert([
            'user_id' => $user->id,
            'ip' => $request->ip(),
            'user_agent' => Str::limit((string) $request->userAgent(), 250, ''),
            'created_at' => now(),
        ]);

        if ($this->recentEvictions($user) === self::EVICTIONS_TO_WARN) {
            PlatformNotification::toAdmins(new PlatformNotification(
                'shared-account',
                '¿Cuenta compartida? '.$user->fullName(),
                'Su cuenta se abrió en otro lugar '.self::EVICTIONS_TO_WARN.' veces en 24 horas y fue cerrando la sesión anterior. Mirá el detalle y, si hace falta, pausala y reseteale la clave.',
                route('admin.students.show', $user),
                'shield-exclamation',
            ));
        }

        $this->logout($request, 'Tu cuenta se abrió en otro dispositivo, así que cerramos esta sesión. Si no fuiste vos, avisale al profe.');
    }

    public function recentEvictions(User $user): int
    {
        return DB::table('session_evictions')->where('user_id', $user->id)->where('created_at', '>=', now()->subDay())->count();
    }

    /** Cuenta pausada por el docente: afuera, con el aviso. */
    public function rejectBlocked(Request $request): void
    {
        $this->logout($request, 'Tu cuenta está pausada. Escribile al profe para reactivarla.');
    }

    /** El docente pausa: se cortan todas las sesiones abiertas (el token deja de coincidir). */
    public function block(User $user): void
    {
        $user->forceFill(['blocked_at' => now(), 'session_token' => Str::random(40), 'remember_token' => Str::random(60)])->saveQuietly();
    }

    public function unblock(User $user): void
    {
        $user->forceFill(['blocked_at' => null])->saveQuietly();
    }

    private function logout(Request $request, string $notice): void
    {
        // logout() también borra la cookie de "recordarme" de este navegador: no vuelve a entrar solo.
        Auth::guard('web')->logout();
        $request->session()->invalidate();
        $request->session()->regenerateToken();
        $request->session()->put(self::NOTICE_KEY, $notice);
    }
}
