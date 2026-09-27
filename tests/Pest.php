<?php

use App\Enums\SubmissionStatus;
use App\Models\Course;
use App\Models\Currency;
use App\Models\EnrollmentRequest;
use App\Models\Node;
use App\Models\Submission;
use App\Models\User;
use App\Services\EnrollmentApprover;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Str;
use Tests\TestCase;

/*
|--------------------------------------------------------------------------
| Test Case
|--------------------------------------------------------------------------
|
| The closure you provide to your test functions is always bound to a specific PHPUnit test
| case class. By default, that class is "PHPUnit\Framework\TestCase". Of course, you may
| need to change it using the "pest()" function to bind different classes or traits.
|
*/

pest()->extend(TestCase::class)
    ->use(RefreshDatabase::class)
    ->in('Feature');

/*
|--------------------------------------------------------------------------
| Expectations
|--------------------------------------------------------------------------
|
| When you're writing tests, you often need to check that values meet certain conditions. The
| "expect()" function gives you access to a set of "expectations" methods that you can use
| to assert different things. Of course, you may extend the Expectation API at any time.
|
*/

expect()->extend('toBeOne', function () {
    return $this->toBe(1);
});

/*
|--------------------------------------------------------------------------
| Functions
|--------------------------------------------------------------------------
|
| While Pest is very powerful out-of-the-box, you may have some testing code specific to your
| project that you don't want to repeat in every file. Here you can also expose helpers as
| global functions to help you to reduce the number of lines of code in your test files.
|
*/

function something()
{
    // ..
}

/*
|--------------------------------------------------------------------------
| Helpers de la plataforma
|--------------------------------------------------------------------------
*/

/**
 * Curso mínimo: raíz (precio 10, 1 obligatoria que paga 10) → "Tema 1" (precio 10,
 * 2 obligatorias + 1 optativa) → "Tema 2". Más un extra pagado con comodines.
 *
 * @return array{course: Course, root: Node, topic1: Node, topic2: Node, extra: Node}
 */
function makeCourse(array $overrides = []): array
{
    $course = Course::create([
        'title' => 'Python', 'slug' => 'python-'.Str::random(6), 'language' => 'python',
        'is_published' => true, 'root_price' => 10, 'subscription_days' => 30, ...$overrides,
    ]);
    Currency::forCourse($course);

    $root = Node::create(['course_id' => $course->id, 'type' => 'root', 'title' => 'Clase 0', 'price' => 10]);
    $root->practices()->create(['title' => 'Primer programa', 'is_required' => true, 'coin_reward' => 10, 'xp_reward' => 10]);

    $topic1 = Node::create(['course_id' => $course->id, 'parent_id' => $root->id, 'type' => 'topic', 'title' => 'Tema 1', 'price' => 10]);
    $topic1->practices()->create(['title' => 'Misión 1', 'is_required' => true, 'coin_reward' => 5]);
    $topic1->practices()->create(['title' => 'Misión 2', 'is_required' => true, 'coin_reward' => 5]);
    $topic1->practices()->create(['title' => 'Encargo', 'is_required' => false, 'coin_reward' => 3]);

    $topic2 = Node::create(['course_id' => $course->id, 'parent_id' => $topic1->id, 'type' => 'topic', 'title' => 'Tema 2', 'price' => 10]);

    $extra = Node::create([
        'course_id' => $course->id, 'parent_id' => $root->id, 'type' => 'extra', 'title' => 'Extra',
        'price' => 3, 'price_currency_id' => Currency::wildcard()->id,
    ]);

    return compact('course', 'root', 'topic1', 'topic2', 'extra');
}

/** Alumno con abono vigente y las monedas del raíz, como si el docente hubiera aprobado el pago. */
function enrolledStudent(Course $course, ?User $student = null): User
{
    $student ??= User::factory()->create();
    $request = EnrollmentRequest::create(['user_id' => $student->id, 'course_id' => $course->id, 'kind' => 'new', 'type' => 'contact']);
    app(EnrollmentApprover::class)->approve($request, User::factory()->admin()->create());

    return $student;
}

/** Marca aprobadas todas las obligatorias de un nodo (sin pasar por la bandeja, que llega en la Fase 4). */
function approveRequiredPractices(User $student, Node $node): void
{
    foreach ($node->practices()->where('is_required', true)->get() as $practice) {
        $submission = Submission::create(['practice_id' => $practice->id, 'user_id' => $student->id, 'attempt' => 1, 'submitted_at' => now()]);
        $submission->forceFill(['status' => SubmissionStatus::Approved, 'reviewed_at' => now()])->save();
    }
}
