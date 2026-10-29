<?php

namespace App\Models;

use App\Enums\ConsumerRequestKind;
use App\Enums\ConsumerRequestStatus;
use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Support\Str;

/** D112: arrepentimiento o baja pedidos desde el pie de página, con su código de trámite. */
#[Fillable(['kind', 'user_id', 'name', 'contact', 'course', 'details'])]
class ConsumerRequest extends Model
{
    /** Mismos valores por defecto que la base. */
    protected $attributes = ['status' => 'pending'];

    protected static function booted(): void
    {
        static::creating(function (self $request) {
            $prefix = $request->kind === ConsumerRequestKind::Cancellation ? 'B-' : 'A-';
            do {
                $request->code = $prefix.Str::upper(Str::random(8));
            } while (static::where('code', $request->code)->exists());
        });
    }

    protected function casts(): array
    {
        return [
            'kind' => ConsumerRequestKind::class,
            'status' => ConsumerRequestStatus::class,
            'handled_at' => 'datetime',
        ];
    }

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function handler(): BelongsTo
    {
        return $this->belongsTo(User::class, 'handled_by');
    }
}
