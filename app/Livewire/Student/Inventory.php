<?php

namespace App\Livewire\Student;

use App\Enums\ItemKind;
use App\Models\Hero;
use App\Models\Item;
use App\Services\Heroes;
use App\Services\Inventory as Bag;
use Flux\Flux;
use Illuminate\Support\Str;
use InvalidArgumentException;
use Livewire\Attributes\Title;
use Livewire\Attributes\Url;
use Livewire\Component;

/**
 * La mochila (D90): una sola por jugador, con una solapa por mundo y una de comunes. Desde acá se equipa
 * a cada protagonista (arma, ropa y accesorio) y se usa el Pergamino del Reinicio.
 */
#[Title('Mochila')]
class Inventory extends Component
{
    /** El slug del curso o 'comunes'. */
    #[Url(as: 'solapa')]
    public string $tab = '';

    public function mount(Bag $bag): void
    {
        $bag->settleItems(auth()->user());
        app(Heroes::class)->settleGold(auth()->user());
    }

    private function hero(int $heroId): Hero
    {
        return Hero::with('course')->where('user_id', auth()->id())->findOrFail($heroId);
    }

    public function equip(int $itemId, int $heroId, Bag $bag): void
    {
        try {
            $bag->equip($this->hero($heroId), Item::findOrFail($itemId));
            Flux::toast(variant: 'success', text: 'Equipado.');
        } catch (InvalidArgumentException $e) {
            Flux::toast(variant: 'danger', text: $e->getMessage());
        }
    }

    public function unequip(int $heroId, string $slot, Bag $bag): void
    {
        try {
            $bag->unequip($this->hero($heroId), $slot);
        } catch (InvalidArgumentException $e) {
            Flux::toast(variant: 'danger', text: $e->getMessage());
        }
    }

    public function useOn(int $itemId, int $heroId, Bag $bag): void
    {
        $hero = $this->hero($heroId);
        try {
            $bag->use(auth()->user(), Item::findOrFail($itemId), $hero);
            Flux::toast(variant: 'success', text: 'Listo: ya podés reacomodar los puntos desde el panel del héroe.');
            $this->redirectRoute('student.hero', $hero->course, navigate: true);
        } catch (InvalidArgumentException $e) {
            Flux::toast(variant: 'danger', text: $e->getMessage());
        }
    }

    public function render(Bag $bag, Heroes $heroes)
    {
        $user = auth()->user();
        $contents = $bag->contents($user);
        $myHeroes = Hero::with(['course', 'weapon', 'armor', 'accessory'])->where('user_id', $user->id)->get();

        // Solapas: un mundo por curso con ítems o con héroe, y los comunes.
        $tabs = $contents->pluck('item.course')->filter()->merge($myHeroes->pluck('course'))->unique('id')->sortBy('title')
            ->map(fn ($course) => ['key' => $course->slug, 'label' => Str::before($course->title, ':'), 'course' => $course])
            ->values()
            ->push(['key' => 'comunes', 'label' => 'Comunes', 'course' => null]);
        $current = $tabs->firstWhere('key', $this->tab) ?? $tabs->first();
        $rows = $contents->filter(fn ($row) => $current['course'] ? $row['item']->course_id === $current['course']->id : $row['item']->course_id === null);

        return view('livewire.student.inventory', [
            'tabs' => $tabs,
            'current' => $current,
            'groups' => $rows->groupBy(fn ($row) => $row['item']->kind->value)
                ->sortBy(fn ($group, $kind) => array_search($kind, array_column(ItemKind::cases(), 'value'), true)),
            'heroes' => $myHeroes,
            // Con quién puede usar cada cosa: el héroe de ese mundo (o todos, si es común).
            'heroesFor' => fn (Item $item) => $myHeroes->filter(fn (Hero $hero) => $item->fitsCourse($hero->course)),
            'protagonist' => fn (Hero $hero) => $heroes->protagonist($hero->course),
            'gold' => $heroes->gold($user),
            'total' => $contents->sum('owned'),
        ]);
    }
}
