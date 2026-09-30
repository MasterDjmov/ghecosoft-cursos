<?php

use App\Enums\RequestKind;
use App\Enums\RequestStatus;
use App\Livewire\Admin\Requests;
use App\Livewire\Admin\Settings;
use App\Livewire\Student\CourseDetail;
use App\Livewire\Student\Worlds;
use App\Models\Currency;
use App\Models\EnrollmentRequest;
use App\Models\Setting;
use App\Models\User;
use App\Services\EnrollmentApprover;
use App\Services\EnrollmentRequester;
use App\Services\Ledger;
use App\Services\TreeAccess;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use Livewire\Livewire;

beforeEach(fn () => Storage::fake('local'));

test('la ficha de un curso sin publicar no se ve', function () {
    ['course' => $course] = makeCourse(['is_published' => false]);

    $this->actingAs(User::factory()->create())->get(route('student.course', $course))->assertForbidden();
});

test('el alumno pide inscripción con comprobante y no puede duplicarla', function () {
    ['course' => $course] = makeCourse();
    $student = User::factory()->create();

    Livewire::actingAs($student)->test(CourseDetail::class, ['course' => $course])
        ->set('receipt', UploadedFile::fake()->image('pago.jpg'))
        ->set('message', 'Pagué por transferencia')
        ->call('sendReceipt')
        ->assertHasNoErrors();

    $request = EnrollmentRequest::where('user_id', $student->id)->firstOrFail();
    expect($request->kind)->toBe(RequestKind::New)
        ->and($request->status)->toBe(RequestStatus::Pending)
        ->and($request->receipt_original_name)->toBe('pago.jpg');
    Storage::disk('local')->assertExists($request->receipt_path);

    Livewire::actingAs($student)->test(CourseDetail::class, ['course' => $course])
        ->set('receipt', UploadedFile::fake()->image('otro.jpg'))
        ->call('sendReceipt');

    expect(EnrollmentRequest::where('user_id', $student->id)->count())->toBe(1);
});

test('el comprobante tiene que ser imagen o PDF de hasta 5 MB', function () {
    ['course' => $course] = makeCourse();

    Livewire::actingAs(User::factory()->create())->test(CourseDetail::class, ['course' => $course])
        ->set('receipt', UploadedFile::fake()->create('pago.exe', 10))
        ->call('sendReceipt')
        ->assertHasErrors('receipt');

    Livewire::actingAs(User::factory()->create())->test(CourseDetail::class, ['course' => $course])
        ->set('receipt', UploadedFile::fake()->create('pago.pdf', 6000, 'application/pdf'))
        ->call('sendReceipt')
        ->assertHasErrors('receipt');
});

test('"Contactar al profe" deja la solicitud y abre WhatsApp con el mensaje', function () {
    ['course' => $course] = makeCourse(['title' => 'Python desde cero']);
    Setting::put('whatsapp_number', '+54 9 380 412-3456');
    $student = User::factory()->create(['name' => 'Kira', 'last_name' => 'Pérez']);

    Livewire::actingAs($student)->test(CourseDetail::class, ['course' => $course])
        ->call('contact')
        ->assertSee('Solicitud pendiente');

    expect(EnrollmentRequest::where('user_id', $student->id)->value('type')->value)->toBe('contact');

    $url = app(EnrollmentRequester::class)->whatsappUrl($student, $course, RequestKind::New);
    expect($url)->toStartWith('https://wa.me/5493804123456?text=')
        ->and(rawurldecode($url))->toContain('Kira Pérez')->toContain('Python desde cero');
});

test('el comprobante lo ven solo su dueño y el docente', function () {
    ['course' => $course] = makeCourse();
    $owner = User::factory()->create();
    Storage::disk('local')->put('receipts/x.pdf', 'PDF');
    $request = EnrollmentRequest::create(['user_id' => $owner->id, 'course_id' => $course->id, 'receipt_path' => 'receipts/x.pdf', 'receipt_original_name' => 'pago.pdf']);

    $this->actingAs($owner)->get(route('files.receipt', $request))->assertOk();
    $this->actingAs(User::factory()->create())->get(route('files.receipt', $request))->assertForbidden();
    $this->actingAs(User::factory()->admin()->create())->get(route('files.receipt', $request))->assertOk();
});

test('el docente aprueba: monedas + abono, y el alumno abre el curso', function () {
    ['course' => $course, 'root' => $root] = makeCourse();
    $student = User::factory()->create();
    $request = EnrollmentRequest::create(['user_id' => $student->id, 'course_id' => $course->id, 'type' => 'contact']);
    $admin = User::factory()->admin()->create();

    Livewire::actingAs($admin)->test(Requests::class)
        ->assertSee($student->fullName())
        ->call('review', $request->id, 'approve')
        ->call('confirm')
        ->assertHasNoErrors();

    expect($request->fresh()->status)->toBe(RequestStatus::Approved)
        ->and(app(Ledger::class)->balance($student, Currency::forCourse($course)))->toBe(10);

    Livewire::actingAs($student)->test(CourseDetail::class, ['course' => $course])
        ->assertSee('Inscripción aprobada')
        ->call('openCourse')
        ->assertRedirect(route('student.node', [$course, $root]));

    expect(app(Ledger::class)->balance($student, Currency::forCourse($course)))->toBe(0);
});

test('rechazar pide motivo y el alumno lo ve', function () {
    ['course' => $course] = makeCourse();
    $student = User::factory()->create();
    $request = EnrollmentRequest::create(['user_id' => $student->id, 'course_id' => $course->id, 'type' => 'contact']);

    Livewire::actingAs(User::factory()->admin()->create())->test(Requests::class)
        ->call('review', $request->id, 'reject')
        ->call('confirm')
        ->assertHasErrors('note')
        ->set('note', 'No encuentro el pago')
        ->call('confirm')
        ->assertHasNoErrors();

    Livewire::actingAs($student)->test(CourseDetail::class, ['course' => $course])->assertSee('No encuentro el pago');
});

test('con un abono previo, lo que se pide es una renovación', function () {
    ['course' => $course] = makeCourse();
    $student = enrolledStudent($course);
    // Abono vencido (sin mover el reloj: las subidas temporales de Livewire vencen si se viaja en el tiempo).
    $student->subscriptions()->update(['starts_at' => now()->subDays(40), 'ends_at' => now()->subDays(10)]);

    Livewire::actingAs($student)->test(CourseDetail::class, ['course' => $course])
        ->assertSee('Renovar abono')
        ->set('receipt', UploadedFile::fake()->image('pago.png'))
        ->call('sendReceipt')
        ->assertHasNoErrors();

    expect(EnrollmentRequest::where('user_id', $student->id)->where('status', 'pending')->value('kind'))->toBe(RequestKind::Renewal);
});

test('sin abono no se abre el curso', function () {
    ['course' => $course] = makeCourse();
    $student = User::factory()->create();

    Livewire::actingAs($student)->test(CourseDetail::class, ['course' => $course])->call('openCourse')->assertNoRedirect();

    expect($student->nodeUnlocks()->count())->toBe(0);
});

test('un alumno no entra a la bandeja ni a la configuración', function () {
    $this->actingAs(User::factory()->create());

    $this->get(route('admin.requests'))->assertRedirect(route('home'));
    $this->get(route('admin.settings'))->assertRedirect(route('home'));
});

test('la configuración guarda el WhatsApp', function () {
    Livewire::actingAs(User::factory()->admin()->create())->test(Settings::class)
        ->set('whatsapp_number', 'abc')
        ->call('save')
        ->assertHasErrors('whatsapp_number')
        ->set('whatsapp_number', '+54 9 380 412-3456')
        ->call('save')
        ->assertHasNoErrors();

    expect(Setting::get('whatsapp_number'))->toBe('+54 9 380 412-3456');
});

test('con la renovación aprobada antes de vencer, el alumno ve la fecha nueva y no el aviso', function () {
    ['course' => $course] = makeCourse();
    $student = enrolledStudent($course);
    Livewire::actingAs($student)->test(CourseDetail::class, ['course' => $course])->call('openCourse');
    $this->travel(27)->days();

    $renewal = EnrollmentRequest::create(['user_id' => $student->id, 'course_id' => $course->id, 'kind' => 'renewal', 'type' => 'contact']);
    app(EnrollmentApprover::class)->approve($renewal, User::factory()->admin()->create());
    $hasta = app(TreeAccess::class)->paidUntil($student, $course);

    expect((int) round(now()->diffInDays($hasta)))->toBe(33);
    Livewire::actingAs($student)->test(CourseDetail::class, ['course' => $course])
        ->assertSee($hasta->format('d/m/Y'))
        ->assertDontSee('Tu abono vence pronto');
    Livewire::actingAs($student)->test(Worlds::class)
        ->assertSee('Abono hasta el '.$hasta->format('d/m/Y'))
        ->assertDontSee('Renovalo');
});
