<?php

namespace App\Livewire\Student;

use App\Livewire\Student\Concerns\RendersToolPage;
use Livewire\Attributes\Title;
use Livewire\Component;

/** Herramientas → Calculadora (D120): simple o para programar. La cuenta se hace en el navegador; es para todos. */
#[Title('Calculadora')]
class CalculatorTool extends Component
{
    use RendersToolPage;

    public function render()
    {
        return $this->toolView('livewire.student.calculator-tool');
    }
}
