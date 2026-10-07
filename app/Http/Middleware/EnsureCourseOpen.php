<?php

namespace App\Http\Middleware;

use App\Models\Course;
use App\Support\Maintenance;
use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

/**
 * Curso en mantenimiento (D86): sus alumnos no entran al detalle, al árbol, a los nodos ni a las misiones.
 * Es persistente en Livewire, así que también frena las acciones de una página que ya estaba abierta.
 */
class EnsureCourseOpen
{
    public function handle(Request $request, Closure $next): Response
    {
        $course = $request->route('course');
        if (is_string($course)) {
            $course = Course::where('slug', $course)->first();
        }

        if ($course instanceof Course && ! Maintenance::letsIntoCourse($request->user(), $course)) {
            if ($request->hasHeader('X-Livewire') || $request->expectsJson()) {
                abort(503, Maintenance::DEFAULT_COURSE_MESSAGE);
            }

            return redirect()->route('student.worlds')->with('maintenance_course', $course->title);
        }

        return $next($request);
    }
}
