<?php

namespace App\Livewire\Admin;

use App\Enums\FragmentTrigger;
use App\Enums\NodeType;
use App\Models\Course;
use App\Models\Node;
use App\Models\NodeUnlock;
use App\Models\StoryFragment;
use App\Models\User;
use App\Rules\SafeUpload;
use App\Support\Chronicles;
use App\Support\Glossary;
use App\Support\Story as StoryText;
use Flux\Flux;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;
use Illuminate\Validation\Rule;
use Livewire\Attributes\Title;
use Livewire\Attributes\Url;
use Livewire\Component;
use Livewire\WithFileUploads;

/**
 * La sala de guion (Mis Crónicas, D80, etapa 2): el libro de cada curso con todo abierto, lo que falta
 * escribir marcado, y los fragmentos del docente (texto e imagen) colgados donde corresponde. «Ver como»
 * muestra el libro tal como lo ve un alumno. Solo el administrador (es contenido).
 */
#[Title('Historia')]
class Story extends Component
{
    use WithFileUploads;

    #[Url(as: 'curso', except: '')]
    public string $courseSlug = '';

    /** '' = todo abierto; si no, el id de un alumno: el libro como lo ve él. */
    #[Url(as: 'como', except: '')]
    public string $viewAs = '';

    // Modal del fragmento.
    public ?int $fragmentId = null;

    public string $trigger = '';

    public ?int $anchorNode = null;

    public ?int $anchorBranch = null;

    public string $title = '';

    public string $body = '';

    public $image = null;

    public bool $removeImage = false;

    public function newFragment(string $trigger, ?int $nodeId = null, ?int $branchId = null): void
    {
        $this->resetValidation();
        $this->reset('fragmentId', 'title', 'body', 'image', 'removeImage');
        $this->trigger = FragmentTrigger::from($trigger)->value;
        $this->anchorNode = $nodeId;
        $this->anchorBranch = $branchId;
        Flux::modal('fragment')->show();
    }

    public function editFragment(int $id): void
    {
        $fragment = $this->fragments()->findOrFail($id);
        $this->resetValidation();
        $this->reset('image', 'removeImage');
        $this->fragmentId = $fragment->id;
        $this->trigger = $fragment->trigger->value;
        $this->anchorNode = $fragment->node_id;
        $this->anchorBranch = $fragment->branch_id;
        $this->title = $fragment->title;
        $this->body = (string) $fragment->body;
        Flux::modal('fragment')->show();
    }

    public function saveFragment(): void
    {
        $course = $this->course();
        abort_unless($course, 404);
        $this->validate([
            'trigger' => ['required', Rule::enum(FragmentTrigger::class)],
            'title' => ['required', 'string', 'max:255'],
            'body' => ['nullable', 'string', 'max:20000'],
            'image' => ['nullable', 'image', 'mimes:'.implode(',', config('uploads.image.mimes')), 'max:'.config('uploads.image.max_kb'), new SafeUpload],
        ], [], ['title' => 'título', 'body' => 'texto', 'image' => 'imagen']);
        // El lugar tiene que ser de este curso.
        abort_if($this->anchorNode && ! $course->nodes()->whereKey($this->anchorNode)->exists(), 404);
        abort_if($this->anchorBranch && ! $course->branches()->whereKey($this->anchorBranch)->exists(), 404);

        $fragment = $this->fragmentId ? $this->fragments()->findOrFail($this->fragmentId) : new StoryFragment([
            'course_id' => $course->id,
            'position' => (int) $this->fragments()->max('position') + 1,
        ]);
        $fragment->fill([
            'trigger' => $this->trigger,
            'node_id' => $this->trigger === FragmentTrigger::NodeCompleted->value ? $this->anchorNode : null,
            'branch_id' => $this->trigger === FragmentTrigger::BranchCompleted->value ? $this->anchorBranch : null,
            'title' => $this->title,
            'body' => $this->body ?: null,
        ]);
        if (($this->image || $this->removeImage) && $fragment->image_path) {
            Storage::disk('public')->delete($fragment->image_path);
            $fragment->image_path = null;
        }
        if ($this->image) {
            $fragment->image_path = $this->image->storeAs('story', Str::uuid().'.'.$this->image->extension(), 'public');
        }
        $fragment->save();

        Flux::modal('fragment')->close();
        Flux::toast(variant: 'success', text: 'Fragmento guardado.');
    }

    public function deleteFragment(int $id): void
    {
        $fragment = $this->fragments()->findOrFail($id);
        if ($fragment->image_path) {
            Storage::disk('public')->delete($fragment->image_path);
        }
        $fragment->delete();
        Flux::toast(text: 'Fragmento borrado.');
    }

    /** Subirlo o bajarlo entre los fragmentos del mismo lugar. */
    public function moveFragment(int $id, int $direction): void
    {
        $fragment = $this->fragments()->findOrFail($id);
        $siblings = $this->fragments()->where('trigger', $fragment->trigger)->where('node_id', $fragment->node_id)->where('branch_id', $fragment->branch_id)
            ->orderBy('position')->orderBy('id')->get()->values();
        $index = $siblings->search(fn ($f) => $f->id === $fragment->id);
        $other = $siblings->get($index + ($direction < 0 ? -1 : 1));
        if ($other) {
            [$a, $b] = [$fragment->position, $other->position === $fragment->position ? $fragment->position + ($direction < 0 ? -1 : 1) : $other->position];
            $fragment->update(['position' => $b]);
            $other->update(['position' => $a]);
        }
    }

    private function course(): ?Course
    {
        return $this->courseSlug !== '' ? Course::where('slug', $this->courseSlug)->first() : null;
    }

    private function fragments()
    {
        return StoryFragment::where('course_id', $this->course()?->id);
    }

    public function render(Glossary $glossary)
    {
        $course = $this->course();
        $student = $this->viewAs !== '' ? User::where('role', 'student')->find((int) $this->viewAs) : null;
        $chronicles = new Chronicles($student ?? auth()->user(), revealAll: ! $student);
        $portrait = function (string $key) use ($glossary, $course): ?string {
            $path = $glossary->resolve($key, $course)['icon_path'];

            return $path ? Storage::disk('public')->url($path) : null;
        };
        // Para «Ver como»: los alumnos que empezaron este curso.
        $students = $course ? User::where('role', 'student')
            ->whereIn('id', NodeUnlock::whereHas('node', fn ($q) => $q->where('course_id', $course->id)->where('type', NodeType::Root))->select('user_id'))
            ->orderBy('name')->get() : collect();

        return view('livewire.admin.story', [
            'courses' => Course::orderBy('position')->orderBy('title')->get(),
            'course' => $course,
            'student' => $student,
            'students' => $students,
            'chapters' => $course ? $chronicles->book($course) : [],
            'prologue' => StoryText::get('story.prologue', null, auth()->user()),
            'scene' => $glossary->scene($course),
            'portrait' => $portrait,
            'hint' => fn () => Chronicles::hint($course, $student ?? auth()->user()),
            'triggers' => FragmentTrigger::cases(),
            'anchorTitle' => $this->anchorNode ? Node::find($this->anchorNode)?->title : null,
        ]);
    }
}
