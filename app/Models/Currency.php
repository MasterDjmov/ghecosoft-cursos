<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

#[Fillable(['code', 'course_id', 'is_wildcard'])]
class Currency extends Model
{
    public const WILDCARD = 'wildcard';

    /** El oro del jugador (D84/D89): moneda de juego, una sola para todos los cursos. Nunca abre nodos. */
    public const GOLD = 'gold';

    protected function casts(): array
    {
        return ['is_wildcard' => 'boolean'];
    }

    public static function wildcard(): self
    {
        return static::firstOrCreate(['code' => self::WILDCARD], ['is_wildcard' => true]);
    }

    public static function gold(): self
    {
        return static::firstOrCreate(['code' => self::GOLD], ['is_wildcard' => false]);
    }

    public function isGold(): bool
    {
        return $this->code === self::GOLD;
    }

    /** El nombre de la moneda para mostrar («escamas», «comodines», «oro»). */
    public function label(int $amount = 2): string
    {
        return match (true) {
            $this->isGold() => 'oro',
            $this->is_wildcard => term('coin.wildcard', null, $amount),
            default => term('coin.course', $this->course, $amount),
        };
    }

    public static function forCourse(Course $course): self
    {
        return static::firstOrCreate(['course_id' => $course->id], ['code' => 'course-'.$course->slug]);
    }

    public function course(): BelongsTo
    {
        return $this->belongsTo(Course::class);
    }
}
