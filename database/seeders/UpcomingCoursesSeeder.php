<?php

namespace Database\Seeders;

use App\Enums\CourseLevel;
use App\Enums\Language;
use App\Models\Course;
use App\Services\TreeEditor;
use Illuminate\Database\Seeder;

/** Demo: cursos "Próximamente" (sin publicar, con temario) para ver el catálogo. Solo en local. */
class UpcomingCoursesSeeder extends Seeder
{
    public function run(TreeEditor $editor): void
    {
        $courses = [
            ['title' => 'JavaScript: La Feria de las Luces', 'slug' => 'javascript', 'language' => Language::JavaScript, 'level' => CourseLevel::Beginner,
                'short_description' => 'El lenguaje del navegador: páginas vivas y juegos web.',
                'syllabus' => "Variables y funciones\nEl DOM\nEventos\nFetch y JSON\nJuegos con canvas"],
        ];

        foreach ($courses as $i => $data) {
            if (Course::where('slug', $data['slug'])->exists()) {
                continue;
            }
            $editor->createCourse([...$data, 'is_upcoming' => true, 'position' => 10 + $i]);
        }
    }
}
