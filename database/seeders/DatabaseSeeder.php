<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Artisan;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        $this->call([
            SettingsSeeder::class,
            LevelSeeder::class,
            UserSeeder::class,
            PythonCourseSeeder::class,
            CCourseSeeder::class,
            CppCourseSeeder::class,
            JavaCourseSeeder::class,
            PhpCourseSeeder::class,
            HtmlCourseSeeder::class,
            UpcomingCoursesSeeder::class,
            DemoEnrollmentSeeder::class,
            DemoTeacherSeeder::class,
            DemoHeroesSeeder::class,
        ]);

        // Los ítems de ejemplo del juego (D90), después de los cursos.
        Artisan::call('app:game-items');
    }
}
