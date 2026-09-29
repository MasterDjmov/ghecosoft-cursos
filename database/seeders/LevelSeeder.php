<?php

namespace Database\Seeders;

use App\Models\Level;
use Illuminate\Database\Seeder;

/**
 * 100 niveles con curva XP = 35 · (n − 1)^1.58 (redondeada), pensada para muchos cursos:
 * el primer nodo ya sube al 2, un curso completo deja entre el 15 y el 21,
 * tres cursos rondan el 37 y el 100 (50 000 XP) pide una docena de cursos.
 * Solo toca la XP: los nombres de los rangos (level.N del diccionario) quedan como estén.
 */
class LevelSeeder extends Seeder
{
    public const LEVELS = 100;

    public const MAX_XP = 50000;

    public const CURVE = 1.58;

    public function run(): void
    {
        foreach (self::thresholds() as $number => $xp) {
            Level::updateOrCreate(['number' => $number], ['xp_required' => $xp]);
        }
    }

    /** @return array<int, int> número de nivel => XP necesaria */
    public static function thresholds(): array
    {
        $scale = self::MAX_XP / (self::LEVELS - 1) ** self::CURVE;
        $levels = [1 => 0];
        for ($n = 2; $n <= self::LEVELS; $n++) {
            $raw = $scale * ($n - 1) ** self::CURVE;
            $step = match (true) {
                $raw < 100 => 5,
                $raw < 1000 => 10,
                $raw < 10000 => 50,
                default => 100,
            };
            $levels[$n] = max((int) (round($raw / $step) * $step), $levels[$n - 1] + $step);
        }

        return $levels;
    }
}
