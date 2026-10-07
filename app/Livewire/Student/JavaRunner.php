<?php

namespace App\Livewire\Student;

use Livewire\Attributes\Title;
use Livewire\Component;

/**
 * Herramientas → Ejecutor de Java (D85): cómo instalar Java y el ejecutor en la compu del alumno para que
 * «Ejecutar» funcione en los cursos de Java, con un botón para probar la conexión. El código corre en su compu.
 */
#[Title('Ejecutor de Java')]
class JavaRunner extends Component
{
    public function render()
    {
        return view('livewire.student.java-runner', [
            'runnerUrl' => config('services.java_runner.url'),
        ]);
    }
}
