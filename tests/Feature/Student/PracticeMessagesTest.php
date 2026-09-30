<?php

use App\Livewire\Admin\Messages;
use App\Livewire\PracticeChat;
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
    expect(Messages::unreadQuery()->count())->toBe(1);

    Livewire::actingAs($admin)->test(Messages::class, ['thread' => $practice->id.'-'.$student->id])
        ->assertSee($student->fullName())
        ->assertSee('¿el total va con decimales?');
    Livewire::actingAs($admin)->test(PracticeChat::class, ['practice' => $practice, 'student' => $student])
        ->set('body', 'Sí, con dos decimales.')
        ->call('send');

    expect(Messages::unreadQuery()->count())->toBe(0)
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
