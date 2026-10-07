<?php

use App\Enums\Language;
use App\Models\User;

/*
 * Java para el alumno (D85): corre en SU compu con el Ejecutor de Java (scripts/JavaRunner.java) abierto, nunca en
 * el servidor. El alumno ve «Ejecutar», un aviso de cómo instalarlo y la página Herramientas → Ejecutor de Java.
 */

function javaCourse(): array
{
    $made = makeCourse(['language' => 'java']);
    $made['root']->update(['example_code' => 'public class Main { public static void main(String[] a) { System.out.println(1); } }', 'example_runnable' => true]);

    return [...$made, 'student' => studentWithRootOpen($made), 'practice' => $made['root']->practices()->first()];
}

test('Java corre con el ejecutor local; C, C++ y PHP siguen siendo solo del docente', function () {
    expect(Language::Java->studentCanRun())->toBeTrue()
        ->and(Language::Java->runsForStudents())->toBeFalse()
        ->and(Language::Python->studentCanRun())->toBeTrue()
        ->and(Language::Cpp->studentCanRun())->toBeFalse()
        ->and(Language::C->studentCanRun())->toBeFalse()
        ->and(Language::Php->studentCanRun())->toBeFalse();
});

test('en un curso de Java, el alumno puede ejecutar y ve cómo instalar el ejecutor', function () {
    ['course' => $course, 'root' => $root, 'student' => $student, 'practice' => $practice] = javaCourse();

    $this->actingAs($student)->get(route('student.node', [$course, $root]))
        ->assertOk()
        ->assertSee('Ejecutar (Ctrl+Enter)', false)
        ->assertSee('data-test="java-runner-hint"', false)
        ->assertSee(route('student.java-runner'), false);

    $this->actingAs($student)->get(route('student.mission', [$course, $root, $practice]))
        ->assertOk()
        ->assertSee('javaHelpUrl', false)
        ->assertSee('Ejecutar (Ctrl+Enter)', false);
});

test('en Python no aparece el aviso del ejecutor de Java', function () {
    $made = makeCourse();
    $made['root']->update(['example_code' => 'print(1)', 'example_runnable' => true]);

    $this->actingAs(studentWithRootOpen($made))->get(route('student.node', [$made['course'], $made['root']]))
        ->assertOk()
        ->assertDontSee('data-test="java-runner-hint"', false);
});

test('la página del ejecutor explica los pasos y el menú la muestra solo a quien cursa Java', function () {
    ['student' => $student] = javaCourse();

    $this->actingAs($student)->get(route('student.java-runner'))
        ->assertOk()
        ->assertSee('data-test="java-runner-download"', false)
        ->assertSee('data-test="java-runner-probe"', false)
        ->assertSee('data-test="menu-java-runner"', false);

    $other = studentWithRootOpen(makeCourse());
    $this->actingAs($other)->get(route('student.worlds'))->assertOk()->assertDontSee('data-test="menu-java-runner"', false);
});

test('el paquete trae el ejecutor, los lanzadores y el LEEME', function () {
    $response = $this->actingAs(User::factory()->create())->get(route('student.java-runner.download'));

    $response->assertOk()->assertDownload('ejecutor-java.zip');
    $zip = new ZipArchive;
    expect($zip->open($response->getFile()->getPathname()))->toBeTrue();
    $names = collect(range(0, $zip->numFiles - 1))->map(fn ($i) => $zip->getNameIndex($i))->sort()->values()->all();
    expect($names)->toBe(['ejecutor-java/Iniciar-ejecutor.bat', 'ejecutor-java/JavaRunner.java', 'ejecutor-java/LEEME.txt', 'ejecutor-java/iniciar-ejecutor.sh'])
        ->and($zip->getFromName('ejecutor-java/JavaRunner.java'))->toContain('127.0.0.1')->toContain('https://gamificado.lariojaclick.ar');
    $zip->close();
});

test('sin cuenta no se baja el ejecutor', function () {
    $this->get(route('student.java-runner.download'))->assertRedirect(route('login'));
});
