<?php

namespace App\Models;

use App\Enums\NodeType;
use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Illuminate\Database\Eloquent\Relations\HasMany;

#[Fillable(['course_id', 'code', 'branch_id', 'parent_id', 'type', 'title', 'position', 'price', 'price_currency_id', 'badge_id', 'video_url', 'chronicle', 'objectives', 'before_you_start', 'content', 'example_code', 'example_language', 'example_runnable', 'expected_output', 'sample_input', 'use_cases', 'common_errors', 'beast_key', 'topics', 'uses', 'self_check', 'teacher_solutions', 'pos_x', 'pos_y', 'is_published'])]
class Node extends Model
{
    /** Mismos valores por defecto que la base. */
    protected $attributes = ['type' => 'topic', 'position' => 0, 'price' => 0, 'is_published' => true, 'example_runnable' => true];

    /** Solo del docente: nunca sale en un array o JSON (D37). */
    protected $hidden = ['teacher_solutions'];

    protected function casts(): array
    {
        return [
            'type' => NodeType::class,
            'price' => 'integer',
            'is_published' => 'boolean',
            'example_runnable' => 'boolean',
            'self_check' => 'array',
            // Universo de cursos (D70): temas del catálogo que enseña y que da por sabidos.
            'topics' => 'array',
            'uses' => 'array',
        ];
    }

    /**
     * Prueba del sello: preguntas con su respuesta (autoevaluación sin nota).
     *
     * @return list<array{question: string, answer: string}>
     */
    public function selfCheckItems(): array
    {
        return array_values(array_filter($this->self_check ?? [], fn ($item) => filled($item['question'] ?? null)));
    }

    /**
     * Requisitos extra (Fase 8): nodos que también hay que completar, además del padre.
     */
    public function requirements(): BelongsToMany
    {
        return $this->belongsToMany(Node::class, 'node_requirements', 'node_id', 'required_node_id')->withTimestamps();
    }

    /** Lo que cuenta para "curso completado": ni extras ni nodos de ramas optativas (extras o Sendas). */
    public function scopeTrunk(Builder $query): void
    {
        $query->where('type', '!=', NodeType::Extra)
            ->where(fn ($q) => $q->whereNull('branch_id')->orWhereHas('branch', fn ($b) => $b->where('is_extra', false)));
    }

    public function isRoot(): bool
    {
        return $this->type === NodeType::Root;
    }

    public function isBoss(): bool
    {
        return $this->type === NodeType::Boss;
    }

    public function unlocks(): HasMany
    {
        return $this->hasMany(NodeUnlock::class);
    }

    /** Algún alumno ya lo abrió o entregó una hoja: borrarlo se llevaría su historial. */
    public function hasStudentActivity(): bool
    {
        return $this->unlocks()->exists()
            || Submission::whereIn('practice_id', Practice::where('node_id', $this->id)->select('id'))->exists();
    }

    public function course(): BelongsTo
    {
        return $this->belongsTo(Course::class);
    }

    public function branch(): BelongsTo
    {
        return $this->belongsTo(Branch::class);
    }

    public function parent(): BelongsTo
    {
        return $this->belongsTo(Node::class, 'parent_id');
    }

    public function children(): HasMany
    {
        return $this->hasMany(Node::class, 'parent_id');
    }

    public function priceCurrency(): BelongsTo
    {
        return $this->belongsTo(Currency::class, 'price_currency_id');
    }

    /** Insignia que entrega el jefe al completarse. */
    public function badge(): BelongsTo
    {
        return $this->belongsTo(Badge::class);
    }

    public function practices(): HasMany
    {
        return $this->hasMany(Practice::class)->orderBy('position');
    }

    public function resources(): HasMany
    {
        return $this->hasMany(NodeResource::class)->orderBy('position');
    }

    /** Moneda con la que se paga: la indicada en el nodo o, si no, la del curso. */
    public function paymentCurrency(): Currency
    {
        return $this->priceCurrency ?? Currency::forCourse($this->course);
    }
}
