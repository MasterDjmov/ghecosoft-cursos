<?php

use App\Enums\CoinReason;
use App\Enums\RequestType;
use App\Exceptions\NodeLocked;
use App\Livewire\Admin\Courses\Form;
use App\Livewire\Student\CourseDetail;
use App\Models\Course;
use App\Models\Currency;
use App\Models\EnrollmentRequest;
use App\Models\Node;
use App\Models\User;
use App\Services\CourseImporter;
use App\Services\EnrollmentApprover;
use App\Services\EnrollmentRequester;
use App\Services\Ledger;
use App\Services\NodeUnlocker;
use App\Services\TreeAccess;
use App\Support\UnlockMessages;
use Livewire\Livewire;

/*
 * D126: requisitos entre cursos. Un curso pide haber completado un nodo de otro (Videojuegos pide el jefe de R02 de C).
 * Sin cumplirlo no se pide la inscripción ni se abre el raíz; la Clase 0 se prueba igual.
 */

/** El curso «base» (C) y el que lo pide (Videojuegos), con el requisito: el «Tema 1» de C. */
function coursesWithPrerequisite(): array
{
    $base = makeCourse(['title' => 'Las Forjas de Hierro', 'language' => 'c']);
    $games = makeCourse(['title' => 'Videojuegos: Ciudad Arcadia', 'language' => 'c']);
    $games['course']->prerequisites()->attach($base['topic1']->id);

    return [$base, $games];
}

/** Completa el «Tema 1» del curso base: abre el raíz y el tema, y aprueba sus obligatorias. */
function completeBaseTopic(User $student, array $base): void
{
    app(Ledger::class)->credit($student, Currency::forCourse($base['course']), 50, CoinReason::ManualAdjustment, note: 'test');
    $unlocker = app(NodeUnlocker::class);
    $unlocker->unlock($student, $base['root']);
    approveRequiredPractices($student, $base['root']);
    $unlocker->unlock($student, $base['topic1']);
    approveRequiredPractices($student, $base['topic1']);
}

test('sin el requisito no se puede pedir la inscripción, con una frase clara', function () {
    [$base, $games] = coursesWithPrerequisite();
    $student = User::factory()->create();

    expect(app(TreeAccess::class)->missingPrerequisites($student, $games['course']))->toHaveCount(1);

    expect(fn () => app(EnrollmentRequester::class)->request($student, $games['course'], RequestType::Contact))
        ->toThrow(DomainException::class, 'Para avanzar se requiere «Tema 1» del curso «Las Forjas de Hierro».');
    expect(EnrollmentRequest::where('user_id', $student->id)->where('course_id', $games['course']->id)->exists())->toBeFalse();
});

test('con el abono aprobado igual, el raíz no se abre hasta cumplir el requisito', function () {
    [$base, $games] = coursesWithPrerequisite();
    $student = enrolledStudent($games['course']);
    $access = app(TreeAccess::class);

    expect($access->unlockBlockers($student, $games['root']))->toContain(TreeAccess::BLOCK_PREREQUISITES)
        ->and(UnlockMessages::for($student, $games['root']))->toContain('Para avanzar se requiere «Tema 1» del curso «Las Forjas de Hierro».');
    expect(fn () => app(NodeUnlocker::class)->unlock($student, $games['root']))->toThrow(NodeLocked::class);

    // Lo cumple en el otro curso (con su propio abono) y ya puede abrirlo.
    enrolledStudent($base['course'], $student);
    completeBaseTopic($student, $base);
    expect($access->missingPrerequisites($student, $games['course']))->toBe([]);
    app(NodeUnlocker::class)->unlock($student, $games['root']);
    expect($access->isRootOpen($student, $games['course']))->toBeTrue();
});

test('cumplido el requisito, se pide la inscripción como siempre', function () {
    [$base, $games] = coursesWithPrerequisite();
    $student = enrolledStudent($base['course']);
    completeBaseTopic($student, $base);

    $request = app(EnrollmentRequester::class)->request($student, $games['course'], RequestType::Contact);
    expect($request->course_id)->toBe($games['course']->id);
});

test('la Clase 0 se prueba igual aunque falte el requisito', function () {
    [, $games] = coursesWithPrerequisite();
    $student = User::factory()->create();

    expect(app(TreeAccess::class)->canTryCourse($student, $games['course']))->toBeTrue();
    $this->actingAs($student)->get(route('student.node', [$games['course'], $games['root']]))->assertOk();
});

test('renovar no pide el requisito: ya lo venía cursando', function () {
    [, $games] = coursesWithPrerequisite();
    $student = User::factory()->create();
    // Se inscribió antes de que el curso pidiera nada.
    $request = EnrollmentRequest::create(['user_id' => $student->id, 'course_id' => $games['course']->id, 'kind' => 'new', 'type' => 'contact']);
    app(EnrollmentApprover::class)->approve($request, User::factory()->admin()->create());

    $renewal = app(EnrollmentRequester::class)->request($student, $games['course'], RequestType::Contact);
    expect($renewal->kind->value)->toBe('renewal');
});

test('el staff no tiene requisitos, y un requisito sin publicar no se exige', function () {
    [$base, $games] = coursesWithPrerequisite();
    $access = app(TreeAccess::class);

    expect($access->missingPrerequisites(User::factory()->admin()->create(), $games['course']))->toBe([]);

    $base['course']->update(['is_published' => false]);
    expect($access->missingPrerequisites(User::factory()->create(), $games['course']))->toBe([]);
});

test('la ficha del curso muestra el cartel con el botón al otro curso y sin «Solicitar inscripción»', function () {
    [$base, $games] = coursesWithPrerequisite();
    $student = User::factory()->create();

    $this->actingAs($student)->get(route('student.course', $games['course']))
        ->assertOk()
        ->assertSee('data-test="course-prerequisites"', false)
        ->assertSee('Para avanzar se requiere «Tema 1» del curso «Las Forjas de Hierro».')
        ->assertSee(route('student.course', $base['course']), false)
        ->assertSee('Probar la clase 0 gratis')
        ->assertDontSee('data-test="request-enrollment"', false);

    // Cumplido, el cartel se va y vuelve el botón.
    enrolledStudent($base['course'], $student);
    completeBaseTopic($student, $base);
    Livewire::actingAs($student)->test(CourseDetail::class, ['course' => $games['course']])
        ->assertDontSee('Este curso se apoya en otro')
        ->assertSeeHtml('data-test="request-enrollment"');
});

test('el admin agrega y quita requisitos de otros cursos', function () {
    [$base, $games] = coursesWithPrerequisite();
    $admin = User::factory()->admin()->create();
    $games['course']->prerequisites()->detach();

    Livewire::actingAs($admin)->test(Form::class, ['course' => $games['course']])
        ->set('prerequisiteCourse', $base['course']->id)
        ->set('prerequisiteNode', $base['topic2']->id)
        ->call('addPrerequisite')
        ->assertHasNoErrors()
        ->assertSee('Tema 2');
    expect($games['course']->prerequisites()->pluck('nodes.id')->all())->toBe([$base['topic2']->id]);

    // Un nodo del mismo curso no vale.
    Livewire::actingAs($admin)->test(Form::class, ['course' => $games['course']])
        ->set('prerequisiteNode', $games['topic1']->id)
        ->call('addPrerequisite')
        ->assertHasErrors('prerequisiteNode');

    Livewire::actingAs($admin)->test(Form::class, ['course' => $games['course']])
        ->call('removePrerequisite', $base['topic2']->id);
    expect($games['course']->prerequisites()->count())->toBe(0);
});

test('el importador lee «requiere» del curso (curso:nodo) y avisa lo que no existe', function () {
    $fixture = file_get_contents(base_path('tests/Fixtures/curso-ejemplo.md'));
    $importer = app(CourseImporter::class);

    $base = $importer->import([['name' => 'c.md', 'content' => str_replace("slug: python-import\n", "slug: forjas-import\n", $fixture)]], dryRun: false);
    expect($base->errors)->toBe([]);

    $withPrerequisite = str_replace("slug: python-import\n", "slug: arcadia-import\nrequiere: forjas-import:R01-N02, nadie:R01-N01\n", $fixture);
    $report = $importer->import([['name' => 'arcadia.md', 'content' => $withPrerequisite]], dryRun: false);

    expect($report->errors)->toBe([])
        ->and(collect($report->warnings)->join(' '))->toContain('nadie:R01-N01');
    $required = Node::whereHas('course', fn ($q) => $q->where('slug', 'forjas-import'))->where('code', 'R01-N02')->value('id');
    expect(Course::where('slug', 'arcadia-import')->first()->prerequisites()->pluck('nodes.id')->all())->toBe([$required]);

    $same = str_replace("slug: python-import\n", "slug: arcadia-import\nrequiere: arcadia-import:R01-N01\n", $fixture);
    expect($importer->import([['name' => 'arcadia.md', 'content' => $same]], dryRun: true)->errors)->not->toBe([]);
});
