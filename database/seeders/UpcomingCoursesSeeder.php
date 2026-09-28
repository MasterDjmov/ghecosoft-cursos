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
            ['title' => 'C desde cero', 'slug' => 'c', 'language' => Language::C, 'level' => CourseLevel::Beginner,
                'short_description' => 'El lenguaje que está debajo de casi todo.',
                'syllabus' => "Compilar y ejecutar\nVariables y tipos\nCondicionales y bucles\nFunciones\nArreglos y cadenas\nPunteros"],
            ['title' => 'C++ intermedio', 'slug' => 'cpp', 'language' => Language::Cpp, 'level' => CourseLevel::Intermediate,
                'short_description' => 'Clases, memoria y la STL, paso a paso.',
                'syllabus' => "Clases y objetos\nHerencia y polimorfismo\nMemoria dinámica\nPlantillas\nLa STL"],
        ];

        foreach ($courses as $i => $data) {
            if (Course::where('slug', $data['slug'])->exists()) {
                continue;
            }
            $editor->createCourse([...$data, 'is_upcoming' => true, 'position' => 10 + $i]);
        }
    }
}
