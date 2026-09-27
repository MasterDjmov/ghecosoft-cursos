<?php

use App\Models\Course;
use App\Models\Currency;
use App\Models\User;
use App\Services\Ledger;
use App\Services\TreeAccess;

test('los seeders dejan al admin, al cliente y el curso demo listos para probar', function () {
    $this->seed();

    $admin = User::where('username', 'admin')->first();
    $student = User::where('username', 'cliente')->first();
    $course = Course::where('slug', 'python')->first();

    expect($admin->isAdmin())->toBeTrue()
        ->and($student->isStudent())->toBeTrue()
        ->and(app(Ledger::class)->balance($student, Currency::forCourse($course)))->toBe(10)
        ->and(app(TreeAccess::class)->state($student, $course->rootNode))->toBe(TreeAccess::STATE_AVAILABLE);

    $this->post(route('login.store'), ['login' => 'cliente', 'password' => 'cliente123'])->assertSessionHasNoErrors();
    $this->assertAuthenticatedAs($student);
});
