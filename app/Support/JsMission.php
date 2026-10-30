<?php

namespace App\Support;

/**
 * La consigna de una micro-misión de JavaScript (D115), como la arma el importador y la lee la caja
 * (resources/js/runners/js-sandbox/world.js): se guarda en `node_steps.checks` como JSON.
 *
 *   #### Página          el HTML donde corre el código (si no hay, la micro-misión es de consola)
 *   #### Eventos         uno por renglón: click #boton · escribir #nombre Ana · tecla ArrowUp · esperar 1000 · cuadros 30 …
 *   #### Estado          qué se revisa al final: #cartel · li # · .farol @class · cookie x · local x · lienzo · pedidos …
 *   #### Almacenamiento  lo que ya está guardado al empezar: local clave = valor · session clave = valor · cookie nombre = valor
 *   #### Archivos        otros archivos que el código importa (import … from './vec2.js'): el nombre en un renglón y,
 *                        debajo, su bloque ```javascript; el alumno los ve pero no los cambia
 *
 * La «Salida esperada» es la consola y, si hay Estado, el bloque «── Estado ──» debajo (lo escribe
 * scripts/js-micro/probar.mjs --fill corriendo la solución, nunca a mano).
 */
class JsMission
{
    public const EVENTS = ['click', 'doble', 'pasar', 'salir', 'mover', 'escribir', 'elegir', 'marcar', 'foco', 'enviar', 'tecla', 'apretar', 'soltar', 'esperar', 'cuadros'];

    /** @param  array<string, string|null>  $fields  los campos de la micro-misión (page, events, state, storage) */
    public static function encode(array $fields): ?string
    {
        $mission = array_filter([
            'page' => self::text($fields['page'] ?? null),
            'events' => self::text($fields['events'] ?? null),
            'checks' => self::text($fields['state'] ?? null),
            ...self::storage((string) ($fields['storage'] ?? '')),
            'files' => self::files((string) ($fields['files'] ?? '')),
        ], fn ($value) => $value !== null && $value !== [] && $value !== '');

        return $mission ? json_encode($mission, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) : null;
    }

    /** @return array{storage?: array{local?: array<string, string>, session?: array<string, string>}, cookies?: string} */
    public static function storage(string $text): array
    {
        $storage = [];
        $cookies = [];
        foreach (preg_split('/\R/u', $text) as $line) {
            if (! preg_match('/^\s*(local|session|cookie)\s+([^=\s]+)\s*=\s*(.*?)\s*$/u', $line, $m)) {
                continue;
            }
            if ($m[1] === 'cookie') {
                $cookies[] = "{$m[2]}={$m[3]}";
            } else {
                $storage[$m[1]][$m[2]] = $m[3];
            }
        }

        return array_filter(['storage' => $storage, 'cookies' => implode('; ', $cookies) ?: null]);
    }

    /** «vec2.js» y su bloque de código, uno detrás del otro → ['vec2.js' => código]. */
    public static function files(string $text): array
    {
        preg_match_all('/^\s*([\w.-]+\.js)\s*\n(`{3,}|~{3,})[\w-]*\n(.*?)\n\s*\2\s*$/msu', $text, $found, PREG_SET_ORDER);

        return collect($found)->mapWithKeys(fn ($m) => [$m[1] => $m[3]])->all();
    }

    /** Los renglones de «Eventos» y de «Almacenamiento» que no se entienden (para el informe del importador). */
    public static function problems(array $fields): array
    {
        $problems = [];
        foreach (preg_split('/\R/u', (string) ($fields['events'] ?? '')) as $line) {
            $line = trim($line);
            if ($line === '' || str_starts_with($line, '//')) {
                continue;
            }
            $verb = mb_strtolower(strtok($line, ' '));
            if (! in_array($verb, self::EVENTS, true)) {
                $problems[] = "tiene un evento que no se entiende: «{$line}» (por ejemplo: click #boton, escribir #nombre Ana, tecla ArrowUp, esperar 1000)";
            }
        }
        foreach (preg_split('/\R/u', (string) ($fields['storage'] ?? '')) as $line) {
            if (trim($line) !== '' && ! preg_match('/^\s*(local|session|cookie)\s+[^=\s]+\s*=/u', $line)) {
                $problems[] = 'tiene en «Almacenamiento» un renglón que no se entiende: «'.trim($line).'» (por ejemplo: local visitas = 1, cookie nombre = Nima)';
            }
        }

        return $problems;
    }

    private static function text(?string $value): ?string
    {
        $value = trim((string) $value);

        return $value === '' ? null : $value;
    }
}
