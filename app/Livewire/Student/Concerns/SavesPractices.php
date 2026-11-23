<?php

namespace App\Livewire\Student\Concerns;

use App\Models\PracticeMessage;
use App\Models\SavedPractice;
use Flux\Flux;
use Illuminate\Support\Facades\Gate;
use Livewire\Attributes\Url;

/**
 * D124: guardar en Mis prácticas desde una herramienta (Practicar, el Gólem 8086, la caja de la Feria). Con
 * ?practica=id la herramienta abre esa práctica: «Guardar» la actualiza, «Copia» guarda otra y el nombre se cambia
 * arriba. Cada herramienta dice qué lenguajes guarda (`savableLanguages`) y cómo se llama (`savedLabel`).
 */
trait SavesPractices
{
    #[Url(as: 'practica', except: null)]
    public ?int $practiceId = null;

    /** El nombre de la práctica abierta (se cambia ahí mismo). */
    public string $title = '';

    /** @return list<string> */
    abstract protected function savableLanguages(): array;

    /** Para el nombre automático: «Práctica de Python…», «Práctica del Gólem…». */
    abstract protected function savedLabel(string $language): string;

    /** Llamarlo en mount(): abre la guardada (o manda a su herramienta si es de otra). */
    protected function openSaved(): bool
    {
        if ($this->practiceId === null) {
            return true;
        }
        $saved = $this->saved();
        if (! in_array($saved->language, $this->savableLanguages(), true)) {
            $this->redirect($saved->url(), navigate: true);

            return false;
        }
        $this->title = $saved->title;

        return true;
    }

    protected function saved(): SavedPractice
    {
        $saved = SavedPractice::findOrFail($this->practiceId);
        Gate::authorize('view', $saved);

        return $saved;
    }

    protected function savedOrNull(): ?SavedPractice
    {
        return $this->practiceId !== null ? $this->saved() : null;
    }

    /** Lo que se puede guardar; si no, avisa por qué. */
    private function storable(string $code, ?string $stdin, ?string $page): bool
    {
        $problem = match (true) {
            trim($code) === '' => 'No hay nada escrito para guardar.',
            mb_strlen($code) > SavedPractice::MAX_CODE => 'El código es muy largo para guardarlo (hasta '.number_format(SavedPractice::MAX_CODE, 0, ',', '.').' caracteres).',
            mb_strlen((string) $stdin) > 10000 => 'La entrada es muy larga para guardarla.',
            mb_strlen((string) $page) > 20000 => 'La página es muy larga para guardarla.',
            default => null,
        };
        if ($problem) {
            Flux::toast(variant: 'danger', text: $problem);
        }

        return $problem === null;
    }

    /** Guardar lo que hay en el editor: en la práctica abierta o, si no hay ninguna, en una nueva. */
    public function save(string $code, ?string $stdin = null, ?string $language = null, ?string $page = null): void
    {
        if ($this->practiceId === null) {
            $this->saveNew($code, $stdin, $language, $page);

            return;
        }
        if (! $this->storable($code, $stdin, $page)) {
            return;
        }
        $saved = $this->saved();
        Gate::authorize('update', $saved);
        $saved->update(['code' => $code, 'stdin' => $stdin]);
        Flux::toast(variant: 'success', text: 'Guardada en Mis prácticas.');
    }

    /** Guardar como una práctica nueva, con un nombre que después se puede cambiar. */
    public function saveNew(string $code, ?string $stdin = null, ?string $language = null, ?string $page = null): void
    {
        $current = $this->savedOrNull();
        $language = $current?->language ?? $language ?? $this->savableLanguages()[0];
        abort_unless(in_array($language, $this->savableLanguages(), true), 422);
        $page = $current ? $current->page : $page;
        if (! $this->storable($code, $stdin, $page)) {
            return;
        }
        $user = auth()->user();
        if (SavedPractice::where('user_id', $user->id)->count() >= SavedPractice::LIMIT) {
            Flux::toast(variant: 'danger', text: 'Ya tenés '.SavedPractice::LIMIT.' prácticas guardadas: borrá alguna en Mis prácticas para guardar otra.');

            return;
        }
        $title = $current ? $current->title.' (copia)' : 'Práctica '.$this->savedLabel($language).' del '.now()->format('d/m H:i');
        $saved = SavedPractice::create([
            'user_id' => $user->id, 'language' => $language, 'title' => mb_substr($title, 0, 120),
            'code' => $code, 'stdin' => $stdin, 'page' => filled($page) ? $page : null,
        ]);

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

    /** La consulta al profe se ofrece al alumno dueño (el staff no se consulta a sí mismo). */
    protected function canConsult(?SavedPractice $saved): bool
    {
        return $saved !== null && ! auth()->user()->isStaff() && Gate::allows('viewThread', [PracticeMessage::class, $saved, auth()->user()]);
    }
}
