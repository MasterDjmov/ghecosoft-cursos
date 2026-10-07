<?php

namespace App\Services;

use App\Enums\RequestType;
use App\Enums\Role;
use App\Models\Course;
use App\Models\CourseSubscription;
use App\Models\EnrollmentRequest;
use App\Models\GuardianAuthorization;
use App\Models\Submission;
use App\Models\User;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;
use InvalidArgumentException;

/**
 * Cuentas que crea el docente (alumnos sin email o que necesitan una mano):
 * alta con clave provisoria, reseteo de clave e inscripción directa.
 */
class StudentAccounts
{
    public function __construct(private readonly EnrollmentApprover $approver) {}

    /**
     * Crea el alumno con clave provisoria; al entrar la tiene que cambiar.
     * Si viene un curso, lo inscribe como una solicitud aprobada (monedas + abono).
     *
     * @param  array{name: string, last_name: string, username: string, email?: ?string, phone?: ?string, birth_date?: ?string}  $data
     */
    public function create(array $data, string $password, User $admin, ?Course $course = null, ?int $cohortId = null): User
    {
        $student = DB::transaction(function () use ($data, $password) {
            $student = User::create([
                'name' => $data['name'],
                'last_name' => $data['last_name'],
                'username' => $data['username'],
                'email' => $data['email'] ?? null,
                'phone' => $data['phone'] ?? null,
                'birth_date' => $data['birth_date'] ?? null,
                'password' => $password,
            ]);

            $student->forceFill([
                'role' => Role::Student,
                'email_verified_at' => now(),
                'must_change_password' => true,
            ])->save();

            return $student;
        });

        if ($course) {
            $this->enroll($student, $course, $admin, $cohortId);
        }

        return $student;
    }

    /** Pasa por EnrollmentApprover, así queda en el libro igual que una inscripción aprobada. */
    public function enroll(User $student, Course $course, User $admin, ?int $cohortId = null): CourseSubscription
    {
        $request = EnrollmentRequest::create([
            'user_id' => $student->id,
            'course_id' => $course->id,
            'cohort_id' => $course->cohorts()->whereKey($cohortId)->value('id'),
            'kind' => app(EnrollmentRequester::class)->kindFor($student, $course),
            'type' => RequestType::Admin,
        ]);

        return $this->approver->approve($request, $admin, 'Alta hecha por el docente.');
    }

    /**
     * Asigna (o quita, con null) la comisión del alumno en un curso. Es solo una etiqueta:
     * va en todos sus abonos del curso y no toca aperturas, monedas, XP ni vencimientos.
     */
    public function changeCohort(User $student, Course $course, ?int $cohortId): void
    {
        $cohortId = $cohortId === null ? null : $course->cohorts()->whereKey($cohortId)->value('id')
            ?? throw new InvalidArgumentException('La comisión no es de este curso.');

        CourseSubscription::where('user_id', $student->id)
            ->where('course_id', $course->id)
            ->update(['cohort_id' => $cohortId]);
    }

    /**
     * Eliminar la cuenta de un alumno (D87), solo el administrador: la cuenta y todo lo suyo (abonos, entregas,
     * solicitudes, movimientos, mensajes) y sus archivos privados (entregas, comprobantes, autorizaciones).
     * Nunca una cuenta de docente o administrador.
     */
    public function delete(User $student): void
    {
        if ($student->role !== Role::Student) {
            throw new InvalidArgumentException('Solo se eliminan cuentas de alumnos.');
        }

        DB::transaction(function () use ($student) {
            $files = collect()
                ->merge(Submission::where('user_id', $student->id)->pluck('file_path'))
                ->merge(EnrollmentRequest::where('user_id', $student->id)->pluck('receipt_path'))
                ->merge(GuardianAuthorization::where('user_id', $student->id)->pluck('file_path'))
                ->filter()->unique()->values()->all();

            $student->delete();

            DB::afterCommit(function () use ($files) {
                Storage::disk('local')->delete($files);
                Ranking::forget();
            });
        });
    }

    /**
     * Lo que se borra al reiniciar una cuenta: tabla → columnas que apuntan al alumno. El orden importa
     * (las expediciones apuntan a los héroes). Un test revisa que toda tabla nueva con el alumno esté acá o en KEEP.
     */
    public const RESET = [
        'expeditions' => ['user_id'], 'crafts' => ['user_id'], 'heroes' => ['user_id'], 'mounts' => ['user_id'],
        'item_movements' => ['user_id'], 'coin_transactions' => ['user_id'], 'xp_transactions' => ['user_id'],
        'node_step_completions' => ['user_id'], 'practice_grants' => ['user_id'], 'node_unlocks' => ['user_id'], 'practice_marks' => ['user_id'],
        'submission_comments' => ['user_id'], 'submissions' => ['user_id'], 'practice_messages' => ['student_id', 'author_id'],
        'course_completions' => ['user_id'], 'user_badges' => ['user_id'], 'ranking_snapshots' => ['user_id'],
        'universe_votes' => ['user_id'], 'course_subscriptions' => ['user_id'], 'enrollment_requests' => ['user_id'],
    ];

    /** Lo que se conserva: cómo entra (llaves de acceso, sesiones), la autorización de menor y los «Avisame». */
    public const KEEP = ['passkeys', 'session_evictions', 'guardian_authorizations', 'course_interests'];

    /**
     * Reiniciar la cuenta: queda como recién creada (mismo usuario, nombre y clave) pero sin cursos ni nada de
     * lo hecho: abonos, progreso, entregas, comprobantes, monedas, XP, oro, héroes, mochila, consultas e
     * insignias. Para volver a empezar un curso de cero. Solo el administrador.
     */
    public function reset(User $student): void
    {
        if ($student->role !== Role::Student) {
            throw new InvalidArgumentException('Solo se reinician cuentas de alumnos.');
        }

        DB::transaction(function () use ($student) {
            $files = collect()
                ->merge(Submission::where('user_id', $student->id)->pluck('file_path'))
                ->merge(EnrollmentRequest::where('user_id', $student->id)->pluck('receipt_path'))
                ->filter()->unique()->values()->all();

            foreach (self::RESET as $table => $columns) {
                DB::table($table)->where(function ($query) use ($columns, $student) {
                    foreach ($columns as $column) {
                        $query->orWhere($column, $student->id);
                    }
                })->delete();
            }
            $student->notifications()->delete();
            $student->forceFill(['xp_total' => 0])->save();

            DB::afterCommit(function () use ($files) {
                Storage::disk('local')->delete($files);
                Ranking::forget();
            });
        });
    }

    /** Nueva clave provisoria; la anterior deja de valer y al entrar la tiene que cambiar. */
    public function resetPassword(User $student): string
    {
        $password = self::temporaryPassword();
        $student->forceFill(['password' => $password, 'must_change_password' => true])->save();

        return $password;
    }

    /** Texto para mandarle por WhatsApp con los datos de acceso. */
    public static function accessMessage(User $student, string $password, bool $reset = false): string
    {
        return implode("\n", [
            $reset
                ? "¡Hola, {$student->name}! Te reseteé la clave de ".config('app.name').'.'
                : "¡Hola, {$student->name}! Ya tenés tu cuenta en ".config('app.name').'.',
            'Entrá en: '.route('login'),
            "Usuario: {$student->username}",
            "Clave provisoria: {$password}",
            'Al entrar te va a pedir que elijas tu propia clave.',
        ]);
    }

    /** Fácil de dictar por WhatsApp: sin letras que se confunden (l, o, i). Ej.: "Kxqa4821". */
    public static function temporaryPassword(): string
    {
        $letters = collect(range(1, 4))->map(fn () => 'abcdefghjkmnpqrstuvwxyz'[random_int(0, 22)])->implode('');

        return Str::ucfirst($letters).random_int(1000, 9999);
    }
}
