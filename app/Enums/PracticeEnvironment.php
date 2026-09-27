<?php

namespace App\Enums;

/** Dónde se resuelve una práctica: en el editor de la plataforma o en la compu del alumno. */
enum PracticeEnvironment: string
{
    case Browser = 'browser';
    case Local = 'local';

    public function label(): string
    {
        return match ($this) {
            self::Browser => 'Navegador',
            self::Local => 'Local',
        };
    }

    public function hint(?SubmissionMode $mode = null): string
    {
        return match (true) {
            $this === self::Browser => 'Se resuelve en el editor de la plataforma.',
            $mode === SubmissionMode::None => 'Se hace en tu compu, fuera de la plataforma. Cuando esté, marcala como completada.',
            $mode === SubmissionMode::Code => 'Se resuelve en tu compu (con lo que instalaste); después pegá el código acá.',
            default => 'Se resuelve en tu compu (con lo que instalaste) y se entrega el archivo.',
        };
    }
}
