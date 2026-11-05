<?php

namespace App\Livewire\Student\Concerns;

use Illuminate\Contracts\View\View;

/** Las Herramientas (D120) se ven como página o, con ?ventana=1, sueltas adentro de la ventana flotante. */
trait RendersToolPage
{
    public bool $inWindow = false;

    public function mountRendersToolPage(): void
    {
        $this->inWindow = request()->boolean('ventana');
    }

    protected function toolView(string $view, array $data = []): View
    {
        $page = view($view, $data);

        return $this->inWindow ? $page->layout('layouts.tool-window') : $page;
    }
}
