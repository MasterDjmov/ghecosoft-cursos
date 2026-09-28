<?php

namespace App\Http\Controllers;

use App\Models\User;
use App\Support\CvData;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;
use Symfony\Component\HttpFoundation\Response;

/**
 * CV público: /cv/{link}. El link es propio del CV (nombre + código al azar) y no
 * revela el usuario de login. Se ve solo si el alumno lo compartió (y, si es menor,
 * con la autorización aprobada); si no, "Este perfil es privado" sin revelar ni el
 * nombre. Si el alumno activó el código de acceso, primero se pide el código. El
 * dueño y el docente lo ven siempre (vista previa).
 */
class CvController extends Controller
{
    /** Después de poner bien el código, ese navegador lo ve sin pedirlo por este tiempo. */
    private const ACCESS_MINUTES = 120;

    /** Intentos con código incorrecto: por compu (cada 10 min) y por CV (por hora, entre todas las compus). */
    private const TRIES_PER_IP = 5;

    private const TRIES_PER_CV = 30;

    public function show(Request $request, string $slug): Response
    {
        $user = $this->visible($slug);
        if (! $user) {
            return response()->view('cv.private', [], 404);
        }

        if ($this->needsCode($request, $user)) {
            return response()->view('cv.code', ['slug' => $slug, 'blocked' => $this->blockedFor($request, $user)]);
        }

        return response()->view('cv.show', [
            ...CvData::for($user),
            'preview' => ! $user->hasPublicProfile(),
        ]);
    }

    public function unlock(Request $request, string $slug): Response|RedirectResponse
    {
        $user = $this->visible($slug);
        if (! $user || ! $user->cv_code) {
            return response()->view('cv.private', [], 404);
        }

        if ($seconds = $this->blockedFor($request, $user)) {
            return back()->withErrors(['code' => 'Demasiados intentos. Probá de nuevo en '.ceil($seconds / 60).' minutos.']);
        }

        $code = preg_replace('/\D+/', '', (string) $request->input('code'));
        if (! hash_equals($user->cv_code, $code)) {
            RateLimiter::hit($this->ipKey($request, $user), 600);
            RateLimiter::hit($this->cvKey($user), 3600);

            return back()->withErrors(['code' => 'El código no es correcto.']);
        }

        RateLimiter::clear($this->ipKey($request, $user));
        $request->session()->put($this->sessionKey($user), ['hash' => $this->codeHash($user), 'until' => now()->addMinutes(self::ACCESS_MINUTES)->timestamp]);

        return redirect()->route('cv.show', $slug);
    }

    /** El alumno del link, si su CV se puede mostrar (público, o lo mira el dueño o el docente). */
    private function visible(string $slug): ?User
    {
        $user = User::where('cv_slug', $slug)->first();
        $viewer = auth()->user();
        $isOwnerOrAdmin = $user && $viewer && ($viewer->id === $user->id || $viewer->isAdmin());

        return $user && $user->isStudent() && ($user->hasPublicProfile() || $isOwnerOrAdmin) ? $user : null;
    }

    private function needsCode(Request $request, User $user): bool
    {
        $viewer = $request->user();
        if (! $user->cv_code || ($viewer && ($viewer->id === $user->id || $viewer->isAdmin()))) {
            return false;
        }

        // Un código nuevo invalida los accesos que dio el anterior.
        $access = $request->session()->get($this->sessionKey($user));

        return ! ($access && hash_equals($access['hash'], $this->codeHash($user)) && $access['until'] > now()->timestamp);
    }

    /** Segundos que faltan para poder volver a probar (0 = puede). */
    private function blockedFor(Request $request, User $user): int
    {
        return max(
            RateLimiter::tooManyAttempts($this->ipKey($request, $user), self::TRIES_PER_IP) ? RateLimiter::availableIn($this->ipKey($request, $user)) : 0,
            RateLimiter::tooManyAttempts($this->cvKey($user), self::TRIES_PER_CV) ? RateLimiter::availableIn($this->cvKey($user)) : 0,
        );
    }

    private function ipKey(Request $request, User $user): string
    {
        return 'cv-code:'.$user->id.':'.$request->ip();
    }

    private function cvKey(User $user): string
    {
        return 'cv-code:'.$user->id;
    }

    private function sessionKey(User $user): string
    {
        return 'cv_access.'.$user->id;
    }

    private function codeHash(User $user): string
    {
        return hash_hmac('sha256', $user->id.'|'.$user->cv_code, (string) config('app.key'));
    }
}
