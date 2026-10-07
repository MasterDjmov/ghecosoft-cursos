<?php

namespace App\Support;

use App\Models\Course;
use App\Models\Setting;
use App\Models\User;

/**
 * Mantenimiento (D86), desde Admin → Configuración. Se lee en cada pedido, sin cron:
 * - de la plataforma: solo el administrador puede entrar; al resto se le cierra la sesión y el login avisa;
 * - de un curso: sus alumnos no entran al curso (detalle, árbol, nodos, misiones) hasta que se reabra.
 */
class Maintenance
{
    public const DEFAULT_MESSAGE = 'Estamos haciendo mejoras en la plataforma. Volvé en un rato: tu progreso está guardado.';

    public const DEFAULT_COURSE_MESSAGE = 'Este curso está en mantenimiento: estamos sumando mejoras. Volvé en un rato: tu progreso está guardado.';

    public static function platform(): bool
    {
        return Setting::get('maintenance_platform') === '1';
    }

    public static function message(): string
    {
        return Setting::get('maintenance_message') ?? self::DEFAULT_MESSAGE;
    }

    /** @return list<int> */
    public static function courseIds(): array
    {
        return array_values(array_filter(array_map('intval', explode(',', (string) Setting::get('maintenance_courses', '')))));
    }

    public static function course(Course $course): bool
    {
        return in_array($course->id, self::courseIds(), true);
    }

    /** Quién sigue entrando con la plataforma en mantenimiento: solo el administrador. */
    public static function letsIn(?User $user): bool
    {
        return ! self::platform() || ($user?->isAdmin() ?? false);
    }

    /** Quién entra a un curso en mantenimiento: el administrador y el docente (para revisarlo). */
    public static function letsIntoCourse(?User $user, Course $course): bool
    {
        return ! self::course($course) || ($user?->isStaff() ?? false);
    }
}
