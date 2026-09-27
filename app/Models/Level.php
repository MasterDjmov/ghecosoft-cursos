<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;

#[Fillable(['number', 'xp_required'])]
class Level extends Model
{
    public static function forXp(int $xp): ?self
    {
        return static::where('xp_required', '<=', $xp)->orderByDesc('number')->first();
    }
}
