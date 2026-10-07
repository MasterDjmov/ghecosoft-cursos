<?php

namespace App\Livewire\Admin;

use App\Support\CharacterSheets;
use Livewire\Attributes\Title;
use Livewire\Attributes\Url;
use Livewire\Component;

/**
 * Historia → Personajes (D84): las fichas de docs/historias/PERSONAJES.md, con el pedido listo para copiar
 * y generar las imágenes siempre iguales (Stitch). Solo lectura: se editan en el .md. Solo el administrador.
 */
#[Title('Personajes')]
class Characters extends Component
{
    #[Url(as: 'faltan', except: false)]
    public bool $onlyMissing = false;

    public function render()
    {
        $sheets = CharacterSheets::all();

        return view('livewire.admin.characters', [
            'groups' => $sheets->when($this->onlyMissing, fn ($all) => $all->where('missing', true))->groupBy('section'),
            'total' => $sheets->count(),
            'missing' => $sheets->where('missing', true)->count(),
        ]);
    }
}
