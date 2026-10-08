<?php

namespace App\Services;

use App\Enums\CoinReason;
use App\Enums\ItemKind;
use App\Enums\ItemReason;
use App\Models\Course;
use App\Models\CourseSubscription;
use App\Models\Currency;
use App\Models\Expedition;
use App\Models\Hero;
use App\Models\Item;
use App\Models\Mount;
use App\Models\Node;
use App\Models\User;
use Illuminate\Support\Carbon;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;
use InvalidArgumentException;
use Random\Engine\Mt19937;
use Random\Randomizer;

/**
 * Las expediciones (D91, JUEGO.md § 8). El héroe sale a un lugar abierto del mapa; al volver, el servidor
 * calcula la exploración y las peleas con una semilla fija por expedición (siempre da lo mismo), y paga el
 * botín: oro por el Ledger, materiales e ítems por la mochila. Si pierde, vuelve sin botín. Sin código del
 * alumno y sin cron: se resuelve cuando el jugador vuelve a mirar.
 */
class Expeditions
{
    /** La criatura → su clave en el diccionario (el nombre en cada mundo). */
    private const TERMS = ['slime' => 'beast.slime', 'goblin' => 'beast.goblin', 'esqueleto' => 'beast.skeleton', 'orco' => 'beast.orc',
        'troll' => 'beast.troll', 'ogro' => 'beast.ogre', 'dragon' => 'beast.dragon'];

    public function __construct(
        private readonly TreeAccess $access,
        private readonly Ledger $ledger,
        private readonly Inventory $inventory,
        private readonly Heroes $heroes,
    ) {}

    /** @return array<string, mixed>|null la configuración de expediciones del mundo */
    public function world(Course $course): ?array
    {
        return $this->heroes->protagonist($course)['expeditions'] ?? null;
    }

    private function node(Course $course, string $code): ?Node
    {
        return $course->nodes()->where('code', $code)->first();
    }

    /**
     * Quien cursa el curso de ese mundo (tiene o tuvo su abono) explora su mapa avanzando en el curso. Los
     * demás jugadores también pueden explorarlo con cualquiera de sus héroes: los lugares se les abren por su
     * nivel de jugador (cursos en paralelo).
     */
    public function studies(User $user, Course $course): bool
    {
        return CourseSubscription::where('user_id', $user->id)->where('course_id', $course->id)->exists();
    }

    /** Los mundos con mapa (para elegir dónde explorar). @return Collection<int, Course> */
    public function worlds(): Collection
    {
        return Course::orderBy('position')->get()->filter(fn (Course $course) => $this->world($course) !== null)->values();
    }

    /** Tiene un héroe de otro curso: viene a explorar este mapa (cursos en paralelo). */
    public function explorer(User $user, Course $course): bool
    {
        return Hero::where('user_id', $user->id)->where('course_id', '!=', $course->id)->exists();
    }

    /**
     * Abierto: a quien cursa ese curso, al completar el nodo `opens_after` (en el Valle, la Posada); a quien
     * tiene un héroe de otro curso, ya (nunca queda peor por cursar los dos).
     */
    public function isOpen(User $user, Course $course): bool
    {
        $world = $this->world($course);
        if (! $world) {
            return false;
        }
        if ($user->isStaff() || $this->explorer($user, $course)) {
            return true;
        }
        $node = $this->node($course, $world['opens_after']);

        return $this->studies($user, $course) && $node && $this->access->isCompleted($user, $node);
    }

    /**
     * Los lugares del mapa, abiertos (su nodo completo) o no.
     *
     * @return Collection<int, array<string, mixed>>
     */
    public function places(User $user, Course $course): Collection
    {
        $nodes = $course->nodes()->get(['id', 'code', 'title', 'course_id', 'type', 'is_published'])->keyBy('code');
        $studies = $this->studies($user, $course);
        $explorer = $this->explorer($user, $course);
        $level = Inventory::playerLevel($user);

        return collect($this->world($course)['places'] ?? [])->map(function (array $place) use ($user, $nodes, $studies, $explorer, $level) {
            $node = $nodes[$place['node']] ?? null;
            // Avanzando en el curso del mapa, o (con un héroe de otro curso) llegando a su nivel de jugador.
            $open = $user->isStaff()
                || ($studies && $node && $this->access->isCompleted($user, $node))
                || ($explorer && $level >= (int) $place['level']);

            return [...$place, 'node_title' => $node?->title, 'by_level' => $explorer && ! $studies, 'open' => $open];
        });
    }

    public function creatureName(string $code, ?Course $course): string
    {
        return isset(self::TERMS[$code]) ? term(self::TERMS[$code], $course) : $code;
    }

    public static function creatureImage(string $code): string
    {
        return asset('img/personajes/'.$code.'.webp');
    }

    public function todayCount(User $user): int
    {
        return Expedition::where('user_id', $user->id)->where('started_at', '>=', now()->startOfDay())->count();
    }

    public function active(User $user): ?Expedition
    {
        return Expedition::where('user_id', $user->id)->whereNull('resolved_at')->latest('id')->first();
    }

    /** Segundos que dura: los minutos del largo, menos lo que acorta la montura (y la velocidad de prueba local). */
    public function seconds(User $user, string $length): int
    {
        $minutes = (int) config('game.expedition.lengths.'.$length.'.minutes');
        $reduction = Mount::where('user_id', $user->id)->first()?->reduction() ?? 0;
        $seconds = (int) round($minutes * 60 * (100 - $reduction) / 100);

        return max(1, intdiv($seconds, max(1, (int) config('game.expedition.speed', 1))));
    }

    /**
     * Las 3 expediciones del momento (corta, media y larga) a lugares abiertos. Salen de una semilla con el
     * jugador, la media hora en curso y cuántas lleva hoy: se renuevan al salir y cada media hora, y no se
     * pueden «tirar de nuevo» recargando.
     *
     * @return list<array<string, mixed>>
     */
    public function offers(User $user, Course $course): array
    {
        $open = $this->places($user, $course)->where('open', true)->values();
        if ($open->isEmpty() || ! $this->isOpen($user, $course)) {
            return [];
        }
        $random = new Randomizer(new Mt19937(crc32($user->id.'|'.$this->slot().'|'.$this->todayCount($user).'|'.$course->id)));
        $offers = [];
        foreach (array_keys(config('game.expedition.lengths')) as $index => $length) {
            // Las largas prefieren los lugares más difíciles que ya abrió.
            $pool = $length === 'long' ? $open->sortByDesc('level')->take(4)->values() : $open;
            $place = $pool[$random->getInt(0, $pool->count() - 1)];
            $offers[] = [
                'index' => $index,
                'length' => $length,
                'label' => config('game.expedition.lengths.'.$length.'.label'),
                'place' => $place,
                'seconds' => $this->seconds($user, $length),
                'gold' => (int) round(config('game.expedition.lengths.'.$length.'.gold') * (1 + 0.1 * ($place['level'] - 1))),
            ];
        }

        return $offers;
    }

    /** La media hora en curso (el número de tanda): cambia sola con el reloj. */
    private function slot(): int
    {
        return intdiv(now()->timestamp, max(1, (int) config('game.expedition.refresh_minutes')) * 60);
    }

    /** Cuándo se sortean las próximas 3. */
    public function nextRefresh(): Carbon
    {
        return Carbon::createFromTimestamp(($this->slot() + 1) * max(1, (int) config('game.expedition.refresh_minutes')) * 60);
    }

    /**
     * Mandar al héroe a una de las 3 expediciones del momento. Con `$place` (el lugar que vio el jugador), si
     * justo se renovaron, no lo manda a otro lugar sin avisar.
     */
    public function start(User $user, Hero $hero, int $index, ?string $place = null, ?Course $world = null): Expedition
    {
        if ($hero->user_id !== $user->id) {
            throw new InvalidArgumentException('Ese héroe no es tuyo.');
        }
        // El mapa: el del mundo elegido (cualquier héroe puede ir a cualquier mapa), o el de su propio curso.
        $course = $world ?? $hero->course;
        if (! $this->isOpen($user, $course)) {
            throw new InvalidArgumentException('Las expediciones de este mundo todavía no se abrieron.');
        }

        return DB::transaction(function () use ($user, $hero, $course, $index, $place) {
            User::whereKey($user->id)->lockForUpdate()->first();
            if ($this->active($user)) {
                throw new InvalidArgumentException('Ya hay una expedición en camino: esperá a que vuelva.');
            }
            if ($this->todayCount($user) >= (int) config('game.expedition.per_day')) {
                throw new InvalidArgumentException('Ya hiciste las '.config('game.expedition.per_day').' expediciones de hoy. Mañana hay más.');
            }
            $offer = $this->offers($user, $course)[$index] ?? null;
            if (! $offer) {
                throw new InvalidArgumentException('Esa expedición ya no está.');
            }
            if ($place !== null && $offer['place']['code'] !== $place) {
                throw new InvalidArgumentException('Las expediciones se renovaron: elegí una de las nuevas.');
            }

            return Expedition::create([
                'user_id' => $user->id, 'hero_id' => $hero->id, 'course_id' => $course->id,
                'place' => $offer['place']['code'], 'length' => $offer['length'],
                'started_at' => now(), 'ends_at' => now()->addSeconds($offer['seconds']),
            ]);
        });
    }

    /** Cuando ya volvió: calcula la exploración y las peleas, y paga el botín. Una sola vez. */
    public function resolve(Expedition $expedition): Expedition
    {
        return DB::transaction(function () use ($expedition) {
            $locked = Expedition::whereKey($expedition->id)->lockForUpdate()->firstOrFail();
            if ($locked->resolved_at || now()->lessThan($locked->ends_at)) {
                return $locked;
            }
            $hero = Hero::with(['course', 'user', 'weapon', 'armor', 'accessory'])->findOrFail($locked->hero_id);
            $result = $this->simulate($locked, $hero);

            $user = $hero->user;
            foreach ($result['potions'] as $itemId => $count) {
                $this->inventory->take($user, Item::findOrFail($itemId), $count, ItemReason::Used, $locked, 'Tomada en la expedición');
            }
            if ($result['won']) {
                if ($result['rewards']['gold'] > 0) {
                    $this->ledger->credit($user, Currency::gold(), $result['rewards']['gold'], CoinReason::ExpeditionLoot, $locked, $hero->course,
                        $this->placeName($locked->course ?? $hero->course, $locked->place));
                }
                foreach ($result['rewards']['items'] as $loot) {
                    $this->inventory->grant($user, Item::findOrFail($loot['id']), $loot['quantity'], ItemReason::Loot, $locked);
                }
            }
            $locked->update(['resolved_at' => now(), 'won' => $result['won'], 'log' => $result['log'], 'rewards' => $result['rewards']]);

            return $locked;
        });
    }

    /** El Reloj de Arena: la expedición en camino termina ya (se gasta uno). */
    public function hurry(User $user): Expedition
    {
        $hourglass = Item::where('code', Item::HOURGLASS)->first();

        return DB::transaction(function () use ($user, $hourglass) {
            User::whereKey($user->id)->lockForUpdate()->first();
            $active = $this->active($user);
            if (! $active || $active->isReady()) {
                throw new InvalidArgumentException('No hay ninguna expedición en camino.');
            }
            if (! $hourglass || $this->inventory->available($user, $hourglass) < 1) {
                throw new InvalidArgumentException('No tenés un Reloj de Arena.');
            }
            $this->inventory->take($user, $hourglass, 1, ItemReason::Used, $active, 'Terminó la expedición al instante');
            $active->update(['ends_at' => now()]);

            return $active;
        });
    }

    public function placeName(Course $course, string $code): string
    {
        return collect($this->world($course)['places'] ?? [])->firstWhere('code', $code)['name'] ?? $code;
    }

    /**
     * La aventura entera, turno por turno (pura: no escribe nada).
     *
     * @return array{won: bool, log: list<array<string, mixed>>, rewards: array<string, mixed>, potions: array<int, int>}
     */
    public function simulate(Expedition $expedition, Hero $hero): array
    {
        $course = $hero->course;
        $map = $expedition->course ?? $course;
        $place = collect($this->world($map)['places'] ?? [])->firstWhere('code', $expedition->place);
        if (! $place) {
            throw new InvalidArgumentException('Ese lugar ya no existe.');
        }
        $r = new Randomizer(new Mt19937($expedition->id * 7919 + 17));
        $chance = fn (float $percent) => $r->getInt(1, 10000) <= (int) round($percent * 100);
        $vary = fn (float $value) => $value * (0.85 + $r->getInt(0, 30) / 100);
        $level = (int) $place['level'];
        $length = config('game.expedition.lengths.'.$expedition->length);
        $name = $this->heroes->protagonist($course)['name'] ?? 'Tu héroe';

        $str = $hero->total('strength');
        $dex = $hero->total('dexterity');
        $int = $hero->total('intelligence');
        $luk = $hero->total('luck');
        $atk = $hero->bonus('attack');
        $def = $hero->bonus('defense');
        $maxHp = $hero->hp();
        $maxMp = $hero->mp();
        $hp = $maxHp;
        $mp = $maxMp;
        $usesMagic = $int > $str;
        $secondLife = in_array($hero->accessory?->code, Item::SECOND_LIFE, true);

        // Pociones disponibles de este mundo o comunes, de la más chica a la más grande.
        $owned = $this->inventory->owned($hero->user);
        $equipped = $this->inventory->equipped($hero->user);
        $potions = Item::whereIn('id', $owned->keys())->where('kind', ItemKind::Potion)->where('heal', '>', 0)->orderBy('heal')->get()
            ->filter(fn (Item $item) => $item->fitsCourse($course))
            ->map(fn (Item $item) => ['item' => $item, 'left' => $owned[$item->id] - (int) ($equipped[$item->id] ?? 0)])
            ->filter(fn ($p) => $p['left'] > 0)->values()->all();
        $used = [];

        $log = [];
        $say = function (string $type, string $text, ?array $enemy = null) use (&$log, &$hp, &$mp, $maxHp) {
            $log[] = ['t' => $type, 'text' => $text, 'hp' => max(0, $hp), 'mp' => $mp, 'hp_max' => $maxHp,
                'enemy' => $enemy['name'] ?? null, 'img' => $enemy['code'] ?? null, 'ehp' => isset($enemy) ? max(0, $enemy['hp']) : null, 'emax' => $enemy['max'] ?? null];
        };
        $drink = function () use (&$potions, &$used, &$hp, $maxHp, $name, $say) {
            foreach ($potions as $i => $potion) {
                if ($potion['left'] > 0 && array_sum($used) < 3) {
                    $potions[$i]['left']--;
                    $used[$potion['item']->id] = ($used[$potion['item']->id] ?? 0) + 1;
                    $hp = min($maxHp, $hp + $potion['item']->heal);
                    $say('potion', "{$name} toma una {$potion['item']->name}: +{$potion['item']->heal} de vida.");

                    return;
                }
            }
        };

        $say('narr', "{$name} sale hacia {$place['name']}. {$place['text']}");
        $bonusGold = 0;
        $enemies = $r->getInt($length['enemies'][0], $length['enemies'][1]);
        $defeated = [];
        $won = true;

        for ($e = 0; $e < $enemies && $won; $e++) {
            // Exploración antes de cada encuentro.
            $roll = $r->getInt(1, 100);
            if ($roll <= 15) {
                $found = $r->getInt(4, 10) * $level;
                $bonusGold += $found;
                $say('event', "{$name} encuentra un cofre escondido: {$found} de oro (si vuelve con vida).");
            } elseif ($roll <= 28) {
                $heal = 10 + 2 * $level;
                $hp = min($maxHp, $hp + $heal);
                $say('event', "{$name} encuentra hierbas del Valle y se cura {$heal}.");
            } elseif ($roll <= 40) {
                if ($chance(min(60, 20 + $dex * 2))) {
                    $say('event', "{$name} ve la trampa a tiempo y la esquiva.");
                } else {
                    $hurt = 4 + 2 * $level;
                    $hp -= $hurt;
                    $say('event', "¡Una trampa! {$name} pierde {$hurt} de vida.");
                }
            } else {
                $say('narr', collect(["{$name} sigue el camino con cuidado.", 'Gheco olfatea el aire: algo se acerca.', "{$name} avanza; el silencio no dura mucho."])->get($r->getInt(0, 2)));
            }

            $code = $place['creatures'][$r->getInt(0, count($place['creatures']) - 1)];
            $base = config('game.creatures.'.$code);
            $max = (int) round($base['hp'] * (1 + 0.12 * ($level - 1)));
            $enemy = [
                'code' => $code, 'name' => $this->creatureName($code, $map), 'hp' => $max, 'max' => $max,
                'attack' => $base['attack'] * (1 + 0.07 * ($level - 1)), 'defense' => $base['defense'] + intdiv($level - 1, 3),
                'dexterity' => $base['dexterity'] + intdiv($level, 2),
            ];
            $say('appear', "¡Aparece un {$enemy['name']} de nivel {$level}!", $enemy);

            $heroFirst = $dex >= $enemy['dexterity'];
            for ($round = 1; $round <= 25 && $hp > 0 && $enemy['hp'] > 0; $round++) {
                foreach ($heroFirst ? ['hero', 'enemy'] : ['enemy', 'hero'] as $who) {
                    if ($hp <= 0 || $enemy['hp'] <= 0) {
                        break;
                    }
                    if ($who === 'hero') {
                        $spell = $usesMagic && $mp >= 8;
                        if ($chance(max(3, min(30, 8 + $enemy['dexterity'] - $dex)))) {
                            $say('miss', "{$name} ".($spell ? 'lanza un hechizo' : 'ataca').', pero el '.$enemy['name'].' lo esquiva.', $enemy);

                            continue;
                        }
                        $raw = $spell ? 4 + $int * 1.4 + intdiv($atk, 2) : 4 + $str + $atk;
                        if ($spell) {
                            $mp -= 8;
                        }
                        $damage = max(1, (int) round($vary($raw)) - $enemy['defense']);
                        $crit = $chance(min(40, 3 + $luk * 1.5));
                        if ($crit) {
                            $damage = (int) round($damage * 1.8);
                        }
                        $enemy['hp'] -= $damage;
                        $say($crit ? 'crit' : ($spell ? 'spell' : 'hit'),
                            ($crit ? '¡Crítico! ' : '').$name.($spell ? ' lanza un rayo rúnico' : ' golpea').": {$damage} de daño.", $enemy);
                    } else {
                        if ($chance(min(35, 5 + max(0, $dex - $enemy['dexterity']) * 2 + intdiv($luk, 3)))) {
                            $say('dodge', "El {$enemy['name']} ataca y {$name} lo esquiva.", $enemy);

                            continue;
                        }
                        $damage = max(1, (int) round($vary($enemy['attack'])) - ($def + intdiv($dex, 3)));
                        $hp -= $damage;
                        $say('enemy', "El {$enemy['name']} pega: {$damage} de daño.", $enemy);
                        if ($hp <= 0 && $secondLife) {
                            $secondLife = false;
                            $hp = (int) ceil($maxHp / 2);
                            $say('revive', "El Amuleto del Traceback brilla: {$name} lee su error de abajo hacia arriba y se levanta con {$hp} de vida.", $enemy);
                        }
                        if ($hp > 0 && $hp < $maxHp * 0.35) {
                            $drink();
                        }
                    }
                }
            }

            if ($enemy['hp'] <= 0) {
                $defeated[] = $code;
                $say('down', "El {$enemy['name']} cae.", $enemy);
                $mp = min($maxMp, $mp + 6);
            } else {
                $won = false;
                $say('defeat', $hp <= 0
                    ? "{$name} cae, pero Gheco llega a tiempo y abre un portal de vuelta: sin botín, y sin perder nada más."
                    : "{$name} no puede con el {$enemy['name']} y se retira: vuelve sin botín.", $enemy);
            }
        }

        $rewards = ['gold' => 0, 'items' => [], 'potions' => array_sum($used), 'enemies' => $enemies, 'defeated' => count($defeated), 'item_rarity' => null, 'place' => $place['name']];
        if ($won) {
            $rewards['gold'] = (int) round($length['gold'] * (1 + 0.1 * ($level - 1)) * (0.8 + $r->getInt(0, 40) / 100)) + $bonusGold;
            // Materiales de las criaturas vencidas.
            foreach (array_count_values($defeated) as $code => $count) {
                $material = config('game.creatures.'.$code.'.material');
                $item = $material ? Item::where('code', $material)->first() : null;
                $quantity = 0;
                for ($i = 0; $i < $count; $i++) {
                    $quantity += (int) $chance(60);
                }
                if ($item && $quantity > 0) {
                    $rewards['items'][] = ['id' => $item->id, 'name' => $item->name, 'quantity' => $quantity, 'rarity' => $item->rarity->value];
                }
            }
            // Un ítem al azar, con contador de mala suerte.
            if ($drop = $this->rollDrop($hero, $map, $r, $chance)) {
                $rewards['items'][] = ['id' => $drop->id, 'name' => $drop->name, 'quantity' => 1, 'rarity' => $drop->rarity->value];
                $rewards['item_rarity'] = $drop->rarity->value;
            }
            $say('victory', "¡{$name} vuelve de {$place['name']} con el botín!");
        }

        return ['won' => $won, 'log' => $log, 'rewards' => $rewards, 'potions' => $used];
    }

    /** El botín es del mapa: ítems de ese mundo o comunes. */
    private function rollDrop(Hero $hero, Course $map, Randomizer $r, \Closure $chance): ?Item
    {
        $drops = config('game.expedition.drops');
        $rarity = match (true) {
            $chance($drops['epic']) => 'epic',
            $chance($drops['rare']) => 'rare',
            $chance($drops['common']) => 'common',
            default => null,
        };
        // A las `pity` expediciones ganadas sin raro (o mejor), cae uno.
        if (! in_array($rarity, ['rare', 'epic'], true)) {
            $recent = Expedition::where('user_id', $hero->user_id)->whereNotNull('resolved_at')->where('won', true)->latest('id')
                ->limit((int) config('game.expedition.pity'))->pluck('rewards');
            $dry = $recent->takeWhile(fn ($rewards) => ! in_array($rewards['item_rarity'] ?? null, ['rare', 'epic'], true))->count();
            if ($dry >= (int) config('game.expedition.pity')) {
                $rarity = 'rare';
            }
        }
        if (! $rarity) {
            return null;
        }
        $pool = Item::where('droppable', true)->where('rarity', $rarity)
            ->where(fn ($q) => $q->where('course_id', $map->id)->orWhereNull('course_id'))->orderBy('id')->get();

        return $pool->isEmpty() ? null : $pool[$r->getInt(0, $pool->count() - 1)];
    }
}
