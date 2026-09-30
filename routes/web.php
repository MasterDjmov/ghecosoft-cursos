<?php

use App\Http\Controllers\CvController;
use App\Http\Controllers\Files\GuardianAuthorizationController;
use App\Http\Controllers\Files\NodeResourceController;
use App\Http\Controllers\Files\ReceiptController;
use App\Http\Controllers\Files\SubmissionFileController;
use App\Http\Controllers\LandingController;
use App\Livewire\Admin\Authorizations;
use App\Livewire\Admin\Badges;
use App\Livewire\Admin\Courses;
use App\Livewire\Admin\Dashboard as AdminDashboard;
use App\Livewire\Admin\Glossary;
use App\Livewire\Admin\Levels;
use App\Livewire\Admin\Messages;
use App\Livewire\Admin\Nodes;
use App\Livewire\Admin\Requests;
use App\Livewire\Admin\Settings;
use App\Livewire\Admin\Students;
use App\Livewire\Admin\Submissions;
use App\Livewire\Student\CourseDetail;
use App\Livewire\Student\CourseTree;
use App\Livewire\Student\Mission;
use App\Livewire\Student\NodeView;
use App\Livewire\Student\RankingBoard;
use App\Livewire\Student\Worlds;
use Illuminate\Support\Facades\Route;

// Portada pública (a quien ya entró lo manda a su inicio).
Route::get('/', LandingController::class)->middleware('throttle:120,1')->name('landing');

// CV público (opt-in del alumno). Sin login.
Route::get('cv/{slug}', [CvController::class, 'show'])->middleware('throttle:60,1')->name('cv.show');
Route::post('cv/{slug}', [CvController::class, 'unlock'])->middleware('throttle:20,1')->name('cv.unlock');
Route::get('cv/{slug}/arbol/{course:slug}', [CvController::class, 'tree'])->middleware('throttle:60,1')->name('cv.tree');

Route::middleware(['auth', 'password.changed'])->group(function () {
    // Destino después de entrar: cada rol a su inicio.
    Route::get('inicio', fn () => auth()->user()->isAdmin()
        ? redirect()->route('admin.dashboard')
        : redirect()->route('student.worlds'))->name('home');

    Route::livewire('mundos', Worlds::class)->name('student.worlds');
    Route::livewire('cursos/{course}', CourseDetail::class)->name('student.course');
    Route::livewire('cursos/{course}/arbol', CourseTree::class)->name('student.tree');
    Route::livewire('cursos/{course}/nodos/{node}', NodeView::class)->name('student.node');
    Route::livewire('cursos/{course}/nodos/{node}/mision/{practice}', Mission::class)->name('student.mission');
    Route::livewire('ranking', RankingBoard::class)->name('student.ranking');
    Route::livewire('ranking/{course}', RankingBoard::class)->name('student.ranking.course');

    // Descargas del disco privado: cada controlador llama a authorize().
    Route::get('archivos/recursos/{resource}', NodeResourceController::class)->name('files.resource');
    Route::get('archivos/comprobantes/{request}', ReceiptController::class)->name('files.receipt');
    Route::get('archivos/entregas/{submission}', SubmissionFileController::class)->name('files.submission');
    Route::get('archivos/autorizaciones/{authorization}', GuardianAuthorizationController::class)->name('files.authorization');
});

Route::middleware(['auth', 'password.changed', 'role:admin'])->prefix('admin')->name('admin.')->group(function () {
    Route::livewire('/', AdminDashboard::class)->name('dashboard');
    Route::livewire('solicitudes', Requests::class)->name('requests');
    Route::livewire('configuracion', Settings::class)->name('settings');

    Route::livewire('entregas', Submissions\Index::class)->name('submissions.index');
    Route::get('entregas/siguiente', fn () => ($next = Submissions\Show::nextPending())
        ? redirect()->route('admin.submissions.show', $next)
        : redirect()->route('admin.submissions.index'))->name('submissions.next');
    Route::livewire('entregas/{submission}', Submissions\Show::class)->name('submissions.show');

    Route::livewire('mensajes', Messages::class)->name('messages');
    Route::livewire('autorizaciones', Authorizations::class)->name('authorizations');
    Route::livewire('alumnos', Students\Index::class)->name('students.index');
    Route::livewire('alumnos/nuevo', Students\Create::class)->name('students.create');
    Route::livewire('alumnos/{user:username}', Students\Show::class)->name('students.show');

    Route::livewire('cursos', Courses\Index::class)->name('courses.index');
    Route::livewire('cursos/nuevo', Courses\Form::class)->name('courses.create');
    Route::livewire('cursos/importar', Courses\Import::class)->name('courses.import');
    Route::livewire('cursos/{course}/editar', Courses\Form::class)->name('courses.edit');
    Route::livewire('cursos/{course}/arbol', Courses\Tree::class)->name('courses.tree');
    Route::livewire('cursos/{course}/nodos/{node}', Nodes\Edit::class)->name('nodes.edit');

    Route::livewire('diccionario', Glossary::class)->name('glossary');
    Route::livewire('niveles', Levels::class)->name('levels');
    Route::livewire('insignias', Badges::class)->name('badges');
});

require __DIR__.'/settings.php';
