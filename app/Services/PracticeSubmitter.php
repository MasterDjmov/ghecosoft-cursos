<?php

namespace App\Services;

use App\Enums\SubmissionMode;
use App\Enums\SubmissionStatus;
use App\Models\Practice;
use App\Models\PracticeMark;
use App\Models\Submission;
use App\Models\User;
use App\Notifications\PlatformNotification;
use App\Support\Reward;
use DomainException;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;

/**
 * El alumno entrega una hoja (código, archivo o ambos) o la marca como completada.
 * Intentos ilimitados: se puede volver a entregar después de un "Rehacer".
 */
class PracticeSubmitter
{
    public function __construct(private readonly TreeAccess $access, private readonly SubmissionReviewer $reviewer) {}

    /** Última entrega del alumno en esa práctica. */
    public function latest(User $user, Practice $practice): ?Submission
    {
        return Submission::where('user_id', $user->id)->where('practice_id', $practice->id)->orderByDesc('attempt')->first();
    }

    public function isApproved(User $user, Practice $practice): bool
    {
        return Submission::where('user_id', $user->id)->where('practice_id', $practice->id)
            ->where('status', SubmissionStatus::Approved)->exists();
    }

    /** Motivo por el que no puede entregar ahora (null = puede). */
    public function blocker(User $user, Practice $practice): ?string
    {
        return match (true) {
            $this->access->isTrial($user, $practice->node) => 'Estás probando la clase gratis: para que el profe te corrija y seguir, pedí tu abono.',
            ! $this->access->isUnlocked($user, $practice->node) => 'Abrí el '.term('node', $practice->node->course).' para entregar.',
            ! $this->access->hasActiveSubscription($user, $practice->node->course) => 'Tu abono no está vigente: renovalo para entregar.',
            $this->isApproved($user, $practice) => 'Ya está aprobada.',
            $this->latest($user, $practice)?->status === SubmissionStatus::Submitted => 'Tu entrega está esperando corrección.',
            default => null,
        };
    }

    public function submit(User $user, Practice $practice, ?string $code, ?UploadedFile $file = null): Submission
    {
        $mode = $practice->submission_mode;
        $code = $code !== null && trim($code) !== '' ? $code : null;

        if ($mode === SubmissionMode::None) {
            throw new DomainException('Esta práctica no lleva entrega: marcala como completada.');
        }
        if ($mode === SubmissionMode::Code && ! $code) {
            throw new DomainException('Escribí tu código antes de entregar.');
        }
        if ($mode === SubmissionMode::File && ! $file) {
            throw new DomainException('Adjuntá el archivo antes de entregar.');
        }
        if ($mode === SubmissionMode::Both && ! $code && ! $file) {
            throw new DomainException('Escribí tu código o adjuntá un archivo.');
        }
        if ($mode === SubmissionMode::Code) {
            $file = null;
        }
        if ($mode === SubmissionMode::File) {
            $code = null;
        }

        $submission = DB::transaction(function () use ($user, $practice, $code, $file) {
            User::whereKey($user->id)->lockForUpdate()->first();

            if ($blocker = $this->blocker($user, $practice)) {
                throw new DomainException($blocker);
            }

            $data = [
                'practice_id' => $practice->id,
                'user_id' => $user->id,
                'attempt' => (int) Submission::where('user_id', $user->id)->where('practice_id', $practice->id)->max('attempt') + 1,
                'code' => $code,
                'submitted_at' => now(),
            ];

            if ($file) {
                $data['file_path'] = $file->storeAs('submissions', Str::uuid().'.'.Str::lower($file->getClientOriginalExtension()), 'local');
                $data['file_original_name'] = Str::limit($file->getClientOriginalName(), 250, '');
            }

            return Submission::create($data);
        });

        PlatformNotification::toStaff(new PlatformNotification(
            'submission.new',
            'Nueva entrega: '.$practice->title,
            $user->fullName().' · '.$practice->node->title.' (intento '.$submission->attempt.')',
            route('admin.submissions.show', $submission),
            'code-bracket-square',
        ), $user, $practice->node->course);

        return $submission;
    }

    /**
     * "Marcar como completada". En una práctica sin entrega cuenta como aprobada
     * (y paga lo que el docente le haya puesto). En las demás es solo una marca
     * personal del alumno; se puede sacar.
     */
    public function toggleMark(User $user, Practice $practice): ?Reward
    {
        // Solo en nodos abiertos: la Clase 0 de prueba (D71) no deja marcas ni registros.
        if (! $this->access->isUnlocked($user, $practice->node)) {
            throw new DomainException((string) $this->blocker($user, $practice));
        }

        if ($practice->submission_mode === SubmissionMode::None) {
            if ($blocker = $this->blocker($user, $practice)) {
                throw new DomainException($blocker);
            }

            $submission = Submission::create([
                'practice_id' => $practice->id,
                'user_id' => $user->id,
                'attempt' => (int) Submission::where('user_id', $user->id)->where('practice_id', $practice->id)->max('attempt') + 1,
                'submitted_at' => now(),
            ]);
            PracticeMark::firstOrCreate(['user_id' => $user->id, 'practice_id' => $practice->id], ['completed_at' => now()]);

            return $this->reviewer->approve($submission, null, notify: false);
        }

        $mark = PracticeMark::where('user_id', $user->id)->where('practice_id', $practice->id)->first();
        $mark ? $mark->delete() : PracticeMark::create(['user_id' => $user->id, 'practice_id' => $practice->id, 'completed_at' => now()]);

        return null;
    }
}
