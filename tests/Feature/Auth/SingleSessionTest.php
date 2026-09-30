<?php

use App\Livewire\Admin\Students\Show;
use App\Models\User;
use App\Services\SingleSession;
use Illuminate\Support\Facades\DB;
use Livewire\Livewire;

/** Sesión única (D65): una cuenta de alumno abierta en un solo lugar a la vez. */
function loginAs(User $user): void
{
    test()->post(route('login.store'), ['login' => $user->email, 'password' => 'password']);
    test()->get(route('student.worlds'))->assertOk();
}

/** Otro dispositivo entró con la misma cuenta: se queda con el token de la cuenta. */
function otherDeviceLogsIn(User $user): void
{
    User::whereKey($user->id)->update(['session_token' => 'token-de-otro-dispositivo-'.uniqid()]);
    // En la app cada pedido lee al usuario de la base; en el test hay que soltar el que quedó en memoria.
    app('auth')->forgetGuards();
}

test('al entrar, la sesión queda como la de la cuenta', function () {
    $student = User::factory()->create();
    loginAs($student);

    expect($student->fresh()->session_token)->not->toBeNull()
        ->toBe(session(SingleSession::SESSION_KEY));
});

test('si la cuenta entra en otro lugar, la sesión anterior se cierra con un aviso y queda anotado', function () {
    $student = User::factory()->create();
    loginAs($student);
    otherDeviceLogsIn($student);

    $this->get(route('student.worlds'))->assertRedirect(route('login'));
    $this->assertGuest();
    expect(DB::table('session_evictions')->where('user_id', $student->id)->count())->toBe(1);

    $this->get(route('login'))->assertSee('Tu cuenta se abrió en otro dispositivo');
});

test('al tercer cierre en 24 horas el docente recibe el aviso de cuenta compartida', function () {
    $admin = User::factory()->admin()->create();
    $student = User::factory()->create();

    foreach ([1, 2, 3] as $vez) {
        loginAs($student);
        otherDeviceLogsIn($student);
        $this->get(route('student.worlds'));
    }

    expect(DB::table('session_evictions')->where('user_id', $student->id)->count())->toBe(3);
    expect($admin->notifications()->where('data->kind', 'shared-account')->count())->toBe(1)
        ->and($admin->notifications()->first()->data['title'])->toContain($student->fullName());
});

test('el docente pausa la cuenta: se cortan las sesiones y no puede volver hasta reactivarla', function () {
    $admin = User::factory()->admin()->create();
    $student = User::factory()->create();
    loginAs($student);

    Livewire::actingAs($admin)->test(Show::class, ['user' => $student])->call('block');
    $this->actingAs($student->fresh())->get(route('student.worlds'))->assertRedirect(route('login'));
    $this->assertGuest();
    $this->get(route('login'))->assertSee('Tu cuenta está pausada');

    loginAs2Fails($student);

    Livewire::actingAs($admin)->test(Show::class, ['user' => $student->fresh()])->call('unblock');
    expect($student->fresh()->blocked_at)->toBeNull();
    app('auth')->forgetGuards();
    loginAs($student->fresh());
});

function loginAs2Fails(User $student): void
{
    test()->post(route('login.store'), ['login' => $student->email, 'password' => 'password']);
    app('auth')->forgetGuards();
    test()->get(route('student.worlds'))->assertRedirect(route('login'));
}

test('al docente no le aplica: puede tener varias sesiones', function () {
    $admin = User::factory()->admin()->create();
    $this->post(route('login.store'), ['login' => $admin->email, 'password' => 'password']);
    $admin->forceFill(['session_token' => 'otro'])->saveQuietly();

    $this->get(route('admin.dashboard'))->assertOk();
    expect(DB::table('session_evictions')->count())->toBe(0);
});
