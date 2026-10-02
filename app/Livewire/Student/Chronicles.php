<?php

namespace App\Livewire\Student;

use App\Support\Chronicles as Book;
use App\Support\Glossary;
use App\Support\Story;
use Illuminate\Support\Facades\Storage;
use Livewire\Attributes\Title;
use Livewire\Attributes\Url;
use Livewire\Component;

/**
 * Mis Crónicas (D80): el prólogo y el libro de cada curso que empezó, que se abre página por página al
 * completar nodos. Al entrar, las páginas nuevas pasan a vistas y el menú deja de latir.
 */
#[Title('Mis Crónicas')]
class Chronicles extends Component
{
    /** 'prologo' o el slug de un curso. */
    #[Url(as: 'libro', except: 'prologo')]
    public string $book = 'prologo';

    public function mount(): void
    {
        abort_unless(auth()->user()->isStudent(), 403);
        $user = auth()->user();
        $user->forceFill(['chronicles_seen' => (new Book($user))->unlockedCount()])->save();
    }

    public function render(Glossary $glossary)
    {
        $user = auth()->user();
        $chronicles = new Book($user);
        $courses = $chronicles->courses();
        $course = $courses->firstWhere('slug', $this->book);
        $portrait = function (string $key) use ($glossary, $course): ?string {
            $path = $glossary->resolve($key, $course)['icon_path'];

            return $path ? Storage::disk('public')->url($path) : null;
        };

        $chapters = $course ? $chronicles->book($course) : [];
        $pages = collect($chapters)->flatMap(fn ($chapter) => $chapter['pages']);

        return view('livewire.student.chronicles', [
            'courses' => $courses,
            'course' => $course,
            'prologue' => Story::get('story.prologue', null, $user),
            'chapters' => $chapters,
            'unlocked' => $pages->where('unlocked', true)->count(),
            'total' => $pages->count(),
            'scene' => $glossary->scene($course),
            'portrait' => $portrait,
            'hint' => fn () => Book::hint($course, $user),
        ]);
    }
}
