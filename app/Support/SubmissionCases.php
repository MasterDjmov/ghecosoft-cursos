<?php

namespace App\Support;

use App\Enums\SubmissionMode;
use App\Models\Submission;

/**
 * Los casos con los que se prueba una entrega al corregirla (D73): el ejemplo de la práctica (si tiene
 * salida esperada) y sus pruebas extra. Solo para quien corrige: las pruebas extra nunca van a una vista
 * del alumno. Corren en el navegador del docente (o, en Java, en su compu): nunca en el servidor.
 */
class SubmissionCases
{
    /** Lenguajes que el docente puede ejecutar al corregir (Python, C/C++ D66, PHP D68, Java D69). */
    public const LANGUAGES = ['python', 'c', 'cpp', 'php', 'java'];

    /** @return list<array{label: string, input: string, expected: string}> */
    public static function for(Submission $submission): array
    {
        $practice = $submission->practice;
        $language = $practice->node->course->language->value;

        if (blank($submission->code)
            || ! in_array($language, self::LANGUAGES, true)
            || in_array($practice->submission_mode, [SubmissionMode::File, SubmissionMode::None], true)) {
            return [];
        }

        $cases = [];
        if (filled($practice->expected_output)) {
            $cases[] = ['label' => 'Ejemplo', 'input' => (string) $practice->sample_input, 'expected' => $practice->expected_output];
        }
        foreach ($practice->tests as $test) {
            $cases[] = ['label' => $test->name, 'input' => (string) $test->input, 'expected' => $test->expected_output];
        }

        return $cases;
    }

    /**
     * Guarda lo que dieron las pruebas (lo manda el navegador de quien corrige). Si los números no
     * cuadran con los casos de la entrega, no se guarda nada.
     */
    public static function store(Submission $submission, int $passed, int $total): bool
    {
        if ($total < 1 || $total !== count(self::for($submission)) || $passed < 0 || $passed > $total) {
            return false;
        }
        $submission->forceFill(['check_result' => ['passed' => $passed, 'total' => $total, 'at' => now()->toIso8601String()]])->save();

        return true;
    }
}
