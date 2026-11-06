<?php

namespace App\Livewire\Student;

use App\Livewire\Student\Concerns\RendersToolPage;
use Livewire\Attributes\Title;
use Livewire\Component;

/** Herramientas → Tabla ASCII (D120): clic para copiar, con la parte extendida de Windows, Unicode y DOS. Es para todos. */
#[Title('Tabla ASCII')]
class AsciiTool extends Component
{
    use RendersToolPage;

    public function render()
    {
        return $this->toolView('livewire.student.ascii-tool');
    }
}
