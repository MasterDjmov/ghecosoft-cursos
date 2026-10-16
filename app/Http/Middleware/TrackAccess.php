<?php

namespace App\Http\Middleware;

use App\Support\DeviceInfo;
use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Symfony\Component\HttpFoundation\Response;

/**
 * Anota desde dónde entra cada alumno (celular, tablet o compu), una vez por sesión y por día; si en el día
 * vuelve a entrar con otra sesión, suma una entrada. El staff no se anota.
 */
class TrackAccess
{
    public const SESSION_KEY = 'access_tracked_on';

    public function handle(Request $request, Closure $next): Response
    {
        $user = $request->user();
        if ($user && $user->isStudent() && $request->hasSession()
            && $request->session()->get(self::SESSION_KEY) !== ($today = now()->toDateString())) {
            $info = DeviceInfo::parse($request->userAgent());
            $now = now();
            DB::table('user_accesses')->upsert(
                [['user_id' => $user->id, 'accessed_on' => $today, ...$info, 'requests' => 1, 'first_at' => $now, 'last_at' => $now]],
                ['user_id', 'accessed_on', 'device', 'os', 'browser'],
                ['requests' => DB::raw('requests + 1'), 'last_at' => $now],
            );
            $request->session()->put(self::SESSION_KEY, $today);
        }

        return $next($request);
    }
}
