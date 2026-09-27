<?php

use App\Enums\CoinReason;
use App\Enums\SubmissionStatus;
use App\Livewire\Student\CourseTree;
use App\Livewire\Student\NodeView;
use App\Models\Currency;
use App\Models\Submission;
use App\Models\User;
use App\Services\Ledger;
use App\Services\NodeUnlocker;
use App\Support\TreeGraph;
use Livewire\Livewire;

function studentWithRootOpen(array $course): User
{
    $student = enrolledStudent($course['course']);
    app(NodeUnlocker::class)->unlock($student, $course['root']);

    return $student;
}

test('sin el raíz abierto, el árbol manda a la ficha del curso', function () {
    ['course' => $course] = makeCourse();
    $student = enrolledStudent($course);

    $this->actingAs($student)->get(route('student.tree', $course))->assertRedirect(route('student.course', $course));
});

test('el árbol muestra estados y oculta las consignas de lo que no abrió', function () {
    $data = makeCourse();
    ['course' => $course, 'topic1' => $topic1, 'topic2' => $topic2] = $data;
    $topic2->update(['is_published' => false]);
    $student = studentWithRootOpen($data);

    $graph = TreeGraph::forStudent($course, $student);
    $nodes = collect($graph['nodes'])->keyBy('id');

    expect($nodes[$data['root']->id]['state'])->toBe('unlocked')
        ->and($nodes[$topic1->id]['state'])->toBe('locked')
        ->and($nodes[$topic1->id]['url'])->toBeNull()
        ->and($nodes->has($topic2->id))->toBeFalse()
        ->and(collect($graph['practices'])->where('node_id', $topic1->id)->pluck('title')->unique()->all())->toBe(['?']);

    $this->actingAs($student)->get(route('student.tree', $course))->assertOk()->assertSee('Tema 1')->assertDontSee('Misión 1');
});

test('abrir un nodo desde el árbol cobra el precio y lleva al nodo', function () {
    $data = makeCourse();
    ['course' => $course, 'root' => $root, 'topic1' => $topic1] = $data;
    $student = studentWithRootOpen($data);
    approveRequiredPractices($student, $root);
    app(Ledger::class)->credit($student, Currency::forCourse($course), 10, CoinReason::ManualAdjustment, note: 'test');

    Livewire::actingAs($student)->test(CourseTree::class, ['course' => $course])
        ->call('selectNode', $topic1->id)
        ->assertSee('Abrir por 10 monedas')
        ->call('unlock', $topic1->id)
        ->assertRedirect(route('student.node', [$course, $topic1]));

    expect($student->nodeUnlocks()->where('node_id', $topic1->id)->exists())->toBeTrue();
});

test('sin cumplir los requisitos no se abre y se explica por qué', function () {
    $data = makeCourse();
    ['course' => $course, 'topic1' => $topic1] = $data;
    $student = studentWithRootOpen($data);

    Livewire::actingAs($student)->test(CourseTree::class, ['course' => $course])
        ->call('selectNode', $topic1->id)
        ->assertSee('Aprobá las prácticas obligatorias de «Clase 0»')
        ->call('unlock', $topic1->id)
        ->assertNoRedirect();

    expect($student->nodeUnlocks()->where('node_id', $topic1->id)->exists())->toBeFalse();
});

test('un nodo sin publicar y sin abrir no se puede tocar', function () {
    $data = makeCourse();
    $data['topic1']->update(['is_published' => false]);
    $student = studentWithRootOpen($data);

    Livewire::actingAs($student)->test(CourseTree::class, ['course' => $data['course']])
        ->call('selectNode', $data['topic1']->id)
        ->assertNotFound();
});

test('el alumno ve solo los nodos que abrió', function () {
    $data = makeCourse();
    ['course' => $course, 'root' => $root, 'topic1' => $topic1] = $data;
    $root->update(['content' => '## Bienvenida al curso', 'example_code' => 'print("hola")']);
    $student = studentWithRootOpen($data);

    $this->actingAs($student)->get(route('student.node', [$course, $root]))
        ->assertOk()->assertSee('Bienvenida al curso')->assertSee('Ejecutar')->assertSee('Primer programa');
    $this->actingAs($student)->get(route('student.node', [$course, $topic1]))->assertForbidden();
    $this->actingAs(User::factory()->create())->get(route('student.node', [$course, $root]))->assertForbidden();
});

test('un nodo pedido con otro curso da 404', function () {
    $data = makeCourse();
    $other = makeCourse();
    $student = studentWithRootOpen($data);

    $this->actingAs($student)->get(route('student.node', [$other['course'], $data['root']]))->assertNotFound();
});

test('con el abono vencido sigue viendo lo que abrió', function () {
    $data = makeCourse();
    $student = studentWithRootOpen($data);
    $this->travel(40)->days();

    $this->actingAs($student)->get(route('student.node', [$data['course'], $data['root']]))->assertOk()->assertSee('no está vigente');
    $this->actingAs($student)->get(route('student.tree', $data['course']))->assertOk();
});

test('se reconoce el video de YouTube para embeberlo', function (string $url, ?string $id) {
    expect(NodeView::youtubeId($url))->toBe($id);
})->with([
    ['https://www.youtube.com/watch?v=dQw4w9WgXcQ', 'dQw4w9WgXcQ'],
    ['https://youtu.be/dQw4w9WgXcQ?t=10', 'dQw4w9WgXcQ'],
    ['https://vimeo.com/123', null],
]);

test('el nodo resume el progreso de las hojas y abre la primera pendiente', function () {
    $data = makeCourse();
    ['course' => $course, 'root' => $root] = $data;
    $root->practices()->create(['title' => 'Segundo programa', 'is_required' => true, 'position' => 1]);
    $root->practices()->create(['title' => 'Reto opcional', 'is_required' => false, 'position' => 2]);
    $student = studentWithRootOpen($data);
    $first = $root->practices()->where('title', 'Primer programa')->first();
    Submission::create(['practice_id' => $first->id, 'user_id' => $student->id, 'attempt' => 1, 'submitted_at' => now()])
        ->forceFill(['status' => SubmissionStatus::Approved, 'reviewed_at' => now()])->save();
    $second = $root->practices()->where('title', 'Segundo programa')->first();

    $this->actingAs($student)->get(route('student.node', [$course, $root]))
        ->assertOk()
        ->assertSeeInOrder(['1 de 3', '1 obligatoria pendiente'])
        ->assertSee('data-first-pending="'.$second->id.'"', false)
        ->assertSeeInOrder(['Segundo programa', 'Desafíos extra', 'Reto opcional'])
        ->assertSee('practica_2.py');
});
