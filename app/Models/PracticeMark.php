<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;

#[Fillable(['user_id', 'practice_id', 'completed_at'])]
class PracticeMark extends Model
{
    public $timestamps = false;

    protected function casts(): array
    {
        return ['completed_at' => 'datetime'];
    }
}
