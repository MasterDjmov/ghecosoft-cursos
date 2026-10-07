<?php

namespace App\Livewire\Admin;

use App\Enums\ItemKind;
use App\Enums\ItemRarity;
use App\Models\Course;
use App\Models\Item;
use App\Models\ItemMovement;
use App\Rules\SafeUpload;
use App\Support\PracticeReferences;
use Flux\Flux;
use Illuminate\Support\Str;
use Illuminate\Validation\Rule;
use Livewire\Attributes\Title;
use Livewire\Attributes\Url;
use Livewire\Component;
use Livewire\Features\SupportFileUploads\TemporaryUploadedFile;
use Livewire\WithFileUploads;

/**
 * Juego → Ítems (D90): el catálogo de armas, ropa, accesorios, pociones, materiales y especiales, con su
 * imagen, sus bonos, el precio en la tienda y si cae en las expediciones.
 */
#[Title('Ítems')]
class Items extends Component
{
    use WithFileUploads;

    /** '' = todos; 'comunes'; o el id de un curso. */
    #[Url(as: 'mundo')]
    public string $world = '';

    #[Url(as: 'sin-imagen', except: false)]
    public bool $onlyMissing = false;

    public ?int $editingId = null;

    /** @var array<string, mixed> */
    public array $form = [];

    /** @var TemporaryUploadedFile|null */
    public $image = null;

    private const FIELDS = ['code', 'name', 'description', 'kind', 'rarity', 'course_id', 'attack', 'defense', 'strength', 'dexterity', 'intelligence', 'luck', 'heal', 'price', 'min_level', 'in_shop', 'droppable', 'image_prompt'];

    public function create(): void
    {
        $this->resetValidation();
        $this->editingId = null;
        $this->image = null;
        $this->form = ['code' => '', 'name' => '', 'description' => '', 'kind' => ItemKind::Weapon->value, 'rarity' => ItemRarity::Common->value,
            'course_id' => ctype_digit($this->world) ? $this->world : '', 'attack' => 0, 'defense' => 0, 'strength' => 0, 'dexterity' => 0,
            'intelligence' => 0, 'luck' => 0, 'heal' => 0, 'price' => '', 'min_level' => 1, 'in_shop' => false, 'droppable' => false, 'image_prompt' => ''];
        Flux::modal('item')->show();
    }

    public function edit(int $id): void
    {
        $this->resetValidation();
        $item = Item::findOrFail($id);
        $this->editingId = $item->id;
        $this->image = null;
        $this->form = collect(self::FIELDS)->mapWithKeys(fn ($field) => [$field => match (true) {
            $item->{$field} instanceof \BackedEnum => $item->{$field}->value,
            $item->{$field} === null => '',
            default => $item->{$field},
        }])->all();
        Flux::modal('item')->show();
    }

    public function save(): void
    {
        $this->form['code'] = Str::slug((string) ($this->form['code'] ?: $this->form['name']));
        $data = $this->validate([
            'form.code' => ['required', 'string', 'max:80', Rule::unique('items', 'code')->ignore($this->editingId)],
            'form.name' => ['required', 'string', 'max:120'],
            'form.description' => ['nullable', 'string', 'max:500'],
            'form.kind' => ['required', Rule::enum(ItemKind::class)],
            'form.rarity' => ['required', Rule::enum(ItemRarity::class)],
            'form.course_id' => ['nullable', 'exists:courses,id'],
            'form.attack' => ['integer', 'between:-50,99'], 'form.defense' => ['integer', 'between:-50,99'],
            'form.strength' => ['integer', 'between:-20,30'], 'form.dexterity' => ['integer', 'between:-20,30'],
            'form.intelligence' => ['integer', 'between:-20,30'], 'form.luck' => ['integer', 'between:-20,30'],
            'form.heal' => ['integer', 'between:0,999'],
            'form.price' => ['nullable', 'integer', 'between:1,1000000'],
            'form.min_level' => ['integer', 'between:1,100'],
            'form.in_shop' => ['boolean'], 'form.droppable' => ['boolean'],
            'form.image_prompt' => ['nullable', 'string', 'max:2000'],
            'image' => ['nullable', 'image', 'mimes:png,jpg,jpeg,webp', 'max:'.PracticeReferences::MAX_KB, new SafeUpload],
        ], [], ['form.code' => 'código', 'form.name' => 'nombre', 'form.price' => 'precio', 'image' => 'imagen'])['form'];

        $data['course_id'] = $data['course_id'] ?: null;
        $data['price'] = $data['price'] === '' ? null : $data['price'];
        $data['description'] = $data['description'] ?: null;
        $data['image_prompt'] = $data['image_prompt'] ?: null;
        if ($data['in_shop'] && $data['price'] === null) {
            $this->addError('form.price', 'Para venderlo en la tienda, ponele precio.');

            return;
        }
        if ($this->image) {
            $data['image_path'] = PracticeReferences::store($this->image->getRealPath(), $this->image->extension());
        }

        $item = Item::updateOrCreate(['id' => $this->editingId], $data);
        $this->image = null;
        Flux::modal('item')->close();
        Flux::toast(variant: 'success', text: "«{$item->name}» guardado.");
    }

    public function removeImage(int $id): void
    {
        Item::findOrFail($id)->update(['image_path' => null]);
    }

    public function delete(int $id): void
    {
        $item = Item::findOrFail($id);
        if (ItemMovement::where('item_id', $item->id)->exists()) {
            Flux::toast(variant: 'danger', text: 'Ya hay jugadores que lo tienen: sacalo de la tienda y de las expediciones en vez de borrarlo.');

            return;
        }
        $item->delete();
        Flux::toast(variant: 'success', text: 'Ítem borrado.');
    }

    public function render()
    {
        $items = Item::with('course')
            ->when($this->world === 'comunes', fn ($q) => $q->whereNull('course_id'))
            ->when(ctype_digit($this->world), fn ($q) => $q->where('course_id', (int) $this->world))
            ->when($this->onlyMissing, fn ($q) => $q->whereNull('image_path'))
            ->orderBy('kind')->orderBy('min_level')->orderBy('name')->get();

        return view('livewire.admin.items', [
            'items' => $items->groupBy(fn (Item $item) => $item->kind->value),
            'courses' => Course::orderBy('title')->get(['id', 'title']),
            'owners' => ItemMovement::groupBy('item_id')->selectRaw('item_id, count(distinct user_id) as total')->pluck('total', 'item_id'),
        ]);
    }
}
