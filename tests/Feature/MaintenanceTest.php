<?php

use App\Livewire\Admin\Settings;
use App\Livewire\Admin\Students\Index;
use App\Models\Setting;
use App\Models\User;
use App\Support\Maintenance;
use Livewire\Livewire;

/*
 * Mantenimiento (D86), desde Admin → Configuración: con la plataforma en mantenimiento solo entra el
 * administrador; con un curso en mantenimiento, sus alumnos no entran a ese curso. Se lee en cada pedido.
 */

test('el administrador prende el mantenimiento de la plataforma y de un curso', function () {
    ['course' => $course] = makeCourse();

    Livewire::actingAs(User::factory()->admin()->create())
        ->test(Settings::class)
        ->set('maintenance_platform', true)
        ->set('maintenance_message', 'Volvemos a las 18.')
        ->set('maintenance_courses', [(string) $course->id])
        ->call('saveMaintenance')
        ->assertHasNoErrors();

    expect(Maintenance::platform())->toBeTrue()
        ->and(Maintenance::message())->toBe('Volvemos a las 18.')
        ->and(Maintenance::course($course))->toBeTrue();
});

test('el docente no puede tocar la configuración', function () {
    $this->actingAs(User::factory()->teacher()->create())->get(route('admin.settings'))->assertRedirect();
});

test('con la plataforma en mantenimiento, el login avisa y solo entra el administrador', function () {
    Setting::put('maintenance_platform', '1');
    $student = User::factory()->create(['username' => 'alumno1', 'password' => 'secreto123']);
    $admin = User::factory()->admin()->create(['username' => 'jefe', 'password' => 'secreto123']);

    $this->get(route('login'))->assertOk()->assertSee('data-test="maintenance-notice"', false);

    $this->post(route('login.store'), ['login' => 'alumno1', 'password' => 'secreto123'])
        ->assertSessionHasErrors(['login' => Maintenance::DEFAULT_MESSAGE]);
    $this->assertGuest();

    $this->post(route('login.store'), ['login' => 'jefe', 'password' => 'secreto123']);
    $this->assertAuthenticatedAs($admin);
});

test('a quien ya estaba adentro se le cierra la sesión', function () {
    $student = studentWithRootOpen(makeCourse());
    Setting::put('maintenance_platform', '1');

    $this->actingAs($student)->get(route('student.worlds'))->assertRedirect(route('login'));
    $this->assertGuest();
});

test('con la plataforma en mantenimiento no se crean cuentas', function () {
    Setting::put('maintenance_platform', '1');

    $this->get(route('register'))->assertOk()->assertSee('data-test="maintenance-notice"', false);
    $this->post(route('register.store'), [
        'name' => 'Ana', 'last_name' => 'Pérez', 'username' => 'ana', 'email' => 'ana@example.com',
        'password' => 'Clave-Segura-2026', 'password_confirmation' => 'Clave-Segura-2026',
    ])->assertSessionHasErrors('email');
    expect(User::where('email', 'ana@example.com')->exists())->toBeFalse();
});

test('un curso en mantenimiento no deja entrar a sus alumnos, pero sí al docente', function () {
    $made = makeCourse();
    $student = studentWithRootOpen($made);
    Setting::put('maintenance_courses', (string) $made['course']->id);

    foreach ([route('student.course', $made['course']), route('student.tree', $made['course']), route('student.node', [$made['course'], $made['root']])] as $url) {
        $this->actingAs($student)->get($url)->assertRedirect(route('student.worlds'));
    }
    $this->actingAs($student)->get(route('student.worlds'))
        ->assertOk()
        ->assertSee('data-test="course-closed"', false);

    $this->actingAs(User::factory()->admin()->create())->get(route('student.tree', $made['course']))->assertOk();
});

test('los otros cursos siguen abiertos', function () {
    $closed = makeCourse();
    $open = makeCourse();
    $student = studentWithRootOpen($open);
    Setting::put('maintenance_courses', (string) $closed['course']->id);

    $this->actingAs($student)->get(route('student.tree', $open['course']))->assertOk();
});

test('un alumno habilitado desde Alumnos entra aunque haya mantenimiento, en la plataforma y en el curso cerrado', function () {
    $made = makeCourse();
    $student = studentWithRootOpen($made);
    $student->update(['password' => 'secreto123']);
    $other = studentWithRootOpen($made);
    Setting::put('maintenance_platform', '1');
    Setting::put('maintenance_courses', (string) $made['course']->id);

    Livewire::actingAs(User::factory()->admin()->create())
        ->test(Index::class)
        ->assertSee('data-test="maintenance-hint"', false)
        ->call('toggleMaintenanceAccess', $student->id);
    expect(Maintenance::isAllowed($student))->toBeTrue();
    auth()->logout();

    $this->post(route('login.store'), ['login' => $student->username, 'password' => 'secreto123']);
    $this->assertAuthenticatedAs($student);
    $this->get(route('student.tree', $made['course']))->assertOk();
    auth()->logout();

    $this->actingAs($other)->get(route('student.worlds'))->assertRedirect(route('login'));
});

test('se deshabilita con el mismo tilde, y el docente no puede tocarlo', function () {
    $student = User::factory()->create();
    Maintenance::toggleAllowed($student);

    Livewire::actingAs(User::factory()->admin()->create())
        ->test(Index::class)
        ->call('toggleMaintenanceAccess', $student->id);
    expect(Maintenance::isAllowed($student))->toBeFalse();

    Livewire::actingAs(User::factory()->teacher()->create())
        ->test(Index::class)
        ->call('toggleMaintenanceAccess', $student->id)
        ->assertForbidden();
});
