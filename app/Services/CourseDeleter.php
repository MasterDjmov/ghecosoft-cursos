<?php

namespace App\Services;

use App\Models\CoinTransaction;
use App\Models\Course;
use App\Models\CourseSubscription;
use App\Models\EnrollmentRequest;
use App\Models\NodeResource;
use App\Models\StoryFragment;
use App\Models\Submission;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Storage;

/**
 * Borrar un curso entero (D87), desde Admin → Cursos → Datos del curso, con doble confirmación. Se usa para
 * casos puntuales: para actualizar un curso se reimporta, que no toca el progreso.
 *
 * Se va todo lo del curso: nodos, prácticas, entregas, abonos, solicitudes (con sus comprobantes), comisiones,
 * diccionario, fragmentos y las monedas del curso. La XP ganada y los comodines quedan en la cuenta de cada
 * alumno (sin curso), y las cuentas no se tocan. Los archivos privados se borran después de la base.
 */
class CourseDeleter
{
    /** Lo que se perdería, para mostrarlo antes de confirmar. */
    public function impact(Course $course): array
    {
        $practiceIds = DB::table('practices')->whereIn('node_id', $course->nodes()->select('id'))->pluck('id');

        return [
            'nodes' => $course->nodes()->count(),
            'practices' => $practiceIds->count(),
            'submissions' => Submission::whereIn('practice_id', $practiceIds)->count(),
            'students' => CourseSubscription::where('course_id', $course->id)->distinct()->count('user_id'),
            'active' => CourseSubscription::where('course_id', $course->id)->where('ends_at', '>=', now())->distinct()->count('user_id'),
            'requests' => EnrollmentRequest::where('course_id', $course->id)->count(),
        ];
    }

    public function delete(Course $course): void
    {
        $files = [];

        DB::transaction(function () use ($course, &$files) {
            $nodeIds = $course->nodes()->pluck('id');
            $practiceIds = DB::table('practices')->whereIn('node_id', $nodeIds)->pluck('id');

            $files = collect()
                ->merge(NodeResource::whereIn('node_id', $nodeIds)->pluck('file_path'))
                ->merge(Submission::whereIn('practice_id', $practiceIds)->pluck('file_path'))
                ->merge(EnrollmentRequest::where('course_id', $course->id)->pluck('receipt_path'))
                ->filter()->unique()->values()->all();
            $images = StoryFragment::where('course_id', $course->id)->pluck('image_path')
                ->push($course->logo, $course->cover)->filter()->all();

            // Las monedas del curso no sirven sin el curso (su moneda se borra con él).
            if ($currency = $course->currency) {
                CoinTransaction::where('currency_id', $currency->id)->delete();
            }

            $course->nodes()->update(['parent_id' => null]);
            $course->delete();

            DB::afterCommit(function () use ($files, $images) {
                Storage::disk('local')->delete($files);
                Storage::disk('public')->delete($images);
            });
        });
    }
}
