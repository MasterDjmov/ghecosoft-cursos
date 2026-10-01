<?php

namespace App\Http\Controllers;

use App\Models\Course;
use App\Models\GlossaryTerm;
use App\Models\Setting;
use App\Services\Ranking;
use App\Support\Glossary;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;

/**
 * Portada pública: qué es, los cursos que más se dictan, "Próximamente", la compañía y sus enemigos,
 * las monedas de cada curso y el top 10 de héroes. Solo datos públicos.
 */
class LandingController
{
    /**
     * Retratos propios de la portada (public/img/personajes), los de la compañía en versión redonda, y qué
     * hace cada uno si el Diccionario no lo dice. El resto sale del Diccionario general con su retrato.
     */
    private const IMAGES = [
        'hero.name' => 'kira', 'mentor.name' => 'profe', 'companion.theory' => 'mia', 'companion.uses' => 'bron',
        'companion.errors' => 'zed', 'companion.guild' => 'gremio',
        'beast.slime' => 'slime', 'beast.goblin' => 'goblin', 'beast.skeleton' => 'esqueleto', 'beast.orc' => 'orco',
        'beast.ogre' => 'ogro', 'beast.troll' => 'troll', 'beast.dragon' => 'dragon',
    ];

    private const ROLES = [
        'hero.name' => 'La heroína del camino. Cuando empezás, le ponés tu nombre.',
        'mentor.name' => 'El mentor: te guía de punta a punta y corrige tus misiones.',
        'companion.theory' => 'Te explica la teoría de cada paso.',
        'companion.uses' => 'Te cuenta para qué sirve en el mundo real.',
        'companion.errors' => 'Te muestra los errores de siempre y cómo salir.',
        'companion.guild' => 'Te da encargos extra que pagan comodines.',
    ];

    /**
     * Los personajes del Diccionario general con ese prefijo (los de fábrica y las claves propias), en el
     * orden del catálogo, y después los propios de cada curso publicado (Ofidia, la mentora de Python). Sin
     * retrato no se muestran.
     *
     * @param  list<string>  $prefixes
     */
    private function cast(Glossary $glossary, array $prefixes): Collection
    {
        $keys = collect(array_keys(config('glossary')))
            ->merge(GlossaryTerm::whereNull('course_id')->pluck('key'))
            ->unique()
            ->filter(fn (string $key) => Str::startsWith($key, $prefixes) || in_array($key, $prefixes, true));

        $general = $keys->map(function (string $key) use ($glossary) {
            $term = $glossary->resolve($key);
            $image = isset(self::IMAGES[$key]) ? asset('img/personajes/'.self::IMAGES[$key].'.webp')
                : ($term['icon_path'] ? Storage::disk('public')->url($term['icon_path']) : null);

            return ['image' => $image, 'name' => Str::ucfirst($term['singular']), 'role' => $term['short_description'] ?: (self::ROLES[$key] ?? null)];
        });

        // Las líderes de cada curso (mentor.name) van en su propia fila: leaders().
        $own = $glossary->courseCharacters($prefixes, publishedOnly: true)
            ->reject(fn (array $term) => $term['key'] === 'mentor.name')
            ->map(fn (array $term) => [
                'image' => $term['icon_path'] ? Storage::disk('public')->url($term['icon_path']) : null,
                'name' => Str::ucfirst($term['singular']),
                'role' => $term['short_description'] ?: (self::ROLES[$term['key']] ?? null),
            ]);

        return $general->values()->concat($own)
            ->filter(fn (array $character) => $character['image'] !== null)
            ->unique('name')
            ->values();
    }

    /** La líder de cada curso publicado (Ofidia en Python, Elefa en PHP…), con retrato del Diccionario. */
    private function leaders(Glossary $glossary): Collection
    {
        return $glossary->courseCharacters(['mentor.name'], publishedOnly: true)
            ->filter(fn (array $term) => $term['icon_path'] !== null)
            ->map(fn (array $term) => [
                'image' => Storage::disk('public')->url($term['icon_path']),
                'name' => Str::ucfirst($term['singular']),
                'course' => Str::before($term['course']->title, ':'),
                'role' => $term['short_description'],
            ])
            ->values();
    }

    public function __invoke(Ranking $ranking, Glossary $glossary)
    {
        if (auth()->check()) {
            return redirect()->route('home');
        }

        $catalog = Course::inCatalog()
            ->with('paths')
            ->withCount(['nodes as published_nodes_count' => fn ($q) => $q->where('is_published', true)])
            ->orderBy('position')
            ->get();
        $published = $catalog->where('is_published', true);
        $featured = $published->where('is_featured', true);

        $whatsapp = preg_replace('/\D+/', '', (string) Setting::get('whatsapp_number'));

        return view('landing', [
            'courses' => $featured->isNotEmpty() ? $featured : $published,
            'upcoming' => $catalog->filter(fn (Course $course) => $course->isUpcoming()),
            'leaders' => $this->leaders($glossary),
            'crew' => $this->cast($glossary, ['hero.name', 'mentor.name', 'companion.']),
            'beasts' => $this->cast($glossary, ['beast.']),
            'coins' => $published->map(fn (Course $course) => ['course' => $course, ...$glossary->resolve('coin.course', $course)]),
            'top' => $ranking->publicTop(),
            'whatsapp' => $whatsapp !== '' ? $whatsapp : null,
        ]);
    }
}
