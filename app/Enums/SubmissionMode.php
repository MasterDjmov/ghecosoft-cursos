<?php

namespace App\Enums;

enum SubmissionMode: string
{
    case Code = 'code';
    case File = 'file';
    case Both = 'both';
    case None = 'none';

    public function label(): string
    {
        return match ($this) {
            self::Code => 'Código',
            self::File => 'Archivo',
            self::Both => 'Código y archivo',
            self::None => 'Sin entrega',
        };
    }
}
