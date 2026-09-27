<?php

namespace Database\Seeders;

use App\Enums\RequestKind;
use App\Enums\RequestType;
use App\Models\Course;
use App\Models\EnrollmentRequest;
use App\Models\User;
use App\Services\EnrollmentApprover;
use Illuminate\Database\Seeder;

/**
 * Deja al alumno "cliente" con la inscripción a Python aprobada: tiene las
 * monedas del raíz y el abono vigente, pero todavía NO abrió el raíz, para
 * probar el circuito desde el principio.
 */
class DemoEnrollmentSeeder extends Seeder
{
    public function run(EnrollmentApprover $approver): void
    {
        $student = User::where('username', 'cliente')->firstOrFail();
        $admin = User::where('username', 'admin')->firstOrFail();
        $course = Course::where('slug', 'python')->firstOrFail();

        if ($student->subscriptions()->where('course_id', $course->id)->exists()) {
            return;
        }

        $request = EnrollmentRequest::create([
            'user_id' => $student->id,
            'course_id' => $course->id,
            'cohort_id' => $course->cohorts()->value('id'),
            'kind' => RequestKind::New,
            'type' => RequestType::Contact,
            'message' => 'Inscripción de prueba creada por el seeder.',
        ]);

        $approver->approve($request, $admin, 'Pago confirmado después de la clase inicial (demo).');
    }
}
