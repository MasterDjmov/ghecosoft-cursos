<?php

namespace App\Services;

use App\Models\Course;
use App\Models\CourseInterest;
use App\Models\User;
use App\Notifications\PlatformNotification;
use DomainException;

/** Cursos "Próximamente": quién pidió que le avisen, y el aviso cuando se publica. */
class CourseCatalog
{
    /** Anota o saca el "Avisame cuando salga". Devuelve si quedó anotado. */
    public function toggleInterest(User $user, Course $course): bool
    {
        if (! $course->isUpcoming()) {
            throw new DomainException('Ese curso no está en "Próximamente".');
        }

        $interest = CourseInterest::where('user_id', $user->id)->where('course_id', $course->id)->first();
        if ($interest) {
            $interest->delete();

            return false;
        }

        CourseInterest::create(['user_id' => $user->id, 'course_id' => $course->id]);

        return true;
    }

    /** Al publicar el curso, avisa una sola vez a cada interesado. */
    public function announceRelease(Course $course): int
    {
        $interests = CourseInterest::with('user')->where('course_id', $course->id)->whereNull('notified_at')->get();

        foreach ($interests as $interest) {
            $interest->user->notify(new PlatformNotification(
                'course.released',
                '¡Ya salió '.$course->title.'!',
                'Pediste que te avisemos. Mirá el curso y sumate cuando quieras.',
                route('student.course', $course),
                'rocket-launch',
            ));
            $interest->forceFill(['notified_at' => now()])->save();
        }

        return $interests->count();
    }
}
