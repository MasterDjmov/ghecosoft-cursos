<?php

use App\Livewire\Admin\Dashboard as AdminDashboard;
use App\Livewire\Student\Worlds;
use Illuminate\Support\Facades\Route;

Route::get('/', fn () => auth()->check() ? redirect()->route('home') : redirect()->route('login'));

Route::middleware('auth')->group(function () {
    // Destino después de entrar: cada rol a su inicio.
    Route::get('inicio', fn () => auth()->user()->isAdmin()
        ? redirect()->route('admin.dashboard')
        : redirect()->route('student.worlds'))->name('home');

    Route::livewire('mundos', Worlds::class)->name('student.worlds');
});

Route::middleware(['auth', 'role:admin'])->prefix('admin')->name('admin.')->group(function () {
    Route::livewire('/', AdminDashboard::class)->name('dashboard');
});

require __DIR__.'/settings.php';
