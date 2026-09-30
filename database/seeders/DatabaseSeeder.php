<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;

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
            UpcomingCoursesSeeder::class,
            DemoEnrollmentSeeder::class,
            DemoTeacherSeeder::class,
            DemoHeroesSeeder::class,
        ]);
    }
}
