<?php

use App\Models\User;

test('un invitado va al login', function () {
    $this->get(route('student.worlds'))->assertRedirect(route('login'));
    $this->get(route('admin.dashboard'))->assertRedirect(route('login'));
});

test('un alumno no puede entrar al panel del docente: vuelve a su inicio, sin ver el panel', function () {
    $student = User::factory()->create();

    $this->actingAs($student)->get(route('admin.dashboard'))->assertRedirect(route('home'));
    $this->actingAs($student)->followingRedirects()->get(route('admin.dashboard'))
        ->assertOk()->assertDontSee('Solicitudes pendientes');
    $this->actingAs($student)->getJson(route('admin.dashboard'))->assertForbidden();
});

test('el docente entra a su panel y también puede ver la vista del alumno', function () {
    $admin = User::factory()->admin()->create();

    $this->actingAs($admin)->get(route('admin.dashboard'))->assertOk()->assertSee('Solicitudes pendientes');
    $this->actingAs($admin)->get(route('student.worlds'))->assertOk();
});

test('el alumno ve sus mundos con el estado de cada curso', function () {
    ['course' => $course] = makeCourse(['title' => 'Python desde cero']);
    ['course' => $closed] = makeCourse(['title' => 'C desde cero']);
    $student = enrolledStudent($course);

    $this->actingAs($student)->get(route('student.worlds'))
        ->assertOk()
        ->assertSeeInOrder(['Python desde cero', 'Listo para abrir', 'Descubrí más mundos', 'C desde cero', 'Ver el curso']);
});

test('los cursos no publicados no aparecen', function () {
    makeCourse(['title' => 'Curso en borrador', 'is_published' => false]);

    $this->actingAs(User::factory()->create())->get(route('student.worlds'))->assertDontSee('Curso en borrador');
});

test('el 403 muestra la página de la zona prohibida con el botón para volver al inicio', function () {
    ['course' => $course, 'root' => $root] = makeCourse();
    $owner = enrolledStudent($course);
    $submission = $root->practices()->first()->submissions()->create([
        'user_id' => $owner->id, 'attempt' => 1, 'file_path' => 'submissions/x.py', 'submitted_at' => now(),
    ]);

    $this->actingAs(User::factory()->create())->get(route('files.submission', $submission))
        ->assertForbidden()
        ->assertSee('Esta puerta está sellada')
        ->assertSee('/images/error-403.webp', false)
        ->assertSee('href="'.route('home').'"', false);
});
