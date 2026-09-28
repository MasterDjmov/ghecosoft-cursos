<?php

use App\Enums\CoinReason;
use App\Enums\RequestStatus;
use App\Enums\RequestType;
use App\Livewire\Admin\Students\Create;
use App\Livewire\Admin\Students\Show;
use App\Livewire\Settings\ChangeTemporaryPassword;
use App\Models\CoinTransaction;
use App\Models\CourseSubscription;
use App\Models\Currency;
use App\Models\EnrollmentRequest;
use App\Models\Setting;
use App\Models\User;
use App\Notifications\PlatformNotification;
use App\Services\Ledger;
use Illuminate\Support\Facades\Hash;
use Livewire\Livewire;

/** Alta de alumnos por el docente, email opcional (D36) y contacto por WhatsApp. */
test('el docente crea un alumno sin email, con clave provisoria', function () {
    Livewire::actingAs(User::factory()->admin()->create())->test(Create::class)
        ->set('name', 'Rosa')
        ->set('last_name', 'Díaz')
        ->set('username', 'rosa_diaz')
        ->set('phone', '+54 9 380 412-3456')
        ->set('password', 'Kxqa4821')
        ->call('save')
        ->assertHasNoErrors()
        ->assertSee('Clave provisoria: Kxqa4821')
        ->assertSee('Usuario: rosa_diaz');

    $student = User::where('username', 'rosa_diaz')->firstOrFail();
    expect($student->email)->toBeNull()
        ->and($student->isStudent())->toBeTrue()
        ->and($student->must_change_password)->toBeTrue()
        ->and(Hash::check('Kxqa4821', $student->password))->toBeTrue();
});

test('al crearlo lo puede inscribir: pasa por el aprobador y queda en el libro', function () {
    ['course' => $course] = makeCourse();
    $cohort = $course->cohorts()->create(['name' => 'Martes']);

    Livewire::actingAs(User::factory()->admin()->create())->test(Create::class)
        ->set('name', 'Rosa')->set('last_name', 'Díaz')->set('username', 'rosa_diaz')
        ->set('courseId', (string) $course->id)
        ->set('cohortId', (string) $cohort->id)
        ->call('save')
        ->assertHasNoErrors();

    $student = User::where('username', 'rosa_diaz')->firstOrFail();
    $request = EnrollmentRequest::where('user_id', $student->id)->firstOrFail();
    expect($request->type)->toBe(RequestType::Admin)
        ->and($request->status)->toBe(RequestStatus::Approved)
        ->and(CourseSubscription::active()->where('user_id', $student->id)->where('cohort_id', $cohort->id)->exists())->toBeTrue()
        ->and(app(Ledger::class)->balance($student, Currency::forCourse($course)))->toBe($course->root_price)
        ->and(CoinTransaction::where('user_id', $student->id)->where('reason', CoinReason::EnrollmentGrant)->exists())->toBeTrue();
});

test('el usuario y el email del alta se validan como en el registro', function () {
    User::factory()->create(['username' => 'ocupado', 'email' => 'ya@esta.com']);

    Livewire::actingAs(User::factory()->admin()->create())->test(Create::class)
        ->set('name', 'Rosa')->set('last_name', 'Díaz')
        ->set('username', 'ocupado')->set('email', 'YA@esta.com')->set('phone', 'llamame')
        ->call('save')
        ->assertHasErrors(['username', 'email', 'phone']);
});

test('con clave provisoria solo puede ir a elegir su clave; después entra normal', function () {
    $student = User::factory()->create(['password' => 'Kxqa4821']);
    $student->forceFill(['must_change_password' => true])->save();

    $this->actingAs($student)->get(route('student.worlds'))->assertRedirect(route('password.change'));
    $this->actingAs($student)->get(route('profile.edit'))->assertRedirect(route('password.change'));
    $this->actingAs($student)->get(route('password.change'))->assertOk()->assertSee('Elegí tu clave');

    Livewire::actingAs($student)->test(ChangeTemporaryPassword::class)
        ->set('password', 'Kxqa4821')->set('password_confirmation', 'Kxqa4821')
        ->call('save')
        ->assertHasErrors('password');

    Livewire::actingAs($student)->test(ChangeTemporaryPassword::class)
        ->set('password', 'MiClave2026')->set('password_confirmation', 'MiClave2026')
        ->call('save')
        ->assertHasNoErrors()
        ->assertRedirect(route('home'));

    expect($student->fresh()->must_change_password)->toBeFalse();
    $this->actingAs($student->fresh())->get(route('student.worlds'))->assertOk();
});

test('el docente cambia usuario, email y teléfono, y resetea la clave', function () {
    $student = User::factory()->create(['username' => 'viejo', 'email' => 'perdido@mail.com', 'password' => 'Vieja1234']);

    Livewire::actingAs(User::factory()->admin()->create())->test(Show::class, ['user' => $student])
        ->set('username', 'nuevo_usuario')->set('email', '')->set('phone', '3804123456')
        ->call('saveAccount')
        ->assertHasNoErrors()
        ->assertRedirect(route('admin.students.show', 'nuevo_usuario'));

    $student->refresh();
    expect($student->username)->toBe('nuevo_usuario')
        ->and($student->email)->toBeNull()
        ->and($student->phone)->toBe('3804123456');

    $component = Livewire::actingAs(User::factory()->admin()->create())->test(Show::class, ['user' => $student])
        ->call('resetPassword')
        ->assertSee('Usuario: nuevo_usuario')
        ->assertSee('wa.me/3804123456');

    $student->refresh();
    preg_match('/Clave provisoria: (\S+)/', $component->get('credentials')['message'], $match);
    expect($student->must_change_password)->toBeTrue()
        ->and(Hash::check($match[1], $student->password))->toBeTrue()
        ->and(Hash::check('Vieja1234', $student->password))->toBeFalse();
});

test('un alumno no puede crear cuentas ni ver la ficha de otro', function () {
    $student = User::factory()->create();
    $other = User::factory()->create();

    $this->actingAs($student)->get(route('admin.students.create'))->assertForbidden();
    $this->actingAs($student)->get(route('admin.students.show', $other))->assertForbidden();
});

test('sin email los avisos quedan solo en la campanita', function () {
    $student = User::factory()->create(['email' => null]);
    $notification = new PlatformNotification('x', 'Hola', 'Texto', '/');

    expect($notification->via($student))->toBe(['database']);
});

test('el login y "olvidé mi clave" ofrecen escribirle al profe si cargó su número', function () {
    $this->get(route('login'))->assertOk()->assertDontSee('Escribile al profe');

    Setting::put('whatsapp_number', '+54 9 380 412-3456');

    $this->get(route('login'))->assertOk()->assertSee('Escribile al profe')->assertSee('wa.me/5493804123456', false);
    $this->get(route('password.request'))->assertOk()->assertSee('wa.me/5493804123456', false)->assertSee('tel:+5493804123456', false);
});
