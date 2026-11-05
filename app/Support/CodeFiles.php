<?php

namespace App\Support;

/**
 * Un ejemplo de varios archivos (D116) escrito como en el material: un renglón con el nombre (`dado.h`, `config.php`) y
 * debajo su bloque de código. El visor lo muestra en solapas, una por archivo; lo que va entre bloques (la explicación)
 * se muestra arriba de la solapa que le sigue. Sin bloques de código, null: se ve entero como siempre.
 */
class CodeFiles
{
    /** El lenguaje del bloque → el del editor (resaltado). */
    private const EDITOR = [
        'c' => 'c', 'h' => 'c', 'cpp' => 'cpp', 'c++' => 'cpp', 'hpp' => 'cpp', 'cc' => 'cpp', 'cmake' => null,
        'java' => 'java', 'csharp' => 'csharp', 'cs' => 'csharp', 'php' => 'php', 'blade' => 'php', 'python' => 'python', 'py' => 'python',
        'html' => 'html', 'xml' => 'html', 'svg' => 'html', 'css' => 'css', 'sql' => 'sql',
        'js' => 'javascript', 'javascript' => 'javascript', 'json' => 'javascript', 'ts' => 'typescript', 'typescript' => 'typescript',
    ];

    /** Por la extensión del nombre, cuando el bloque no dice su lenguaje. */
    private const EXTENSIONS = [
        'c' => 'c', 'h' => 'c', 'cpp' => 'cpp', 'hpp' => 'cpp', 'java' => 'java', 'cs' => 'csharp', 'php' => 'php', 'py' => 'python',
        'html' => 'html', 'xml' => 'html', 'svg' => 'html', 'css' => 'css', 'sql' => 'sql', 'js' => 'javascript', 'json' => 'javascript', 'ts' => 'typescript',
    ];

    private const SHELL = ['bash', 'sh', 'shell', 'console', 'powershell', 'ps', 'cmd', 'bat'];

    /**
     * @return array{files: list<array{name: string, language: ?string, text: string, note: ?string, after: ?string}>, run: ?int}|null
     *                                                                                                                                 `run`: el único archivo del lenguaje del curso (el que se ejecuta), -1 si se ejecuta todo junto, o null si no se puede.
     */
    public static function split(string $code, string $language, string $name = 'main', string $extension = 'txt'): ?array
    {
        if (! preg_match('/^[ \t]*(```+|~~~+)/m', $code)) {
            return self::marked($code);
        }

        $lines = explode("\n", str_replace("\r\n", "\n", $code));
        $files = [];
        $prose = [];
        $fence = null;
        $body = [];
        $label = null;
        $blockLanguage = '';

        foreach ($lines as $line) {
            if ($fence !== null) {
                if (preg_match('/^[ \t]*'.preg_quote($fence, '/').'[ \t]*$/', $line)) {
                    $files[] = self::file($label, $blockLanguage, implode("\n", $body), self::note($prose), $language, $name, $extension, $files);
                    [$fence, $body, $prose, $label] = [null, [], [], null];

                    continue;
                }
                $body[] = $line;

                continue;
            }
            if (preg_match('/^[ \t]*(```+|~~~+)[ \t]*([\w+.-]*)/', $line, $m)) {
                [$fence, $blockLanguage] = [$m[1], strtolower($m[2])];
                // El nombre es el último renglón de texto antes del bloque, si es solo `nombre`.
                $last = array_key_last(array_filter($prose, fn ($l) => trim($l) !== ''));
                if ($last !== null && preg_match('/^\s*\*{0,2}`([^`\s][^`]*)`\*{0,2}\s*:?\s*$/', $prose[$last], $n)) {
                    $label = trim($n[1]);
                    $prose = array_slice($prose, 0, $last);
                }

                continue;
            }
            $prose[] = $line;
        }

        // Un bloque sin cerrar: se ve entero, para no perder nada.
        if ($fence !== null || $files === []) {
            return null;
        }
        // Lo que viene después del último bloque, debajo de su solapa.
        $files[array_key_last($files)]['after'] = self::note($prose);

        $runnable = array_keys(array_filter($files, fn ($f) => $f['language'] === (self::EDITOR[$language] ?? $language)));

        return ['files' => $files, 'run' => count($runnable) === 1 ? $runnable[0] : null];
    }

    /** El renglón (pegado al margen: uno con sangría separa partes de una función, no archivos) que separa los archivos simulados en un solo programa: `/* ---- dado.h: la tapa ---- *\/`, `// ===== Mundo.cpp =====`. */
    private const MARKER = '/^(?:\/\*|\/\/|#)[ \t]*(?:-{2,}|={3,})[ \t]*([\w.\/-]+\.(?:c|h|cpp|hpp|py|java|php|js|txt|csv|json|sql))\b.*$/';

    /**
     * Un solo programa con los archivos simulados por comentarios (D116): cada parte en su solapa, con su renglón de
     * separación adentro, y se ejecuta entero (`run` = -1). Pegadas con "\n" dan exactamente el original.
     */
    private static function marked(string $code): ?array
    {
        $lines = explode("\n", $code);
        $starts = [];
        foreach ($lines as $i => $line) {
            if (preg_match(self::MARKER, $line, $m)) {
                $starts[$i] = $m[1];
            }
        }
        if (count($starts) < 2) {
            return null;
        }

        $files = [];
        $indexes = array_keys($starts);
        foreach ($indexes as $k => $start) {
            // Lo que va antes del primer separador (los #include) queda en la primera solapa.
            $from = $k === 0 ? 0 : $start;
            $to = $indexes[$k + 1] ?? count($lines);
            $name = $starts[$start];
            $base = $name;
            for ($n = 2; in_array($name, array_column($files, 'name'), true); $n++) {
                $name = "{$base} ({$n})";
            }
            $files[] = [
                'name' => $name, 'language' => self::EXTENSIONS[strtolower(pathinfo($base, PATHINFO_EXTENSION))] ?? null,
                'text' => implode("\n", array_slice($lines, $from, $to - $from)), 'note' => null, 'after' => null,
            ];
        }

        return ['files' => $files, 'run' => -1];
    }

    private static function note(array $lines): ?string
    {
        $text = trim(implode("\n", $lines));

        return $text === '' ? null : $text;
    }

    /** @param list<array{name: string}> $previous */
    private static function file(?string $label, string $blockLanguage, string $text, ?string $note, string $language, string $name, string $extension, array $previous): array
    {
        $byName = $label !== null ? (self::EXTENSIONS[strtolower(pathinfo($label, PATHINFO_EXTENSION))] ?? null) : null;
        $editor = array_key_exists($blockLanguage, self::EDITOR) ? self::EDITOR[$blockLanguage] : $byName;
        // Sin nombre ni lenguaje: el primero es el programa; uno más abajo, lo que se escribe en la terminal.
        $shell = in_array($blockLanguage, self::SHELL, true) || ($blockLanguage === '' && $label === null && $previous !== []);
        if ($blockLanguage === '' && $label === null && $previous === []) {
            $editor = $language;
        }

        $label ??= match (true) {
            $shell => 'terminal',
            $editor === $language => "{$name}.{$extension}",
            $blockLanguage !== '' => "{$name}.{$blockLanguage}",
            default => 'texto',
        };
        // Dos archivos con el mismo nombre (dos terminales): el segundo lleva un número.
        $base = $label;
        $taken = array_column($previous, 'name');
        for ($i = 2; in_array($label, $taken, true); $i++) {
            $label = "{$base} ({$i})";
        }

        return ['name' => $label, 'language' => $editor, 'text' => $text, 'note' => $note, 'after' => null];
    }
}
