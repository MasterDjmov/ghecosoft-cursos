<?php

namespace App\Support;

use App\Enums\NodeType;
use App\Models\Course;
use App\Models\Currency;
use App\Models\Mount;
use App\Models\Node;
use App\Models\NodeUnlock;
use App\Models\User;
use App\Services\Heroes;
use Illuminate\Support\Collection;
use Illuminate\Support\Str;

/**
 * Clases, Monturas y Reinos de la Gran Enciclopedia (D104, etapa 3). Las entradas tienen la misma forma que
 * las de `Encyclopedia` y `EncyclopediaItems` para usar la misma pantalla y el mismo modal.
 *
 * Clases: cada curso publicado, siempre visible (es la puerta de entrada): su mundo, su guía, su protagonista,
 * su moneda y cuántos nodos tiene. Monturas: las especies de `config('game.mounts')` con sus cinco niveles; se
 * descubre la que tiene el jugador. Reinos: el fondo y el mapa de cada mundo, su guía y los lugares de las
 * expediciones; se descubre al abrir el raíz de ese curso. Lo no descubierto no manda su texto.
 */
class EncyclopediaWorlds
{
    public const CLASSES = 'clases';

    public const MOUNTS = 'monturas';

    public const REALMS = 'reinos';

    /** @var Collection<int, Course>|null */
    private ?Collection $courses = null;

    public function __construct(private readonly User $user) {}

    /** @return Collection<int, array<string, mixed>> */
    public function classes(): Collection
    {
        return $this->courses()->map(function (Course $course) {
            $world = Str::before($course->title, ':');
            $hero = Heroes::protagonistOf($course);
            $nodes = Node::where('course_id', $course->id)->where('is_published', true)->count();
            $currency = Currency::forCourse($course);

            return $this->entry(self::CLASSES, 'clase-'.$course->slug, $world, 'Los cursos del Mundo del Código', $course, true, [
                'portrait' => $course->logoUrl(),
                'square' => true,
                'subtitle' => term('world.region', $course),
                'fields' => array_filter([
                    'De qué se trata' => (string) $course->short_description,
                    'Región' => term('world.region', $course),
                    'Guía' => term('mentor.name', $course),
                    'Protagonista' => $hero ? $hero['name'].', '.Str::lcfirst($hero['title']) : '',
                    'Moneda' => $course->language->isSelfChecked() ? '' : Str::ucfirst($currency->label(2)),
                    'Tamaño' => $nodes.' '.term('node', $course, $nodes),
                ]),
                'sources' => [$this->enrolled($course) ? 'Ya estás cursando '.$world.'.' : 'Se abre al inscribirte en '.$world.'.'],
            ]);
        })->values();
    }

    /** @return Collection<int, array<string, mixed>> */
    public function mounts(): Collection
    {
        $staff = $this->user->isStaff();
        $mine = Mount::where('user_id', $this->user->id)->value('species');
        $levels = config('game.mounts.levels');
        $first = $levels[1];
        $how = 'En los Establos: desde el nivel '.$first['min_level'].' del jugador, por '.$first['price'].' de oro. Después se mejora hasta el nivel '.array_key_last($levels).'.';

        return collect(config('game.mounts.species'))->map(function (string $name, string $species) use ($staff, $mine, $levels, $how) {
            $discovered = $staff || $mine === $species;

            return $this->entry(self::MOUNTS, 'montura-'.$species, $name, 'Las monturas', null, $discovered, [
                'portrait' => Mount::imageUrl($species, 1),
                'figure' => Mount::imageUrl($species, 5),
                'square' => true,
                'subtitle' => $mine === $species ? 'Tu montura' : null,
                'gallery' => $discovered ? collect($levels)->keys()->map(fn (int $level) => ['url' => Mount::imageUrl($species, $level), 'label' => 'n'.$level])->all() : [],
                'fields' => $discovered ? array_filter([
                    'Cómo es' => (string) config('game.mounts.about.'.$species, ''),
                    'Qué hace' => 'Acorta las expediciones: '.collect($levels)->map(fn ($l, $n) => 'n'.$n.' −'.$l['reduction'].' %')->join(', ', ' y ').'. La especie no cambia el efecto; el nivel, sí.',
                ]) : [],
                'sources' => [$how, 'La especie se puede cambiar cuando quieras, sin perder el nivel.'],
            ]);
        })->values();
    }

    /** @return Collection<int, array<string, mixed>> */
    public function realms(): Collection
    {
        $glossary = app(Glossary::class);

        return $this->courses()->map(function (Course $course) use ($glossary) {
            $world = Str::before($course->title, ':');
            $discovered = $this->user->isStaff() || $this->rootOpen($course);
            $expeditions = Heroes::protagonistOf($course)['expeditions'] ?? null;
            $map = isset($expeditions['map']) ? asset($expeditions['map']) : null;
            $places = collect($expeditions['places'] ?? []);

            return $this->entry(self::REALMS, 'reino-'.$course->slug, term('world.region', $course), 'Las regiones del Mundo del Código', $course, $discovered, [
                'portrait' => $glossary->scene($course) ?? $map,
                'figure' => $map ?? $glossary->scene($course),
                'subtitle' => $world,
                'fields' => $discovered ? array_filter([
                    'Su lengua' => $world,
                    'Quién la guía' => term('mentor.name', $course),
                    'Lugares' => $places->map(fn ($place) => '**'.$place['name'].'** (nivel '.$place['level'].'): '.$place['text'])->join("\n\n"),
                ]) : [],
                'sources' => [$discovered ? 'Sus lugares se recorren en las expediciones de '.$world.'.' : 'Se abre al empezar '.$world.' (al abrir su '.term('node.root', $course).').'],
            ]);
        })->values();
    }

    /** @param  array<string, mixed>  $extra */
    private function entry(string $section, string $key, string $name, string $group, ?Course $course, bool $discovered, array $extra): array
    {
        return [
            'key' => $key,
            'name' => $name,
            'section' => $section,
            'group' => $group,
            'course' => $course,
            'portrait' => null,
            'figure' => null,
            'square' => false,
            'discovered' => $discovered,
            'boss' => false,
            'defeated' => false,
            'subtitle' => null,
            'where' => null,
            'sources' => [],
            'fields' => [],
            ...$extra,
        ];
    }

    private function enrolled(Course $course): bool
    {
        return $this->user->subscriptions()->where('course_id', $course->id)->exists();
    }

    private function rootOpen(Course $course): bool
    {
        return NodeUnlock::where('user_id', $this->user->id)
            ->whereIn('node_id', Node::where('course_id', $course->id)->where('type', NodeType::Root)->select('id'))
            ->exists();
    }

    /** @return Collection<int, Course> */
    private function courses(): Collection
    {
        return $this->courses ??= Course::where('is_published', true)->orderBy('id')->get();
    }
}
