<?php

namespace App\Livewire\Student;

use App\Livewire\Student\Concerns\RendersToolPage;
use App\Livewire\Student\Concerns\SavesPractices;
use App\Support\PracticeTools;
use Livewire\Attributes\Locked;
use Livewire\Component;

/**
 * Herramientas → Practicar (D120): un editor suelto de cada lenguaje, para probar lo que se quiera sin instalar nada.
 * No cuenta para el curso. Lo escrito queda en el navegador y, si se guarda (D124), en Mis prácticas: con
 * ?practica=id se abre una guardada, se sigue y se le puede consultar al profe desde ahí.
 */
class PracticeTool extends Component
{
    use RendersToolPage, SavesPractices;

    #[Locked]
    public string $language;

    public function mount(string $language): void
    {
        abort_unless(isset(PracticeTools::TOOLS[$language]), 404);
        abort_unless(PracticeTools::allows(auth()->user(), $language), 403);
        $this->language = $language;
        $this->openSaved();
    }

    protected function savableLanguages(): array
    {
        return [$this->language];
    }

    protected function savedLabel(string $language): string
    {
        return 'de '.PracticeTools::TOOLS[$language]['label'];
    }

    public function render()
    {
        $tool = PracticeTools::TOOLS[$this->language];
        $saved = $this->savedOrNull();

        return $this->toolView('livewire.student.practice-tool', [
            'tool' => $tool,
            'saved' => $saved,
            'canConsult' => $this->canConsult($saved),
        ])->title($saved ? $saved->title : 'Practicar '.$tool['label']);
    }
}
