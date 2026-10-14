<?php

namespace App\Support;

use App\Models\Course;
use App\Models\CourseSubscription;
use App\Models\Currency;
use App\Models\Item;
use App\Models\ItemMovement;
use App\Models\NodeStep;
use App\Models\User;
use App\Services\Ledger;
use Illuminate\Support\Collection;
use Illuminate\Support\Str;

/**
 * Artefactos y Monedas de la Gran Enciclopedia (D104, etapa 2). Las entradas tienen la misma forma que las de
 * `Encyclopedia` (personajes) para usar la misma pantalla y el mismo modal.
 *
 * Artefactos: todos los ítems de los cursos publicados y los comunes, con **dónde se consigue** armado solo de
 * lo que ya existe: la micro-misión que lo da, la tienda de cada mundo, la receta del taller, la criatura que lo
 * suelta y el botín de las expediciones. Se descubre al tenerlo alguna vez (`item_movements`); hasta entonces,
 * silueta, nombre y dónde se consigue, sin su descripción ni sus bonos.
 * Monedas: la de cada curso, el comodín y el oro, con cómo se ganan y en qué se gastan.
 */
class EncyclopediaItems
{
    public const ARTIFACTS = 'artefactos';

    public const COINS = 'monedas';

    /** El nombre de cada criatura de las expediciones (config('game.creatures')), en plural. */
    private const CREATURES = ['slime' => 'los slimes', 'goblin' => 'los goblins', 'esqueleto' => 'los esqueletos', 'orco' => 'los orcos',
        'troll' => 'los trolls', 'ogro' => 'los ogros', 'dragon' => 'los dragones'];

    /** @var Collection<int, Course>|null */
    private ?Collection $courses = null;

    public function __construct(private readonly User $user) {}

    /** @return Collection<int, array<string, mixed>> */
    public function artifacts(): Collection
    {
        $courses = $this->courses();
        $owned = $this->user->isStaff() ? null : ItemMovement::where('user_id', $this->user->id)->distinct()->pluck('item_id')->flip();
        $items = Item::with('course')->where(fn ($q) => $q->whereNull('course_id')->orWhereIn('course_id', $courses->pluck('id')))->get();
        $sources = $this->sources($items, $courses);
        $uses = $this->uses($items);

        return $items
            ->sortBy(fn (Item $item) => [$item->course_id === null ? 0 : $courses->search(fn ($c) => $c->id === $item->course_id) + 1, $item->kind->value, $item->name])
            ->map(function (Item $item) use ($owned, $sources, $uses) {
                $discovered = $owned === null || $owned->has($item->id);

                return [
                    'key' => 'item-'.$item->code,
                    'name' => $item->name,
                    'section' => self::ARTIFACTS,
                    'group' => $item->course ? Str::before($item->course->title, ':') : 'Comunes a todos los mundos',
                    'course' => $item->course,
                    'portrait' => $item->thumbUrl(),
                    'figure' => $item->imageUrl(),
                    'square' => true,
                    'discovered' => $discovered,
                    'boss' => false,
                    'defeated' => false,
                    'rarity' => $item->rarity,
                    'subtitle' => $item->rarity->label().' · '.$item->kind->label(),
                    'where' => null,
                    'sources' => $sources[$item->id] ?? [],
                    'fields' => $discovered ? array_filter([
                        'Bonos' => implode(' · ', $item->bonuses()),
                        'Qué es' => (string) $item->description,
                        'Nivel mínimo' => $item->min_level > 1 ? (string) $item->min_level : '',
                        'Sirve en el taller para' => implode('; ', $uses[$item->code] ?? []),
                    ]) : [],
                ];
            })->values();
    }

    /** @return Collection<int, array<string, mixed>> */
    public function coins(): Collection
    {
        $ledger = app(Ledger::class);
        $enrolled = CourseSubscription::where('user_id', $this->user->id)->pluck('course_id')->flip();
        $coin = fn (Currency $currency, ?Course $course, string $group, bool $discovered, array $fields, array $sources) => [
            'key' => 'coin-'.$currency->code,
            'name' => Str::ucfirst($currency->label(1)),
            'section' => self::COINS,
            'group' => $group,
            'course' => $course,
            'portrait' => null,
            'figure' => null,
            'currency' => $currency,
            'square' => true,
            'discovered' => $discovered,
            'boss' => false,
            'defeated' => false,
            'subtitle' => $course ? 'Moneda de '.Str::before($course->title, ':') : null,
            'where' => null,
            'sources' => $sources,
            'fields' => $discovered ? [...$fields, 'Tenés' => $ledger->balance($this->user, $currency).' '.$currency->label($ledger->balance($this->user, $currency))] : [],
        ];

        $world = $this->courses()->map(function (Course $course) use ($coin, $enrolled) {
            $world = Str::before($course->title, ':');
            $discovered = $this->user->isStaff() || $enrolled->has($course->id);

            // D106: en las Crónicas en Inglés los episodios se abren sin monedas.
            if ($course->language->isSelfChecked()) {
                return $coin(Currency::forCourse($course), $course, 'Las monedas de los mundos', $discovered, [
                    'Para qué sirve' => 'Es el sello de '.$world.'. Ahí los episodios se abren sin monedas: el primero con el abono y los demás al terminarlo.',
                ], ['Se ve al inscribirte en '.$world.'.']);
            }

            return $coin(Currency::forCourse($course), $course, 'Las monedas de los mundos', $discovered, [
                'Para qué sirve' => 'Para abrir los '.term('node', $course, 2).' de '.$world.'. Solo vale en ese mundo.',
            ], [
                'Al inscribirte en '.$world.' (lo que cuesta la Clase 0).',
                'Al aprobar las '.term('practice', $course, 2).' obligatorias de '.$world.'.',
            ]);
        });

        return collect([
            $coin(Currency::wildcard(), null, 'Las que valen en todos lados', true, [
                'Para qué sirve' => 'Para abrir los '.term('node', null, 2).' extra de cualquier mundo.',
            ], ['Al aprobar las '.term('practice', null, 2).' optativas (los encargos) de cualquier curso.']),
            $coin(Currency::gold(), null, 'Las que valen en todos lados', true, [
                'Para qué sirve' => 'Para comprar en las tiendas, conseguir monturas y mejorar los atributos de tu héroe.',
            ], ['Al superar micro-misiones.', 'Al volver de las expediciones con el botín.']),
        ])->concat($world)->values();
    }

    /**
     * Dónde se consigue cada ítem, en frases: «HTML y CSS · micro-misión «…» («nodo»)», «En el carro de Chispa
     * (C), 40 de oro», «En el taller: 2 × Vidrio y 1 × Plomo», «Lo sueltan los slimes en las expediciones».
     *
     * @return array<int, list<string>>
     */
    private function sources(Collection $items, Collection $courses): array
    {
        $byCode = $items->keyBy('code');
        $out = [];
        $add = function (?Item $item, string $text) use (&$out) {
            if ($item && ! in_array($text, $out[$item->id] ?? [], true)) {
                $out[$item->id][] = $text;
            }
        };

        // Micro-misiones (el `item` de la micro-misión: «Nombre» o «Nombre x3»).
        NodeStep::with('node.course')->whereNotNull('item')->where('item', '!=', '')
            ->whereHas('node', fn ($q) => $q->where('is_published', true)->whereIn('course_id', $courses->pluck('id')))
            ->get()->each(function (NodeStep $step) use ($items, $add) {
                $raw = trim(preg_replace('/\s+x\d+$/iu', '', trim($step->item)));
                $course = $step->node->course;
                $item = $items->first(fn (Item $i) => $i->name === $raw && ($i->course_id === $course->id || $i->course_id === null));
                $add($item, Str::before($course->title, ':').' · micro-misión «'.$step->title.'» («'.$step->node->title.'»)');
            });

        // Tiendas: lo de un mundo, en la suya; lo común, en todas.
        $shops = $courses->mapWithKeys(fn (Course $course) => [$course->id => config('game.protagonists.'.$course->language->value.'.shop.name')])->filter();
        foreach ($items->where('in_shop', true)->whereNotNull('price') as $item) {
            $where = $item->course_id ? (isset($shops[$item->course_id]) ? $shops[$item->course_id].' ('.Str::before($item->course->title, ':').')' : null) : 'cualquier tienda';
            if ($where) {
                $add($item, 'En '.$where.', a '.$item->price.' de oro'.($item->min_level > 1 ? ', desde el nivel '.$item->min_level : '').'.');
            }
        }

        // El taller.
        foreach (config('game.recipes') as $recipe) {
            $needs = collect($recipe['needs'])->map(fn ($n, $code) => $n.' × '.($byCode[$code]->name ?? $code))->join(', ', ' y ');
            foreach ($recipe['gives'] as $code => $n) {
                $add($byCode[$code] ?? null, 'En el taller, con '.$needs.($recipe['min_level'] > 1 ? ' (desde el nivel '.$recipe['min_level'].')' : '').'.');
            }
        }

        // Expediciones: los materiales de las criaturas y el botín al azar.
        foreach (config('game.creatures') as $code => $creature) {
            if (! empty($creature['material'])) {
                $add($byCode[$creature['material']] ?? null, 'Lo sueltan '.(self::CREATURES[$code] ?? $code).' al vencerlos en las expediciones.');
            }
        }
        foreach ($items->where('droppable', true) as $item) {
            $add($item, 'Botín '.Str::lower($item->rarity->label()).' de las expediciones'.($item->course ? ' de '.Str::before($item->course->title, ':') : ' de cualquier mundo').'.');
        }

        return $out;
    }

    /** @return array<string, list<string>> código del ítem → para qué recetas sirve */
    private function uses(Collection $items): array
    {
        $byCode = $items->keyBy('code');
        $out = [];
        foreach (config('game.recipes') as $recipe) {
            $gives = collect($recipe['gives'])->keys()->map(fn ($code) => $byCode[$code]->name ?? $code)->join(', ');
            foreach (array_keys($recipe['needs']) as $code) {
                $out[$code][] = $gives;
            }
        }

        return array_map(fn ($list) => array_values(array_unique($list)), $out);
    }

    /** @return Collection<int, Course> */
    private function courses(): Collection
    {
        return $this->courses ??= Course::where('is_published', true)->orderBy('id')->get();
    }
}
