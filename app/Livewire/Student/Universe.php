<?php

namespace App\Livewire\Student;

use App\Models\UniverseVote;
use App\Support\UniverseGraph;
use Livewire\Attributes\Renderless;
use Livewire\Attributes\Title;
use Livewire\Component;

/**
 * El Universo para el alumno (D81): todos los cursos y sus temas en el mapa 3D, para mirar y girar. Ve sus
 * nodos abiertos con nombre y el resto como puntos sin nombre (nunca lo que no abrió). Puede votar
 * «Quiero aprender esto» a los temas que ningún curso enseña y a los cursos que vienen.
 */
#[Title('Universo')]
class Universe extends Component
{
    public function mount(): void
    {
        abort_unless(auth()->user()->isStudent(), 403);
    }

    /**
     * Un voto por alumno y por tema o curso; si ya lo había votado, lo saca.
     *
     * @return array{voted: bool, count: int}
     */
    #[Renderless]
    public function toggleVote(string $target): array
    {
        abort_unless(auth()->user()->isStudent() && UniverseGraph::canVoteFor($target), 403);

        $vote = UniverseVote::where('user_id', auth()->id())->where('target', $target)->first();
        $vote ? $vote->delete() : UniverseVote::create(['user_id' => auth()->id(), 'target' => $target]);

        return ['voted' => ! $vote, 'count' => UniverseVote::where('target', $target)->count()];
    }

    public function render()
    {
        return view('livewire.student.universe', ['graph' => UniverseGraph::build(auth()->user())]);
    }
}
