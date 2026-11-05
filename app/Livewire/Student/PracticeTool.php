<?php

namespace App\Livewire\Student;

use App\Livewire\Student\Concerns\RendersToolPage;
use App\Support\PracticeTools;
use Livewire\Component;

/**
 * Herramientas → Practicar (D120): un editor suelto de cada lenguaje, para probar lo que se quiera sin instalar nada.
 * No cuenta para el curso y no guarda nada en el servidor; lo escrito queda en el navegador de quien lo usa.
 */
class PracticeTool extends Component
{
    use RendersToolPage;

    public string $language;

    public function mount(string $language): void
    {
        abort_unless(isset(PracticeTools::TOOLS[$language]), 404);
        abort_unless(PracticeTools::allows(auth()->user(), $language), 403);
        $this->language = $language;
    }

    public function render()
    {
        $tool = PracticeTools::TOOLS[$this->language];

        return $this->toolView('livewire.student.practice-tool', ['tool' => $tool])
            ->title('Practicar '.$tool['label']);
    }
}
