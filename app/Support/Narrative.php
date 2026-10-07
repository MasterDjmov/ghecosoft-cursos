<?php

namespace App\Support;

use App\Models\Course;
use App\Models\User;
use Illuminate\Support\Str;

/**
 * Marcadores de los textos del curso: {heroe}, {mentor}, {mundo} y {region}.
 * Se reemplazan antes del markdown, así una crónica escrita una vez sirve para
 * cualquier alumno y cualquier nombre que cargue el docente en el diccionario.
 */
class Narrative
{
    public static function fill(?string $text, ?Course $course = null, ?User $user = null): ?string
    {
        if ($text === null || ! str_contains($text, '{')) {
            return $text;
        }

        $user ??= auth()->user();
        $values = [
            'heroe' => self::hero($course, $user),
            'mentor' => term('mentor.name', $course),
            'mundo' => term('world.name', $course),
            'region' => term('world.region', $course),
        ];

        // {heroe} o {héroe}, en cualquier combinación de mayúsculas.
        return preg_replace_callback('/\{(h[eé]roe|mentor|mundo|regi[oó]n)\}/iu', function ($match) use ($values) {
            $key = Str::lower(Str::ascii($match[1]));

            return $values[$key];
        }, $text);
    }

    /**
     * {heroe} (D84 § 1): en un curso con protagonista, el protagonista (Mia en Python); en los textos generales
     * (el prólogo), el jugador: su nombre de héroe si eligió uno, o su nombre.
     */
    public static function hero(?Course $course, ?User $user): string
    {
        if ($course && ($protagonist = config('game.protagonists.'.$course->language->value))) {
            return $protagonist['name'];
        }
        if ($course === null && $user) {
            return $user->hero_name ?: Str::before(trim((string) $user->name), ' ') ?: $user->heroName();
        }

        return $user?->heroName() ?? term('hero.name', $course);
    }

    /** Reemplaza los marcadores y pasa el texto a HTML (markdown). */
    public static function render(?string $text, ?Course $course = null, ?User $user = null): string
    {
        return Markdown::render(self::fill($text, $course, $user));
    }
}
