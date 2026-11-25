<?php

use App\Models\User;
use App\Support\PracticeTools;

/*
 * D126, fase 1: el prototipo de juegos con SDL3 (Herramientas → Juegos con SDL3). El juego se compila y corre en el
 * navegador (Clang de C + el SDL3 de la plataforma, en su propio worker); mientras es prueba, solo lo ve el staff.
 * El juego en sí se prueba en Chrome con node scripts/videojuegos/probar.mjs.
 */

test('el staff abre el prototipo con el Pong para jugar', function () {
    $this->actingAs(User::factory()->admin()->create())
        ->get(route('student.game-tool'))
        ->assertOk()
        ->assertSee('Juegos con SDL3 (prueba)')
        ->assertSee('data-test="game-board"', false)
        ->assertSee('La Cancha de las Paletas');
});

test('un alumno no ve el prototipo ni en el menú', function () {
    $student = User::factory()->create();

    $this->actingAs($student)->get(route('student.game-tool'))->assertForbidden();
    expect(collect(PracticeTools::menu($student))->pluck('key'))->not->toContain('game-tool');
});

test('el Pong usa SDL3 como en la compu: el encabezado real y su main', function () {
    $pong = file_get_contents(resource_path('games/pong.c'));
    $header = file_get_contents(resource_path('js/runners/sdl3/SDL.h'));

    expect($pong)->toContain('#include <SDL3/SDL.h>')
        ->and($pong)->toContain('#include <SDL3/SDL_main.h>')
        ->and($pong)->toContain('int main(int argc, char *argv[])');

    // Cada función de SDL que usa el Pong existe en el SDL3 de la plataforma.
    preg_match_all('/\b(SDL_[A-Za-z]+)\s*\(/', $pong, $calls);
    foreach (array_unique($calls[1]) as $function) {
        expect($header)->toMatch("/\\b{$function}\\s*\\(/");
    }
});
