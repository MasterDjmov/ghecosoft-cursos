<?php

use App\Livewire\Admin\Courses\Form as CourseForm;
use App\Livewire\Admin\Courses\Index as CourseIndex;
use App\Livewire\Student\Worlds;
use App\Models\Course;
use App\Models\CourseInterest;
use App\Models\User;
use App\Services\NodeUnlocker;
use App\Services\TreeEditor;
use Livewire\Livewire;

/** Catálogo: "Mis cursos" aparte de "Descubrí más mundos", y cursos "Próximamente". */
function upcomingCourse(array $overrides = []): Course
{
    return app(TreeEditor::class)->createCourse([
        'title' => 'C desde cero', 'slug' => 'c-'.Str::lower(Str::random(5)), 'language' => 'c',
        'is_upcoming' => true, 'syllabus' => "Punteros\nArreglos", ...$overrides,
    ]);
}

test('mis cursos van arriba con el nodo en el que va; el resto, en Descubrí', function () {
    ['course' => $mine, 'root' => $root] = makeCourse(['title' => 'Mi Python']);
    ['course' => $other] = makeCourse(['title' => 'Otro curso']);
    upcomingCourse(['title' => 'C que viene']);
    Course::create(['title' => 'Borrador oculto', 'slug' => 'oculto']);
    $student = enrolledStudent($mine);
    app(NodeUnlocker::class)->unlock($student, $root);

    $this->actingAs($student)->get(route('student.worlds'))
        ->assertOk()
        ->assertSeeInOrder(['Seguí donde dejaste', 'Mi Python', 'Vas por:', 'Clase 0', 'Descubrí más mundos', 'Otro curso', 'C que viene', 'Punteros', 'Avisame cuando salga'])
        ->assertDontSee('Borrador oculto');
});

test('sin cursos propios ve la bienvenida y la oferta', function () {
    makeCourse(['title' => 'Python para empezar']);

    $this->actingAs(User::factory()->create())->get(route('student.worlds'))
        ->assertOk()
        ->assertSee('Todavía no estás en ningún mundo')
        ->assertSee('Python para empezar')
        ->assertDontSee('Seguí donde dejaste');
});

test('un curso "Próximamente" no se abre: ni ficha ni árbol', function () {
    $course = upcomingCourse();
    $student = User::factory()->create();

    $this->actingAs($student)->get(route('student.course', $course))->assertForbidden();
    $this->actingAs($student)->get(route('student.tree', $course))->assertForbidden();
});

test('"Avisame cuando salga" se anota y se saca; solo en cursos que vienen', function () {
    $course = upcomingCourse();
    ['course' => $published] = makeCourse();
    $student = User::factory()->create();

    Livewire::actingAs($student)->test(Worlds::class)->call('toggleInterest', $course->id);
    expect(CourseInterest::where('user_id', $student->id)->where('course_id', $course->id)->exists())->toBeTrue();

    Livewire::actingAs($student)->test(Worlds::class)->call('toggleInterest', $course->id);
    expect(CourseInterest::where('user_id', $student->id)->exists())->toBeFalse();

    Livewire::actingAs($student)->test(Worlds::class)->call('toggleInterest', $published->id);
    expect(CourseInterest::count())->toBe(0);
});

test('al publicarlo se avisa una sola vez a los interesados', function () {
    $course = upcomingCourse();
    $student = User::factory()->create();
    CourseInterest::create(['user_id' => $student->id, 'course_id' => $course->id]);
    $this->actingAs(User::factory()->admin()->create());

    Livewire::test(CourseIndex::class)->call('togglePublished', $course->id);
    Livewire::test(CourseIndex::class)->call('togglePublished', $course->id); // despublica
    Livewire::test(CourseIndex::class)->call('togglePublished', $course->id); // publica otra vez

    expect($course->fresh()->is_published)->toBeTrue()
        ->and($student->notifications()->where('data->kind', 'course.released')->count())->toBe(1);
});

test('el docente carga nivel, temario, destacado y "Próximamente"', function () {
    ['course' => $course] = makeCourse();
    $course->update(['is_published' => false]);

    Livewire::actingAs(User::factory()->admin()->create())->test(CourseForm::class, ['course' => $course])
        ->set('level', 'intermediate')
        ->set('syllabus', "  Clases \n\nHerencia\n")
        ->set('is_featured', true)
        ->set('is_upcoming', true)
        ->call('save')
        ->assertHasNoErrors();

    $course->refresh();
    expect($course->level->label())->toBe('Intermedio')
        ->and($course->syllabusItems())->toBe(['Clases', 'Herencia'])
        ->and($course->is_featured)->toBeTrue()
        ->and($course->isUpcoming())->toBeTrue();
});
