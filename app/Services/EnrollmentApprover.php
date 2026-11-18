<?php

namespace App\Services;

use App\Enums\CoinReason;
use App\Enums\RequestKind;
use App\Enums\RequestStatus;
use App\Models\CourseSubscription;
use App\Models\Currency;
use App\Models\EnrollmentRequest;
use App\Models\User;
use App\Notifications\PlatformNotification;
use DomainException;
use Illuminate\Support\Carbon;
use Illuminate\Support\Facades\DB;

class EnrollmentApprover
{
    /** Duraciones largas que se pueden dar al aprobar (en meses); sin elegir, vale el abono del curso. */
    public const MONTHS = [2, 3, 6, 12];

    public function __construct(private readonly Ledger $ledger) {}

    /**
     * Inscripción nueva: acredita las monedas del curso (precio del raíz) y abre el abono.
     * Renovación: solo extiende el abono; arranca cuando vence el actual (o hoy).
     * Con $months, el abono dura esos meses en vez de los días del curso (un pago de varios meses juntos).
     */
    public function approve(EnrollmentRequest $request, User $admin, ?string $note = null, ?int $months = null): CourseSubscription
    {
        if ($months !== null && ! in_array($months, self::MONTHS, true)) {
            throw new DomainException('Esa duración no está entre las que se ofrecen.');
        }

        $subscription = DB::transaction(function () use ($request, $admin, $note, $months) {
            $request = EnrollmentRequest::whereKey($request->id)->lockForUpdate()->firstOrFail();

            if ($request->status !== RequestStatus::Pending) {
                throw new DomainException('La solicitud ya fue revisada.');
            }

            $course = $request->course;
            $student = $request->user;

            $request->forceFill([
                'status' => RequestStatus::Approved,
                'admin_note' => $note,
                'reviewed_at' => now(),
                'reviewed_by' => $admin->id,
            ])->save();

            if ($request->kind === RequestKind::New && $course->root_price > 0) {
                $this->ledger->credit(
                    $student,
                    Currency::forCourse($course),
                    $course->root_price,
                    CoinReason::EnrollmentGrant,
                    $request,
                    $course,
                    by: $admin,
                );
            }

            // Si ya tiene abono (vigente o programado), el nuevo arranca cuando termina el último.
            $latestEnd = CourseSubscription::where('user_id', $student->id)
                ->where('course_id', $course->id)
                ->max('ends_at');
            $startsAt = $latestEnd && now()->lt($latestEnd) ? Carbon::parse($latestEnd) : now();

            // Una renovación sin comisión elegida sigue en la que ya tenía.
            $cohortId = $request->cohort_id ?? CourseSubscription::where('user_id', $student->id)
                ->where('course_id', $course->id)
                ->latest('ends_at')
                ->value('cohort_id');

            return CourseSubscription::create([
                'user_id' => $student->id,
                'course_id' => $course->id,
                'cohort_id' => $cohortId,
                'starts_at' => $startsAt,
                'ends_at' => $months ? $startsAt->copy()->addMonthsNoOverflow($months) : $startsAt->copy()->addDays($course->subscription_days),
                'enrollment_request_id' => $request->id,
                'granted_by' => $admin->id,
            ]);
        });

        $request->refresh();
        $course = $request->course;
        $request->user->notify(new PlatformNotification(
            'request.approved',
            '¡Aprobada! '.$course->title,
            $request->kind === RequestKind::New
                ? "Recibiste {$course->root_price} ".term('coin.course', $course, $course->root_price).'. Ya podés abrir el curso.'
                : 'Tu abono ahora vence el '.$subscription->ends_at->format('d/m/Y').'.',
            route('student.course', $course),
            'check-circle',
        ));

        return $subscription;
    }

    public function reject(EnrollmentRequest $request, User $admin, ?string $note = null): void
    {
        DB::transaction(function () use ($request, $admin, $note) {
            $request = EnrollmentRequest::whereKey($request->id)->lockForUpdate()->firstOrFail();

            if ($request->status !== RequestStatus::Pending) {
                throw new DomainException('La solicitud ya fue revisada.');
            }

            $request->forceFill([
                'status' => RequestStatus::Rejected,
                'admin_note' => $note,
                'reviewed_at' => now(),
                'reviewed_by' => $admin->id,
            ])->save();
        });

        $request->refresh();
        $request->user->notify(new PlatformNotification(
            'request.rejected',
            'Solicitud rechazada: '.$request->course->title,
            $note ?: 'Escribile al profe para ver qué pasó.',
            route('student.course', $request->course),
            'x-circle',
        ));
    }
}
