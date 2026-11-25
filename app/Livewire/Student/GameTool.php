<?php

namespace App\Livewire\Student;

use App\Livewire\Student\Concerns\RendersToolPage;
use App\Models\User;
use Livewire\Component;

/**
 * D126, fase 1 (prototipo): un juego en C con SDL3, editable y jugable en la página. Compila con el Clang de C en el
 * navegador y corre con el SDL3 de la plataforma (resources/js/runners/sdl.js); el mismo archivo compila con SDL3
 * real en la compu. Mientras es prueba, solo lo ve el staff.
 */
class GameTool extends Component
{
    use RendersToolPage;

    public static function allowed(User $user): bool
    {
        return $user->isStaff();
    }

    public function mount(): void
    {
        abort_unless(self::allowed(auth()->user()), 403);
    }

    public function render()
    {
        return $this->toolView('livewire.student.game-tool', [
            'starter' => file_get_contents(resource_path('games/pong.c')),
        ])->title('Juegos con SDL3');
    }
}
