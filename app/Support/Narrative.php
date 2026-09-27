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
            'heroe' => $user?->heroName() ?? term('hero.name', $course),
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

    /** Reemplaza los marcadores y pasa el texto a HTML (markdown). */
    public static function render(?string $text, ?Course $course = null, ?User $user = null): string
    {
        return Markdown::render(self::fill($text, $course, $user));
    }
}
