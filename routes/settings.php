<?php

use App\Livewire\Settings\ChangeTemporaryPassword;
use App\Livewire\Settings\Movements;
use App\Livewire\Settings\Privacy;
use App\Livewire\Settings\Profile;
use App\Livewire\Settings\Security;
use Illuminate\Support\Facades\Route;

// Primer ingreso con la clave provisoria del docente: único lugar al que puede ir.
Route::livewire('mi-cuenta/clave-nueva', ChangeTemporaryPassword::class)->middleware('auth')->name('password.change');

Route::middleware(['auth', 'password.changed'])->group(function () {
    Route::livewire('mi-cuenta', Profile::class)->name('profile.edit');
    Route::livewire('mi-cuenta/movimientos', Movements::class)->name('movements');
    Route::livewire('mi-cuenta/privacidad', Privacy::class)->name('privacy');

    Route::livewire('mi-cuenta/seguridad', Security::class)
        ->middleware(['password.confirm'])
        ->name('security.edit');
});

Route::get('.well-known/passkey-endpoints', function () {
    return response()->json([
        'enroll' => route('security.edit'),
        'manage' => route('security.edit'),
    ]);
})->name('well-known.passkeys');
