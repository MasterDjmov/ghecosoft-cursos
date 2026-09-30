<?php

namespace Database\Seeders;

use App\Models\Cohort;
use App\Models\Course;
use App\Models\CourseSubscription;
use App\Models\User;
use Illuminate\Database\Seeder;

/**
 * DESARROLLO (D72): el docente "docente" tiene una comisión de Python con el alumno "cliente",
 * para probar lo que ve y corrige un docente.
 */
class DemoTeacherSeeder extends Seeder
{
    public function run(): void
    {
        $teacher = User::where('username', 'docente')->firstOrFail();
        $student = User::where('username', 'cliente')->firstOrFail();
        $course = Course::where('slug', 'python')->firstOrFail();

        $cohort = Cohort::firstOrCreate(
            ['course_id' => $course->id, 'name' => 'Comisión del docente de prueba'],
            ['teacher_id' => $teacher->id, 'schedule_text' => 'Lunes y miércoles 18 a 20 h'],
        );

        CourseSubscription::where('user_id', $student->id)->where('course_id', $course->id)->update(['cohort_id' => $cohort->id]);
    }
}
