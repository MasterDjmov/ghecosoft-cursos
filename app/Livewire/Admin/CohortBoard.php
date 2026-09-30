<?php

namespace App\Livewire\Admin;

use App\Models\Course;
use Livewire\Attributes\Title;
use Livewire\Component;

/**
 * Comisiones (D72): los cursos de la plataforma, cada uno con sus comisiones. El docente crea y maneja
 * las suyas (y sus alumnos son los que estén en ellas); el administrador ve todas y elige el docente.
 * Los cursos los habilita el administrador: acá no se editan.
 */
#[Title('Comisiones')]
class CohortBoard extends Component
{
    public function render()
    {
        return view('livewire.admin.cohort-board', [
            'courses' => Course::where('is_published', true)->orderBy('position')->orderBy('title')->get(),
        ]);
    }
}
