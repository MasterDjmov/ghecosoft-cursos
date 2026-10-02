<?php

namespace App\Support;

use App\Models\Course;
use App\Models\GlossaryTerm;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Storage;
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
        $general = $this->termsFor(null)[$key] ?? null;
        $term = ($course ? $this->termsFor($course->id)[$key] ?? null : null) ?? $general;

        // Las claves llevan punto (coin.course): no se puede usar config('glossary.coin.course').
        $default = config('glossary')[$key] ?? null;
        $singular = $term['singular'] ?? $default['singular'] ?? $this->fallback($key, $course);

        return [
            'singular' => $singular,
            // El plural en español no se deduce: si no está cargado, se repite el singular.
            'plural' => $term['plural'] ?? $default['plural'] ?? $singular,
            'gender' => $term['gender'] ?? $default['gender'] ?? 'm',
            // Sin retrato propio en el curso, el del Diccionario general si es el mismo personaje (el slime de
            // todos los cursos); si el curso lo renombró (su mentor es Ofidia, no «el profe»), no.
            'icon_path' => $term['icon_path']
                ?? (Str::lower($general['singular'] ?? '') === Str::lower($singular) ? $general['icon_path'] ?? null : null),
            'short_description' => $term['short_description'] ?? null,
            // Algunas historias traen texto de fábrica (el prólogo de Mis Crónicas, D80).
            'lore' => $term['lore'] ?? $default['lore'] ?? null,
        ];
    }

    /**
     * El fondo del mundo (16:9) de un curso: la imagen de su región (world.region del curso) o, si no tiene,
     * la del Mundo del Código (world.name del General). Null si ninguna tiene imagen.
     */
    public function scene(?Course $course = null): ?string
    {
        $path = ($course ? $this->termsFor($course->id)['world.region']['icon_path'] ?? null : null)
            ?? $this->termsFor(null)['world.name']['icon_path'] ?? null;

        return $path ? Storage::disk('public')->url($path) : null;
    }

    /**
     * Los personajes propios de cada curso (Ofidia, la mentora de Python): términos de un curso con ese
     * prefijo que se llaman distinto que en el general, y por eso no heredan su retrato.
     *
     * @param  list<string>  $prefixes
     * @return Collection<int, array{course: Course, key: string, singular: string, short_description: ?string, icon_path: ?string}>
     */
    public function courseCharacters(array $prefixes, bool $publishedOnly = false): Collection
    {
        $courses = Course::query()->when($publishedOnly, fn ($q) => $q->where('is_published', true))->orderBy('position')->get();

        return $courses->flatMap(fn (Course $course) => GlossaryTerm::where('course_id', $course->id)
            ->where(fn ($q) => collect($prefixes)->each(fn ($prefix) => $q->orWhere('key', 'like', $prefix.'%')))
            ->orderBy('key')
            ->get()
            ->filter(fn (GlossaryTerm $term) => Str::lower($this->resolve($term->key)['singular']) !== Str::lower($term->singular))
            ->map(fn (GlossaryTerm $term) => [
                'course' => $course,
                'key' => $term->key,
                'singular' => $term->singular,
                'short_description' => $term->short_description,
                'icon_path' => $term->icon_path,
            ]))->values();
    }

    /** Nombre técnico en español para claves sin valor: "Nivel 3" para level.3. */
    private function fallback(string $key, ?Course $course): string
    {
        if (preg_match('/^level\.(\d+)$/', $key, $match)) {
            return Str::ucfirst($this->term('level', $course)).' '.$match[1];
        }

        return Str::headline($key);
    }

    /** De dónde sale el valor: 'course', 'general', 'default' o null (no existe en ningún lado). */
    public function source(string $key, ?Course $course = null): ?string
    {
        return match (true) {
            $course !== null && isset($this->termsFor($course->id)[$key]) => 'course',
            isset($this->termsFor(null)[$key]) => 'general',
            isset(config('glossary')[$key]) => 'default',
            default => null,
        };
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
