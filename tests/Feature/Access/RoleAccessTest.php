<?php

use App\Models\User;

test('un invitado va al login', function () {
    $this->get(route('student.worlds'))->assertRedirect(route('login'));
    $this->get(route('admin.dashboard'))->assertRedirect(route('login'));
});

test('un alumno no puede entrar al panel del docente', function () {
    $this->actingAs(User::factory()->create())->get(route('admin.dashboard'))->assertForbidden();
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
