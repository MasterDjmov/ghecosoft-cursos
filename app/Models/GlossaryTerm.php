<?php

namespace App\Models;

use App\Enums\Gender;
use App\Support\Glossary;
use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

#[Fillable(['key', 'course_id', 'singular', 'plural', 'gender', 'icon_path', 'figure_path', 'short_description', 'lore'])]
class GlossaryTerm extends Model
{
    protected static function booted(): void
    {
        $flush = fn (GlossaryTerm $term) => Glossary::flush($term->course_id);

        static::saved($flush);
        static::deleted($flush);
    }

    protected function casts(): array
    {
        return ['gender' => Gender::class];
    }

    public function course(): BelongsTo
    {
        return $this->belongsTo(Course::class);
    }
}
