<?php

namespace App\Livewire\Admin;

use App\Enums\AuthorizationStatus;
use App\Enums\RequestStatus;
use App\Enums\Role;
use App\Enums\SubmissionStatus;
use App\Models\Course;
use App\Models\CourseSubscription;
use App\Models\EnrollmentRequest;
use App\Models\GuardianAuthorization;
use App\Models\Submission;
use App\Models\User;
use App\Support\PracticeStats;
use Livewire\Attributes\Title;
use Livewire\Attributes\Url;
use Livewire\Component;

#[Title('Inicio del docente')]
class Dashboard extends Component
{
    public const PERIODS = ['7' => 'Últimos 7 días', '30' => 'Últimos 30 días', '90' => 'Últimos 90 días', 'all' => 'Desde el principio'];

    /** Estadísticas: '' todos los cursos o el id de uno. */
    #[Url(as: 'curso', except: '')]
    public string $statsCourse = '';

    #[Url(as: 'periodo', except: '30')]
    public string $period = '30';

    public function render()
    {
        $stats = new PracticeStats(
            courseId: $this->statsCourse !== '' ? (int) $this->statsCourse : null,
            since: array_key_exists($this->period, self::PERIODS) && $this->period !== 'all' ? now()->subDays((int) $this->period) : null,
        );

        return view('livewire.admin.dashboard', [
            'counters' => [
                ['label' => 'Solicitudes pendientes', 'value' => EnrollmentRequest::where('status', RequestStatus::Pending)->count(), 'icon' => 'inbox-arrow-down', 'url' => route('admin.requests')],
                ['label' => 'Entregas por corregir', 'value' => Submission::where('status', SubmissionStatus::Submitted)->count(), 'icon' => 'code-bracket-square', 'url' => route('admin.submissions.index')],
                ['label' => 'Alumnos con abono vigente', 'value' => CourseSubscription::active()->distinct()->count('user_id'), 'icon' => 'users', 'url' => route('admin.students.index')],
                ['label' => 'Autorizaciones pendientes', 'value' => GuardianAuthorization::where('status', AuthorizationStatus::Pending)->count(), 'icon' => 'document-check', 'url' => route('admin.authorizations')],
            ],
            'students' => User::where('role', Role::Student)->count(),
            'summary' => $stats->summary(),
            'byCourse' => $this->statsCourse === '' ? $stats->byCourse() : collect(),
            'mostChosen' => $stats->mostChosen(),
            'hardest' => $stats->hardest(),
            'courses' => Course::orderBy('position')->get(['id', 'title']),
            'periods' => self::PERIODS,
        ]);
    }
}
