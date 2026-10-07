<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Support\Collection;

/** El protagonista de un curso en manos de un jugador (D89). Se crea y se mejora solo con `App\Services\Heroes`. */
#[Fillable(['user_id', 'course_id', 'look', 'strength', 'dexterity', 'intelligence', 'luck', 'weapon_item_id', 'armor_item_id', 'accessory_item_id', 'respec_available'])]
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

    protected $attributes = ['look' => 1, 'respec_available' => false];

    protected function casts(): array
    {
        return [
            'look' => 'integer',
            'strength' => 'integer',
            'dexterity' => 'integer',
            'intelligence' => 'integer',
            'luck' => 'integer',
            'respec_available' => 'boolean',
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

    /** Lo que suma el equipo puesto a un campo (un atributo, `attack` o `defense`). */
    public function bonus(string $field): int
    {
        return $this->equipment()->sum(fn (Item $item) => (int) $item->{$field});
    }

    /** El atributo con el equipo. */
    public function total(string $stat): int
    {
        return max(1, $this->{$stat} + $this->bonus($stat));
    }

    /** Vida: sale de la Fuerza (con el equipo). */
    public function hp(): int
    {
        return 50 + 10 * $this->total('strength');
    }

    /** Maná: sale de la Inteligencia (con el equipo). */
    public function mp(): int
    {
        return 20 + 5 * $this->total('intelligence');
    }

    /** @return Collection<string, Item> lo que tiene puesto, por columna */
    public function equipment(): Collection
    {
        return collect(['weapon_item_id' => $this->weapon, 'armor_item_id' => $this->armor, 'accessory_item_id' => $this->accessory])->filter();
    }

    public function weapon(): BelongsTo
    {
        return $this->belongsTo(Item::class, 'weapon_item_id');
    }

    public function armor(): BelongsTo
    {
        return $this->belongsTo(Item::class, 'armor_item_id');
    }

    public function accessory(): BelongsTo
    {
        return $this->belongsTo(Item::class, 'accessory_item_id');
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
