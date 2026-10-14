<?php

namespace App\Support;

use Illuminate\Support\Str;

/**
 * El «#### Ejercicio» de una micro-misión de inglés (D106, docs/INGLES.md § 4 y § 6). Se escribe en líneas
 * simples y se guarda armado (JSON en `node_steps.checks`); lo comprueba english.js en el navegador.
 *
 *   tipo: completar             leer, escuchar, completar, ordenar, letras, escribir, dictado, responder, transformar
 *   consigna: Pintá el vitral.
 *   opciones: hello, girl, gecko escuchar: lo que se toca
 *   banco: red, blue, yellow    completar: las fichas (con «reusar: si» no se gastan)
 *   hablar: The glass is red.   el extra opcional «Decilo en voz alta» (§ 4 bis)
 *   - [#EF4444] {red}           completar y escribir: huecos {a|b}; {*nombre} y {*numero} son libres
 *   - three = 3                 escuchar: la voz dice «three» y la respuesta es «3»
 *   - My name is Teo.           ordenar: la frase (las fichas son sus palabras, mezcladas)
 *   - door | b, e               letras: la palabra y letras de más
 *   - A glass without lead…     dictado: la frase que dice la voz
 *   - Question? => patrón || otro patrón   responder y transformar
 */
class EnglishExercise
{
    /** Lo que manda el navegador al superarla: la comprobación de verdad es la de english.js. */
    public const PASSED = 'superada';

    public const TYPES = [
        'leer' => 'read',
        'escuchar' => 'listen',
        'completar' => 'fill',
        'ordenar' => 'order',
        'letras' => 'letters',
        'escribir' => 'write',
        'dictado' => 'dictation',
        'responder' => 'answer',
        'transformar' => 'transform',
    ];

    /** Huecos libres: {*nombre}, {*numero}. */
    public const FREE = ['nombre' => 'name', 'numero' => 'number'];

    /** @return array{exercise: array<string, mixed>, errors: list<string>} */
    public static function parse(string $text): array
    {
        $exercise = ['type' => null, 'prompt' => null, 'options' => [], 'bank' => [], 'reuse' => false, 'speak' => null, 'items' => []];
        $errors = [];

        foreach (preg_split('/\R/u', trim($text)) as $line) {
            $line = trim($line);
            if ($line === '') {
                continue;
            }
            if (str_starts_with($line, '- ')) {
                $exercise['items'][] = trim(substr($line, 2));

                continue;
            }
            if (! preg_match('/^([\p{L} ]+):\s*(.*)$/u', $line, $m)) {
                $errors[] = "línea sin entender: «{$line}»";

                continue;
            }
            $value = trim($m[2]);
            match (Str::lower(Str::ascii(trim($m[1])))) {
                'tipo' => $rawType = $value,
                'consigna' => $exercise['prompt'] = $value,
                'opciones' => $exercise['options'] = self::list($value),
                'banco' => $exercise['bank'] = self::list($value),
                'reusar' => $exercise['reuse'] = in_array(Str::lower(Str::ascii($value)), ['si', 'yes', 'true'], true),
                'hablar' => $exercise['speak'] = $value,
                default => $errors[] = "clave «{$m[1]}» desconocida",
            };
        }

        $exercise['type'] = isset($rawType) ? (self::TYPES[Str::lower(Str::ascii($rawType))] ?? null) : null;
        if ($exercise['type'] === null) {
            $errors[] = isset($rawType)
                ? "tipo «{$rawType}» desconocido (".implode(', ', array_keys(self::TYPES)).')'
                : 'falta «tipo:»';

            return ['exercise' => $exercise, 'errors' => $errors];
        }

        foreach ($exercise['items'] as $index => $item) {
            $exercise['items'][$index] = self::item($exercise['type'], $item, $errors);
        }
        if ($exercise['type'] !== 'read' && $exercise['items'] === []) {
            $errors[] = 'no tiene ítems (líneas que empiezan con «- »)';
        }
        if ($exercise['type'] === 'listen') {
            foreach ($exercise['items'] as $item) {
                if (! in_array($item['answer'], $exercise['options'], true)) {
                    $errors[] = "la respuesta «{$item['answer']}» no está en «opciones:»";
                }
            }
        }
        if ($exercise['type'] === 'fill') {
            foreach ($exercise['items'] as $item) {
                foreach ($item['parts'] as $part) {
                    if (isset($part['hole']) && $exercise['bank'] !== [] && ! in_array($part['hole'][0], $exercise['bank'], true)) {
                        $errors[] = "la respuesta «{$part['hole'][0]}» no está en «banco:»";
                    }
                }
            }
        }

        return ['exercise' => $exercise, 'errors' => $errors];
    }

    /** @param  list<string>  $errors */
    private static function item(string $type, string $text, array &$errors): array
    {
        switch ($type) {
            case 'listen':
                [$say, $answer] = array_pad(array_map('trim', explode('=', $text, 2)), 2, null);

                return ['say' => $say, 'answer' => $answer ?? $say];
            case 'fill':
            case 'write':
                $swatch = null;
                if (preg_match('/^\[(#[0-9a-fA-F]{3,8})\]\s*(.*)$/u', $text, $m)) {
                    [$swatch, $text] = [$m[1], $m[2]];
                }
                $parts = self::template($text);
                if (! collect($parts)->contains(fn ($p) => isset($p['hole']) || isset($p['free']))) {
                    $errors[] = "«{$text}» no tiene huecos ({respuesta})";
                }

                return ['swatch' => $swatch, 'parts' => $parts];
            case 'letters':
                [$word, $extra] = array_pad(array_map('trim', explode('|', $text, 2)), 2, '');

                return ['word' => $word, 'extra' => self::list($extra)];
            case 'answer':
            case 'transform':
                [$prompt, $answers] = array_pad(array_map('trim', explode('=>', $text, 2)), 2, null);
                if ($answers === null) {
                    $errors[] = "«{$text}» no tiene «=>» con la respuesta";
                }

                return ['prompt' => $prompt, 'answers' => array_values(array_filter(array_map('trim', explode('||', (string) $answers))))];
            case 'order':
                return ['answer' => $text];
            default:
                return ['say' => $text];
        }
    }

    /**
     * «Iris has {a} book.» → partes de texto y huecos.
     *
     * @return list<array{t?: string, hole?: list<string>, free?: string}>
     */
    public static function template(string $text): array
    {
        $parts = [];
        foreach (preg_split('/(\{[^}]*\})/u', $text, -1, PREG_SPLIT_DELIM_CAPTURE | PREG_SPLIT_NO_EMPTY) as $chunk) {
            if (preg_match('/^\{\*(\w+)\}$/u', $chunk, $m)) {
                $parts[] = ['free' => self::FREE[Str::lower(Str::ascii($m[1]))] ?? 'name'];
            } elseif (preg_match('/^\{(.*)\}$/u', $chunk, $m)) {
                $parts[] = ['hole' => array_map('trim', explode('|', $m[1]))];
            } else {
                $parts[] = ['t' => $chunk];
            }
        }

        return $parts;
    }

    /** @return list<string> */
    private static function list(string $value): array
    {
        return array_values(array_filter(array_map('trim', explode(',', $value)), fn ($v) => $v !== ''));
    }
}
