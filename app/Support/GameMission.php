<?php

namespace App\Support;

/**
 * La prueba de una micro-misión de juego (D126, fase 4: C con SDL3). La corre el «robot de Arcadia» en el navegador
 * (resources/js/runners/sdl.js, `parseGameTest`, y el modo prueba de workers/sdl-run.worker.js): juega solo, con un
 * reloj de mentira y el azar fijo, así el mismo código da siempre el mismo resultado. Se guarda en `node_steps.checks`
 * como JSON.
 *
 *   #### Eventos   uno por renglón, en orden (si no hay, el juego corre 30 cuadros):
 *                  cuadros 30 · tecla W · apretar Arriba · soltar Arriba · mouse 100 200 · clic 100 200 ·
 *                  boton A · apretar boton A · soltar boton A · palanca izquierda · cerrar
 *   #### Estado    qué se mira al final, un pedido por renglón:
 *                  ventana · pixel 320 240 · buscar #ffffff · textos · sonido · terminó
 *
 * La «Salida esperada» es lo que imprimió el juego (printf, SDL_Log) y, si hay Estado, el bloque «── Estado ──» con el
 * informe (lo escribe `node scripts/videojuegos/probar-curso.mjs cursos/videojuegos --fill` corriendo la solución).
 */
class GameMission
{
    public const EVENTS = ['cuadros', 'tecla', 'apretar', 'soltar', 'mouse', 'clic', 'boton', 'botón', 'palanca', 'cerrar'];

    public const CHECKS = ['ventana', 'pixel', 'buscar', 'textos', 'sonido', 'terminó', 'termino'];

    /** ¿Es una micro-misión de juego? (C que incluye SDL3) */
    public static function isGame(?string $code): bool
    {
        return str_contains((string) $code, '<SDL3/');
    }

    /** @param  array<string, string|null>  $fields  los campos de la micro-misión (events, state) */
    public static function encode(array $fields): string
    {
        return json_encode([
            'events' => trim((string) ($fields['events'] ?? '')),
            'checks' => self::lines((string) ($fields['state'] ?? '')),
        ], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    }

    /** Los renglones de «Eventos» y de «Estado» que no se entienden (para el informe del importador). */
    public static function problems(array $fields): array
    {
        $problems = [];
        foreach (self::lines((string) ($fields['events'] ?? '')) as $line) {
            $verb = mb_strtolower(strtok($line, ' '));
            if (! in_array($verb, self::EVENTS, true)) {
                $problems[] = "tiene un evento que no se entiende: «{$line}» (por ejemplo: cuadros 30, tecla W, apretar Arriba, clic 100 200, boton A)";
            } elseif ($verb === 'cuadros' && ! preg_match('/^cuadros\s+\d+$/iu', $line)) {
                $problems[] = "tiene «{$line}»: después de «cuadros» va cuántos (por ejemplo: cuadros 30)";
            }
        }
        foreach (self::lines((string) ($fields['state'] ?? '')) as $line) {
            $what = mb_strtolower(strtok($line, ' '));
            if (! in_array($what, self::CHECKS, true)) {
                $problems[] = "tiene en «Estado» un pedido que no se entiende: «{$line}» (por ejemplo: ventana, pixel 320 240, buscar #ffffff, textos, sonido, terminó)";
            } elseif ($what === 'pixel' && ! preg_match('/^pixel\s+\d+\s+\d+$/iu', $line)) {
                $problems[] = "tiene «{$line}»: el pixel va con su x y su y (por ejemplo: pixel 320 240)";
            } elseif ($what === 'buscar' && ! preg_match('/^buscar\s+#[0-9a-f]{6}$/iu', $line)) {
                $problems[] = "tiene «{$line}»: se busca un color como #rrggbb (por ejemplo: buscar #ffffff)";
            }
        }

        return $problems;
    }

    /** @return list<string> los renglones con algo (sin los comentarios «//») */
    private static function lines(string $text): array
    {
        return collect(preg_split('/\R/u', $text))
            ->map(fn ($line) => trim($line))
            ->filter(fn ($line) => $line !== '' && ! str_starts_with($line, '//'))
            ->values()
            ->all();
    }
}
