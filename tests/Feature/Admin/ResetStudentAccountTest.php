<?php

use App\Enums\CoinReason;
use App\Enums\ItemReason;
use App\Livewire\Admin\Students\Show;
use App\Models\CoinTransaction;
use App\Models\CourseSubscription;
use App\Models\Currency;
use App\Models\Item;
use App\Models\ItemMovement;
use App\Models\NodeStep;
use App\Models\NodeStepCompletion;
use App\Models\NodeUnlock;
use App\Models\Submission;
use App\Models\User;
use App\Services\Heroes;
use App\Services\Inventory;
use App\Services\Ledger;
use App\Services\PracticeSubmitter;
use App\Services\StepCompleter;
use App\Services\StudentAccounts;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;
use Livewire\Livewire;

/*
 * Reiniciar la cuenta de un alumno: queda como recién creada (mismo usuario y clave), sin cursos ni nada de lo
 * hecho, para volver a empezar de cero. Solo el administrador.
 */

test('reinicia todo lo del alumno, conserva su usuario y su clave, y no toca a los demás', function () {
    $made = makeCourse();
    $made['step'] = NodeStep::create(['node_id' => $made['root']->id, 'code' => 'R00-N01-P1', 'position' => 1, 'title' => 'Hola',
        'card_title' => 'print', 'card_body' => 'print("x")', 'xp_reward' => 10, 'gold_reward' => 15, 'expected_output' => 'Hola']);
    $student = studentWithRootOpen($made);
    $student->forceFill(['password' => 'clave-del-alumno'])->save();
    $other = studentWithRootOpen($made);
    foreach ([$student, $other] as $user) {
        app(StepCompleter::class)->complete($user, $made['step'], 'Hola');
        app(PracticeSubmitter::class)->submit($user, $made['root']->practices()->first(), 'print("hola")');
        app(Heroes::class)->create($user, $made['course'], 1, ['strength' => 6, 'dexterity' => 6, 'intelligence' => 6, 'luck' => 6]);
        app(Ledger::class)->credit($user, Currency::gold(), 5, CoinReason::ManualAdjustment);
        app(Inventory::class)->grant($user, Item::firstOrCreate(['code' => 'pocion'], ['name' => 'Poción', 'kind' => 'potion']), 2, ItemReason::ManualAdjustment);
    }
    $admin = User::factory()->admin()->create();

    Livewire::actingAs($admin)->test(Show::class, ['user' => $student])
        ->set('resetConfirm', 'mal')->call('resetAccount')->assertHasErrors('resetConfirm');
    Livewire::actingAs($admin)->test(Show::class, ['user' => $student])
        ->set('resetConfirm', $student->username)->call('resetAccount')->assertHasNoErrors();

    $student->refresh();
    expect(User::find($student->id))->not->toBeNull()
        ->and(Hash::check('clave-del-alumno', $student->password))->toBeTrue()
        ->and($student->xp_total)->toBe(0)
        ->and(CourseSubscription::where('user_id', $student->id)->exists())->toBeFalse()
        ->and(NodeUnlock::where('user_id', $student->id)->exists())->toBeFalse()
        ->and(NodeStepCompletion::where('user_id', $student->id)->exists())->toBeFalse()
        ->and(Submission::where('user_id', $student->id)->exists())->toBeFalse()
        ->and(CoinTransaction::where('user_id', $student->id)->exists())->toBeFalse()
        ->and(ItemMovement::where('user_id', $student->id)->exists())->toBeFalse()
        ->and(app(Heroes::class)->heroOf($student, $made['course']))->toBeNull();

    // El otro alumno queda igual.
    expect(CourseSubscription::where('user_id', $other->id)->exists())->toBeTrue()
        ->and(NodeStepCompletion::where('user_id', $other->id)->exists())->toBeTrue()
        ->and(Submission::where('user_id', $other->id)->exists())->toBeTrue()
        ->and(app(Heroes::class)->heroOf($other, $made['course']))->not->toBeNull()
        ->and($other->fresh()->xp_total)->toBeGreaterThan(0);

    // Puede entrar y volver a empezar: se lo habilita de nuevo.
    app(StudentAccounts::class)->enroll($student, $made['course'], $admin);
    expect(CourseSubscription::where('user_id', $student->id)->exists())->toBeTrue();
});

test('el docente no reinicia cuentas, y no se reinician docentes ni administradores', function () {
    $made = makeCourse();
    $student = studentWithRootOpen($made);
    $teacher = User::factory()->teacher()->create();
    $cohort = $made['course']->cohorts()->create(['name' => 'Tarde', 'teacher_id' => $teacher->id]);
    $student->subscriptions()->update(['cohort_id' => $cohort->id]);

    Livewire::actingAs($teacher)->test(Show::class, ['user' => $student])
        ->set('resetConfirm', $student->username)->call('resetAccount')->assertForbidden();
    expect(CourseSubscription::where('user_id', $student->id)->exists())->toBeTrue()
        ->and(fn () => app(StudentAccounts::class)->reset($teacher))->toThrow(InvalidArgumentException::class);
});

test('toda tabla con datos del alumno está en el reinicio o en lo que se conserva', function () {
    $tables = collect(DB::select("select k.TABLE_NAME as t from information_schema.KEY_COLUMN_USAGE k
        join information_schema.REFERENTIAL_CONSTRAINTS r on r.CONSTRAINT_NAME = k.CONSTRAINT_NAME and r.CONSTRAINT_SCHEMA = k.CONSTRAINT_SCHEMA
        where k.REFERENCED_TABLE_NAME = 'users' and k.TABLE_SCHEMA = DATABASE() and r.DELETE_RULE = 'CASCADE'"))->pluck('t')->unique();

    expect($tables->diff([...array_keys(StudentAccounts::RESET), ...StudentAccounts::KEEP])->values()->all())->toBe([]);
});
