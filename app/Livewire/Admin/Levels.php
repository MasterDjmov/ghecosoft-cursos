<?php

namespace App\Livewire\Admin;

use App\Models\GlossaryTerm;
use App\Models\Level;
use Flux\Flux;
use Livewire\Attributes\Title;
use Livewire\Component;

/** Niveles (rangos): XP necesaria y nombre (guardado en el diccionario como level.{n}). */
#[Title('Niveles')]
class Levels extends Component
{
    /** @var array<int, array{xp_required: int|string, name: string}> */
    public array $rows = [];

    public function mount(): void
    {
        $this->loadRows();
    }

    private function loadRows(): void
    {
        $this->rows = Level::orderBy('number')->get()
            ->mapWithKeys(fn (Level $level) => [$level->number => [
                'xp_required' => $level->xp_required,
                'name' => (string) GlossaryTerm::whereNull('course_id')->where('key', 'level.'.$level->number)->value('singular'),
            ]])
            ->all();
    }

    public function add(): void
    {
        $last = Level::orderByDesc('number')->first();
        Level::create(['number' => ($last->number ?? 0) + 1, 'xp_required' => ($last->xp_required ?? 0) + 500]);
        $this->loadRows();
    }

    /** Solo se borra el último, así los números quedan corridos. */
    public function removeLast(): void
    {
        $last = Level::orderByDesc('number')->first();
        if (! $last || $last->number === 1) {
            return;
        }

        GlossaryTerm::whereNull('course_id')->where('key', 'level.'.$last->number)->get()->each->delete();
        $last->delete();
        $this->loadRows();
    }

    public function save(): void
    {
        $this->validate([
            'rows' => ['required', 'array'],
            'rows.*.xp_required' => ['required', 'integer', 'min:0', 'max:10000000'],
            'rows.*.name' => ['nullable', 'string', 'max:60'],
        ], [], ['rows.*.xp_required' => 'XP', 'rows.*.name' => 'nombre']);

        // El nivel 1 arranca en 0 y cada uno pide más XP que el anterior.
        $previous = null;
        foreach ($this->rows as $number => $row) {
            $xp = (int) $row['xp_required'];
            if ($number === 1 && $xp !== 0) {
                $this->addError("rows.{$number}.xp_required", 'El nivel 1 empieza en 0 XP.');

                return;
            }
            if ($previous !== null && $xp <= $previous) {
                $this->addError("rows.{$number}.xp_required", 'Tiene que pedir más XP que el nivel anterior.');

                return;
            }
            $previous = $xp;
        }

        foreach ($this->rows as $number => $row) {
            Level::where('number', $number)->update(['xp_required' => (int) $row['xp_required']]);

            $key = 'level.'.$number;
            $name = trim($row['name']);
            $term = GlossaryTerm::whereNull('course_id')->where('key', $key)->first();

            if ($name === '') {
                $term?->delete();
            } else {
                ($term ?? new GlossaryTerm(['key' => $key]))->fill(['singular' => $name, 'plural' => $name, 'gender' => 'm'])->save();
            }
        }

        Flux::toast(variant: 'success', text: 'Niveles guardados.');
    }

    public function render()
    {
        return view('livewire.admin.levels');
    }
}
