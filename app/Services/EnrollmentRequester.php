<?php

namespace App\Services;

use App\Enums\RequestKind;
use App\Enums\RequestStatus;
use App\Enums\RequestType;
use App\Models\Course;
use App\Models\CourseSubscription;
use App\Models\EnrollmentRequest;
use App\Models\Setting;
use App\Models\User;
use App\Notifications\PlatformNotification;
use DomainException;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Str;

/**
 * El alumno pide entrar a un curso (o renovar el abono): con comprobante o
 * avisando por WhatsApp. El docente la aprueba después con EnrollmentApprover.
 */
class EnrollmentRequester
{
    public function pending(User $user, Course $course): ?EnrollmentRequest
    {
        return EnrollmentRequest::where('user_id', $user->id)
            ->where('course_id', $course->id)
            ->where('status', RequestStatus::Pending)
            ->latest()
            ->first();
    }

    /** Si ya tuvo un abono en el curso, lo que pide es una renovación (no da monedas). */
    public function kindFor(User $user, Course $course): RequestKind
    {
        return CourseSubscription::where('user_id', $user->id)->where('course_id', $course->id)->exists()
            ? RequestKind::Renewal
            : RequestKind::New;
    }

    public function request(User $user, Course $course, RequestType $type, ?UploadedFile $receipt = null, ?string $message = null, ?int $cohortId = null): EnrollmentRequest
    {
        if (! $course->is_published) {
            throw new DomainException('El curso no está disponible.');
        }
        if ($this->pending($user, $course)) {
            throw new DomainException('Ya tenés una solicitud pendiente para este curso.');
        }
        if ($type === RequestType::Receipt && ! $receipt) {
            throw new DomainException('Adjuntá el comprobante.');
        }

        $data = [
            'user_id' => $user->id,
            'course_id' => $course->id,
            'cohort_id' => $course->cohorts()->whereKey($cohortId)->where('is_open_for_enrollment', true)->value('id'),
            'kind' => $this->kindFor($user, $course),
            'type' => $type,
            'message' => $message ? Str::limit(trim($message), 1000, '') : null,
        ];

        if ($receipt) {
            $data['receipt_path'] = $receipt->storeAs('receipts', Str::uuid().'.'.Str::lower($receipt->getClientOriginalExtension()), 'local');
            $data['receipt_original_name'] = Str::limit($receipt->getClientOriginalName(), 250, '');
        }

        $request = EnrollmentRequest::create($data);

        PlatformNotification::toAdmins(new PlatformNotification(
            'request.new',
            ($request->kind === RequestKind::Renewal ? 'Renovación: ' : 'Nueva inscripción: ').$course->title,
            $user->fullName().($type === RequestType::Receipt ? ' mandó el comprobante.' : ' te va a escribir por WhatsApp.'),
            route('admin.requests'),
            'inbox-arrow-down',
        ));

        return $request;
    }

    /** Link de WhatsApp al profe con el mensaje armado, o null si no cargó su número. */
    public function whatsappUrl(User $user, Course $course, RequestKind $kind): ?string
    {
        $number = preg_replace('/\D+/', '', (string) Setting::get('whatsapp_number'));
        if ($number === '') {
            return null;
        }

        $message = strtr((string) Setting::get('whatsapp_message', 'Hola profe, soy {nombre}. Quiero inscribirme en {curso}.'), [
            '{nombre}' => $user->fullName(),
            '{usuario}' => $user->username,
            '{curso}' => $course->title,
        ]);
        if ($kind === RequestKind::Renewal) {
            $message .= ' (renovación del abono)';
        }

        return 'https://wa.me/'.$number.'?text='.rawurlencode($message);
    }
}
