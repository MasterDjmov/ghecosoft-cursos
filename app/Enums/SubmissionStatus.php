<?php

namespace App\Enums;

enum SubmissionStatus: string
{
    case Submitted = 'submitted';
    case Approved = 'approved';
    case Redo = 'redo';

    public function label(): string
    {
        return match ($this) {
            self::Submitted => 'Entregada',
            self::Approved => 'Aprobada',
            self::Redo => 'Rehacer',
        };
    }
}
