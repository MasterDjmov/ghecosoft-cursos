<?php

use App\Enums\ConsumerRequestKind;
use App\Livewire\Admin\ConsumerRequests;
use App\Livewire\Legal\ConsumerRequestForm;
use App\Models\ConsumerRequest;
use App\Models\User;
use Livewire\Livewire;

// D112: legales, consentimiento y botones de Defensa del Consumidor.

test('términos y privacidad se ven sin cuenta, con la leyenda de la AAIP', function () {
    $this->get(route('legal.terms'))->assertOk()->assertSee('data-test="legal-terms"', false)->assertSee('No se renueva solo', false);
    $this->get(route('legal.privacy'))->assertOk()->assertSee('AGENCIA DE ACCESO A LA INFORMACIÓN PÚBLICA')->assertSee(config('legal.email'));
});

test('la portada y el registro muestran los botones de arrepentimiento y de baja', function () {
    foreach ([route('landing'), route('register'), route('login')] as $url) {
        $this->get($url)->assertOk()->assertSee(route('legal.withdrawal'))->assertSee(route('legal.cancellation'));
    }
});

test('el registro pide aceptar los términos y guarda la versión aceptada', function () {
    $data = ['name' => 'Kira', 'last_name' => 'Pérez', 'username' => 'kira_perez', 'password' => 'Secreta123', 'password_confirmation' => 'Secreta123'];

    $this->post(route('register.store'), $data)->assertSessionHasErrors('terms');
    $this->assertGuest();

    $this->post(route('register.store'), [...$data, 'terms' => '1'])->assertSessionHasNoErrors();
    $user = User::where('username', 'kira_perez')->firstOrFail();
    expect($user->terms_version)->toBe(config('legal.version'))
        ->and($user->terms_accepted_at)->not->toBeNull();
});

test('el arrepentimiento se pide sin cuenta, da el código y avisa al administrador', function () {
    $admin = User::factory()->admin()->create();

    $this->get(route('legal.withdrawal'))->assertOk()->assertSee('Botón de arrepentimiento');

    Livewire::test(ConsumerRequestForm::class)
        ->set('name', 'Ana Gómez')->set('contact', 'ana@example.com')->set('course', 'Python')
        ->call('send')
        ->assertHasNoErrors()
        ->assertSee('data-test="consumer-request-code"', false);

    $request = ConsumerRequest::sole();
    expect($request->kind)->toBe(ConsumerRequestKind::Withdrawal)
        ->and($request->code)->toStartWith('A-')
        ->and($request->user_id)->toBeNull()
        ->and($admin->notifications()->count())->toBe(1);
});

test('la baja de un alumno con sesión queda ligada a su cuenta', function () {
    $student = User::factory()->create();

    $this->actingAs($student)->get(route('legal.cancellation'))->assertOk()->assertSee('Botón de baja');

    Livewire::actingAs($student)->test(ConsumerRequestForm::class, ['kind' => 'cancellation'])
        ->set('contact', 'kira@example.com')
        ->call('send')->assertHasNoErrors();

    $request = ConsumerRequest::sole();
    expect($request->kind)->toBe(ConsumerRequestKind::Cancellation)
        ->and($request->code)->toStartWith('B-')
        ->and($request->user_id)->toBe($student->id);
});

test('solo el administrador ve y resuelve los arrepentimientos', function () {
    $request = ConsumerRequest::create(['kind' => ConsumerRequestKind::Withdrawal, 'name' => 'Ana', 'contact' => 'ana@example.com']);

    $this->actingAs(User::factory()->teacher()->create())->get(route('admin.consumer-requests'))->assertRedirect();
    $this->actingAs(User::factory()->create())->get(route('admin.consumer-requests'))->assertRedirect();

    $admin = User::factory()->admin()->create();
    $this->actingAs($admin)->get(route('admin.consumer-requests'))->assertOk()->assertSee($request->code);

    Livewire::actingAs($admin)->test(ConsumerRequests::class)->set('notes.'.$request->id, 'Devuelto por transferencia')->call('resolve', $request->id);
    expect($request->fresh()->status->value)->toBe('handled')
        ->and($request->fresh()->handled_by)->toBe($admin->id);
});

test('el pago del abono muestra las condiciones y el botón de arrepentimiento', function () {
    $made = makeCourse();

    $this->actingAs(User::factory()->create())->get(route('student.course', $made['course']))
        ->assertOk()->assertSee('data-test="payment-conditions"', false)->assertSee('no se renueva solo', false);
});
