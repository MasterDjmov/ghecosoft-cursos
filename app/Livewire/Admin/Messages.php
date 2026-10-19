<?php

namespace App\Livewire\Admin;

use App\Models\NodeStep;
use App\Models\NodeStepCompletion;
use App\Models\Practice;
use App\Models\PracticeMessage;
use App\Models\Submission;
use App\Models\User;
use App\Services\PracticeMessenger;
use App\Services\TeacherScope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Support\Collection;
use Livewire\Attributes\On;
use Livewire\Attributes\Title;
use Livewire\Attributes\Url;
use Livewire\Component;

/**
 * Admin → Mensajes (D63): las consultas de los alumnos por práctica y por micro-misión (D110), sin leer primero.
 * Al abrir una, todo lo necesario para ayudar está en la misma pantalla del chat: la consigna, el código que el
 * alumno tenía en el editor y la solución, los dos con «Ejecutar».
 */
#[Title('Mensajes')]
class Messages extends Component
{
    /** Hilo abierto: «idPráctica-idAlumno» o «m idMicroMisión-idAlumno». */
    #[Url(as: 'hilo')]
    public string $thread = '';

    #[Url(as: 'alumno')]
    public string $student = '';

    /** Lo que el docente todavía no leyó: mensajes de alumnos sin read_at (del docente: de sus comisiones, D72). */
    public static function unreadQuery(?User $viewer = null): Builder
    {
        return app(TeacherScope::class)->messages(PracticeMessage::query(), $viewer ?? auth()->user())
            ->whereNull('read_at')->whereColumn('author_id', 'student_id');
    }

    /** Al responder, la lista se reordena en el momento. */
    #[On('practice-chat-sent')]
    public function refreshThreads(): void {}

    public function open(string $thread): void
    {
        $this->thread = $thread;
    }

    /** @return Collection<int, object> */
    private function threads(): Collection
    {
        $rows = app(TeacherScope::class)->messages(PracticeMessage::query(), auth()->user())
            ->selectRaw('practice_id, node_step_id, student_id, max(id) as last_id, max(created_at) as last_at')
            ->selectRaw('sum(case when read_at is null and author_id = student_id then 1 else 0 end) as unread')
            ->when($this->student !== '', fn ($q) => $q->where('student_id', (int) $this->student))
            ->groupBy('practice_id', 'node_step_id', 'student_id')
            ->orderByRaw('sum(case when read_at is null and author_id = student_id then 1 else 0 end) > 0 desc')
            ->orderByDesc('last_at')
            ->limit(100)
            ->get();

        $last = PracticeMessage::whereIn('id', $rows->pluck('last_id'))->get()->keyBy('id');
        $practices = Practice::with('node.course')->whereIn('id', $rows->pluck('practice_id')->filter())->get()->keyBy('id');
        $steps = NodeStep::with('node.course')->whereIn('id', $rows->pluck('node_step_id')->filter())->get()->keyBy('id');
        $students = User::whereIn('id', $rows->pluck('student_id'))->get()->keyBy('id');

        return $rows->map(function ($row) use ($practices, $steps, $students, $last) {
            $subject = $row->practice_id ? ($practices[$row->practice_id] ?? null) : ($steps[$row->node_step_id] ?? null);

            return (object) [
                'key' => $subject ? PracticeMessage::threadKey($subject, $row->student_id) : '',
                'subject' => $subject,
                'isStep' => $subject instanceof NodeStep,
                'student' => $students[$row->student_id] ?? null,
                'last' => $last[$row->last_id] ?? null,
                'unread' => (int) $row->unread,
            ];
        })->filter(fn ($t) => $t->subject && $t->student && $t->last)->values();
    }

    /**
     * Lo que se ve arriba del chat para ayudar sin salir de la pantalla.
     *
     * @return array{language: string, challenge: ?string, studentCode: ?string, studentCodeFrom: ?string, solution: ?string, stdin: string, expected: string, checks: ?string}
     */
    private function context(Practice|NodeStep $subject, User $student): array
    {
        $course = $subject->node->course;
        // El código del alumno: el que mandó con su último mensaje; si no, lo último que resolvió o entregó.
        $withCode = PracticeMessage::thread($subject, $student)->whereNotNull('code')->latest('id')->first();
        $code = $withCode?->code;
        $from = $withCode ? 'con su consulta del '.$withCode->created_at->format('d/m H:i') : null;
        if ($code === null && $subject instanceof NodeStep) {
            $done = NodeStepCompletion::where('user_id', $student->id)->where('node_step_id', $subject->id)->first();
            [$code, $from] = [$done?->code, $done ? 'cuando la superó' : null];
        }
        if ($code === null && $subject instanceof Practice) {
            $last = Submission::where('user_id', $student->id)->where('practice_id', $subject->id)->latest('submitted_at')->first();
            [$code, $from] = [$last?->code, $last ? 'en su última entrega' : null];
        }

        return [
            'language' => ($subject instanceof NodeStep ? $subject->runLanguage($course) : $course->language)->value,
            'challenge' => $subject instanceof NodeStep ? $subject->challenge : $subject->instructions,
            'studentCode' => $code,
            'studentCodeFrom' => $from,
            'solution' => $subject instanceof NodeStep ? $subject->solution : $subject->reference_solution,
            'stdin' => (string) $subject->sample_input,
            'expected' => (string) $subject->expected_output,
            'checks' => $subject instanceof NodeStep ? $subject->checks : null,
        ];
    }

    public function render()
    {
        [$subject, $selectedStudent] = PracticeMessage::fromThreadKey($this->thread);
        // Un docente solo abre hilos de alumnos de sus comisiones (D72).
        if ($subject && $selectedStudent && auth()->user()->cannot('viewThread', [PracticeMessage::class, $subject, $selectedStudent])) {
            [$subject, $selectedStudent] = [null, null];
        }
        if ($subject && $selectedStudent) {
            // Abrir la conversación la marca leída antes de dibujar la lista.
            app(PracticeMessenger::class)->markRead(auth()->user(), $subject, $selectedStudent);
        }
        $open = $subject && $selectedStudent;

        return view('livewire.admin.messages', [
            'threads' => $this->threads(),
            'subject' => $open ? $subject : null,
            'isStep' => $open && $subject instanceof NodeStep,
            'selectedStudent' => $open ? $selectedStudent : null,
            'context' => $open ? $this->context($subject, $selectedStudent) : null,
            'filteredStudent' => $this->student !== '' ? User::find((int) $this->student) : null,
        ]);
    }
}
