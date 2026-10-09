<?php

namespace App\Models;

use App\Enums\Language;
use App\Support\LocalCodeRunner;
use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Support\Facades\Storage;

/**
 * Una micro-misión (D84 § 3): un paso corto del nodo con escena, pista de Gheco, desafío y recompensa.
 * Se comprueba sola (salida esperada) y solo da premios de juego: nunca monedas del curso ni aperturas.
 */
#[Fillable(['node_id', 'code', 'language', 'position', 'title', 'place', 'characters', 'creature', 'card_title', 'card_body', 'xp_reward', 'gold_reward', 'item', 'image_path', 'scene', 'hint', 'challenge', 'starter_code', 'sample_input', 'checks', 'expected_output', 'solution', 'success_text', 'unlocks', 'image_prompt'])]
class NodeStep extends Model
{
    /** Mismos valores por defecto que la base. */
    protected $attributes = ['position' => 0, 'xp_reward' => 0, 'gold_reward' => 0];

    /** La solución nunca sale en un array o JSON (como las del docente, D37). */
    protected $hidden = ['solution'];

    protected function casts(): array
    {
        return ['position' => 'integer', 'xp_reward' => 'integer', 'gold_reward' => 'integer'];
    }

    public function node(): BelongsTo
    {
        return $this->belongsTo(Node::class);
    }

    public function completions(): HasMany
    {
        return $this->hasMany(NodeStepCompletion::class);
    }

    /** Con qué se ejecuta: su propio lenguaje (SQL en un curso de Java) o el del curso. */
    public function runLanguage(Course $course): Language
    {
        return ($this->language ? Language::tryFrom($this->language) : null) ?? $course->language;
    }

    public function imageUrl(): ?string
    {
        return $this->image_path ? Storage::disk('public')->url($this->image_path) : null;
    }

    /** Lo que se compara: igual que en la corrección asistida y en el navegador (LocalCodeRunner::normalize). */
    public static function normalizeOutput(?string $text): string
    {
        return LocalCodeRunner::normalize((string) $text);
    }

    public function accepts(?string $output): bool
    {
        return self::normalizeOutput($output) === self::normalizeOutput($this->expected_output);
    }
}
