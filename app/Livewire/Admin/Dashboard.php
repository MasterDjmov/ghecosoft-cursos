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
use Livewire\Attributes\Title;
use Livewire\Component;

#[Title('Inicio del docente')]
class Dashboard extends Component
{
    public function render()
    {
        return view('livewire.admin.dashboard', [
            'counters' => [
                ['label' => 'Solicitudes pendientes', 'value' => EnrollmentRequest::where('status', RequestStatus::Pending)->count(), 'icon' => 'inbox-arrow-down', 'url' => route('admin.requests')],
                ['label' => 'Entregas por corregir', 'value' => Submission::where('status', SubmissionStatus::Submitted)->count(), 'icon' => 'code-bracket-square'],
                ['label' => 'Alumnos con abono vigente', 'value' => CourseSubscription::active()->distinct()->count('user_id'), 'icon' => 'users'],
                ['label' => 'Autorizaciones pendientes', 'value' => GuardianAuthorization::where('status', AuthorizationStatus::Pending)->count(), 'icon' => 'document-check'],
            ],
            'students' => User::where('role', Role::Student)->count(),
        ]);
    }
}
