<?php

namespace App\Livewire\Student;

use App\Livewire\Student\Concerns\RendersToolPage;
use App\Models\PracticeMessage;
use App\Models\SavedPractice;
use App\Support\PracticeTools;
use Flux\Flux;
use Illuminate\Support\Facades\Gate;
use Livewire\Attributes\Locked;
use Livewire\Attributes\Url;
use Livewire\Component;

/**
 * Herramientas → Practicar (D120): un editor suelto de cada lenguaje, para probar lo que se quiera sin instalar nada.
 * No cuenta para el curso. Lo escrito queda en el navegador y, si se guarda (D124), en Mis prácticas: con
 * ?practica=id se abre una guardada, se sigue y se le puede consultar al profe desde ahí.
 */
class PracticeTool extends Component
{
    use RendersToolPage;

    #[Locked]
    public string $language;

    #[Url(as: 'practica', except: null)]
    public ?int $practiceId = null;

    /** El nombre de la práctica abierta (se cambia ahí mismo). */
    public string $title = '';

    public function mount(string $language): void
    {
        abort_unless(isset(PracticeTools::TOOLS[$language]), 404);
        abort_unless(PracticeTools::allows(auth()->user(), $language), 403);
        $this->language = $language;
        if ($this->practiceId !== null) {
            $saved = $this->saved();
            // Si la guardada es de otro lenguaje, se abre en la herramienta que corresponde.
            if ($saved->language !== $language) {
                $this->redirect($saved->url(), navigate: true);

                return;
            }
            $this->title = $saved->title;
        }
    }

    private function saved(): SavedPractice
    {
        $saved = SavedPractice::findOrFail($this->practiceId);
        Gate::authorize('view', $saved);

        return $saved;
    }

    /** Lo que se puede guardar; si no, avisa por qué. */
    private function storable(string $code, ?string $stdin): bool
    {
        $problem = match (true) {
            trim($code) === '' => 'No hay nada escrito para guardar.',
            mb_strlen($code) > SavedPractice::MAX_CODE => 'El código es muy largo para guardarlo (hasta '.number_format(SavedPractice::MAX_CODE, 0, ',', '.').' caracteres).',
            mb_strlen((string) $stdin) > 10000 => 'La entrada es muy larga para guardarla.',
            default => null,
        };
        if ($problem) {
            Flux::toast(variant: 'danger', text: $problem);
        }

        return $problem === null;
    }

    /** Guardar lo que hay en el editor: en la práctica abierta o, si no hay ninguna, en una nueva. */
    public function save(string $code, ?string $stdin = null): void
    {
        if ($this->practiceId === null) {
            $this->saveNew($code, $stdin);

            return;
        }
        if (! $this->storable($code, $stdin)) {
            return;
        }
        $saved = $this->saved();
        Gate::authorize('update', $saved);
        $saved->update(['code' => $code, 'stdin' => $stdin]);
        Flux::toast(variant: 'success', text: 'Guardada en Mis prácticas.');
    }

    /** Guardar como una práctica nueva, con un nombre que después se puede cambiar. */
    public function saveNew(string $code, ?string $stdin = null): void
    {
        if (! $this->storable($code, $stdin)) {
            return;
        }
        $user = auth()->user();
        if (SavedPractice::where('user_id', $user->id)->count() >= SavedPractice::LIMIT) {
            Flux::toast(variant: 'danger', text: 'Ya tenés '.SavedPractice::LIMIT.' prácticas guardadas: borrá alguna en Mis prácticas para guardar otra.');

            return;
        }
        $label = PracticeTools::TOOLS[$this->language]['label'];
        $title = $this->practiceId !== null ? $this->title.' (copia)' : 'Práctica de '.$label.' del '.now()->format('d/m H:i');
        $saved = SavedPractice::create(['user_id' => $user->id, 'language' => $this->language, 'title' => mb_substr($title, 0, 120), 'code' => $code, 'stdin' => $stdin]);

        Flux::toast(variant: 'success', text: 'Guardada en Mis prácticas. Ponele un nombre arriba.');
        $this->redirect($saved->url().($this->inWindow ? '&ventana=1' : ''), navigate: true);
    }

    public function updatedTitle(): void
    {
        $this->validate(['title' => ['required', 'string', 'max:120']], [], ['title' => 'nombre']);
        $saved = $this->saved();
        Gate::authorize('update', $saved);
        $saved->update(['title' => trim($this->title)]);
        Flux::toast(variant: 'success', text: 'Nombre guardado.');
    }

    public function render()
    {
        $tool = PracticeTools::TOOLS[$this->language];
        $saved = $this->practiceId !== null ? $this->saved() : null;

        return $this->toolView('livewire.student.practice-tool', [
            'tool' => $tool,
            'saved' => $saved,
            'canConsult' => $saved && ! auth()->user()->isStaff() && Gate::allows('viewThread', [PracticeMessage::class, $saved, auth()->user()]),
        ])->title($saved ? $saved->title : 'Practicar '.$tool['label']);
    }
}
