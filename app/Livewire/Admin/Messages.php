<?php

namespace App\Livewire\Admin;

use App\Models\Practice;
use App\Models\PracticeMessage;
use App\Models\User;
use App\Services\PracticeMessenger;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Support\Collection;
use Livewire\Attributes\On;
use Livewire\Attributes\Title;
use Livewire\Attributes\Url;
use Livewire\Component;

/** Admin → Mensajes (D63): las consultas de los alumnos por práctica, sin leer primero; leer y responder. */
#[Title('Mensajes')]
class Messages extends Component
{
    /** Hilo abierto: «idPráctica-idAlumno». */
    #[Url(as: 'hilo')]
    public string $thread = '';

    #[Url(as: 'alumno')]
    public string $student = '';

    /** Lo que el docente todavía no leyó: mensajes de alumnos sin read_at. */
    public static function unreadQuery(): Builder
    {
        return PracticeMessage::whereNull('read_at')->whereColumn('author_id', 'student_id');
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
        $rows = PracticeMessage::query()
            ->selectRaw('practice_id, student_id, max(id) as last_id, max(created_at) as last_at')
            ->selectRaw('sum(case when read_at is null and author_id = student_id then 1 else 0 end) as unread')
            ->when($this->student !== '', fn ($q) => $q->where('student_id', (int) $this->student))
            ->groupBy('practice_id', 'student_id')
            ->orderByRaw('sum(case when read_at is null and author_id = student_id then 1 else 0 end) > 0 desc')
            ->orderByDesc('last_at')
            ->limit(100)
            ->get();

        $last = PracticeMessage::whereIn('id', $rows->pluck('last_id'))->get()->keyBy('id');
        $practices = Practice::with('node.course')->whereIn('id', $rows->pluck('practice_id'))->get()->keyBy('id');
        $students = User::whereIn('id', $rows->pluck('student_id'))->get()->keyBy('id');

        return $rows->map(fn ($row) => (object) [
            'key' => $row->practice_id.'-'.$row->student_id,
            'practice' => $practices[$row->practice_id] ?? null,
            'student' => $students[$row->student_id] ?? null,
            'last' => $last[$row->last_id] ?? null,
            'unread' => (int) $row->unread,
        ])->filter(fn ($t) => $t->practice && $t->student && $t->last)->values();
    }

    public function render()
    {
        [$practiceId, $studentId] = array_pad(array_map('intval', explode('-', $this->thread)), 2, 0);
        $practice = $practiceId ? Practice::with('node.course')->find($practiceId) : null;
        $selectedStudent = $studentId ? User::find($studentId) : null;
        if ($practice && $selectedStudent) {
            // Abrir la conversación la marca leída antes de dibujar la lista.
            app(PracticeMessenger::class)->markRead(auth()->user(), $practice, $selectedStudent);
        }

        return view('livewire.admin.messages', [
            'threads' => $this->threads(),
            'practice' => $practice && $selectedStudent ? $practice : null,
            'selectedStudent' => $practice && $selectedStudent ? $selectedStudent : null,
            'filteredStudent' => $this->student !== '' ? User::find((int) $this->student) : null,
        ]);
    }
}
