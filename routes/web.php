<?php

use App\Http\Controllers\CvController;
use App\Http\Controllers\Files\GuardianAuthorizationController;
use App\Http\Controllers\Files\NodeResourceController;
use App\Http\Controllers\Files\ReceiptController;
use App\Http\Controllers\Files\SubmissionFileController;
use App\Http\Controllers\JavaRunnerDownloadController;
use App\Http\Controllers\LandingController;
use App\Livewire\Admin\Authorizations;
use App\Livewire\Admin\Badges;
use App\Livewire\Admin\CohortBoard;
use App\Livewire\Admin\Courses;
use App\Livewire\Admin\Dashboard as AdminDashboard;
use App\Livewire\Admin\Glossary;
use App\Livewire\Admin\Levels;
use App\Livewire\Admin\Messages;
use App\Livewire\Admin\Nodes;
use App\Livewire\Admin\Requests;
use App\Livewire\Admin\Scenes;
use App\Livewire\Admin\Settings;
use App\Livewire\Admin\Story as StoryRoom;
use App\Livewire\Admin\Students;
use App\Livewire\Admin\Submissions;
use App\Livewire\Admin\Syllabus;
use App\Livewire\Admin\Universe;
use App\Livewire\Student\Chronicles as StudentChronicles;
use App\Livewire\Student\CourseDetail;
use App\Livewire\Student\CourseTree;
use App\Livewire\Student\Grimoire;
use App\Livewire\Student\Hero;
use App\Livewire\Student\Heroes;
use App\Livewire\Student\JavaRunner as StudentJavaRunner;
use App\Livewire\Student\Mission;
use App\Livewire\Student\NodeView;
use App\Livewire\Student\RankingBoard;
use App\Livewire\Student\Universe as StudentUniverse;
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
    Route::get('inicio', fn () => match (true) {
        auth()->user()->isAdmin() => redirect()->route('admin.dashboard'),
        auth()->user()->isTeacher() => redirect()->route('admin.submissions.index'),
        default => redirect()->route('student.worlds'),
    })->name('home');

    Route::livewire('mundos', Worlds::class)->name('student.worlds');
    // Un curso en mantenimiento (D86) no deja entrar a sus alumnos.
    Route::middleware('course.open')->group(function () {
        Route::livewire('cursos/{course}', CourseDetail::class)->name('student.course');
        Route::livewire('cursos/{course}/arbol', CourseTree::class)->name('student.tree');
        Route::livewire('cursos/{course}/nodos/{node}', NodeView::class)->name('student.node');
        Route::livewire('cursos/{course}/nodos/{node}/mision/{practice}', Mission::class)->name('student.mission');
        Route::livewire('cursos/{course}/heroe', Hero::class)->name('student.hero');
    });
    Route::livewire('ranking', RankingBoard::class)->name('student.ranking');
    Route::livewire('universo', StudentUniverse::class)->name('student.universe');
    Route::livewire('cronicas', StudentChronicles::class)->name('student.chronicles');
    // El juego (D89): los protagonistas y el grimorio.
    Route::livewire('heroes', Heroes::class)->name('student.heroes');
    Route::livewire('grimorio', Grimoire::class)->name('student.grimoire');
    Route::livewire('herramientas/ejecutor-java', StudentJavaRunner::class)->name('student.java-runner');
    Route::get('herramientas/ejecutor-java/descargar', JavaRunnerDownloadController::class)->middleware('throttle:20,1')->name('student.java-runner.download');
    Route::livewire('ranking/{course}', RankingBoard::class)->name('student.ranking.course');

    // Descargas del disco privado: cada controlador llama a authorize().
    Route::get('archivos/recursos/{resource}', NodeResourceController::class)->name('files.resource');
    Route::get('archivos/comprobantes/{request}', ReceiptController::class)->name('files.receipt');
    Route::get('archivos/entregas/{submission}', SubmissionFileController::class)->name('files.submission');
    Route::get('archivos/autorizaciones/{authorization}', GuardianAuthorizationController::class)->name('files.authorization');
});

// Solo el administrador: pagos, contenido, juego y configuración.
Route::middleware(['auth', 'password.changed', 'role:admin'])->prefix('admin')->name('admin.')->group(function () {
    Route::livewire('/', AdminDashboard::class)->name('dashboard');
    Route::livewire('solicitudes', Requests::class)->name('requests');
    Route::livewire('configuracion', Settings::class)->name('settings');

    Route::livewire('autorizaciones', Authorizations::class)->name('authorizations');
    Route::livewire('alumnos/nuevo', Students\Create::class)->name('students.create');

    Route::livewire('cursos', Courses\Index::class)->name('courses.index');
    Route::livewire('universo', Universe::class)->name('universe');
    Route::livewire('cursos/nuevo', Courses\Form::class)->name('courses.create');
    Route::livewire('cursos/importar', Courses\Import::class)->name('courses.import');
    Route::livewire('cursos/{course}/editar', Courses\Form::class)->name('courses.edit');
    Route::livewire('cursos/{course}/arbol', Courses\Tree::class)->name('courses.tree');
    Route::livewire('cursos/{course}/nodos/{node}', Nodes\Edit::class)->name('nodes.edit');

    Route::livewire('diccionario', Glossary::class)->name('glossary');
    Route::livewire('historia', StoryRoom::class)->name('story');
    Route::livewire('historia/escenas', Scenes::class)->name('scenes');
    Route::livewire('niveles', Levels::class)->name('levels');
    Route::livewire('insignias', Badges::class)->name('badges');
});

// Administrador y docentes (D72): cada pantalla muestra al docente solo lo de sus comisiones (TeacherScope).
Route::middleware(['auth', 'password.changed', 'role:admin,teacher'])->prefix('admin')->name('admin.')->group(function () {
    Route::livewire('entregas', Submissions\Index::class)->name('submissions.index');
    Route::get('entregas/siguiente', fn () => ($next = Submissions\Show::nextPending())
        ? redirect()->route('admin.submissions.show', $next)
        : redirect()->route('admin.submissions.index'))->name('submissions.next');
    Route::livewire('entregas/{submission}', Submissions\Show::class)->name('submissions.show');

    Route::livewire('mensajes', Messages::class)->name('messages');
    Route::livewire('comisiones', CohortBoard::class)->name('cohorts');
    Route::livewire('cursos/{course}/temario', Syllabus::class)->name('syllabus');
    Route::livewire('alumnos', Students\Index::class)->name('students.index');
    Route::livewire('alumnos/{user:username}', Students\Show::class)->name('students.show');
    Route::livewire('alumnos/{user:username}/arbol/{course}', Students\Tree::class)->name('students.tree');
});

require __DIR__.'/settings.php';
