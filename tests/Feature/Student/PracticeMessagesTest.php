<?php

use App\Livewire\Admin\Messages;
use App\Livewire\PracticeChat;
use App\Models\NodeStep;
use App\Models\PracticeMessage;
use App\Models\User;
use App\Services\NodeUnlocker;
use Livewire\Livewire;

/** Consultas por práctica (D63): el alumno pregunta sin entregar y el docente responde desde su bandeja. */
function chatSetup(): array
{
    $data = makeCourse();
    $student = enrolledStudent($data['course']);
    app(NodeUnlocker::class)->unlock($student, $data['root']);
    $practice = $data['root']->practices()->first();
    $admin = User::factory()->admin()->create();

    return [...$data, 'student' => $student, 'practice' => $practice, 'admin' => $admin];
}

test('el alumno consulta, el docente lo ve en su bandeja, responde y a cada uno le llega el aviso', function () {
    ['student' => $student, 'practice' => $practice, 'admin' => $admin] = chatSetup();

    Livewire::actingAs($student)->test(PracticeChat::class, ['practice' => $practice, 'student' => $student])
        ->assertSee('Escribile al profe acá')
        ->set('body', 'Profe, ¿el total va con decimales? 🤔')
        ->call('send')
        ->assertHasNoErrors()
        ->assertSee('Profe, ¿el total va con decimales? 🤔');

    expect($admin->unreadNotifications->firstWhere('data.kind', 'message')->data)
        ->title->toBe('Consulta de '.$student->fullName())
        ->url->toContain('hilo='.$practice->id.'-'.$student->id);
    expect(Messages::unreadQuery($admin)->count())->toBe(1);

    Livewire::actingAs($admin)->test(Messages::class, ['thread' => $practice->id.'-'.$student->id])
        ->assertSee($student->fullName())
        ->assertSee('¿el total va con decimales?');
    Livewire::actingAs($admin)->test(PracticeChat::class, ['practice' => $practice, 'student' => $student])
        ->set('body', 'Sí, con dos decimales.')
        ->call('send');

    expect(Messages::unreadQuery($admin)->count())->toBe(0)
        ->and($student->unreadNotifications->firstWhere('data.kind', 'message')->data['title'])->toBe('El profe te respondió')
        ->and(PracticeMessage::thread($practice, $student)->unreadFor($student)->count())->toBe(1);

    $this->actingAs($student)->get(route('student.mission', [$practice->node->course, $practice->node, $practice]))
        ->assertSee('data-test="messages-tab"', false);
});

test('un alumno no ve ni escribe en el hilo de otro, ni en prácticas de nodos que no abrió', function () {
    ['student' => $student, 'practice' => $practice, 'topic1' => $topic1, 'course' => $course] = chatSetup();
    $other = enrolledStudent($course);

    Livewire::actingAs($other)->test(PracticeChat::class, ['practice' => $practice, 'student' => $student])->assertForbidden();
    Livewire::actingAs($student)->test(PracticeChat::class, ['practice' => $topic1->practices()->first(), 'student' => $student])->assertForbidden();
    $this->actingAs($student)->get(route('admin.messages'))->assertRedirect(route('home'));
});

test('con el abono vencido se lee la conversación pero no se escribe', function () {
    ['student' => $student, 'practice' => $practice] = chatSetup();
    PracticeMessage::create(['practice_id' => $practice->id, 'student_id' => $student->id, 'author_id' => $student->id, 'body' => 'Hola profe']);
    $this->travel(31)->days();

    Livewire::actingAs($student)->test(PracticeChat::class, ['practice' => $practice, 'student' => $student])
        ->assertSee('Hola profe')
        ->assertSee('para escribir tenés que renovarlo')
        ->set('body', 'otra')
        ->call('send')
        ->assertForbidden();
});

test('la bandeja pone primero lo que el docente no leyó', function () {
    ['student' => $student, 'practice' => $practice, 'admin' => $admin, 'course' => $course] = chatSetup();
    $other = enrolledStudent($course);
    app(NodeUnlocker::class)->unlock($other, $practice->node);

    PracticeMessage::create(['practice_id' => $practice->id, 'student_id' => $other->id, 'author_id' => $other->id, 'body' => 'Leído', 'read_at' => now()]);
    $this->travel(1)->minutes();
    PracticeMessage::create(['practice_id' => $practice->id, 'student_id' => $other->id, 'author_id' => $admin->id, 'body' => 'Respuesta más nueva']);
    PracticeMessage::create(['practice_id' => $practice->id, 'student_id' => $student->id, 'author_id' => $student->id, 'body' => 'Sin leer']);

    Livewire::actingAs($admin)->test(Messages::class)
        ->assertSeeInOrder([$student->fullName(), $other->fullName()]);
});

/*
 * D110: también se consulta desde una micro-misión (en todos los cursos). El mensaje del alumno lleva la foto de su
 * código y de su salida, y el docente los ve junto a la solución sin salir del chat.
 */
function stepChatSetup(): array
{
    $data = chatSetup();
    $step = NodeStep::create([
        'node_id' => $data['root']->id, 'code' => 'R00-N01-P1', 'position' => 1, 'title' => 'La primera palanca',
        'challenge' => 'Poné un 5 en AX.', 'starter_code' => 'print(___)', 'expected_output' => '5', 'solution' => 'print(5)  # SOLUCION-SECRETA',
    ]);

    return [...$data, 'step' => $step];
}

test('el alumno consulta desde una micro-misión con su código y el docente lo ve junto a la solución', function () {
    ['student' => $student, 'step' => $step, 'admin' => $admin] = stepChatSetup();

    Livewire::actingAs($student)->test(PracticeChat::class, ['step' => $step, 'student' => $student])
        ->assertSee('le llega el código que tenés en el editor')
        ->set('body', 'No me sale')
        ->call('send', 'print(4)', '4')
        ->assertHasNoErrors()
        ->assertSee('No me sale')
        ->assertSee('print(4)');

    $message = PracticeMessage::where('node_step_id', $step->id)->firstOrFail();
    expect($message->practice_id)->toBeNull()
        ->and($message->code)->toBe('print(4)')
        ->and($message->output)->toBe('4');

    $key = 'm'.$step->id.'-'.$student->id;
    expect($admin->unreadNotifications->firstWhere('data.kind', 'message')->data)
        ->body->toContain('Micro-misión «La primera palanca»')
        ->url->toContain('hilo='.$key);

    Livewire::actingAs($admin)->test(Messages::class, ['thread' => $key])
        ->assertSee('Poné un 5 en AX.')
        ->assertSee('print(4)')
        ->assertSee('SOLUCION-SECRETA')
        ->assertSee('data-test="message-context"', false);
    expect(Messages::unreadQuery($admin)->count())->toBe(0);

    // La respuesta del profe no guarda código, y al alumno le llega el aviso con el link a la micro-misión.
    Livewire::actingAs($admin)->test(PracticeChat::class, ['step' => $step, 'student' => $student])
        ->set('body', 'Fijate el número')->call('send', 'print(99)', '99');
    expect(PracticeMessage::where('author_id', $admin->id)->first()->code)->toBeNull()
        ->and($student->unreadNotifications->firstWhere('data.kind', 'message')->data['url'])->toContain('#micro-'.$step->id);
});

test('la consulta de una micro-misión respeta los mismos permisos que la de una práctica', function () {
    ['student' => $student, 'step' => $step, 'course' => $course] = stepChatSetup();
    $other = enrolledStudent($course);

    Livewire::actingAs($other)->test(PracticeChat::class, ['step' => $step, 'student' => $student])->assertForbidden();

    // Sin el nodo abierto (Clase 0 de prueba), no hay chat.
    $visitor = User::factory()->create();
    Livewire::actingAs($visitor)->test(PracticeChat::class, ['step' => $step, 'student' => $visitor])->assertForbidden();

    // Un docente solo ve las consultas de los alumnos de sus comisiones.
    $teacher = User::factory()->create(['role' => 'teacher']);
    Livewire::actingAs($student)->test(PracticeChat::class, ['step' => $step, 'student' => $student])->set('body', 'Hola')->call('send');
    expect(Messages::unreadQuery($teacher)->count())->toBe(0);
});
