<?php

namespace App\Livewire\Student;

use App\Models\Course;
use App\Models\Expedition;
use App\Models\Hero;
use App\Models\Item;
use App\Models\Mount;
use App\Services\Expeditions as Service;
use App\Services\Heroes;
use App\Services\Inventory;
use Flux\Flux;
use Illuminate\Support\Facades\RateLimiter;
use InvalidArgumentException;
use Livewire\Attributes\Title;
use Livewire\Component;

/**
 * Las expediciones de un mundo (D91): el mapa con los lugares abiertos, las 3 del momento, la que está en
 * camino (con su reloj) y, al volver, la exploración y la pelea turno por turno.
 */
#[Title('Expediciones')]
class Expeditions extends Component
{
    public Course $course;

    /** La expedición cuya pelea se está mirando. */
    public ?int $watching = null;

    /** Sube con cada «Ver la pelea»: vuelve a arrancar la repetición aunque sea la misma pelea. */
    public int $replay = 0;

    /** El héroe que va: cualquiera de los del jugador puede ir a cualquier mapa (cursos en paralelo). */
    public ?int $heroId = null;

    public function mount(Course $course, Heroes $heroes): void
    {
        abort_if(app(Service::class)->world($course) === null, 404);
        $user = auth()->user();
        // Quien cursa (o prueba) este curso, o cualquier jugador con algún héroe, que viene a explorar.
        abort_unless($user->can('play', $course) || Hero::where('user_id', $user->id)->exists(), 403);
        $heroes->settleGold($user);
        $this->heroId = $heroes->heroOf($user, $course)?->id
            ?? Hero::where('user_id', $user->id)->latest('updated_at')->value('id');
    }

    public function send(int $index, Service $service, Heroes $heroes, ?string $place = null): void
    {
        $key = 'expedition-start:'.auth()->id();
        if (RateLimiter::tooManyAttempts($key, 10)) {
            Flux::toast(variant: 'danger', text: 'Más despacio: probá en un minuto.');

            return;
        }
        RateLimiter::hit($key, 60);

        $hero = Hero::where('user_id', auth()->id())->find($this->heroId);
        if (! $hero) {
            Flux::toast(variant: 'danger', text: 'Primero tomá el control de un héroe.');

            return;
        }
        try {
            $service->start(auth()->user(), $hero, $index, $place, $this->course);
            Flux::toast(variant: 'success', text: '¡En camino!');
        } catch (InvalidArgumentException $e) {
            Flux::toast(variant: 'danger', text: $e->getMessage());
        }
    }

    /** Volvió: se calcula la aventura y se paga el botín (una sola vez), y se muestra la pelea. */
    public function claim(Service $service): void
    {
        $active = $service->active(auth()->user());
        if (! $active || ! $active->isReady()) {
            return;
        }
        $this->watching = $service->resolve($active)->id;
    }

    /** El Reloj de Arena: termina ya la que está en camino. */
    public function hurry(Service $service): void
    {
        try {
            $service->hurry(auth()->user());
            Flux::toast(variant: 'success', text: 'La arena cae de golpe: ¡ya volvió!');
        } catch (InvalidArgumentException $e) {
            Flux::toast(variant: 'danger', text: $e->getMessage());
        }
    }

    public function showFight(int $id): void
    {
        $this->watching = Expedition::where('user_id', auth()->id())->whereNotNull('resolved_at')->findOrFail($id)->id;
        $this->replay++;
    }

    public function render(Service $service, Heroes $heroes, Inventory $inventory)
    {
        $user = auth()->user();
        $myHeroes = Hero::with('course')->where('user_id', $user->id)->orderBy('id')->get();
        $hero = $myHeroes->firstWhere('id', $this->heroId);
        $world = $service->world($this->course);
        $active = $service->active($user);
        $mount = Mount::where('user_id', $user->id)->first();
        // El que va (su nombre y su cara): el héroe elegido; si todavía no tiene ninguno, el de este mundo.
        $protagonist = $hero ? $heroes->protagonist($hero->course) : $heroes->protagonist($this->course);
        $activeHero = $active ? $myHeroes->firstWhere('id', $active->hero_id) : null;

        return view('livewire.student.expeditions', [
            'hero' => $hero,
            'myHeroes' => $myHeroes,
            'heroFace' => fn (Hero $h) => Heroes::lookUrl($heroes->protagonist($h->course), $h->look),
            'heroName' => fn (?Hero $h) => $h ? ($heroes->protagonist($h->course)['name'] ?? 'Tu héroe') : 'Tu héroe',
            'activeHero' => $activeHero,
            'worlds' => $service->worlds(),
            'studies' => ! $service->explorer($user, $this->course) || $service->studies($user, $this->course),
            'protagonist' => $protagonist,
            'world' => $world,
            'open' => $service->isOpen($user, $this->course),
            'opensAfter' => $this->course->nodes()->where('code', $world['opens_after'])->value('title'),
            'places' => $service->places($user, $this->course),
            'offers' => $hero && ! $active ? $service->offers($user, $this->course) : [],
            'active' => $active,
            'activePlace' => $active ? $service->placeName($active->course, $active->place) : null,
            'today' => $service->todayCount($user),
            'perDay' => (int) config('game.expedition.per_day'),
            'refreshIn' => (int) max(1, now()->diffInSeconds($service->nextRefresh(), false)),
            'history' => Expedition::where('user_id', $user->id)->where('course_id', $this->course->id)->whereNotNull('resolved_at')->latest('id')->limit(8)->get(),
            'fight' => $this->watching ? Expedition::where('user_id', $user->id)->find($this->watching) : null,
            'mount' => $mount,
            'heroImage' => $hero ? Heroes::lookUrl($protagonist, $hero->look) : null,
            'service' => $service,
            'hourglasses' => ($hourglass = Item::where('code', Item::HOURGLASS)->first()) ? $inventory->available($user, $hourglass) : 0,
        ]);
    }
}
