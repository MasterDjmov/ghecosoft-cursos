<?php

namespace App\Livewire\Student;

use App\Exceptions\InsufficientFunds;
use App\Models\Course;
use App\Models\Hero as HeroModel;
use App\Models\Level;
use App\Models\NodeStepCompletion;
use App\Models\XpTransaction;
use App\Services\Heroes;
use Flux\Flux;
use Illuminate\Support\Facades\RateLimiter;
use InvalidArgumentException;
use Livewire\Attributes\Title;
use Livewire\Component;

/**
 * El panel del protagonista de un curso (D89). La primera vez, «Tomá el control»: el aspecto (6 variantes,
 * solo cosméticas) y el reparto de 24 puntos. Después, la vida, el maná, los atributos (se suben con oro)
 * y el equipo.
 */
#[Title('Mi héroe')]
class Hero extends Component
{
    public Course $course;

    /** Lo que elige al tomar el control (y el aspecto, al cambiarlo). */
    public int $look = 1;

    /** El reparto: empieza con el mínimo en cada uno y los puntos que sobran, libres. @var array<string, int> */
    public array $stats = ['strength' => 4, 'dexterity' => 4, 'intelligence' => 4, 'luck' => 4];

    /** Reacomodando los puntos (gratis mientras no haya comprado ninguno con oro). */
    public bool $editing = false;

    public function mount(Course $course, Heroes $heroes): void
    {
        $this->authorize('play', $course);
        abort_if($heroes->protagonist($course) === null, 404);
        $heroes->settleGold(auth()->user());
        if ($hero = $heroes->heroOf(auth()->user(), $course)) {
            $this->look = $hero->look;
        }
    }

    public function takeControl(Heroes $heroes): void
    {
        try {
            $heroes->create(auth()->user(), $this->course, $this->look, array_map('intval', $this->stats));
        } catch (InvalidArgumentException $e) {
            $this->addError('stats', $e->getMessage());

            return;
        }
        Flux::toast(variant: 'success', text: '¡Tomaste el control de '.$heroes->protagonist($this->course)['name'].'!');
    }

    public function startEditing(Heroes $heroes): void
    {
        $hero = $heroes->heroOf(auth()->user(), $this->course);
        if (! $hero || ! $heroes->canRedistribute($hero)) {
            return;
        }
        $this->stats = collect(HeroModel::STATS)->mapWithKeys(fn ($stat) => [$stat => $hero->{$stat}])->all();
        $this->editing = true;
    }

    public function redistribute(Heroes $heroes): void
    {
        $hero = $heroes->heroOf(auth()->user(), $this->course);
        abort_unless($hero, 404);
        try {
            $heroes->redistribute($hero, array_map('intval', $this->stats));
        } catch (InvalidArgumentException $e) {
            $this->addError('stats', $e->getMessage());

            return;
        }
        $this->editing = false;
        Flux::toast(variant: 'success', text: 'Puntos reacomodados.');
    }

    public function changeLook(int $look, Heroes $heroes): void
    {
        $hero = $heroes->heroOf(auth()->user(), $this->course);
        if (! $hero) {
            $this->look = max(1, min(HeroModel::LOOKS, $look));

            return;
        }
        try {
            $heroes->changeLook($hero, $look);
            $this->look = $look;
        } catch (InvalidArgumentException $e) {
            Flux::toast(variant: 'danger', text: $e->getMessage());
        }
    }

    public function upgrade(string $stat, Heroes $heroes): void
    {
        $key = 'hero-upgrade:'.auth()->id();
        if (RateLimiter::tooManyAttempts($key, 30)) {
            Flux::toast(variant: 'danger', text: 'Más despacio: probá en un minuto.');

            return;
        }
        RateLimiter::hit($key, 60);

        $hero = $heroes->heroOf(auth()->user(), $this->course);
        abort_unless($hero, 404);
        try {
            $heroes->upgrade($hero, $stat);
            Flux::toast(variant: 'success', text: HeroModel::statLabel($stat).' sube a '.$hero->{$stat}.'.');
        } catch (InsufficientFunds $e) {
            Flux::toast(variant: 'danger', text: 'No te alcanza el oro: tenés '.$e->balance.' y hacen falta '.$e->required.'.');
        } catch (InvalidArgumentException $e) {
            Flux::toast(variant: 'danger', text: $e->getMessage());
        }
    }

    public function render(Heroes $heroes)
    {
        $user = auth()->user();
        $protagonist = $heroes->protagonist($this->course);

        return view('livewire.student.hero', [
            'protagonist' => $protagonist,
            'hero' => $hero = $heroes->heroOf($user, $this->course),
            'canRedistribute' => $hero && $heroes->canRedistribute($hero),
            'looks' => collect($protagonist['looks'])->map(fn ($name, $n) => ['n' => $n, 'name' => $name, 'url' => Heroes::lookUrl($protagonist, $n)]),
            'gold' => $heroes->gold($user),
            'level' => Level::forXp($user->xp_total),
            'nextLevel' => Level::where('xp_required', '>', $user->xp_total)->orderBy('xp_required')->first(),
            'courseXp' => (int) XpTransaction::where('user_id', $user->id)->where('course_id', $this->course->id)->sum('amount'),
            'cards' => NodeStepCompletion::where('user_id', $user->id)
                ->whereHas('step', fn ($q) => $q->whereNotNull('card_title')->whereHas('node', fn ($n) => $n->where('course_id', $this->course->id)))->count(),
        ]);
    }
}
