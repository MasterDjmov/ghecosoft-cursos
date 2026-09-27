<?php

namespace App\Livewire\Admin;

use App\Enums\RequestStatus;
use App\Models\Course;
use App\Models\EnrollmentRequest;
use App\Services\EnrollmentApprover;
use DomainException;
use Flux\Flux;
use Livewire\Attributes\Title;
use Livewire\Attributes\Url;
use Livewire\Component;
use Livewire\WithPagination;

/** Solicitudes de inscripción y renovación: aprobar (monedas + abono) o rechazar. */
#[Title('Solicitudes')]
class Requests extends Component
{
    use WithPagination;

    #[Url(as: 'estado', except: 'pending')]
    public string $status = 'pending';

    #[Url(as: 'curso', except: '')]
    public string $courseId = '';

    public ?int $reviewingId = null;

    public string $decision = 'approve';

    public string $note = '';

    public function updated(string $property): void
    {
        if (in_array($property, ['status', 'courseId'], true)) {
            $this->resetPage();
        }
    }

    public function review(int $requestId, string $decision): void
    {
        $this->reviewingId = EnrollmentRequest::where('status', RequestStatus::Pending)->findOrFail($requestId)->id;
        $this->decision = $decision === 'reject' ? 'reject' : 'approve';
        $this->note = '';
        $this->resetValidation();

        Flux::modal('review')->show();
    }

    public function confirm(EnrollmentApprover $approver): void
    {
        $this->validate(
            ['note' => [$this->decision === 'reject' ? 'required' : 'nullable', 'string', 'max:1000']],
            ['note.required' => 'Contale al alumno por qué (lo va a ver en la ficha del curso).'],
            ['note' => 'nota'],
        );

        $request = EnrollmentRequest::findOrFail($this->reviewingId);

        try {
            if ($this->decision === 'approve') {
                $subscription = $approver->approve($request, auth()->user(), $this->note ?: null);
                $text = 'Aprobada: abono hasta el '.$subscription->ends_at->format('d/m/Y').'.';
            } else {
                $approver->reject($request, auth()->user(), $this->note);
                $text = 'Solicitud rechazada.';
            }
        } catch (DomainException $e) {
            Flux::toast(variant: 'danger', text: $e->getMessage());

            return;
        }

        Flux::modal('review')->close();
        Flux::toast(variant: 'success', text: $text);
        $this->reviewingId = null;
    }

    public function render()
    {
        $requests = EnrollmentRequest::with(['user', 'course', 'cohort', 'reviewer:id,name'])
            ->when($this->status !== 'all', fn ($q) => $q->where('status', $this->status))
            ->when($this->courseId !== '', fn ($q) => $q->where('course_id', (int) $this->courseId))
            ->orderByRaw("status = 'pending' desc")
            ->latest()
            ->paginate(20);

        return view('livewire.admin.requests', [
            'requests' => $requests,
            'courses' => Course::orderBy('position')->get(['id', 'title']),
            'reviewing' => $this->reviewingId ? EnrollmentRequest::with(['user', 'course'])->find($this->reviewingId) : null,
            'pendingCount' => EnrollmentRequest::where('status', RequestStatus::Pending)->count(),
        ]);
    }
}
