<?php

use App\Enums\Language;
use App\Livewire\Student\CourseTree;
use App\Livewire\Student\NodeView;
use App\Models\Course;
use App\Models\CourseSubscription;
use App\Models\NodeStep;
use App\Models\User;
use App\Services\CourseImporter;
use App\Services\NodeUnlocker;
use App\Services\StepCompleter;
use App\Services\TreeAccess;
use App\Support\AsmState;
use Livewire\Livewire;

/*
 * Ensamblador 8086 (D110): un curso que se comprueba solo, con el árbol y los nodos de siempre. Cada micro-misión
 * se aprueba por la salida y/o por el «Estado esperado» (registros, banderas y memoria al llegar a fin:), que el
 * navegador informa con el mismo formato que arma el servidor.
 */

function importAsmCourse(): Course
{
    $files = collect(glob(base_path('cursos/ensamblador/*.md')))->sort()
        ->map(fn (string $file) => ['name' => basename($file), 'content' => file_get_contents($file)])
        ->values()->all();
    $report = app(CourseImporter::class)->import($files, dryRun: false);
    expect($report->errors)->toBe([]);

    return Course::where('slug', 'ensamblador')->firstOrFail();
}

test('el estado esperado se normaliza como lo informa el navegador', function () {
    expect(AsmState::normalizeLine('AX = 5'))->toBe('AX = 0005h')
        ->and(AsmState::normalizeLine('bl = 255'))->toBe('BL = FFh')
        ->and(AsmState::normalizeLine('CX = FFh'))->toBe('CX = 00FFh')
        ->and(AsmState::normalizeLine('zf = 1'))->toBe('ZF = 1')
        ->and(AsmState::normalizeLine('[pociones] = 4'))->toBe('[pociones] = 04h')
        ->and(AsmState::normalizeLine('word [vida] = 300'))->toBe('word [vida] = 012Ch')
        ->and(AsmState::normalizeLine("AL = 'A'"))->toBe('AL = 41h')
        ->and(AsmState::normalizeLine('cualquier cosa'))->toBeNull()
        ->and(AsmState::expected("9\n", "BL = 9\n"))->toBe("9\n── Estado ──\nBL = 09h")
        ->and(AsmState::expected(null, 'AX = 7'))->toBe("── Estado ──\nAX = 0007h")
        ->and(AsmState::invalidLines("AX = 1\nXX = 2"))->toBe(['XX = 2']);
});

test('el curso de ensamblador se comprueba solo pero se ve como árbol', function () {
    expect(Language::Asm->isSelfChecked())->toBeTrue()
        ->and(Language::Asm->isLibrary())->toBeFalse()
        ->and(Language::English->isLibrary())->toBeTrue()
        ->and(Language::Asm->studentCanRun())->toBeTrue();

    $course = importAsmCourse();
    expect($course->language)->toBe(Language::Asm)
        ->and($course->nodes()->count())->toBe(27)
        ->and($course->nodes()->whereHas('practices')->exists())->toBeFalse();

    // La micro-misión de estado guarda la salida esperada con el informe debajo.
    $step = NodeStep::where('code', 'R00-N01-P4')->whereIn('node_id', $course->nodes()->pluck('id'))->firstOrFail();
    expect($step->expected_output)->toBe("── Estado ──\nAX = 1234h")
        ->and($step->checks)->toBe('AX = 1234h');
    $mixed = NodeStep::where('code', 'R01-N02-P6')->whereIn('node_id', $course->nodes()->pluck('id'))->firstOrFail();
    expect($mixed->expected_output)->toBe("9\n── Estado ──\nBL = 09h");
});

test('superar las micro-misiones de la Clase 0 completa el nodo y abre el siguiente gratis', function () {
    $course = importAsmCourse();
    $student = enrolledStudent($course);
    $root = $course->rootNode;
    app(NodeUnlocker::class)->unlock($student, $root);

    foreach ($root->steps()->orderBy('position')->get() as $step) {
        // Lo que manda el navegador: la pantalla (vacía) y el informe del estado.
        app(StepCompleter::class)->complete($student, $step, $step->expected_output);
    }

    $access = app(TreeAccess::class);
    expect($access->isCompleted($student, $root))->toBeTrue();

    $next = $course->nodes()->where('code', 'R01-N01')->firstOrFail();
    expect($access->unlockBlockers($student, $next))->toBe([]);
    app(NodeUnlocker::class)->unlock($student, $next);
    expect($access->isUnlocked($student, $next))->toBeTrue();
});

test('un estado que no coincide no aprueba la micro-misión', function () {
    $course = importAsmCourse();
    $student = enrolledStudent($course);
    app(NodeUnlocker::class)->unlock($student, $course->rootNode);
    $step = $course->rootNode->steps()->orderBy('position')->first();

    expect(fn () => app(StepCompleter::class)->complete($student, $step, "── Estado ──\nAX = 0006h"))
        ->toThrow(InvalidArgumentException::class);
});

test('el árbol y el nodo de ensamblador usan las vistas de siempre, con el tablero del Gólem', function () {
    $course = importAsmCourse();
    $student = enrolledStudent($course);
    app(NodeUnlocker::class)->unlock($student, $course->rootNode);

    Livewire::actingAs($student)->test(CourseTree::class, ['course' => $course])
        ->assertViewIs('livewire.student.course-tree');

    Livewire::actingAs($student)->test(NodeView::class, ['course' => $course, 'node' => $course->rootNode])
        ->assertSee('data-test="asm-board"', false)
        ->assertDontSee('mov dx, 3', false);
});

test('el tablero suelto del Gólem pide el abono vigente de un curso de ensamblador', function () {
    $course = importAsmCourse();
    $course->update(['is_published' => true]);

    $outsider = User::factory()->create();
    $this->actingAs($outsider)->get(route('student.asm-tool'))->assertForbidden();

    $student = enrolledStudent($course);
    $this->actingAs($student)->get(route('student.asm-tool'))
        ->assertOk()
        ->assertSee('data-test="asm-board"', false)
        ->assertSee('data-test="menu-asm-tool"', false);

    // Con el abono vencido, no.
    CourseSubscription::where('user_id', $student->id)->update(['ends_at' => now()->subDay()]);
    $this->actingAs($student)->get(route('student.asm-tool'))->assertForbidden();
});

test('en Mis Crónicas, la página de un nodo se lee recién al superar sus micro-misiones', function () {
    $course = importAsmCourse();
    $student = enrolledStudent($course);
    $root = $course->rootNode;
    app(NodeUnlocker::class)->unlock($student, $root);
    $url = route('student.chronicles', ['libro' => $course->slug]);

    // Abierto pero sin superar: la página se ve, pero su texto no sale del servidor.
    $this->actingAs($student)->get($url)->assertOk()->assertDontSee('Después, una chispa');

    foreach ($root->steps()->orderBy('position')->get() as $step) {
        app(StepCompleter::class)->complete($student, $step, $step->expected_output);
    }

    $this->actingAs($student)->get($url)->assertOk()->assertSee('Después, una chispa');
});
