<?php

namespace App\Support;

/**
 * D123: qué renglones cambian entre el código inicial de una micro-misión y su solución (la subsecuencia común más
 * larga, renglón por renglón). Se compara sin los espacios del final; la sangría sí cuenta (en Python cambia el
 * programa).
 */
class LineDiff
{
    /** Más renglones que esto no se comparan (una micro-misión tiene muchos menos). */
    private const MAX_LINES = 400;

    /**
     * @return list<array{op: 'same'|'del'|'add', a: ?int, b: ?int}> a: índice en el inicial, b: en la solución (desde 0)
     */
    public static function ops(string $from, string $to): array
    {
        $a = self::lines($from);
        $b = self::lines($to);
        $n = count($a);
        $m = count($b);
        if ($n > self::MAX_LINES || $m > self::MAX_LINES) {
            return [];
        }
        $ka = array_map(self::key(...), $a);
        $kb = array_map(self::key(...), $b);

        // Largo de la subsecuencia común desde (i, j) hasta el final.
        $lcs = array_fill(0, $n + 1, array_fill(0, $m + 1, 0));
        for ($i = $n - 1; $i >= 0; $i--) {
            for ($j = $m - 1; $j >= 0; $j--) {
                $lcs[$i][$j] = $ka[$i] === $kb[$j] ? $lcs[$i + 1][$j + 1] + 1 : max($lcs[$i + 1][$j], $lcs[$i][$j + 1]);
            }
        }

        $ops = [];
        $i = $j = 0;
        while ($i < $n || $j < $m) {
            if ($i < $n && $j < $m && $ka[$i] === $kb[$j]) {
                $ops[] = ['op' => 'same', 'a' => $i++, 'b' => $j++];
            } elseif ($j < $m && ($i >= $n || $lcs[$i][$j + 1] >= $lcs[$i + 1][$j])) {
                $ops[] = ['op' => 'add', 'a' => null, 'b' => $j++];
            } else {
                $ops[] = ['op' => 'del', 'a' => $i++, 'b' => null];
            }
        }

        return $ops;
    }

    /** @return list<string> */
    public static function lines(string $text): array
    {
        $text = rtrim(str_replace(["\r\n", "\r"], "\n", $text), "\n");

        return $text === '' ? [] : explode("\n", $text);
    }

    public static function key(string $line): string
    {
        return rtrim($line);
    }
}
