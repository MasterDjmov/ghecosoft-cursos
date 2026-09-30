<?php

namespace App\Livewire\Admin\Courses;

use App\Enums\Modality;
use App\Enums\Role;
use App\Models\Course;
use App\Models\User;
use Flux\Flux;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Support\Facades\DB;
use Illuminate\Validation\Rule;
use Livewire\Attributes\Locked;
use Livewire\Component;

/** Comisiones de un curso (en la pantalla de datos del curso). Son solo una etiqueta del abono. */
class Cohorts extends Component
{
    #[Locked]
    public Course $course;

    #[Locked]
    public ?int $editingId = null;

    /** Título del bloque (en Comisiones va el nombre del curso). */
    #[Locked]
    public ?string $heading = null;

    public string $name = '';

    public string $modality = 'virtual';

    public string $schedule_text = '';

    public string $starts_on = '';

    public bool $is_open_for_enrollment = true;

    /** Solo el administrador: el docente a cargo ('' = sin docente, la atiende el administrador). */
    public string $teacher_id = '';

    public function create(): void
    {
        $this->resetForm();
        Flux::modal($this->modalName())->show();
    }

    public function edit(int $id): void
    {
        $cohort = $this->mine()->findOrFail($id);
        $this->resetErrorBag();
        $this->editingId = $cohort->id;
        $this->name = $cohort->name;
        $this->modality = $cohort->modality->value;
        $this->schedule_text = (string) $cohort->schedule_text;
        $this->starts_on = (string) $cohort->starts_on?->format('Y-m-d');
        $this->is_open_for_enrollment = $cohort->is_open_for_enrollment;
        $this->teacher_id = (string) $cohort->teacher_id;
        Flux::modal($this->modalName())->show();
    }

    public function save(): void
    {
        $data = $this->validate([
            'name' => ['required', 'string', 'max:80'],
            'modality' => ['required', Rule::enum(Modality::class)],
            'schedule_text' => ['nullable', 'string', 'max:120'],
            'starts_on' => ['nullable', 'date'],
            'is_open_for_enrollment' => ['boolean'],
        ], [], ['name' => 'nombre', 'modality' => 'modalidad', 'schedule_text' => 'horario', 'starts_on' => 'inicio']);

        $data['schedule_text'] = trim($data['schedule_text'] ?? '') ?: null;
        $data['starts_on'] = $data['starts_on'] ?: null;
        // El docente crea comisiones a su nombre; el administrador elige el docente (D72).
        $viewer = auth()->user();
        if ($viewer->isAdmin()) {
            $data['teacher_id'] = User::where('role', Role::Teacher)->whereKey((int) $this->teacher_id)->value('id');
        } elseif (! $this->editingId) {
            $data['teacher_id'] = $viewer->id;
        }

        $this->editingId
            ? $this->mine()->findOrFail($this->editingId)->update($data)
            : $this->course->cohorts()->create($data);

        Flux::modal($this->modalName())->close();
        Flux::toast(variant: 'success', text: $this->editingId ? 'Comisión guardada.' : 'Comisión creada.');
        $this->resetForm();
    }

    public function toggleOpen(int $id): void
    {
        $cohort = $this->mine()->findOrFail($id);
        $cohort->update(['is_open_for_enrollment' => ! $cohort->is_open_for_enrollment]);
    }

    /** Sus alumnos siguen cursando igual; solo quedan sin comisión. */
    public function delete(int $id): void
    {
        $this->mine()->findOrFail($id)->delete();
        Flux::toast(variant: 'success', text: 'Comisión borrada.');
    }

    private function resetForm(): void
    {
        $this->resetErrorBag();
        $this->reset('editingId', 'name', 'modality', 'schedule_text', 'starts_on', 'is_open_for_enrollment', 'teacher_id');
    }

    /** Las comisiones que maneja quien mira: todas (administrador) o las suyas (docente, D72). */
    private function mine(): HasMany
    {
        return $this->course->cohorts()->when(! auth()->user()->isAdmin(), fn ($q) => $q->where('teacher_id', auth()->id()));
    }

    public function modalName(): string
    {
        return 'cohort-form-'.$this->course->id;
    }

    public function render()
    {
        return view('livewire.admin.courses.cohorts', [
            'cohorts' => $this->mine()
                ->with('teacher:id,name,last_name')
                ->withCount(['subscriptions as students_count' => fn ($q) => $q->select(DB::raw('count(distinct user_id)'))])
                ->orderBy('name')
                ->get(),
            'modalities' => Modality::cases(),
            'teachers' => auth()->user()->isAdmin() ? User::where('role', Role::Teacher)->orderBy('name')->get(['id', 'name', 'last_name']) : collect(),
        ]);
    }
}
