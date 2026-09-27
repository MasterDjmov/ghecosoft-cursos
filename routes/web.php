<?php

use App\Http\Controllers\Files\NodeResourceController;
use App\Http\Controllers\Files\ReceiptController;
use App\Livewire\Admin\Badges;
use App\Livewire\Admin\Courses;
use App\Livewire\Admin\Dashboard as AdminDashboard;
use App\Livewire\Admin\Glossary;
use App\Livewire\Admin\Levels;
use App\Livewire\Admin\Nodes;
use App\Livewire\Admin\Requests;
use App\Livewire\Admin\Settings;
use App\Livewire\Student\CourseDetail;
use App\Livewire\Student\CourseTree;
use App\Livewire\Student\NodeView;
use App\Livewire\Student\Worlds;
use Illuminate\Support\Facades\Route;

Route::get('/', fn () => auth()->check() ? redirect()->route('home') : redirect()->route('login'));

Route::middleware('auth')->group(function () {
    // Destino después de entrar: cada rol a su inicio.
    Route::get('inicio', fn () => auth()->user()->isAdmin()
        ? redirect()->route('admin.dashboard')
        : redirect()->route('student.worlds'))->name('home');

    Route::livewire('mundos', Worlds::class)->name('student.worlds');
    Route::livewire('cursos/{course}', CourseDetail::class)->name('student.course');
    Route::livewire('cursos/{course}/arbol', CourseTree::class)->name('student.tree');
    Route::livewire('cursos/{course}/nodos/{node}', NodeView::class)->name('student.node');

    // Descargas del disco privado: cada controlador llama a authorize().
    Route::get('archivos/recursos/{resource}', NodeResourceController::class)->name('files.resource');
    Route::get('archivos/comprobantes/{request}', ReceiptController::class)->name('files.receipt');
});

Route::middleware(['auth', 'role:admin'])->prefix('admin')->name('admin.')->group(function () {
    Route::livewire('/', AdminDashboard::class)->name('dashboard');
    Route::livewire('solicitudes', Requests::class)->name('requests');
    Route::livewire('configuracion', Settings::class)->name('settings');

    Route::livewire('cursos', Courses\Index::class)->name('courses.index');
    Route::livewire('cursos/nuevo', Courses\Form::class)->name('courses.create');
    Route::livewire('cursos/{course}/editar', Courses\Form::class)->name('courses.edit');
    Route::livewire('cursos/{course}/arbol', Courses\Tree::class)->name('courses.tree');
    Route::livewire('cursos/{course}/nodos/{node}', Nodes\Edit::class)->name('nodes.edit');

    Route::livewire('diccionario', Glossary::class)->name('glossary');
    Route::livewire('niveles', Levels::class)->name('levels');
    Route::livewire('insignias', Badges::class)->name('badges');
});

require __DIR__.'/settings.php';
