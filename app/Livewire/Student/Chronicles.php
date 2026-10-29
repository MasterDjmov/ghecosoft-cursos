<?php

namespace App\Livewire\Student;

use App\Models\Course;
use App\Services\Heroes;
use App\Support\Chronicles as Book;
use App\Support\Glossary;
use App\Support\Story;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;
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
    /** 'prologo', 'portal' o el slug de un curso. */
    #[Url(as: 'libro', except: 'prologo')]
    public string $book = 'prologo';

    public function mount(): void
    {
        abort_unless(auth()->user()->isStudent(), 403);
        $user = auth()->user();
        $user->forceFill(['chronicles_seen' => (new Book($user))->unlockedCount()])->save();
    }

    /**
     * La narradora sin imagen en el Diccionario (story.narrator, D106) usa la del protagonista del curso, si
     * es el mismo personaje: su retrato de la enciclopedia (o su primer aspecto) y su cuerpo entero.
     */
    private function narratorImage(string $key, ?Course $course, string $kind): ?string
    {
        $hero = $course ? Heroes::protagonistOf($course) : null;
        if ($key !== 'story.narrator' || ! $hero || Str::lower(app(Glossary::class)->term($key, $course)) !== Str::lower($hero['name'])) {
            return null;
        }
        $file = $kind === 'figure' ? "img/enciclopedia/{$hero['slug']}-cuerpo.webp" : "img/enciclopedia/{$hero['slug']}.webp";
        if (is_file(public_path($file))) {
            return asset($file);
        }

        return $kind === 'portrait' && is_file(public_path("img/protagonistas/{$hero['slug']}/1.webp")) ? Heroes::lookUrl($hero, 1) : null;
    }

    public function render(Glossary $glossary)
    {
        $user = auth()->user();
        $chronicles = new Book($user);
        $courses = $chronicles->courses();
        $course = $courses->firstWhere('slug', $this->book);
        $figure = function (string $key) use ($glossary, $course): ?string {
            $path = $glossary->resolve($key, $course)['figure_path'];

            return $path ? Storage::disk('public')->url($path) : $this->narratorImage($key, $course, 'figure');
        };
        $portrait = function (string $key) use ($glossary, $course): ?string {
            $path = $glossary->resolve($key, $course)['icon_path'];

            return $path ? Storage::disk('public')->url($path) : $this->narratorImage($key, $course, 'portrait');
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
            'portal' => $this->book === 'portal' ? $chronicles->portal() : [],
            'glossary' => $glossary,
            'portrait' => $portrait,
            'figure' => $figure,
            'hint' => fn () => Book::hint($course, $user),
        ]);
    }
}
