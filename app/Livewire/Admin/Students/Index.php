<?php

namespace App\Livewire\Admin\Students;

use App\Enums\Role;
use App\Models\Cohort;
use App\Models\Course;
use App\Models\CourseSubscription;
use App\Models\User;
use App\Services\StudentAccounts;
use App\Services\TeacherScope;
use Flux\Flux;
use Livewire\Attributes\Title;
use Livewire\Attributes\Url;
use Livewire\Component;
use Livewire\WithPagination;

/**
 * Alumnos (y, para el administrador, los docentes). Tocar un alumno despliega sus cursos con la
 * comisión de cada uno, para cambiarla ahí mismo. El docente (D72) ve a los alumnos de sus comisiones
 * y busca a los demás (solo nombre y usuario) para sumarlos a una comisión suya.
 */
#[Title('Alumnos')]
class Index extends Component
{
    use WithPagination;

    #[Url(as: 'buscar', except: '')]
    public string $search = '';

    /** Administrador: '' alumnos | 'docentes'. Docente: '' sus alumnos | 'sumar' (buscar a los demás). */
    #[Url(as: 'ver', except: '')]
    public string $tab = '';

    public ?int $expanded = null;

    public function updatedSearch(): void
    {
        $this->resetPage();
    }

    public function updatedTab(): void
    {
        $this->reset('expanded');
        $this->resetPage();
    }

    public function toggle(int $id): void
    {
        $this->expanded = $this->expanded === $id ? null : $id;
    }

    /** Comisión del alumno en un curso ('' = sin comisión). */
    public function assignCohort(StudentAccounts $accounts, int $userId, int $courseId, string $cohortId): void
    {
        $student = User::where('role', Role::Student)->findOrFail($userId);
        $course = Course::whereIn('id', $student->subscriptions()->select('course_id'))->findOrFail($courseId);
        $target = $cohortId === '' ? null : (int) $cohortId;
        $this->authorize('assignCohort', [$student, $course, $target]);

        try {
            $accounts->changeCohort($student, $course, $target);
        } catch (\InvalidArgumentException) {
            Flux::toast(variant: 'danger', text: 'Esa comisión no es de este curso.');

            return;
        }

        Flux::toast(variant: 'success', text: $target ? 'Comisión actualizada.' : 'Quedó sin comisión en este curso.');
    }

    /**
     * Sin comisiones propias en ese curso: crea una (a nombre del docente; del administrador, sin docente)
     * con un nombre por defecto y suma al alumno. El nombre se cambia después en Comisiones.
     */
    public function createCohortFor(StudentAccounts $accounts, int $userId, int $courseId): void
    {
        $student = User::where('role', Role::Student)->findOrFail($userId);
        $course = Course::whereIn('id', $student->subscriptions()->select('course_id'))->findOrFail($courseId);
        $viewer = auth()->user();
        // Crear no mueve a nadie de la comisión de otro docente.
        $this->authorize('assignCohort', [$student, $course, null]);

        $cohort = $course->cohorts()->create([
            'name' => $viewer->isTeacher() ? 'Comisión de '.$viewer->fullName() : 'Comisión '.($course->cohorts()->count() + 1),
            'teacher_id' => $viewer->isTeacher() ? $viewer->id : null,
        ]);
        $accounts->changeCohort($student, $course, $cohort->id);

        Flux::toast(variant: 'success', text: 'Creaste «'.$cohort->name.'» y '.$student->name.' quedó adentro. El nombre y el horario se cambian en Comisiones.');
    }

    /** Solo el administrador: la cuenta de un docente vuelve a ser de alumno (sus comisiones quedan sin docente). */
    public function demote(int $userId): void
    {
        abort_unless(auth()->user()->isAdmin(), 403);
        $teacher = User::where('role', Role::Teacher)->findOrFail($userId);
        Cohort::where('teacher_id', $teacher->id)->update(['teacher_id' => null]);
        $teacher->forceFill(['role' => Role::Student])->save();
        Flux::toast(variant: 'success', text: $teacher->fullName().' volvió a ser alumno.');
    }

    public function render(TeacherScope $scope)
    {
        $viewer = auth()->user();
        $teachers = $viewer->isAdmin() && $this->tab === 'docentes';
        $finding = $viewer->isTeacher() && $this->tab === 'sumar';
        $term = trim($this->search);

        $query = User::where('role', $teachers ? Role::Teacher : Role::Student)
            ->when($viewer->isTeacher() && ! $finding, fn ($q) => $scope->students($q, $viewer))
            // Buscando a los demás, el docente solo ve nombre y usuario y tiene que escribir algo.
            ->when($finding && mb_strlen($term) < 2, fn ($q) => $q->whereRaw('1 = 0'))
            ->when($term !== '', function ($q) use ($term, $finding) {
                $like = '%'.$term.'%';
                $q->where(fn ($w) => $w->where('name', 'like', $like)->orWhere('last_name', 'like', $like)->orWhere('username', 'like', $like)
                    ->when(! $finding, fn ($w) => $w->orWhere('email', 'like', $like)->orWhere('phone', 'like', $like)->orWhere('dni', 'like', $like)));
            })
            ->when($teachers, fn ($q) => $q->withCount('taughtCohorts'))
            ->orderBy('last_name')->orderBy('name');
        $people = $query->paginate(30);

        return view('livewire.admin.students.index', [
            'people' => $people,
            'teachers' => $teachers,
            'finding' => $finding,
            'active' => CourseSubscription::active()->whereIn('user_id', $people->pluck('id'))->pluck('user_id')->flip(),
            'detail' => $this->expanded && ! $teachers ? $this->detail($this->expanded, $viewer, $scope) : null,
        ]);
    }

    /**
     * Los cursos del alumno desplegado: su comisión en cada uno y a cuáles la puede cambiar quien mira.
     *
     * @return list<array<string, mixed>>
     */
    private function detail(int $userId, User $viewer, TeacherScope $scope): array
    {
        $student = User::where('role', Role::Student)->find($userId);
        if (! $student) {
            return [];
        }
        $mine = $viewer->isTeacher() ? $scope->cohortIds($viewer) : null;

        return $student->subscriptions()->with(['course.cohorts.teacher:id,name,last_name', 'cohort.teacher:id,name,last_name'])
            ->orderByDesc('ends_at')->get()->unique('course_id')
            ->map(function ($subscription) use ($student, $viewer, $mine) {
                $course = $subscription->course;
                $options = $course->cohorts->filter(fn (Cohort $cohort) => $mine === null || in_array($cohort->id, $mine, true))->values();

                return [
                    'course' => $course,
                    'cohort' => $subscription->cohort,
                    'active' => $subscription->ends_at->isFuture(),
                    'options' => $options,
                    'canChange' => $viewer->isAdmin() || ($options->isNotEmpty() && $viewer->can('assignCohort', [$student, $course, null])),
                    // Sin comisiones para elegir (y sin estar en la de otro docente): se crea una ahí mismo.
                    'canCreate' => $options->isEmpty() && $viewer->can('assignCohort', [$student, $course, null]),
                ];
            })->values()->all();
    }
}
