<?php

use App\Enums\NodeType;
use App\Exceptions\TreeEditRefused;
use App\Livewire\Admin\Courses\Tree;
use App\Models\Branch;
use App\Models\Currency;
use App\Models\Node;
use App\Models\NodeUnlock;
use App\Models\Submission;
use App\Models\User;
use App\Services\TreeEditor;
use Livewire\Livewire;

beforeEach(function () {
    $this->actingAs(User::factory()->admin()->create());
    $this->editor = app(TreeEditor::class);
});

test('se crea una rama y un nodo que depende del último de la rama', function () {
    ['course' => $course, 'root' => $root] = makeCourse();

    $component = Livewire::test(Tree::class, ['course' => $course])
        ->call('openBranch')
        ->set('branchTitle', 'Fundamentos')
        ->call('saveBranch')
        ->assertHasNoErrors();

    $branch = Branch::where('course_id', $course->id)->where('title', 'Fundamentos')->firstOrFail();

    $component->call('openNode', $branch->id)
        ->assertSet('nodeParentId', $root->id)
        ->set('nodeTitle', 'Comentarios')
        ->call('saveNode')
        ->assertHasNoErrors();

    $node = Node::where('title', 'Comentarios')->firstOrFail();
    $component->assertRedirect(route('admin.nodes.edit', [$course, $node]));

    expect($node->branch_id)->toBe($branch->id)
        ->and($node->parent_id)->toBe($root->id)
        ->and($node->type)->toBe(NodeType::Topic)
        ->and($node->price_currency_id)->toBeNull();

    $component->call('openNode', $branch->id)->assertSet('nodeParentId', $node->id);
});

test('solo un extra se puede pagar con comodines', function () {
    ['course' => $course, 'root' => $root] = makeCourse();

    Livewire::test(Tree::class, ['course' => $course])
        ->call('openNode')
        ->set('nodeTitle', 'Tema caro')
        ->set('nodeType', 'topic')
        ->set('nodePaidWith', 'wildcard')
        ->set('nodeParentId', $root->id)
        ->call('saveNode');

    Livewire::test(Tree::class, ['course' => $course])
        ->call('openNode')
        ->set('nodeTitle', 'Extra de comodín')
        ->set('nodeType', 'extra')
        ->set('nodePaidWith', 'wildcard')
        ->set('nodeParentId', $root->id)
        ->call('saveNode');

    expect(Node::where('title', 'Tema caro')->first()->price_currency_id)->toBeNull()
        ->and(Node::where('title', 'Extra de comodín')->first()->price_currency_id)->toBe(Currency::wildcard()->id);
});

test('no se crea un segundo raíz ni un nodo sin requisito o con requisito de otro curso', function () {
    ['course' => $course, 'root' => $root] = makeCourse();
    ['root' => $foreignRoot] = makeCourse();

    expect(fn () => $this->editor->createNode($course, ['title' => 'Otro raíz', 'type' => 'root', 'parent_id' => $root->id]))
        ->toThrow(TreeEditRefused::class);
    expect(fn () => $this->editor->createNode($course, ['title' => 'Suelto', 'type' => 'topic']))
        ->toThrow(TreeEditRefused::class);
    expect(fn () => $this->editor->createNode($course, ['title' => 'Cruzado', 'type' => 'topic', 'parent_id' => $foreignRoot->id]))
        ->toThrow(TreeEditRefused::class);
});

test('un nodo no puede depender de sí mismo ni de un descendiente (sin ciclos)', function () {
    ['course' => $course, 'topic1' => $topic1, 'topic2' => $topic2] = makeCourse();

    expect(fn () => $this->editor->updateNode($topic1, ['parent_id' => $topic1->id]))->toThrow(TreeEditRefused::class);
    expect(fn () => $this->editor->updateNode($topic1, ['parent_id' => $topic2->id]))->toThrow(TreeEditRefused::class);
    expect($this->editor->allowedParents($course, $topic1)->pluck('id'))->not->toContain($topic1->id, $topic2->id);
});

test('el raíz no cambia de tipo, requisito ni precio desde el nodo', function () {
    ['course' => $course, 'root' => $root, 'topic1' => $topic1] = makeCourse();

    $this->editor->updateNode($root, ['title' => 'Clase 0 · Entorno', 'type' => 'topic', 'parent_id' => $topic1->id, 'price' => 99]);

    $root->refresh();
    expect($root->title)->toBe('Clase 0 · Entorno')
        ->and($root->type)->toBe(NodeType::Root)
        ->and($root->parent_id)->toBeNull()
        ->and($root->price)->toBe(10);
});

test('no se borra el raíz, un nodo con dependientes ni uno que un alumno ya abrió', function () {
    ['course' => $course, 'root' => $root, 'topic1' => $topic1, 'topic2' => $topic2] = makeCourse();

    expect(fn () => $this->editor->deleteNode($root))->toThrow(TreeEditRefused::class, 'raíz');
    expect(fn () => $this->editor->deleteNode($topic1))->toThrow(TreeEditRefused::class, 'dependen');

    NodeUnlock::create(['user_id' => User::factory()->create()->id, 'node_id' => $topic2->id, 'price_paid' => 10, 'unlocked_at' => now()]);

    expect(fn () => $this->editor->deleteNode($topic2))->toThrow(TreeEditRefused::class, 'despublicalo');
});

test('un nodo sin alumnos ni dependientes se borra con sus hojas', function () {
    ['course' => $course, 'topic2' => $topic2] = makeCourse();
    $topic2->practices()->create(['title' => 'Hoja']);

    Livewire::test(Tree::class, ['course' => $course])
        ->call('confirmDeleteNode', $topic2->id)
        ->call('deleteNode');

    expect(Node::find($topic2->id))->toBeNull();
});

test('duplicar copia el nodo con sus hojas, sin publicar', function () {
    ['course' => $course, 'topic1' => $topic1] = makeCourse();

    $copy = $this->editor->duplicateNode($topic1);

    expect($copy->title)->toBe('Tema 1 (copia)')
        ->and($copy->is_published)->toBeFalse()
        ->and($copy->parent_id)->toBe($topic1->parent_id)
        ->and($copy->practices()->pluck('title')->all())->toBe($topic1->practices()->pluck('title')->all());
});

test('arrastrar un nodo a otra rama cambia la rama y el orden', function () {
    ['course' => $course, 'topic1' => $topic1, 'topic2' => $topic2] = makeCourse();
    $a = $this->editor->createBranch($course, 'A');
    $b = $this->editor->createBranch($course, 'B');
    $topic1->update(['branch_id' => $a->id, 'position' => 1]);
    $topic2->update(['branch_id' => $a->id, 'position' => 2]);

    Livewire::test(Tree::class, ['course' => $course])
        ->call('sortNode', $topic2->id, 0, (string) $b->id)
        ->call('sortBranch', $b->id, 0);

    expect($topic2->fresh()->branch_id)->toBe($b->id)
        ->and($b->fresh()->position)->toBe(1)
        ->and($a->fresh()->position)->toBe(2);
});

test('una rama con nodos no se borra', function () {
    ['course' => $course, 'topic1' => $topic1] = makeCourse();
    $branch = $this->editor->createBranch($course, 'Fundamentos');
    $topic1->update(['branch_id' => $branch->id]);

    expect(fn () => $this->editor->deleteBranch($branch))->toThrow(TreeEditRefused::class);

    $topic1->update(['branch_id' => null]);
    $this->editor->deleteBranch($branch);
    expect(Branch::find($branch->id))->toBeNull();
});

test('una hoja con entregas no se borra', function () {
    ['topic1' => $topic1] = makeCourse();
    $practice = $topic1->practices()->first();
    Submission::create(['practice_id' => $practice->id, 'user_id' => User::factory()->create()->id, 'attempt' => 1, 'submitted_at' => now()]);

    expect(fn () => $this->editor->deletePractice($practice))->toThrow(TreeEditRefused::class);
});
