<?php

namespace App\Enums;

enum RankingDisplay: string
{
    case Name = 'name';
    case Nickname = 'nickname';

    public function label(): string
    {
        return match ($this) {
            self::Name => 'Nombre',
            self::Nickname => 'Apodo',
        };
    }
}
