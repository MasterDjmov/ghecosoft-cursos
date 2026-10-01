<?php

namespace App\Support;

use Illuminate\Support\Str;
use Symfony\Component\Process\ExecutableFinder;
use Symfony\Component\Process\Process;
use Throwable;

/**
 * Corre código en ESTA compu, para las herramientas locales del docente: el súper test
 * (app:simulate-course) y la verificación de pruebas (app:course-tests, D73). Nunca se usa
 * con código de alumnos en el servidor: la plataforma no lo llama desde ninguna request.
 */
class LocalCodeRunner
{
    /** Ruta del ejecutable (python3, gcc, g++, java o php8.3), o null si no está instalado. */
    public readonly ?string $binary;

    private string $workDir;

    public function __construct(public readonly string $language, ?string $workDir = null, private int $timeout = 5)
    {
        // PHP: la versión del hosting (8.3) si está instalada; si no, la que haya.
        $tool = ['python' => 'python3', 'c' => 'gcc', 'cpp' => 'g++', 'java' => 'java', 'php' => 'php8.3'][$language] ?? null;
        $this->binary = $tool ? ((new ExecutableFinder)->find($tool) ?? ($language === 'php' ? (new ExecutableFinder)->find('php') : null)) : null;
        $this->workDir = $workDir ?? storage_path('app/simulacion');
        @mkdir($this->workDir, 0775, true);
    }

    public function available(): bool
    {
        return $this->binary !== null;
    }

    /**
     * En Java, el docente no puede probar acá lo que necesita la base (PostgreSQL), una ventana,
     * varios archivos o lo que no es un programa (un script SQL): eso lo compara con la solución de referencia.
     * En PHP, lo mismo con las páginas web, la base (MariaDB), los include y los argumentos de la terminal.
     */
    public function canRun(string $code): bool
    {
        return match ($this->language) {
            'java' => str_contains($code, 'static void main') && ! preg_match('/```|jdbc:|javax\.swing|java\.awt|^\s*package\s/m', $code),
            'php' => str_starts_with(ltrim($code), '<?php')
                && ! preg_match('/```|mysql:|new PDO|\$_(GET|POST|SESSION|COOKIE|FILES|SERVER)\b|\$argv|\b(require|include)(_once)?\b|session_start|header\(|<html/i', $code),
            default => true,
        };
    }

    /** @return array{0: string, 1: ?string} salida, y el error (del compilador o de la ejecución) si hubo */
    public function run(string $code, ?string $stdin): array
    {
        return $this->runMany($code, [$stdin])[0];
    }

    /**
     * El mismo programa con varias entradas: en C y C++ se compila una sola vez.
     *
     * @param  list<?string>  $inputs
     * @return list<array{0: string, 1: ?string}>
     */
    public function runMany(string $code, array $inputs): array
    {
        $dir = $this->workDir.'/run-'.Str::random(8);
        @mkdir($dir, 0775, true);

        try {
            if ($this->language === 'python') {
                file_put_contents($dir.'/main.py', $code);
                $command = [$this->binary, 'main.py'];
            } elseif ($this->language === 'php') {
                // Como lo corre el alumno, pero con todos los avisos a la vista.
                file_put_contents($dir.'/main.php', $code);
                $command = [$this->binary, '-d', 'display_errors=stderr', '-d', 'error_reporting=-1', '-d', 'date.timezone=America/Argentina/Buenos_Aires', 'main.php'];
            } elseif ($this->language === 'java') {
                // `java Main.java` compila en memoria y corre la primera clase del archivo.
                file_put_contents($dir.'/Main.java', $code);
                $command = [$this->binary, '-Dfile.encoding=UTF-8', '-Dstdout.encoding=UTF-8', 'Main.java'];
            } else {
                // Como compila el alumno en su compu: con advertencias, y la matemática enlazada.
                $source = $this->language === 'c' ? 'main.c' : 'main.cpp';
                file_put_contents($dir.'/'.$source, $code);
                $compile = new Process([$this->binary, $this->language === 'c' ? '-std=c11' : '-std=c++20', '-Wall', '-Wextra', '-o', 'programa', $source, '-lm'], $dir, null, null, 30);
                $compile->run();
                if (! $compile->isSuccessful()) {
                    $first = collect(explode("\n", $compile->getErrorOutput()))->first(fn ($line) => str_contains($line, 'error'));

                    return array_map(fn () => ['', $first ?: 'No compila.'], $inputs);
                }
                $command = ['./programa'];
            }

            return array_map(fn ($stdin) => $this->execute($command, $dir, $stdin), $inputs);
        } finally {
            exec('rm -rf '.escapeshellarg($dir));
        }
    }

    /** @return array{0: string, 1: ?string} */
    private function execute(array $command, string $dir, ?string $stdin): array
    {
        $output = '';
        $error = null;

        try {
            // La JVM tarda en arrancar y compilar: le damos más margen que a un programa nativo.
            $process = new Process($command, $dir, ['PYTHONIOENCODING' => 'utf-8', 'PYTHONDONTWRITEBYTECODE' => '1'], $stdin ?? '', $this->language === 'java' ? max(20, $this->timeout) : $this->timeout);
            $process->run();
            $output = $process->getOutput();
            // Un código de salida distinto de 0 puede ser a propósito (exit(1) cuando la consigna lo pide):
            // es un error solo si hay uno de verdad (excepción, Fatal error, traceback).
            $lines = collect(explode("\n", trim($process->getErrorOutput())));
            if ($this->language === 'java' && ! $process->isSuccessful()) {
                $error = $lines->first(fn ($line) => str_contains($line, 'error:') || str_starts_with($line, 'Exception'));
            } elseif ($this->language === 'php' && ! $process->isSuccessful()) {
                $error = $lines->first(fn ($line) => preg_match('/(Fatal|Parse) error/', $line));
            } elseif ($this->language === 'python' && ! $process->isSuccessful()) {
                $error = $lines->contains(fn ($line) => str_starts_with($line, 'Traceback')) ? $lines->last() : null;
            } elseif ($process->hasBeenSignaled() || $process->getExitCode() >= 128) {
                // En C, un código de salida distinto de 0 puede ser a propósito; una señal (violación de segmento) no.
                $error = 'El programa se cortó (código '.$process->getExitCode().': ¿un puntero o un índice fuera de lugar?).';
            }
        } catch (Throwable) {
            $error = "Tardó más de {$this->timeout} segundos (¿un bucle que no termina?).";
        }

        return [$output, $error];
    }

    /**
     * ¿Coinciden? Como en la corrección asistida (D73): se ignoran los espacios al final de cada
     * línea, las líneas vacías del principio y del final (y los \r de Windows). Los espacios al
     * principio de una línea sí cuentan: son la sangría que pide la consigna.
     */
    public static function matches(string $output, string $expected): bool
    {
        return self::normalize($output) === self::normalize($expected);
    }

    public static function normalize(string $text): string
    {
        return trim(preg_replace('/[ \t]+$/m', '', str_replace("\r\n", "\n", $text)), "\n");
    }
}
