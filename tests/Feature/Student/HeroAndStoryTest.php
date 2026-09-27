<?php

use App\Enums\CoinReason;
use App\Enums\XpReason;
use App\Livewire\Admin\Students\Show as StudentShow;
use App\Livewire\Settings\Profile;
use App\Models\Branch;
use App\Models\CourseCompletion;
use App\Models\Currency;
use App\Models\GlossaryTerm;
use App\Models\Submission;
use App\Models\User;
use App\Services\Ledger;
use App\Services\NodeUnlocker;
use App\Services\PracticeSubmitter;
use App\Services\Ranking;
use App\Services\SubmissionReviewer;
use App\Support\Glossary;
use App\Support\Narrative;
use Livewire\Livewire;

/** Fase 9: el héroe del alumno (D38) y la historia en pantalla. */
function storyTerm(string $key, $course, string $singular, ?string $lore = null): void
{
    GlossaryTerm::create(['key' => $key, 'course_id' => $course?->id, 'singular' => $singular, 'gender' => 'f', 'lore' => $lore]);
    Glossary::flush($course?->id);
}

function approveAll(User $student, $node): void
{
    $reviewer = app(SubmissionReviewer::class);
    foreach ($node->practices()->where('is_required', true)->get() as $practice) {
        $submission = Submission::create(['practice_id' => $practice->id, 'user_id' => $student->id, 'attempt' => 1, 'submitted_at' => now()]);
        $reviewer->approve($submission, User::factory()->admin()->create());
    }
}

test('el alumno elige su héroe; es único sin distinguir mayúsculas ni tildes', function () {
    $taken = User::factory()->create(['hero_name' => 'Kirá']);
    $student = User::factory()->create();

    Livewire::actingAs($student)->test(Profile::class)
        ->set('hero_name', 'kira')
        ->call('saveHero')
        ->assertHasErrors(['hero_name' => 'unique']);

    Livewire::actingAs($student)->test(Profile::class)
        ->set('hero_name', 'Zed<script>')
        ->call('saveHero')
        ->assertHasErrors(['hero_name' => 'regex']);

    Livewire::actingAs($student)->test(Profile::class)
        ->set('hero_name', '  Luna   Roja ')
        ->call('saveHero')
        ->assertHasNoErrors();

    expect($student->fresh()->hero_name)->toBe('Luna Roja')
        ->and($taken->fresh()->hero_name)->toBe('Kirá');
});

test('el docente puede cambiar un héroe inapropiado', function () {
    $student = User::factory()->create(['hero_name' => 'Feo']);

    Livewire::actingAs(User::factory()->admin()->create())->test(StudentShow::class, ['user' => $student])
        ->set('heroName', 'Nombre Nuevo')
        ->call('saveHero')
        ->assertHasNoErrors();

    expect($student->fresh()->hero_name)->toBe('Nombre Nuevo');
});

test('los marcadores de la historia se reemplazan con el héroe y el diccionario', function () {
    ['course' => $course] = makeCourse();
    storyTerm('mentor.name', $course, 'Ofidia');
    $student = User::factory()->create(['hero_name' => 'Luna']);
    $anonymous = User::factory()->create();

    expect(Narrative::fill('—Bien hecho, {heroe} —dice {mentor}.', $course, $student))->toBe('—Bien hecho, Luna —dice Ofidia.')
        ->and(Narrative::fill('Hola, {Héroe}.', $course, $anonymous))->toBe('Hola, Kira.');
});

test('la crónica del nodo llama al alumno por su héroe', function () {
    ['course' => $course, 'root' => $root] = makeCourse();
    $root->update(['chronicle' => '—Adelante, {heroe}.']);
    $student = enrolledStudent($course);
    $student->update(['hero_name' => 'Luna']);
    app(NodeUnlocker::class)->unlock($student, $root);

    $this->actingAs($student)->get(route('student.node', [$course, $root]))
        ->assertOk()->assertSee('—Adelante, Luna.')->assertDontSee('{heroe}');
});

test('el héroe aparece en el ranking y en el CV', function () {
    ['course' => $course] = makeCourse();
    $student = enrolledStudent($course);
    $student->update(['hero_name' => 'Luna', 'cv_public' => true, 'birth_date' => now()->subYears(20)]);
    app(Ledger::class)->addXp($student, 50, XpReason::ManualAdjustment, note: 'test');
    Ranking::forget();

    $this->actingAs($student)->get(route('student.ranking'))->assertOk()->assertSee('Luna');
    $this->get(route('cv.show', $student->username))->assertOk()->assertSee('Héroe: Luna');
});

test('la bienvenida del curso se ve en la ficha y en el árbol, y el jefe se presenta', function () {
    ['course' => $course, 'root' => $root, 'topic1' => $topic1] = makeCourse();
    storyTerm('story.course_intro', $course, 'Bienvenida al Valle', 'Despertaste en el Valle, {heroe}.');
    $student = enrolledStudent($course);
    $student->update(['hero_name' => 'Luna']);

    $this->actingAs($student)->get(route('student.course', $course))->assertOk()->assertSee('Despertaste en el Valle, Luna.');
    app(NodeUnlocker::class)->unlock($student, $root);
    $this->actingAs($student)->get(route('student.tree', $course))->assertOk()->assertSee('Bienvenida al Valle');

    $topic1->update(['type' => 'boss']);
    approveAll($student, $root);
    app(NodeUnlocker::class)->unlock($student, $topic1);
    $this->actingAs($student)->get(route('student.node', [$course, $topic1]))
        ->assertOk()->assertSee('proyecto integrador')->assertSee('+'.config('game.boss_defeated_xp'));
});

test('completar una rama avisa con su historia', function () {
    ['course' => $course, 'root' => $root, 'topic1' => $topic1] = makeCourse();
    storyTerm('story.branch_completed', $course, '¡Rama completada!', 'Bien hecho, {heroe}.');
    $branch = Branch::create(['course_id' => $course->id, 'title' => 'Fundamentos']);
    $topic1->update(['branch_id' => $branch->id]);
    $student = enrolledStudent($course);
    $student->update(['hero_name' => 'Luna']);
    app(NodeUnlocker::class)->unlock($student, $root);
    approveAll($student, $root);
    app(NodeUnlocker::class)->unlock($student, $topic1);

    approveAll($student, $topic1);

    $notification = $student->notifications()->get()->firstWhere('data.kind', 'story.branch_completed');
    expect($notification)->not->toBeNull()
        ->and($notification->data['title'])->toBe('¡«Fundamentos» completada!')
        ->and($notification->data['body'])->toBe('Bien hecho, Luna.');
});

test('la Encrucijada (misión de reflexión sin entrega) cierra el curso con su historia', function () {
    ['course' => $course, 'root' => $root, 'topic1' => $topic1, 'topic2' => $topic2] = makeCourse();
    storyTerm('story.course_completed', $course, '¡Dominaste el Valle!', 'Elegí tu Senda, {heroe}.');
    $reflection = $topic2->practices()->create(['title' => 'Mirá hacia atrás', 'is_required' => true, 'submission_mode' => 'none', 'xp_reward' => 10]);
    $student = enrolledStudent($course);
    app(NodeUnlocker::class)->unlock($student, $root);
    approveAll($student, $root);
    app(NodeUnlocker::class)->unlock($student, $topic1);
    approveAll($student, $topic1);
    app(Ledger::class)->credit($student, Currency::forCourse($course), 10, CoinReason::ManualAdjustment, note: 'test');
    app(NodeUnlocker::class)->unlock($student, $topic2);

    app(PracticeSubmitter::class)->toggleMark($student, $reflection);

    expect(CourseCompletion::where('user_id', $student->id)->where('course_id', $course->id)->exists())->toBeTrue()
        ->and($student->notifications()->get()->pluck('data.kind'))->toContain('story.course_completed');

    $this->actingAs($student)->get(route('student.tree', $course))->assertOk()->assertSee('¡Dominaste el Valle!')->assertSee('Ver mi CV');
});

test('quien no eligió héroe ve el aviso en Mundos', function () {
    $student = User::factory()->create();

    $this->actingAs($student)->get(route('student.worlds'))->assertOk()->assertSee('Elegí el nombre de tu héroe');
    $student->update(['hero_name' => 'Luna']);
    $this->actingAs($student->fresh())->get(route('student.worlds'))->assertOk()->assertDontSee('Elegí el nombre de tu héroe');
});
