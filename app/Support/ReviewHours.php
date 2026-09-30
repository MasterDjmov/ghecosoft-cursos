<?php

namespace App\Support;

use Carbon\CarbonInterface;

/**
 * El horario en que el docente corrige (hora de Argentina, la de la app). Una entrega
 * fuera de ese horario se revisa en el próximo turno: al alumno se le avisa cuándo.
 */
class ReviewHours
{
    public const OPENS = 8;

    public const CLOSES = 22;

    public static function isOutside(CarbonInterface $at): bool
    {
        return $at->hour < self::OPENS || $at->hour >= self::CLOSES;
    }

    /** El día en que se revisa lo entregado en $at, o null si se entregó en horario. */
    public static function reviewDay(CarbonInterface $at): ?CarbonInterface
    {
        if (! self::isOutside($at)) {
            return null;
        }

        return $at->hour >= self::CLOSES ? $at->copy()->addDay()->startOfDay() : $at->copy()->startOfDay();
    }

    /** Aviso para el alumno: «el profe la revisa mañana (01/10) entre las 8 y las 22 h». Null en horario. */
    public static function notice(CarbonInterface $at): ?string
    {
        $day = self::reviewDay($at);
        if ($day === null) {
            return null;
        }
        $when = match (true) {
            $day->isToday() => 'hoy',
            $day->isTomorrow() => 'mañana ('.$day->format('d/m').')',
            default => 'el '.$day->format('d/m'),
        };

        return 'La entregaste fuera del horario de corrección: el profe la revisa '.$when.' entre las '.self::OPENS.' y las '.self::CLOSES.' h.';
    }
}
