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
            UpcomingCoursesSeeder::class,
            DemoEnrollmentSeeder::class,
            DemoHeroesSeeder::class,
        ]);
    }
}
