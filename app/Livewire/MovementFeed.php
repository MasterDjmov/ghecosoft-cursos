<?php

namespace App\Livewire;

use App\Models\User;
use App\Support\MovementFeed as Feed;
use Livewire\Attributes\On;
use Livewire\Attributes\Url;
use Livewire\Component;

/**
 * Movimientos de un alumno, separados por curso: lo ve el alumno en Mi cuenta y
 * el docente en la ficha del alumno (con quién hizo cada ajuste).
 */
class MovementFeed extends Component
{
    private const PAGE = 25;

    public User $user;

    public bool $showAuthor = false;

    /** Slug del curso elegido; vacío = todos. */
    #[Url(as: 'curso', except: '')]
    public string $course = '';

    public int $limit = self::PAGE;

    public function selectCourse(string $slug = ''): void
    {
        $this->course = $slug;
        $this->limit = self::PAGE;
    }

    /** El docente hizo un ajuste en la ficha: se vuelve a dibujar. */
    #[On('ledger-updated')]
    public function refreshFeed(): void {}

    public function more(): void
    {
        $this->limit += self::PAGE;
    }

    public function render()
    {
        // Solo el propio alumno o el docente.
        abort_unless(auth()->id() === $this->user->id || auth()->user()?->isAdmin(), 403);

        $courses = Feed::courses($this->user);
        $selected = $courses->first(fn ($item) => $item['course']->slug === $this->course)['course'] ?? null;
        $feed = Feed::entries($this->user, $selected, $this->limit);

        return view('livewire.movement-feed', [
            'courses' => $courses,
            'selected' => $selected,
            'totals' => Feed::totals($this->user),
            'entries' => $feed['entries'],
            'hasMore' => $feed['has_more'],
        ]);
    }
}
