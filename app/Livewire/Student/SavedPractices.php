<?php

namespace App\Livewire\Student;

use App\Models\SavedPractice;
use App\Support\PracticeTools;
use Flux\Flux;
use Illuminate\Support\Facades\Gate;
use Livewire\Attributes\Title;
use Livewire\Attributes\Url;
use Livewire\Component;
use Symfony\Component\HttpFoundation\StreamedResponse;

/**
 * D124: Mis prácticas. Lo guardado desde Herramientas → Practicar, de cada uno: abrir para seguir, bajar el archivo,
 * borrar. Si el profe respondió una consulta, se marca.
 */
#[Title('Mis prácticas')]
class SavedPractices extends Component
{
    #[Url(as: 'lenguaje', except: '')]
    public string $language = '';

    #[Url(as: 'buscar', except: '')]
    public string $search = '';

    private function mine(int $id): SavedPractice
    {
        $practice = SavedPractice::findOrFail($id);
        Gate::authorize('view', $practice);

        return $practice;
    }

    public function download(int $id): StreamedResponse
    {
        $practice = $this->mine($id);

        return response()->streamDownload(fn () => print ($practice->code), $practice->fileName(), ['Content-Type' => 'text/plain; charset=utf-8']);
    }

    public function delete(int $id): void
    {
        $practice = $this->mine($id);
        Gate::authorize('delete', $practice);
        $practice->delete();
        Flux::toast(text: '«'.$practice->title.'» se borró.');
    }

    public function render()
    {
        $user = auth()->user();
        $all = SavedPractice::where('user_id', $user->id);
        $practices = (clone $all)
            ->when($this->language !== '', fn ($q) => $q->where('language', $this->language))
            ->when(trim($this->search) !== '', fn ($q) => $q->where('title', 'like', '%'.trim($this->search).'%'))
            ->withCount([
                'messages',
                'messages as unread_count' => fn ($q) => $q->whereNull('read_at')->where('author_id', '!=', $user->id),
            ])
            ->latest('updated_at')->get(['id', 'user_id', 'language', 'title', 'updated_at']);

        return view('livewire.student.saved-practices', [
            'practices' => $practices,
            'total' => (clone $all)->count(),
            'languages' => (clone $all)->distinct()->pluck('language')->mapWithKeys(fn ($key) => [$key => PracticeTools::TOOLS[$key]['label'] ?? $key])->sort(),
            // Para arrancar una nueva: los lenguajes con los que puede practicar.
            'tools' => collect(PracticeTools::TOOLS)->filter(fn ($tool, $key) => PracticeTools::allows($user, $key))->map(fn ($tool, $key) => ['label' => $tool['label'], 'url' => route('student.practice-tool', $key)]),
            'limit' => SavedPractice::LIMIT,
            'canConsult' => ! $user->isStaff(),
        ]);
    }
}
