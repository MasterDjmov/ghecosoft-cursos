<?php

namespace App\Support;

/**
 * El «Estado esperado» de una micro-misión de Ensamblador 8086 (D110): cómo tienen que quedar los registros, las
 * banderas y la memoria cuando el programa llega a la etiqueta `fin:`. El navegador arma su informe con el mismo
 * formato (resources/js/runners/asm8086/index.js, stateReport) y se compara como cualquier salida.
 *
 *   AX = 1234h          → «AX = 1234h»
 *   BL = 255            → «BL = FFh»
 *   ZF = 1              → «ZF = 1»
 *   [pociones] = 4      → «[pociones] = 04h»    (un byte de la variable)
 *   word [vida] = 10    → «word [vida] = 000Ah» (un word)
 */
class AsmState
{
    public const HEADER = '── Estado ──';

    private const REG16 = ['ax', 'bx', 'cx', 'dx', 'si', 'di', 'bp', 'sp', 'cs', 'ds', 'ss', 'es', 'ip'];

    private const REG8 = ['al', 'ah', 'bl', 'bh', 'cl', 'ch', 'dl', 'dh'];

    private const FLAGS = ['cf', 'pf', 'af', 'zf', 'sf', 'tf', 'if', 'df', 'of'];

    /** La línea normalizada, o null si no se entiende. */
    public static function normalizeLine(string $line): ?string
    {
        if (! preg_match('/^\s*(word\s+|byte\s+)?([^=]+?)\s*=\s*(.+?)\s*$/i', $line, $m)) {
            return null;
        }
        $width = trim(strtolower($m[1])) === 'word' ? 16 : 8;
        $name = trim($m[2]);
        $lower = strtolower($name);
        $value = self::parseValue(trim($m[3]));
        if ($value === null) {
            return null;
        }
        if (in_array($lower, self::REG16, true)) {
            return strtoupper($name).' = '.self::hex($value, 16);
        }
        if (in_array($lower, self::REG8, true)) {
            return strtoupper($name).' = '.self::hex($value, 8);
        }
        if (in_array($lower, self::FLAGS, true)) {
            return strtoupper($name).' = '.($value ? '1' : '0');
        }
        if (preg_match('/^\[\s*(.+?)\s*\]$/', $name, $mem)) {
            return ($width === 16 ? 'word ' : '')."[{$mem[1]}] = ".self::hex($value, $width);
        }

        return null;
    }

    /** Las líneas que no se entienden (para avisar al importar). */
    public static function invalidLines(string $checks): array
    {
        return array_values(array_filter(self::lines($checks), fn ($l) => self::normalizeLine($l) === null));
    }

    /** La salida esperada completa: lo que muestra la pantalla y, debajo, el informe del estado. */
    public static function expected(?string $output, string $checks): string
    {
        $report = array_filter(array_map(fn ($l) => self::normalizeLine($l), self::lines($checks)));
        $state = $report ? self::HEADER."\n".implode("\n", $report) : '';
        $output = rtrim((string) $output);

        return trim($output !== '' && $state !== '' ? "{$output}\n{$state}" : $output.$state);
    }

    private static function lines(string $checks): array
    {
        return array_values(array_filter(array_map('trim', explode("\n", $checks)), fn ($l) => $l !== ''));
    }

    private static function parseValue(string $text): ?int
    {
        if (preg_match("/^'(.)'$/", $text, $m)) {
            return ord($m[1]);
        }
        $negative = str_starts_with($text, '-');
        $t = strtolower(ltrim($text, '-'));
        $value = match (true) {
            (bool) preg_match('/^[0-9a-f]+h$/', $t) => hexdec(substr($t, 0, -1)),
            (bool) preg_match('/^[01]+b$/', $t) => bindec(substr($t, 0, -1)),
            (bool) preg_match('/^[0-9]+d?$/', $t) => (int) $t,
            default => null,
        };

        return $value === null ? null : ($negative ? -$value : $value);
    }

    private static function hex(int $value, int $bits): string
    {
        $masked = $value & ($bits === 8 ? 0xFF : 0xFFFF);

        return strtoupper(str_pad(dechex($masked), $bits / 4, '0', STR_PAD_LEFT)).'h';
    }
}
