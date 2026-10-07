<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

/** La montura del jugador (D91): la especie es cosmética; el nivel acorta las expediciones. */
#[Fillable(['user_id', 'species', 'level'])]
class Mount extends Model
{
    protected $attributes = ['level' => 1];

    protected function casts(): array
    {
        return ['level' => 'integer'];
    }

    public function name(): string
    {
        return config('game.mounts.species.'.$this->species, $this->species);
    }

    public function reduction(): int
    {
        return (int) config('game.mounts.levels.'.$this->level.'.reduction', 0);
    }

    public static function imageUrl(string $species, int $level): string
    {
        return asset('img/monturas/'.$species.'/n'.$level.'.webp');
    }

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}
