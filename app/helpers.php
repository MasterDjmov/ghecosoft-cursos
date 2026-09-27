<?php

use App\Models\Course;
use App\Support\Glossary;

if (! function_exists('term')) {
    /** Nombre narrativo de una clave del diccionario: term('coin.course', $course, 3) → "escamas". */
    function term(string $key, ?Course $course = null, int $count = 1): string
    {
        return app(Glossary::class)->term($key, $course, $count);
    }
}
