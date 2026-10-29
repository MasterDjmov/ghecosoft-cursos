<?php

namespace App\Console\Commands;

use Illuminate\Console\Attributes\Description;
use Illuminate\Console\Attributes\Signature;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;

/**
 * D113 (minimización, Ley 25.326): borra la IP y el navegador de las sesiones cerradas por entrar en otro lado
 * (session_evictions) y los accesos por dispositivo (user_accesses) más viejos que el plazo de la Privacidad.
 * Sin cron: lo corre deploy.sh en cada actualización.
 */
#[Signature('app:prune-access-logs {--months=12 : Cuántos meses se guardan}')]
#[Description('Borra los registros de acceso (IP, dispositivo y navegador) más viejos que el plazo de la Privacidad')]
class PruneAccessLogs extends Command
{
    public function handle(): int
    {
        $months = max(1, (int) $this->option('months'));
        $limit = now()->subMonths($months);

        $evictions = DB::table('session_evictions')->where('created_at', '<', $limit)->delete();
        $accesses = DB::table('user_accesses')->where('accessed_on', '<', $limit->toDateString())->delete();

        $this->info("Borrados {$evictions} cierres de sesión y {$accesses} accesos de más de {$months} meses.");

        return self::SUCCESS;
    }
}
