<?php

namespace App\Livewire\Admin;

use App\Enums\Role;
use App\Models\Cohort;
use App\Models\Course;
use App\Models\CourseSubscription;
use App\Models\User;
use App\Services\TeacherScope;
use App\Support\PracticeStats;
use App\Support\ProgressStats;
use Illuminate\Database\Eloquent\Builder;
use Livewire\Attributes\Title;
use Livewire\Attributes\Url;
use Livewire\Component;

/**
 * D107 fase 2: dónde se traban los alumnos, con filtros de curso, comisión, período y alumno. El administrador ve
 * todo; el docente, solo a los alumnos de sus comisiones en sus cursos (TeacherScope).
 */
#[Title('Estadísticas')]
class Statistics extends Component
{
    #[Url(as: 'curso', except: '')]
    public string $course = '';

    #[Url(as: 'comision', except: '')]
    public string $cohort = '';

    #[Url(as: 'periodo', except: '30')]
    public string $period = '30';

    #[Url(as: 'alumno', except: '')]
    public string $student = '';

    public function updatedCourse(): void
    {
        $this->reset('cohort', 'student');
    }

    public function updatedCohort(): void
    {
        $this->reset('student');
    }

    /** Las comisiones que puede elegir: todas, o las del docente; las del curso elegido. */
    private function cohorts(TeacherScope $scope): Builder
    {
        $viewer = auth()->user();

        return Cohort::query()
            ->when(! $viewer->isAdmin(), fn ($q) => $q->whereIn('id', $scope->cohortIds($viewer) ?: [0]))
            ->when($this->course !== '', fn ($q) => $q->where('course_id', (int) $this->course));
    }

    /**
     * Los alumnos que entran en los números, según el que mira y los filtros. Para los números no hace falta pedir
     * la inscripción al curso (ya se filtran por curso); para la lista del filtro de alumnos, sí.
     */
    private function students(TeacherScope $scope, bool $forOptions = false): Builder
    {
        $query = $scope->students(User::where('role', Role::Student->value), auth()->user());
        if ($this->cohort !== '') {
            $cohort = $this->cohorts($scope)->find((int) $this->cohort);
            $query->whereIn('users.id', CourseSubscription::where('cohort_id', $cohort?->id ?? 0)->select('user_id'));
        } elseif ($forOptions && $this->course !== '') {
            $query->whereIn('users.id', CourseSubscription::where('course_id', (int) $this->course)->select('user_id'));
        }
        if (! $forOptions && $this->student !== '') {
            $query->where('users.id', (int) $this->student);
        }

        return $query;
    }

    public function render(TeacherScope $scope)
    {
        $viewer = auth()->user();
        $courseIds = $viewer->isAdmin() ? null : Cohort::whereIn('id', $scope->cohortIds($viewer) ?: [0])->pluck('course_id')->unique()->values()->all();
        $courses = Course::when($courseIds !== null, fn ($q) => $q->whereIn('id', $courseIds ?: [0]))->orderBy('position')->get(['id', 'title', 'slug']);
        $courseId = $this->course !== '' && $courses->contains('id', (int) $this->course) ? (int) $this->course : null;
        $since = array_key_exists($this->period, Dashboard::PERIODS) && $this->period !== 'all' ? now()->subDays((int) $this->period) : null;
        $students = $this->students($scope)->select('users.id');

        $progress = new ProgressStats($students, $courseId, $since, $courseIds);
        $practices = new PracticeStats($courseId, $since, $students, $courseIds);
        $chosen = $this->student !== '' ? User::find((int) $this->student) : null;

        return view('livewire.admin.statistics', [
            'courses' => $courses,
            'selectedCourse' => $courseId ? $courses->firstWhere('id', $courseId) : null,
            'cohortOptions' => $this->cohorts($scope)->with('course:id,title')->orderBy('name')->get(['id', 'name', 'course_id']),
            'studentOptions' => $this->students($scope, forOptions: true)->orderBy('name')->orderBy('last_name')->get(['users.id', 'name', 'last_name', 'username']),
            'chosen' => $chosen,
            'periods' => Dashboard::PERIODS,
            'summary' => $progress->summary(),
            'devices' => $progress->devices(),
            'funnel' => $progress->funnel(),
            'hardestSteps' => $progress->hardestSteps(),
            'stuck' => $progress->stuck(),
            'practiceSummary' => $practices->summary(),
            'mostChosen' => $practices->mostChosen(),
            'hardest' => $practices->hardest(),
        ]);
    }
}
