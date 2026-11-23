<?php

use App\Livewire\Admin\Messages;
use App\Livewire\PracticeChat;
use App\Livewire\Student\PracticeTool;
use App\Livewire\Student\SavedPractices;
use App\Models\Cohort;
use App\Models\CourseSubscription;
use App\Models\PracticeMessage;
use App\Models\SavedPractice;
use App\Models\User;
use App\Notifications\PlatformNotification;
use Illuminate\Support\Facades\Notification;
use Livewire\Livewire;

/** D124: Mis prácticas: guardar lo de Practicar, retomarlo, bajarlo y consultarle al profe. */
beforeEach(function () {
    $this->course = makeCourse(['language' => 'python', 'is_published' => true])['course'];
    $this->student = enrolledStudent($this->course);
});

test('guarda lo de Practicar, lo retoma, le cambia el nombre y guarda una copia', function () {
    Livewire::actingAs($this->student)->test(PracticeTool::class, ['language' => 'python'])
        ->assertSee('data-test="practice-save"', false)
        ->call('save', 'print("hola")', '3')
        ->assertRedirect();

    $saved = SavedPractice::sole();
    expect($saved)->user_id->toBe($this->student->id)->language->toBe('python')->code->toBe('print("hola")')->stdin->toBe('3')
        ->and($saved->title)->toStartWith('Práctica de Python del ');

    $page = Livewire::actingAs($this->student)->withQueryParams(['practica' => $saved->id])->test(PracticeTool::class, ['language' => 'python'])
        ->assertSee('hola')
        ->assertSee('data-test="saved-practice-header"', false)
        ->set('title', 'Clase de listas')
        ->call('save', 'print("chau")');
    expect($saved->fresh())->title->toBe('Clase de listas')->code->toBe('print("chau")');

    $page->call('saveNew', 'print("otra")');
    expect(SavedPractice::where('title', 'Clase de listas (copia)')->sole()->code)->toBe('print("otra")');
});

test('no guarda una práctica vacía ni pasa el tope', function () {
    Livewire::actingAs($this->student)->test(PracticeTool::class, ['language' => 'python'])->call('save', '   ');
    expect(SavedPractice::count())->toBe(0);
});

test('nadie más abre, cambia ni borra la práctica de otro, ni el administrador', function () {
    $saved = SavedPractice::create(['user_id' => $this->student->id, 'language' => 'python', 'title' => 'Mía', 'code' => 'x = 1']);
    $other = enrolledStudent($this->course);

    foreach ([$other, User::factory()->admin()->create()] as $intruder) {
        $this->actingAs($intruder)->get(route('student.practice-tool', ['language' => 'python', 'practica' => $saved->id]))->assertForbidden();
        Livewire::actingAs($intruder)->test(SavedPractices::class)->call('delete', $saved->id)->assertForbidden();
    }
    expect($saved->fresh())->not->toBeNull();
});

test('Mis prácticas lista las propias, las baja como archivo y las borra', function () {
    $saved = SavedPractice::create(['user_id' => $this->student->id, 'language' => 'python', 'title' => 'Clase de listas', 'code' => 'print([1, 2])']);
    SavedPractice::create(['user_id' => enrolledStudent($this->course)->id, 'language' => 'python', 'title' => 'De otro', 'code' => 'x']);

    $this->actingAs($this->student)->get(route('student.saved-practices'))
        ->assertOk()->assertSee('Clase de listas')->assertDontSee('De otro')
        ->assertSee('data-test="menu-saved-practices"', false);

    Livewire::actingAs($this->student)->test(SavedPractices::class)
        ->call('download', $saved->id)
        ->assertFileDownloaded('clase_de_listas.py', 'print([1, 2])')
        ->call('delete', $saved->id);
    expect(SavedPractice::find($saved->id))->toBeNull();
});

test('consulta al profe desde la práctica: le llega a su docente con el código, y el docente responde', function () {
    Notification::fake();
    $teacher = User::factory()->teacher()->create();
    $cohort = Cohort::create(['course_id' => $this->course->id, 'teacher_id' => $teacher->id, 'name' => 'Martes']);
    CourseSubscription::where('user_id', $this->student->id)->update(['cohort_id' => $cohort->id]);
    $saved = SavedPractice::create(['user_id' => $this->student->id, 'language' => 'python', 'title' => 'Clase de listas', 'code' => 'print(1)']);

    $this->actingAs($this->student)->get($saved->url())->assertSee('data-test="saved-practice-chat"', false);
    Livewire::actingAs($this->student)->test(PracticeChat::class, ['saved' => $saved, 'student' => $this->student])
        ->set('body', '¿Por qué no anda?')->call('send', 'print(2)', '2')->assertHasNoErrors();

    $message = PracticeMessage::sole();
    expect($message->saved_practice_id)->toBe($saved->id)->and($message->code)->toBe('print(2)');
    Notification::assertSentTo($teacher, PlatformNotification::class, fn ($n) => str_contains($n->body, 'Mi práctica «Clase de listas»') && str_contains($n->url, 'hilo=p'.$saved->id));

    $key = PracticeMessage::threadKey($saved, $this->student);
    Livewire::actingAs($teacher)->test(Messages::class, ['thread' => $key])
        ->assertSee('mi práctica')
        ->assertSee('print(2)')
        ->assertDontSee('La solución');
    Livewire::actingAs($teacher)->test(PracticeChat::class, ['saved' => $saved, 'student' => $this->student])
        ->set('body', 'Te falta el paréntesis')->call('send')->assertHasNoErrors();

    $this->actingAs($this->student)->get(route('student.saved-practices'))->assertSee('el profe te respondió');

    // Un docente que no lo tiene en sus comisiones no ve el hilo.
    $stranger = User::factory()->teacher()->create();
    expect($stranger->can('viewThread', [PracticeMessage::class, $saved, $this->student]))->toBeFalse();
    Livewire::actingAs($stranger)->test(Messages::class)->assertDontSee('Clase de listas');
});

test('sin abono vigente puede leer la conversación pero no escribir', function () {
    $saved = SavedPractice::create(['user_id' => $this->student->id, 'language' => 'python', 'title' => 'Vieja', 'code' => 'x']);
    CourseSubscription::where('user_id', $this->student->id)->update(['ends_at' => now()->subDay()]);

    expect($this->student->can('viewThread', [PracticeMessage::class, $saved, $this->student]))->toBeTrue()
        ->and($this->student->can('send', [PracticeMessage::class, $saved, $this->student]))->toBeFalse();
});
