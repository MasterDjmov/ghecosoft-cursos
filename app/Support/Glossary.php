<?php

namespace App\Support;

use App\Models\Course;
use App\Models\GlossaryTerm;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Str;

/**
 * Resuelve los nombres narrativos: término del curso → término general →
 * valor por defecto (config/glossary.php) → la clave tal cual.
 */
class Glossary
{
    public static function cacheKey(?int $courseId): string
    {
        return 'glossary.'.($courseId ?? 'general');
    }

    public static function flush(?int $courseId): void
    {
        Cache::forget(self::cacheKey($courseId));
    }

    /** @return array{singular: string, plural: string, gender: string, icon_path: ?string, short_description: ?string, lore: ?string} */
    public function resolve(string $key, ?Course $course = null): array
    {
        $term = ($course ? $this->termsFor($course->id)[$key] ?? null : null)
            ?? $this->termsFor(null)[$key]
            ?? null;

        // Las claves llevan punto (coin.course): no se puede usar config('glossary.coin.course').
        $default = config('glossary')[$key] ?? null;
        $singular = $term['singular'] ?? $default['singular'] ?? Str::headline($key);

        return [
            'singular' => $singular,
            'plural' => $term['plural'] ?? $default['plural'] ?? Str::plural($singular),
            'gender' => $term['gender'] ?? $default['gender'] ?? 'm',
            'icon_path' => $term['icon_path'] ?? null,
            'short_description' => $term['short_description'] ?? null,
            'lore' => $term['lore'] ?? null,
        ];
    }

    public function term(string $key, ?Course $course = null, int $count = 1): string
    {
        $term = $this->resolve($key, $course);

        return abs($count) === 1 ? $term['singular'] : $term['plural'];
    }

    /** @return array<string, array<string, mixed>> */
    private function termsFor(?int $courseId): array
    {
        return Cache::rememberForever(self::cacheKey($courseId), fn () => GlossaryTerm::query()
            ->where('course_id', $courseId)
            ->get()
            ->mapWithKeys(fn (GlossaryTerm $term) => [$term->key => [
                'singular' => $term->singular,
                'plural' => $term->plural,
                'gender' => $term->gender->value,
                'icon_path' => $term->icon_path,
                'short_description' => $term->short_description,
                'lore' => $term->lore,
            ]])
            ->all());
    }
}
