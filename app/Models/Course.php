<?php

namespace App\Models;

use App\Enums\Language;
use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\Relations\HasOne;

#[Fillable(['title', 'slug', 'short_description', 'description', 'language', 'logo', 'cover', 'is_published', 'position', 'root_price', 'subscription_days'])]
class Course extends Model
{
    /** Mismos valores por defecto que la base. */
    protected $attributes = ['language' => 'python', 'is_published' => false, 'position' => 0, 'root_price' => 10, 'subscription_days' => 30];

    use HasFactory;

    protected function casts(): array
    {
        return [
            'language' => Language::class,
            'is_published' => 'boolean',
            'root_price' => 'integer',
            'subscription_days' => 'integer',
        ];
    }

    public function getRouteKeyName(): string
    {
        return 'slug';
    }

    public function cohorts(): HasMany
    {
        return $this->hasMany(Cohort::class);
    }

    public function branches(): HasMany
    {
        return $this->hasMany(Branch::class)->orderBy('position');
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
