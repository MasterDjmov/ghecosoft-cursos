<?php

namespace App\Enums;

/** Rarezas con marco gris, azul, violeta y dorado (D84 § 7). */
enum ItemRarity: string
{
    case Common = 'common';
    case Rare = 'rare';
    case Epic = 'epic';
    case Legendary = 'legendary';

    public function label(): string
    {
        return match ($this) {
            self::Common => 'Común',
            self::Rare => 'Raro',
            self::Epic => 'Épico',
            self::Legendary => 'Legendario',
        };
    }

    /** Clases del marco y del texto. */
    public function classes(): string
    {
        return match ($this) {
            self::Common => 'border-zinc-500/60 text-zinc-300',
            self::Rare => 'border-sky-400/70 text-sky-300',
            self::Epic => 'border-violet-400/70 text-violet-300',
            self::Legendary => 'border-amber-400/80 text-amber-300',
        };
    }
}
