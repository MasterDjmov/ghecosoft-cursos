<?php

namespace App\Http\Controllers;

use App\Models\Course;
use App\Models\Setting;
use App\Services\Ranking;
use App\Support\Glossary;

/**
 * Portada pública: qué es, los cursos que más se dictan, "Próximamente",
 * las monedas de cada curso y el top 10 de héroes. Solo datos públicos.
 */
class LandingController
{
    public function __invoke(Ranking $ranking, Glossary $glossary)
    {
        if (auth()->check()) {
            return redirect()->route('home');
        }

        $catalog = Course::inCatalog()
            ->with('paths')
            ->withCount(['nodes as published_nodes_count' => fn ($q) => $q->where('is_published', true)])
            ->orderBy('position')
            ->get();
        $published = $catalog->where('is_published', true);
        $featured = $published->where('is_featured', true);

        $whatsapp = preg_replace('/\D+/', '', (string) Setting::get('whatsapp_number'));

        return view('landing', [
            'courses' => $featured->isNotEmpty() ? $featured : $published,
            'upcoming' => $catalog->filter(fn (Course $course) => $course->isUpcoming()),
            'coins' => $published->map(fn (Course $course) => ['course' => $course, ...$glossary->resolve('coin.course', $course)]),
            'top' => $ranking->publicTop(),
            'whatsapp' => $whatsapp !== '' ? $whatsapp : null,
        ]);
    }
}
