<?php

namespace App\Livewire\Admin;

use App\Enums\AuthorizationStatus;
use App\Enums\RequestStatus;
use App\Enums\Role;
use App\Enums\SubmissionStatus;
use App\Models\CourseSubscription;
use App\Models\EnrollmentRequest;
use App\Models\GuardianAuthorization;
use App\Models\Submission;
use App\Models\User;
use App\Support\PracticeStats;
use App\Support\ProgressStats;
use Livewire\Attributes\Title;
use Livewire\Component;

#[Title('Inicio del docente')]
class Dashboard extends Component
{
    /** Los períodos de las estadísticas (también los usa Estadísticas). */
    public const PERIODS = ['7' => 'Últimos 7 días', '30' => 'Últimos 30 días', '90' => 'Últimos 90 días', 'all' => 'Desde el principio'];

    public function render()
    {
        // El resumen de los últimos 30 días; el detalle, en Estadísticas (D107).
        $since = now()->subDays(30);
        $students = User::where('role', Role::Student->value)->select('id');

        return view('livewire.admin.dashboard', [
            'counters' => [
                ['label' => 'Solicitudes pendientes', 'value' => EnrollmentRequest::where('status', RequestStatus::Pending)->count(), 'icon' => 'inbox-arrow-down', 'url' => route('admin.requests')],
                ['label' => 'Entregas por corregir', 'value' => Submission::where('status', SubmissionStatus::Submitted)->count(), 'icon' => 'code-bracket-square', 'url' => route('admin.submissions.index')],
                ['label' => 'Alumnos con abono vigente', 'value' => CourseSubscription::active()->distinct()->count('user_id'), 'icon' => 'users', 'url' => route('admin.students.index')],
                ['label' => 'Autorizaciones pendientes', 'value' => GuardianAuthorization::where('status', AuthorizationStatus::Pending)->count(), 'icon' => 'document-check', 'url' => route('admin.authorizations')],
            ],
            'students' => User::where('role', Role::Student)->count(),
            'practices' => (new PracticeStats(since: $since))->summary(),
            'progress' => (new ProgressStats($students, since: $since))->summary(),
        ]);
    }
}
