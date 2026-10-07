<?php

namespace App\Livewire\Student;

use App\Models\Course;
use App\Models\Hero;
use App\Services\Heroes as HeroService;
use Illuminate\Support\Facades\Gate;
use Livewire\Attributes\Title;
use Livewire\Component;

/** Mis héroes (D89): el protagonista de cada curso que puede jugar, con su estado o «Tomá el control». */
#[Title('Mis héroes')]
class Heroes extends Component
{
    public function render(HeroService $heroes)
    {
        $user = auth()->user();
        $owned = Hero::where('user_id', $user->id)->get()->keyBy('course_id');
        $cards = Course::where('is_published', true)->orderBy('title')->get()
            ->filter(fn (Course $course) => $heroes->protagonist($course) !== null && Gate::allows('play', $course))
            ->map(fn (Course $course) => [
                'course' => $course,
                'protagonist' => $protagonist = $heroes->protagonist($course),
                'hero' => $hero = $owned[$course->id] ?? null,
                'image' => HeroService::lookUrl($protagonist, $hero?->look ?? 1),
            ])
            ->values();

        return view('livewire.student.heroes', [
            'cards' => $cards,
            'gold' => $heroes->gold($user),
        ]);
    }
}
