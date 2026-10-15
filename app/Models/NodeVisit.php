<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

/** D107: un alumno miró un nodo un día (una fila por día, con cuántas veces entró). */
#[Fillable(['user_id', 'node_id', 'course_id', 'visited_on', 'views', 'first_at', 'last_at'])]
class NodeVisit extends Model
{
    public $timestamps = false;

    protected $attributes = ['views' => 1];

    protected function casts(): array
    {
        return ['visited_on' => 'date', 'first_at' => 'datetime', 'last_at' => 'datetime'];
    }

    public function node(): BelongsTo
    {
        return $this->belongsTo(Node::class);
    }
}
