<?php

namespace App\Support;

use App\Models\Badge;
use App\Models\Level;

/** Lo que ganó el alumno con una aprobación (para el aviso). */
class Reward
{
    public int $coins = 0;

    public ?string $coinName = null;

    public int $xp = 0;

    public bool $nodeCompleted = false;

    public ?Badge $badge = null;

    public ?int $newLevel = null;

    public function summary(): string
    {
        $parts = [];
        if ($this->coins > 0) {
            $parts[] = "+{$this->coins} {$this->coinName}";
        }
        if ($this->xp > 0) {
            $parts[] = "+{$this->xp} ".term('xp.short');
        }
        if ($this->nodeCompleted) {
            $parts[] = ucfirst(term('node')).' completado';
        }
        if ($this->badge) {
            $parts[] = 'insignia «'.$this->badge->name.'»';
        }
        if ($this->newLevel) {
            $parts[] = '¡subiste a '.Level::where('number', $this->newLevel)->first()?->name().'!';
        }

        return implode(' · ', $parts);
    }
}
