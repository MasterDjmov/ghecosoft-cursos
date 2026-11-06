<?php

use App\Models\Course;
use App\Models\User;
use App\Support\PracticeTools;

/*
 * D120: Herramientas. Cada lenguaje se habilita con el abono vigente de un curso que lo usa; el staff los tiene todos.
 * El código corre en el navegador (o, en Java, en la compu de quien ejecuta): el servidor solo sirve la página.
 */

function practiceCourse(string $language): array
{
    $course = makeCourse(['language' => $language, 'is_published' => true])['course'];

    return [enrolledStudent($course), $course];
}

test('el staff tiene todas las herramientas de práctica aunque no haya cursos', function () {
    $admin = User::factory()->admin()->create();

    foreach (array_keys(PracticeTools::TOOLS) as $key) {
        $this->actingAs($admin)->get(route('student.practice-tool', $key))->assertOk()->assertSee('data-test="practice-tool"', false);
    }
});

test('un alumno con el abono de un curso practica ese lenguaje, y lo ve en la tarjeta', function () {
    [$student] = practiceCourse('csharp');

    $this->actingAs($student)->get(route('student.practice-tool', 'csharp'))
        ->assertOk()
        ->assertSee('Practicar C#')
        ->assertSee('data-test="menu-tools"', false)
        ->assertSee('data-test="menu-csharp"', false)
        ->assertDontSee('data-test="menu-python"', false);
});

test('un alumno no entra a la herramienta de un lenguaje que no cursa, ni con la Clase 0', function () {
    [$student] = practiceCourse('csharp');
    makeCourse(['language' => 'python', 'is_published' => true]);

    $this->actingAs($student)->get(route('student.practice-tool', 'python'))->assertForbidden();
});

test('sin abono vigente se cierra la herramienta y desaparece la tarjeta', function () {
    [$student, $course] = practiceCourse('c');
    $course->subscriptions()->where('user_id', $student->id)->update(['ends_at' => now()->subDay()]);

    expect(PracticeTools::menu($student->fresh()))->toBe([]);
    $this->actingAs($student)->get(route('student.practice-tool', 'c'))->assertForbidden();
});

test('un curso sin publicar no habilita su herramienta', function () {
    [$student, $course] = practiceCourse('c');
    Course::whereKey($course->id)->update(['is_published' => false]);

    $this->actingAs($student)->get(route('student.practice-tool', 'c'))->assertForbidden();
});

test('SQL se practica con un curso de PHP', function () {
    [$student] = practiceCourse('php');

    $this->actingAs($student)->get(route('student.practice-tool', 'sql'))->assertOk();
});

test('un lenguaje que no tiene herramienta da 404', function () {
    $this->actingAs(User::factory()->admin()->create())->get(route('student.practice-tool', 'cobol'))->assertNotFound();
});

test('quien no inició sesión no entra', function () {
    $this->get(route('student.practice-tool', 'python'))->assertRedirect(route('login'));
});

test('en la ventana flotante la herramienta va suelta, sin el menú ni otra ventana', function () {
    [$student] = practiceCourse('asm');

    $this->actingAs($student)->get(route('student.asm-tool', ['ventana' => 1]))
        ->assertOk()
        ->assertSee('data-test="asm-tool"', false)
        ->assertDontSee('data-test="menu-tools"', false)
        ->assertDontSee('data-tool-window', false);

    $this->actingAs($student)->get(route('student.asm-tool'))
        ->assertSee('data-test="menu-asm-tool"', false)
        ->assertSee('data-tool-window', false);
});

test('la calculadora y la tabla son para todos los que iniciaron sesión, sin abono', function () {
    $student = User::factory()->create();
    expect(PracticeTools::menu($student))->toBe([]);

    $this->actingAs($student)->get(route('student.worlds'))
        ->assertSee('data-test="menu-tools"', false)
        ->assertSee('data-test="menu-ascii"', false)
        ->assertSee('data-test="menu-calculator"', false);

    $this->actingAs($student)->get(route('student.calculator'))->assertOk()->assertSee('data-test="calculator-tool"', false);
    $this->actingAs($student)->get(route('student.ascii'))->assertOk()->assertSee('data-test="ascii-tool"', false);
});

test('la calculadora y la tabla piden iniciar sesión', function () {
    $this->get(route('student.calculator'))->assertRedirect(route('login'));
    $this->get(route('student.ascii'))->assertRedirect(route('login'));
});

test('en la ventana flotante la calculadora y la tabla van sueltas', function () {
    $student = User::factory()->create();

    foreach (['student.calculator', 'student.ascii'] as $route) {
        $this->actingAs($student)->get(route($route, ['ventana' => 1]))
            ->assertOk()
            ->assertDontSee('data-test="menu-tools"', false)
            ->assertDontSee('data-tool-window', false);
    }
});
