<?php

namespace App\Models;

use App\Enums\BranchKind;
use App\Enums\CourseLevel;
use App\Enums\Language;
use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\Relations\HasOne;
use Illuminate\Support\Facades\Storage;

#[Fillable(['title', 'slug', 'short_description', 'description', 'language', 'level', 'syllabus', 'logo', 'cover', 'is_published', 'is_featured', 'is_upcoming', 'position', 'root_price', 'subscription_days'])]
class Course extends Model
{
    /** Mismos valores por defecto que la base. */
    protected $attributes = ['language' => 'python', 'level' => 'beginner', 'is_published' => false, 'is_featured' => false, 'is_upcoming' => false, 'position' => 0, 'root_price' => 10, 'subscription_days' => 30];

    use HasFactory;

    protected function casts(): array
    {
        return [
            'language' => Language::class,
            'level' => CourseLevel::class,
            'is_published' => 'boolean',
            'is_featured' => 'boolean',
            'is_upcoming' => 'boolean',
            'root_price' => 'integer',
            'subscription_days' => 'integer',
        ];
    }

    public function getRouteKeyName(): string
    {
        return 'slug';
    }

    /** "Próximamente": se muestra como adelanto pero no se abre (si se publica, deja de serlo). */
    public function isUpcoming(): bool
    {
        return $this->is_upcoming && ! $this->is_published;
    }

    /** Publicados y "Próximamente": lo que se muestra en el catálogo. */
    public function scopeInCatalog(Builder $query): void
    {
        $query->where(fn ($q) => $q->where('is_published', true)->orWhere('is_upcoming', true));
    }

    /** Temario corto: un tema por línea. */
    public function syllabusItems(): array
    {
        return array_values(array_filter(array_map('trim', preg_split('/\R/', (string) $this->syllabus))));
    }

    public function coverUrl(): ?string
    {
        return $this->cover ? Storage::disk('public')->url($this->cover) : null;
    }

    public function interests(): HasMany
    {
        return $this->hasMany(CourseInterest::class);
    }

    public function logoUrl(): ?string
    {
        return $this->logo ? Storage::disk('public')->url($this->logo) : null;
    }

    public function cohorts(): HasMany
    {
        return $this->hasMany(Cohort::class);
    }

    public function branches(): HasMany
    {
        return $this->hasMany(Branch::class)->orderBy('position');
    }

    /** Sendas con algún nodo publicado: el temario del catálogo las muestra como opcionales. */
    public function paths(): HasMany
    {
        return $this->branches()
            ->where('kind', BranchKind::Path)
            ->whereHas('nodes', fn ($q) => $q->where('is_published', true));
    }

    public function nodes(): HasMany
    {
        return $this->hasMany(Node::class);
    }

    public function rootNode(): HasOne
    {
        return $this->hasOne(Node::class)->where('type', 'root');
    }

    public function currency(): HasOne
    {
        return $this->hasOne(Currency::class);
    }

    public function subscriptions(): HasMany
    {
        return $this->hasMany(CourseSubscription::class);
    }

    public function glossaryTerms(): HasMany
    {
        return $this->hasMany(GlossaryTerm::class);
    }
}
