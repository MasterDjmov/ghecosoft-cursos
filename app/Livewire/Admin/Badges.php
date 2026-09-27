<?php

namespace App\Livewire\Admin;

use App\Models\Badge;
use App\Models\Course;
use Flux\Flux;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;
use Illuminate\Validation\Rule;
use Livewire\Attributes\Title;
use Livewire\Component;
use Livewire\Features\SupportFileUploads\TemporaryUploadedFile;
use Livewire\WithFileUploads;

/** Insignias: las entregan los jefes (se eligen en el editor del nodo). */
#[Title('Insignias')]
class Badges extends Component
{
    use WithFileUploads;

    public ?int $badgeId = null;

    public string $name = '';

    public string $code = '';

    public string $description = '';

    /** '' = general, o el id del curso. */
    public string $course_id = '';

    /** @var TemporaryUploadedFile|null */
    public $icon = null;

    public function create(): void
    {
        $this->resetValidation();
        $this->reset('badgeId', 'name', 'code', 'description', 'course_id', 'icon');

        Flux::modal('badge')->show();
    }

    public function edit(int $badgeId): void
    {
        $badge = Badge::findOrFail($badgeId);

        $this->resetValidation();
        $this->reset('icon');
        $this->badgeId = $badge->id;
        $this->name = $badge->name;
        $this->code = $badge->code;
        $this->description = (string) $badge->description;
        $this->course_id = (string) $badge->course_id;

        Flux::modal('badge')->show();
    }

    public function updatedName(string $value): void
    {
        if (! $this->badgeId) {
            $this->code = Str::slug($value, '_');
        }
    }

    public function save(): void
    {
        $this->validate([
            'name' => ['required', 'string', 'max:120'],
            'code' => ['required', 'string', 'max:60', 'regex:/^[a-z0-9_]+$/', Rule::unique('badges', 'code')->ignore($this->badgeId)],
            'description' => ['nullable', 'string', 'max:255'],
            'course_id' => ['nullable', Rule::exists('courses', 'id')],
            'icon' => ['nullable', 'image', 'mimes:'.implode(',', config('uploads.image.mimes')), 'max:'.config('uploads.image.max_kb')],
        ], ['code.regex' => 'El código va en minúsculas, sin espacios: rey_slime.'], ['name' => 'nombre', 'code' => 'código', 'course_id' => 'curso']);

        $badge = $this->badgeId ? Badge::findOrFail($this->badgeId) : new Badge;
        $badge->fill([
            'name' => $this->name,
            'code' => $this->code,
            'description' => $this->description ?: null,
            'course_id' => $this->course_id !== '' ? (int) $this->course_id : null,
        ]);

        if ($this->icon) {
            if ($badge->icon) {
                Storage::disk('public')->delete($badge->icon);
            }
            $badge->icon = $this->icon->storeAs('badges', Str::uuid().'.'.$this->icon->extension(), 'public');
        }

        $badge->save();

        Flux::modal('badge')->close();
        Flux::toast(variant: 'success', text: 'Insignia guardada.');
    }

    public function delete(int $badgeId): void
    {
        $badge = Badge::withCount('users')->findOrFail($badgeId);

        if ($badge->users_count > 0) {
            Flux::toast(variant: 'danger', text: 'Hay alumnos que ya ganaron esta insignia: no se puede borrar.');

            return;
        }

        if ($badge->icon) {
            Storage::disk('public')->delete($badge->icon);
        }
        $badge->delete();

        Flux::toast(variant: 'success', text: 'Insignia borrada.');
    }

    public function render()
    {
        return view('livewire.admin.badges', [
            'badges' => Badge::with(['course:id,title', 'nodes:id,badge_id,title'])->withCount('users')->orderBy('course_id')->orderBy('name')->get(),
            'courses' => Course::orderBy('position')->get(['id', 'title']),
        ]);
    }
}
