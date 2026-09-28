<?php

namespace App\Livewire\Student;

use App\Livewire\Student\Concerns\WorksOnPractice;
use App\Models\Practice;
use App\Services\PracticeSubmitter;
use Livewire\Component;
use Livewire\Features\SupportFileUploads\TemporaryUploadedFile;
use Livewire\WithFileUploads;

/** Una hoja dentro del nodo: consigna, editor, entregar, historial y comentarios. */
class PracticeCard extends Component
{
    use WithFileUploads, WorksOnPractice;

    public Practice $practice;

    /** Número de la hoja dentro del nodo (para el nombre del archivo: practica_N.py). */
    public int $number = 1;

    /** @var TemporaryUploadedFile|null */
    public $file = null;

    public string $comment = '';

    public function mount(Practice $practice): void
    {
        // El componente vive dentro de NodeView, que ya autorizó el nodo; igual se revisa.
        $this->authorize('view', $practice->node);
    }

    public function render(PracticeSubmitter $submitter)
    {
        return view('livewire.student.practice-card', $this->practiceState($submitter));
    }
}
