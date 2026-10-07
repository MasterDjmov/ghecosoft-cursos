<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

/** El protagonista de un curso en manos de un jugador (D89). Se crea y se mejora solo con `App\Services\Heroes`. */
#[Fillable(['user_id', 'course_id', 'look', 'strength', 'dexterity', 'intelligence', 'luck'])]
class Hero extends Model
{
    /** Los atributos, en el orden en que se muestran. */
    public const STATS = ['strength', 'dexterity', 'intelligence', 'luck'];

    /** Puntos para repartir al tomar el control, y el mínimo y el máximo de cada atributo en ese reparto. */
    public const POINTS = 24;

    public const MIN_STAT = 4;

    public const MAX_START = 12;

    /** Tope de un atributo subido con oro. */
    public const MAX_STAT = 99;

    public const LOOKS = 6;

    protected $attributes = ['look' => 1];

    protected function casts(): array
    {
        return [
            'look' => 'integer',
            'strength' => 'integer',
            'dexterity' => 'integer',
            'intelligence' => 'integer',
            'luck' => 'integer',
        ];
    }

    public static function statLabel(string $stat): string
    {
        return match ($stat) {
            'strength' => 'Fuerza',
            'dexterity' => 'Destreza',
            'intelligence' => 'Inteligencia',
            'luck' => 'Suerte',
        };
    }

    /** Qué hace cada atributo en el juego (lo que se le explica al jugador). */
    public static function statHelp(string $stat): string
    {
        return match ($stat) {
            'strength' => 'Golpes más fuertes y más vida.',
            'dexterity' => 'Pegás primero y esquivás más.',
            'intelligence' => 'Hechizos más fuertes y más maná.',
            'luck' => 'Más golpes críticos y mejor botín.',
        };
    }

    public static function statShort(string $stat): string
    {
        return match ($stat) {
            'strength' => 'FUE',
            'dexterity' => 'DES',
            'intelligence' => 'INT',
            'luck' => 'SUE',
        };
    }

    /** Vida: sale de la Fuerza. */
    public function hp(): int
    {
        return 50 + 10 * $this->strength;
    }

    /** Maná: sale de la Inteligencia. */
    public function mp(): int
    {
        return 20 + 5 * $this->intelligence;
    }

    /** Lo que cuesta subir un punto: 100 × el valor actual (JUEGO.md § 6). */
    public function upgradeCost(string $stat): int
    {
        return 100 * $this->{$stat};
    }

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function course(): BelongsTo
    {
        return $this->belongsTo(Course::class);
    }
}
