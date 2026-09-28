<?php

namespace App\Livewire\Admin\Courses;

use App\Enums\Modality;
use App\Models\Course;
use Flux\Flux;
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

    public string $name = '';

    public string $modality = 'virtual';

    public string $schedule_text = '';

    public string $starts_on = '';

    public bool $is_open_for_enrollment = true;

    public function create(): void
    {
        $this->resetForm();
        Flux::modal('cohort-form')->show();
    }

    public function edit(int $id): void
    {
        $cohort = $this->course->cohorts()->findOrFail($id);
        $this->resetErrorBag();
        $this->editingId = $cohort->id;
        $this->name = $cohort->name;
        $this->modality = $cohort->modality->value;
        $this->schedule_text = (string) $cohort->schedule_text;
        $this->starts_on = (string) $cohort->starts_on?->format('Y-m-d');
        $this->is_open_for_enrollment = $cohort->is_open_for_enrollment;
        Flux::modal('cohort-form')->show();
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

        $this->editingId
            ? $this->course->cohorts()->findOrFail($this->editingId)->update($data)
            : $this->course->cohorts()->create($data);

        Flux::modal('cohort-form')->close();
        Flux::toast(variant: 'success', text: $this->editingId ? 'Comisión guardada.' : 'Comisión creada.');
        $this->resetForm();
    }

    public function toggleOpen(int $id): void
    {
        $cohort = $this->course->cohorts()->findOrFail($id);
        $cohort->update(['is_open_for_enrollment' => ! $cohort->is_open_for_enrollment]);
    }

    /** Sus alumnos siguen cursando igual; solo quedan sin comisión. */
    public function delete(int $id): void
    {
        $this->course->cohorts()->findOrFail($id)->delete();
        Flux::toast(variant: 'success', text: 'Comisión borrada.');
    }

    private function resetForm(): void
    {
        $this->resetErrorBag();
        $this->reset('editingId', 'name', 'modality', 'schedule_text', 'starts_on', 'is_open_for_enrollment');
    }

    public function render()
    {
        return view('livewire.admin.courses.cohorts', [
            'cohorts' => $this->course->cohorts()
                ->withCount(['subscriptions as students_count' => fn ($q) => $q->select(DB::raw('count(distinct user_id)'))])
                ->orderBy('name')
                ->get(),
            'modalities' => Modality::cases(),
        ]);
    }
}
