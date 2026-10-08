<?php

namespace App\Console\Commands;

use App\Actions\Fortify\CreateNewUser;
use App\Enums\RequestStatus;
use App\Enums\RequestType;
use App\Enums\Role;
use App\Enums\SubmissionMode;
use App\Enums\SubmissionStatus;
use App\Models\CoinTransaction;
use App\Models\Course;
use App\Models\CourseCompletion;
use App\Models\CourseSubscription;
use App\Models\Currency;
use App\Models\EnrollmentRequest;
use App\Models\Node;
use App\Models\NodeUnlock;
use App\Models\Practice;
use App\Models\Submission;
use App\Models\User;
use App\Models\XpTransaction;
use App\Services\EnrollmentApprover;
use App\Services\EnrollmentRequester;
use App\Services\Ledger;
use App\Services\NodeUnlocker;
use App\Services\PracticeSubmitter;
use App\Services\Ranking;
use App\Services\StepCompleter;
use App\Services\StudentAccounts;
use App\Services\SubmissionReviewer;
use App\Services\TreeAccess;
use App\Support\LocalCodeRunner;
use Carbon\Carbon;
use Carbon\CarbonImmutable;
use DomainException;
use Illuminate\Console\Attributes\Description;
use Illuminate\Console\Attributes\Signature;
use Illuminate\Console\Command;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\RateLimiter;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;
use Throwable;
use ZipArchive;

/**
 * "Súper test" de un curso (docs/SIMULACION.md): 5 alumnos se inscriben, el docente
 * los aprueba, juegan día por día hasta abrir todo el árbol y el docente corrige
 * (aprueba o pide rehacer según el código funcione). Todo pasa por los mismos
 * servicios que usan las pantallas; al final se revisan las reglas de la economía.
 *
 * Solo para la base local: nunca en producción.
 */
#[Signature('app:simulate-course {course : Slug del curso publicado}
    {--days=90 : Días hacia atrás desde hoy en que arranca la cursada}
    {--seed=2026 : Semilla (misma semilla, misma historia)}
    {--reset : Borrar antes a los alumnos de una simulación anterior}
    {--report : No simular: solo mostrar el informe de la simulación que ya está en la base}')]
#[Description('Simula 5 alumnos cursando un curso completo y al docente corrigiendo (solo local)')]
class SimulateCourse extends Command
{
    /** Los alumnos simulados se reconocen por este dominio de email. */
    public const DOMAIN = 'simulacion.test';

    /**
     * Cada alumno juega distinto: cuánto se equivoca, cuántas optativas hace,
     * cuántas acciones por día, cuántos días falta y cómo se inscribe.
     */
    private const PERSONAS = [
        ['name' => 'Valentina', 'last_name' => 'Ríos', 'username' => 'valen', 'password' => 'Valen2026', 'hero' => 'Valkiria', 'errors' => 0.08, 'optionals' => 1.0, 'pace' => [5, 9], 'skip' => 0.08, 'start' => 0, 'via' => 'receipt', 'renew_delay' => 0],
        ['name' => 'Tomás', 'last_name' => 'Herrera', 'username' => 'tomi', 'password' => 'Tomi2026', 'hero' => 'Toro', 'errors' => 0.25, 'optionals' => 0.5, 'pace' => [6, 11], 'skip' => 0.15, 'start' => 0, 'via' => 'contact', 'renew_delay' => 1],
        ['name' => 'Camila', 'last_name' => 'Sosa', 'username' => 'cami', 'password' => 'Cami2026', 'hero' => 'Cometa', 'errors' => 0.15, 'optionals' => 0.7, 'pace' => [4, 8], 'skip' => 0.1, 'start' => 1, 'via' => 'receipt', 'renew_delay' => 0],
        ['name' => 'Mateo', 'last_name' => 'Quiroga', 'username' => 'mateo', 'password' => 'Mateo2026', 'hero' => 'Martillo', 'errors' => 0.35, 'optionals' => 0.3, 'pace' => [4, 9], 'skip' => 0.25, 'start' => 2, 'via' => 'receipt', 'renew_delay' => 4],
        ['name' => 'Lucía', 'last_name' => 'Fernández', 'username' => 'lu', 'password' => 'Lucia2026', 'hero' => 'Luna', 'errors' => 0.12, 'optionals' => 0.6, 'pace' => [5, 9], 'skip' => 0.1, 'start' => 3, 'via' => 'admin', 'renew_delay' => 0],
    ];

    private Course $course;

    private User $teacher;

    /** @var array<string, array<string, mixed>> estado y números de cada alumno */
    private array $students = [];

    /** @var list<string> lo que salió mal en el sistema (excepciones inesperadas) */
    private array $failures = [];

    /** Lenguaje del curso y el programa con que el docente prueba el código (python3, gcc, g++), si está instalado. */
    private string $language = '';

    private ?string $runner = null;

    private $nodes = null;

    private string $workDir;

    private LocalCodeRunner $local;

    public function handle(): int
    {
        if (app()->isProduction()) {
            $this->error('La simulación es solo para la base local.');

            return self::FAILURE;
        }
        // Nunca un mail de verdad: con el SMTP del docente en el .env local, una simulación agotó el límite
        // diario de Gmail (que comparte con producción y con su otra página). Los avisos quedan en la campanita.
        config(['mail.default' => 'array']);
        app('mail.manager')->forgetMailers();

        $course = Course::where('slug', $this->argument('course'))->first();
        $teacher = User::where('role', Role::Admin)->orderBy('id')->first();
        if (! $course || ! $course->is_published) {
            $this->error('No hay un curso publicado con ese slug.');

            return self::FAILURE;
        }
        if (! $teacher) {
            $this->error('Falta un docente (admin) en la base.');

            return self::FAILURE;
        }
        $this->course = $course;
        $this->teacher = $teacher;

        if ($this->option('report')) {
            foreach (self::PERSONAS as $persona) {
                if ($user = User::where('username', $persona['username'])->where('email', 'like', '%@'.self::DOMAIN)->first()) {
                    $this->students[$persona['username']] = ['persona' => $persona, 'user' => $user, 'stuck' => null, 'attempts' => Submission::where('user_id', $user->id)->whereHas('practice.node', fn ($q) => $q->where('course_id', $course->id))->count(),
                        'redos' => Submission::where('user_id', $user->id)->where('status', SubmissionStatus::Redo)->whereHas('practice.node', fn ($q) => $q->where('course_id', $course->id))->count(),
                        'renewals' => EnrollmentRequest::where('user_id', $user->id)->where('course_id', $course->id)->where('kind', 'renewal')->where('status', RequestStatus::Approved)->count()];
                }
            }
            $this->report(null);

            return self::SUCCESS;
        }

        // Los alumnos de una simulación anterior (de otro curso) se reutilizan: así se prueban cursos en paralelo.
        // Si ya cursaron ESTE curso, hay que empezar de cero con --reset.
        if ($this->option('reset')) {
            $this->reset();
        } elseif (CourseSubscription::where('course_id', $course->id)->whereIn('user_id', $this->simulatedIds())->exists()) {
            $this->error('Los alumnos simulados ya cursaron este curso: usá --reset para borrarlos y empezar de nuevo.');

            return self::FAILURE;
        }

        mt_srand((int) $this->option('seed'));
        $this->language = $course->language->value;
        $this->workDir = storage_path('app/simulacion');
        // Python corta a los 5 s como Pyodide en el navegador; lo compilado corre en la compu del alumno
        // y hay prácticas que miden rendimiento (C++ R05-N03-M3 ronda los 5 s sin optimizar).
        $this->local = new LocalCodeRunner($this->language, $this->workDir, timeout: $this->language === 'python' ? 5 : 20);
        $this->runner = $this->local->binary;

        $this->info("Simulando «{$course->title}»: ".count(self::PERSONAS).' alumnos, corrige '.$teacher->name.'.');
        $this->line($this->runner ? 'El docente prueba el código con '.basename($this->runner).'.' : 'El docente compara el código con la solución de referencia.');

        $start = CarbonImmutable::today()->subDays((int) $this->option('days'))->setTime(9, 0);
        $today = CarbonImmutable::today();

        try {
            for ($day = 0; $start->addDays($day)->lte($today); $day++) {
                $this->simulateDay($start->addDays($day), $day);
                if ($this->students !== [] && collect($this->students)->every(fn ($s) => $s['finished_on'] !== null)) {
                    break;
                }
            }
        } finally {
            $this->travel(null);
        }

        $this->keepSubscriptionsActive();
        // Los avisos de la simulación le llegan al docente ya leídos (quedan en el historial).
        $this->teacher->unreadNotifications()->where('created_at', '>=', $start)->update(['read_at' => now()]);
        Cache::forget('ranking.global');
        Cache::forget("ranking.course.{$course->id}");

        $this->report($day);

        return $this->failures === [] ? self::SUCCESS : self::FAILURE;
    }

    // ---------------------------------------------------------------- días

    private function simulateDay(CarbonImmutable $date, int $day): void
    {
        // A la mañana, el docente: aprueba inscripciones y corrige lo que llegó.
        $this->travel($date->setTime(8, mt_rand(0, 59)));
        $this->teacherMorning();

        // Se inscriben los que arrancan hoy.
        foreach (self::PERSONAS as $persona) {
            if ($persona['start'] === $day) {
                $this->travel($date->setTime(10, mt_rand(0, 59)));
                $this->enroll($persona, $day);
            }
        }

        // Cada alumno juega un rato (algunos días no entra).
        foreach ($this->students as $username => $state) {
            if ($state['finished_on'] !== null || $state['enrolled_on'] === null || mt_rand() / mt_getrandmax() < $state['persona']['skip']) {
                continue;
            }
            $this->travel($date->setTime(mt_rand(14, 21), mt_rand(0, 59)));
            $this->play($username, $day);
        }

        // Una foto del ranking por día (así la landing muestra tendencias).
        $this->travel($date->setTime(23, 0));
        $ranking = app(Ranking::class);
        Cache::forget('ranking.global');
        $this->attempt('ranking', fn () => $ranking->trends($ranking->global()));
    }

    private function teacherMorning(): void
    {
        $requests = EnrollmentRequest::where('course_id', $this->course->id)->where('status', RequestStatus::Pending)
            ->whereIn('user_id', $this->simulatedIds())->get();
        foreach ($requests as $request) {
            $this->attempt('aprobar inscripción', function () use ($request) {
                app(EnrollmentApprover::class)->approve($request, $this->teacher, 'Pago recibido. ¡Bienvenido/a!');
                $state = &$this->students[$request->user->username];
                $state['enrolled_on'] ??= now();
                $state[$request->kind->value === 'renewal' ? 'renewals' : 'enrollments']++;
            });
        }

        $pending = Submission::where('status', SubmissionStatus::Submitted)
            ->whereIn('user_id', $this->simulatedIds())
            ->whereHas('practice.node', fn ($q) => $q->where('course_id', $this->course->id))
            ->with('practice', 'user')->orderBy('submitted_at')->get();
        foreach ($pending as $submission) {
            $this->attempt('corregir', fn () => $this->review($submission));
        }
    }

    private function enroll(array $persona, int $day): void
    {
        $this->students[$persona['username']] = [
            'persona' => $persona, 'user' => null, 'enrolled_on' => null, 'finished_on' => null, 'started_day' => $day,
            'enrollments' => 0, 'renewals' => 0, 'attempts' => 0, 'redos' => 0, 'unlocks' => 0, 'active_days' => 0,
            'stuck' => null, 'expired_since' => null,
        ];

        $this->attempt('inscribir a '.$persona['username'], function () use ($persona) {
            $email = $persona['username'].'@'.self::DOMAIN;
            $data = ['name' => $persona['name'], 'last_name' => $persona['last_name'], 'username' => $persona['username'], 'email' => $email];

            // Ya existe (cursó otro curso en una simulación anterior): se inscribe en este.
            if ($existente = User::where('username', $persona['username'])->where('email', $email)->first()) {
                if ($persona['via'] === 'admin') {
                    app(StudentAccounts::class)->enroll($existente, $this->course, $this->teacher);
                    $this->students[$persona['username']]['enrolled_on'] = now();
                    $this->students[$persona['username']]['enrollments']++;
                } else {
                    $type = $persona['via'] === 'contact' ? RequestType::Contact : RequestType::Receipt;
                    app(EnrollmentRequester::class)->request($existente, $this->course, $type, $type === RequestType::Receipt ? $this->receipt() : null, 'Hola profe, ahora quiero hacer este curso.');
                }
                $this->students[$persona['username']]['user'] = $existente;

                return;
            }

            if ($persona['via'] === 'admin') {
                // La crea el docente con clave provisoria, ya inscripta; ella la cambia al entrar.
                $user = app(StudentAccounts::class)->create($data + ['birth_date' => '2000-05-10'], StudentAccounts::temporaryPassword(), $this->teacher, $this->course);
                $user->forceFill(['password' => $persona['password'], 'must_change_password' => false])->save();
                $this->students[$persona['username']]['enrolled_on'] = now();
                $this->students[$persona['username']]['enrollments']++;
            } else {
                // El tope de registros por IP es para la web; acá se inscriben todos desde la misma compu.
                RateLimiter::clear('register:'.request()->ip());
                $user = app(CreateNewUser::class)->create($data + ['password' => $persona['password'], 'password_confirmation' => $persona['password']]);
                $type = $persona['via'] === 'contact' ? RequestType::Contact : RequestType::Receipt;
                app(EnrollmentRequester::class)->request($user, $this->course, $type, $type === RequestType::Receipt ? $this->receipt() : null, 'Hola profe, quiero arrancar.');
            }

            $user->forceFill(['hero_name' => $persona['hero'], 'birth_date' => '2000-05-10', 'cv_public' => true, 'email_verified_at' => now()])->save();
            $this->students[$persona['username']]['user'] = $user;
        });
    }

    // ---------------------------------------------------------------- el alumno

    private function play(string $username, int $day): void
    {
        $state = &$this->students[$username];
        $user = $state['user']->fresh();
        $access = app(TreeAccess::class);

        // Abono vencido: pide la renovación (algunos tardan unos días).
        if (! $access->hasActiveSubscription($user, $this->course)) {
            $state['expired_since'] ??= $day;
            if ($day - $state['expired_since'] >= $state['persona']['renew_delay'] && ! app(EnrollmentRequester::class)->pending($user, $this->course)) {
                $this->attempt("renovar ({$username})", fn () => app(EnrollmentRequester::class)->request($user, $this->course, RequestType::Receipt, $this->receipt(), 'Renuevo el abono.'));
            }

            return;
        }
        $state['expired_since'] = null;
        $state['active_days']++;

        [$min, $max] = $state['persona']['pace'];
        for ($i = mt_rand($min, $max); $i > 0; $i--) {
            $action = $this->nextAction($user, $state);
            if ($action === null) {
                return;
            }
            $this->attempt("{$username}: {$action['what']}", $action['run']);
            $this->travel(now()->addMinutes(mt_rand(8, 40)));
        }
    }

    /** Qué hace ahora: entregar lo pendiente, abrir el siguiente nodo, o esperar. */
    private function nextAction(User $user, array &$state): ?array
    {
        $access = app(TreeAccess::class);
        $nodes = $this->nodes();
        $unlockedIds = NodeUnlock::where('user_id', $user->id)->pluck('node_id')->flip();
        $unlocked = $nodes->filter(fn (Node $node) => $unlockedIds->has($node->id));
        $latest = Submission::where('user_id', $user->id)->orderBy('attempt')->get()->keyBy('practice_id');
        $approved = Submission::where('user_id', $user->id)->where('status', SubmissionStatus::Approved)->pluck('practice_id')->flip();

        // Se puede entregar: no está aprobada ni esperando corrección (el servicio lo vuelve a controlar).
        $open = fn (Practice $practice) => ! $approved->has($practice->id) && $latest->get($practice->id)?->status !== SubmissionStatus::Submitted;
        $todo = fn (bool $allOptionals) => $unlocked->flatMap(fn (Node $node) => $node->practices->sortBy([['is_required', 'desc'], ['position', 'asc']]))
            ->first(fn (Practice $practice) => ($practice->is_required || $allOptionals || $this->wants($user, $practice, $state['persona']['optionals'])) && $open($practice));

        if ($practice = $todo(false)) {
            return ['what' => 'entrega «'.$practice->title.'»', 'run' => function () use ($user, $practice, &$state) {
                $this->submit($user, $practice, $state);
            }];
        }

        if ($node = $nodes->first(fn (Node $node) => ! $unlocked->contains($node) && $access->canUnlock($user, $node))) {
            return ['what' => 'abre «'.$node->title.'»', 'run' => function () use ($user, $node, &$state) {
                app(NodeUnlocker::class)->unlock($user, $node);
                $state['unlocks']++;
            }];
        }

        if ($latest->contains(fn (Submission $submission) => $submission->status === SubmissionStatus::Submitted)) {
            return null;
        }

        if ($unlocked->count() === $nodes->count() && $access->isCourseCompleted($user, $this->course)) {
            $state['finished_on'] ??= now();

            return null;
        }

        // Le faltan monedas para abrir algo (comodines para una Senda): vuelve a hacer optativas que había dejado.
        $short = $nodes->first(fn (Node $node) => ! $unlocked->contains($node) && $access->unlockBlockers($user, $node) === [TreeAccess::BLOCK_INSUFFICIENT_FUNDS]);
        if ($short && ($practice = $todo(true))) {
            return ['what' => 'optativa para juntar monedas: «'.$practice->title.'»', 'run' => function () use ($user, $practice, &$state) {
                $this->submit($user, $practice, $state);
            }];
        }

        $locked = $nodes->first(fn (Node $node) => ! $unlocked->contains($node));
        $state['stuck'] = $locked ? '«'.$locked->title.'»: '.implode(', ', $access->unlockBlockers($user, $locked)) : 'sin nada para hacer';

        return null;
    }

    private function submit(User $user, Practice $practice, array &$state): void
    {
        $previous = app(PracticeSubmitter::class)->latest($user, $practice);

        // D95: antes de las prácticas, supera las micro-misiones del nodo.
        if (! app(TreeAccess::class)->practicesOpen($user, $practice->node)) {
            foreach ($practice->node->steps as $step) {
                app(StepCompleter::class)->complete($user, $step, (string) $step->expected_output);
            }
        }

        // Después de una corrección, a veces le contesta al profe.
        if ($previous?->status === SubmissionStatus::Redo && mt_rand(1, 3) === 1) {
            app(SubmissionReviewer::class)->comment($previous, $user, collect(['Listo, ahí lo corregí.', 'Gracias profe, no había visto eso.', 'Ahora sí, creo.'])->random());
        }

        if ($practice->submission_mode === SubmissionMode::None) {
            app(PracticeSubmitter::class)->toggleMark($user, $practice);
            $state['attempts']++;

            return;
        }

        // En el segundo intento se equivoca bastante menos.
        $chance = $state['persona']['errors'] * ($previous ? 0.3 : 1);
        $wrong = mt_rand() / mt_getrandmax() < $chance;

        $code = in_array($practice->submission_mode, [SubmissionMode::Code, SubmissionMode::Both], true) ? $this->studentCode($practice, $wrong) : null;
        $file = in_array($practice->submission_mode, [SubmissionMode::File, SubmissionMode::Both], true) ? $this->studentFile($practice, $wrong) : null;

        app(PracticeSubmitter::class)->submit($user, $practice, $code, $file);
        $state['attempts']++;
    }

    /** Los nodos del curso con sus prácticas (no cambian durante la simulación). */
    private function nodes()
    {
        return $this->nodes ??= $this->course->nodes()->where('is_published', true)->orderBy('id')->with('practices')->get();
    }

    private function wants(User $user, Practice $practice, float $probability): bool
    {
        return (crc32($user->id.'-'.$practice->id) % 1000) / 1000 < $probability;
    }

    private function studentCode(Practice $practice, bool $wrong): string
    {
        $code = trim((string) ($practice->reference_solution ?: $practice->starter_code ?: '# Mi solución'))."\n";

        if (! $wrong) {
            return $code;
        }

        // Errores típicos: una variable mal escrita, o un print de más que cambia la salida.
        if ($this->runner && $this->language === 'python') {
            return $practice->expected_output && mt_rand(0, 1)
                ? $code."print('listo')\n"
                : "resultado = valor_que_no_existe\n".$code;
        }

        // En Java: una variable sin declarar (no compila) o una línea de más al empezar el main.
        if ($this->runner && $this->language === 'java') {
            return $practice->expected_output && mt_rand(0, 1)
                ? preg_replace('/(static void main\(String\[\] \w+\)[^{]*\{)/', "$1\n        System.out.println(\"listo\");", $code, 1)
                : $code."\nclass Rota { int funcion() { return valorQueNoExiste; } }\n";
        }

        // En PHP: una función que no existe (error fatal) o un echo de más al final.
        if ($this->runner && $this->language === 'php') {
            return $practice->expected_output && mt_rand(0, 1)
                ? $code."echo \"listo\\n\";\n"
                : $code."funcion_que_no_existe();\n";
        }

        // En C/C++: una variable sin declarar (no compila) o una línea de más antes del último return.
        if ($this->runner) {
            $at = strrpos($code, 'return 0;');
            $extra = $this->language === 'c' ? 'printf("listo\\n");' : 'std::cout << "listo\\n";';

            return $practice->expected_output && $at !== false && mt_rand(0, 1)
                ? substr($code, 0, $at).$extra."\n    ".substr($code, $at)
                : $code."\nint funcion_rota(void) { return valor_que_no_existe; }\n";
        }

        return implode("\n", array_slice(explode("\n", trim($code)), 0, -1))."\n";
    }

    private function studentFile(Practice $practice, bool $wrong): UploadedFile
    {
        $extension = Str::of($practice->allowed_extensions ?: 'py')->explode(',')->map(fn ($e) => trim($e))->filter()->first();
        $body = $wrong ? "# No me salió, lo sigo intentando\n" : trim((string) ($practice->reference_solution ?: $practice->starter_code ?: "# Entrega de «{$practice->title}»\nprint('hecho')"))."\n";
        $path = $this->workDir.'/'.Str::uuid().'.'.$extension;

        match ($extension) {
            'zip' => (function () use ($path, $body) {
                $zip = new ZipArchive;
                $zip->open($path, ZipArchive::CREATE);
                $zip->addFromString('main.py', $body);
                $zip->close();
            })(),
            'pdf' => file_put_contents($path, "%PDF-1.4\n% {$body}\n%%EOF\n"),
            'png', 'jpg', 'jpeg' => copy($this->receipt()->getRealPath(), $path),
            default => file_put_contents($path, $body),
        };

        return new UploadedFile($path, Str::slug($practice->title).'.'.$extension, null, null, true);
    }

    // ---------------------------------------------------------------- el docente

    private function review(Submission $submission): void
    {
        [$ok, $comment] = $this->judge($submission);
        $reviewer = app(SubmissionReviewer::class);

        if ($ok) {
            $reviewer->approve($submission, $this->teacher, mt_rand(1, 4) === 1 ? collect(['¡Muy bien!', 'Prolijo, así se hace.', 'Perfecto. Seguí así.'])->random() : null);

            return;
        }

        $reviewer->redo($submission, $this->teacher, $comment);
        $this->students[$submission->user->username]['redos']++;
    }

    /** @return array{0: bool, 1: string} ¿aprueba? y el comentario si no */
    private function judge(Submission $submission): array
    {
        $practice = $submission->practice;

        if ($submission->file_path) {
            $content = (string) Storage::disk('local')->get($submission->file_path);
            if (str_ends_with($submission->file_path, '.zip')) {
                $zip = new ZipArchive;
                $content = $zip->open(Storage::disk('local')->path($submission->file_path)) === true ? (string) $zip->getFromName('main.py') : '';
            }
            if (str_contains($content, 'No me salió')) {
                return [false, 'El archivo está incompleto: todavía no tiene el programa. Mandalo cuando lo tengas andando y, si te trabás, preguntame acá.'];
            }
        }

        if ($submission->code === null) {
            return [true, ''];
        }

        if (! $this->runner || ! $this->local->canRun($submission->code)) {
            $reference = trim((string) $practice->reference_solution);

            return $reference === '' || trim($submission->code) === $reference
                ? [true, '']
                : [false, 'Le falta una parte: compará con lo que pide la consigna, paso por paso.'];
        }

        [$output, $error] = $this->local->run($submission->code, $practice->sample_input);
        if ($error !== null) {
            return [false, match ($this->language) {
                'python' => "Tu programa termina con un error:\n\n    {$error}\n\nLeé la última línea del traceback: te dice qué nombre no existe.",
                'php' => "Tu programa termina con un error:\n\n    {$error}\n\nLeé el mensaje de PHP: dice qué pasó y en qué línea.",
                default => "Tu programa no compila o termina con error:\n\n    {$error}\n\nLeé el primer error del compilador: dice el archivo, la línea y qué falta.",
            }];
        }
        if ($practice->expected_output && ! LocalCodeRunner::matches($output, $practice->expected_output)) {
            $got = collect(explode("\n", trim($output)));
            $want = collect(explode("\n", trim($practice->expected_output)));
            $line = $got->keys()->merge($want->keys())->unique()->first(fn ($i) => ($got[$i] ?? null) !== ($want[$i] ?? null));

            return [false, 'La salida no coincide con la esperada. En la línea '.($line + 1).' esperaba «'.($want[$line] ?? '(nada)').'» y tu programa mostró «'.($got[$line] ?? '(nada)').'».'];
        }

        // Pruebas extra (D73): el docente las corre todas antes de aprobar.
        $tests = $practice->tests;
        if ($tests->isNotEmpty()) {
            foreach ($this->local->runMany($submission->code, $tests->pluck('input')->all()) as $i => [$output, $error]) {
                if ($error !== null || ! LocalCodeRunner::matches($output, $tests[$i]->expected_output)) {
                    return [false, "Con el ejemplo anda, pero no pasa la prueba «{$tests[$i]->name}». Probá tu programa con otros datos: el caso vacío, el borde, el dato inválido."];
                }
            }
        }

        return [true, ''];
    }

    // ---------------------------------------------------------------- final

    /** Los que terminaron siguen con abono vigente, para poder mirar su árbol. */
    private function keepSubscriptionsActive(): void
    {
        foreach ($this->students as $state) {
            $user = $state['user'];
            if ($user && ! app(TreeAccess::class)->hasActiveSubscription($user, $this->course)) {
                $this->attempt('renovación final', function () use ($user) {
                    $request = app(EnrollmentRequester::class)->pending($user, $this->course)
                        ?? app(EnrollmentRequester::class)->request($user, $this->course, RequestType::Receipt, $this->receipt(), 'Renuevo para seguir mirando.');
                    app(EnrollmentApprover::class)->approve($request, $this->teacher);
                });
            }
        }
    }

    private function report(?int $days): void
    {
        $access = app(TreeAccess::class);
        $ledger = app(Ledger::class);
        $nodes = $this->course->nodes()->where('is_published', true)->count();
        $practices = Practice::whereHas('node', fn ($q) => $q->where('course_id', $this->course->id)->where('is_published', true))->count();
        $coin = Currency::forCourse($this->course);

        $this->newLine();
        $this->info($days === null ? 'Simulación guardada en la base:' : "Resultado después de {$days} días simulados:");
        $this->table(
            ['Alumno', 'Clave', 'Nodos', 'Prácticas', 'Entregas', 'Rehacer', 'Renov.', 'XP del curso', 'Monedas', 'Comodines', 'Terminó', 'Días'],
            collect($this->students)->filter(fn ($state) => $state['user'] !== null)->map(function ($state) use ($ledger, $nodes, $practices, $coin) {
                $user = $state['user']->fresh();
                $delCurso = fn ($q) => $q->where('course_id', $this->course->id);
                $approved = Submission::where('user_id', $user->id)->where('status', SubmissionStatus::Approved)
                    ->whereHas('practice.node', $delCurso)->distinct('practice_id')->count('practice_id');
                $completion = CourseCompletion::where('user_id', $user->id)->where('course_id', $this->course->id)->first();

                return [
                    $user->username, $state['persona']['password'],
                    NodeUnlock::where('user_id', $user->id)->whereHas('node', $delCurso)->count()."/{$nodes}",
                    "{$approved}/{$practices}",
                    $state['attempts'], $state['redos'], $state['renewals'],
                    (int) XpTransaction::where('user_id', $user->id)->where('course_id', $this->course->id)->sum('amount'),
                    $ledger->balance($user, $coin),
                    $ledger->balance($user, Currency::wildcard()),
                    $completion ? 'sí' : ($state['stuck'] ? 'trabado: '.$state['stuck'] : 'no'),
                    $completion?->days_taken ?? '—',
                ];
            })->values()->all(),
        );

        $this->newLine();
        $this->info('Controles del sistema:');
        foreach ($this->checks() as [$ok, $text]) {
            $this->line(($ok ? '  <fg=green>✓</> ' : '  <fg=red>✗</> ').$text);
        }

        if ($this->failures !== []) {
            $this->newLine();
            $this->error(count($this->failures).' error(es) inesperado(s):');
            foreach (array_slice($this->failures, 0, 20) as $failure) {
                $this->line('  - '.$failure);
            }
        }

        $best = collect($this->students)->first();
        $this->newLine();
        $this->info('Para mirar el recorrido completo: usuario «'.$best['persona']['username'].'», clave «'.$best['persona']['password'].'».');
    }

    /** @return list<array{0: bool, 1: string}> */
    private function checks(): array
    {
        $ids = $this->simulatedIds();
        $ledger = app(Ledger::class);
        $access = app(TreeAccess::class);
        $users = User::whereIn('id', $ids)->get();

        $negative = $users->filter(fn (User $user) => $ledger->balances($user)->contains(fn ($total) => $total < 0));

        $paidTwice = CoinTransaction::whereIn('coin_transactions.user_id', $ids)->where('reason', 'practice_approved')
            ->join('submissions', fn ($join) => $join->on('submissions.id', '=', 'coin_transactions.source_id')->where('coin_transactions.source_type', Submission::class))
            ->groupBy('coin_transactions.user_id', 'submissions.practice_id')->havingRaw('COUNT(*) > 1')
            ->selectRaw('coin_transactions.user_id, submissions.practice_id')->get()->count();
        $xpTwice = XpTransaction::whereIn('xp_transactions.user_id', $ids)->where('reason', 'practice_approved')
            ->join('submissions', fn ($join) => $join->on('submissions.id', '=', 'xp_transactions.source_id')->where('xp_transactions.source_type', Submission::class))
            ->groupBy('xp_transactions.user_id', 'submissions.practice_id')->havingRaw('COUNT(*) > 1')
            ->selectRaw('xp_transactions.user_id, submissions.practice_id')->get()->count();

        $xpMismatch = $users->filter(fn (User $user) => (int) XpTransaction::where('user_id', $user->id)->sum('amount') !== (int) $user->xp_total);

        $unpaidUnlocks = NodeUnlock::whereIn('user_id', $ids)->with('node')->get()
            ->filter(fn (NodeUnlock $unlock) => $unlock->node->price > 0 && ! CoinTransaction::where('source_type', NodeUnlock::class)->where('source_id', $unlock->id)->exists());

        $orphanUnlocks = NodeUnlock::whereIn('user_id', $ids)->with('node.parent')->get()
            ->filter(fn (NodeUnlock $unlock) => $unlock->node->parent && ! $access->isCompleted($unlock->user, $unlock->node->parent));

        $approvedLocked = Submission::whereIn('user_id', $ids)->where('status', SubmissionStatus::Approved)->with('practice.node', 'user')->get()
            ->filter(fn (Submission $submission) => ! $access->isUnlocked($submission->user, $submission->practice->node));

        $bosses = $this->course->nodes()->where('type', 'boss')->whereNotNull('badge_id')->get();
        $missingBadges = $users->sum(fn (User $user) => $bosses->filter(fn (Node $boss) => $access->isCompleted($user, $boss) && ! $user->badges()->whereKey($boss->badge_id)->exists())->count());

        $completedWithout = $users->filter(fn (User $user) => $access->isCourseCompleted($user, $this->course)
            && ! CourseCompletion::where('user_id', $user->id)->where('course_id', $this->course->id)->exists());

        return [
            [$negative->isEmpty(), 'Ningún saldo quedó negativo'],
            [$paidTwice === 0 && $xpTwice === 0, 'Ninguna práctica se pagó dos veces (monedas ni XP), aunque se haya rehecho'],
            [$xpMismatch->isEmpty(), 'La XP de cada alumno es la suma de su libro de movimientos'],
            [$unpaidUnlocks->isEmpty(), 'Cada nodo abierto se pagó'],
            [$orphanUnlocks->isEmpty(), 'Nadie tiene abierto un nodo sin haber completado el anterior'],
            [$approvedLocked->isEmpty(), 'No hay prácticas aprobadas en nodos cerrados'],
            [$missingBadges === 0, 'Cada jefe vencido dio su insignia'],
            [$completedWithout->isEmpty(), 'Quien completó el tronco tiene el curso terminado (para el CV)'],
            [$this->failures === [], 'Sin errores inesperados del sistema'],
        ];
    }

    // ---------------------------------------------------------------- utilidades

    private function attempt(string $what, callable $run): mixed
    {
        try {
            return DB::transaction(fn () => $run());
        } catch (DomainException $e) {
            // El sistema dijo que no a algo que el simulador creía posible: se anota.
            $this->failures[] = now()->format('d/m H:i')." {$what}: el sistema lo frenó («{$e->getMessage()}»)";
        } catch (Throwable $e) {
            $this->failures[] = now()->format('d/m H:i')." {$what}: ".class_basename($e).': '.$e->getMessage().' ('.str_replace(base_path().'/', '', $e->getFile()).':'.$e->getLine().')';
        }

        return null;
    }

    private function travel(?CarbonImmutable $moment): void
    {
        Carbon::setTestNow($moment);
        CarbonImmutable::setTestNow($moment);
    }

    private function receipt(): UploadedFile
    {
        $path = $this->workDir.'/'.Str::uuid().'.png';
        $image = imagecreatetruecolor(40, 20);
        imagefill($image, 0, 0, imagecolorallocate($image, 34, 211, 238));
        imagepng($image, $path);

        return new UploadedFile($path, 'comprobante.png', 'image/png', null, true);
    }

    /** @return list<int> */
    private function simulatedIds(): array
    {
        return User::where('email', 'like', '%@'.self::DOMAIN)->pluck('id')->all();
    }

    private function reset(): void
    {
        $users = User::where('email', 'like', '%@'.self::DOMAIN)->get();
        foreach ($users as $user) {
            DB::table('notifications')->where('notifiable_type', User::class)->where('notifiable_id', $user->id)->delete();
            $user->delete();
        }
        $this->line("Borrados {$users->count()} alumnos de la simulación anterior.");
    }
}
