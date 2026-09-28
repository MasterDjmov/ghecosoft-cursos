<?php

namespace App\Rules;

use Closure;
use finfo;
use Illuminate\Contracts\Validation\ValidationRule;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Str;

/**
 * Que el contenido del archivo sea lo que dice su extensión, y que no sea un
 * tipo peligroso. Va junto con `extensions:` (qué nombres se aceptan):
 *
 * - Nunca se aceptan programas del servidor (php…) ni ejecutables de Windows.
 * - Imágenes, PDF, zip y documentos de Office se reconocen por su contenido:
 *   un .exe renombrado a .pdf no pasa.
 * - Código y texto (py, c, txt, md…) no pueden tener bytes binarios.
 * - Otras extensiones que el docente habilite se aceptan con el tamaño máximo.
 *
 * Además, los archivos se guardan en el disco privado con nombre UUID y se
 * bajan como adjunto con `nosniff`: nunca se ejecutan ni se muestran como página.
 */
class SafeUpload implements ValidationRule
{
    public const BLOCKED = [
        'php', 'php3', 'php4', 'php5', 'php7', 'php8', 'phtml', 'phar', 'pht', 'phps', 'htaccess', 'htpasswd', 'user.ini',
        'cgi', 'pl', 'asp', 'aspx', 'jsp', 'shtml',
        'exe', 'com', 'bat', 'cmd', 'scr', 'msi', 'dll', 'vbs', 'vbe', 'wsf', 'ps1', 'lnk', 'hta', 'cpl', 'jse',
    ];

    /** Extensión => tipos de contenido aceptados (lo que detecta el servidor). */
    private const BINARY = [
        'pdf' => ['application/pdf'],
        'png' => ['image/png'],
        'jpg' => ['image/jpeg'],
        'jpeg' => ['image/jpeg'],
        'webp' => ['image/webp'],
        'gif' => ['image/gif'],
        'zip' => ['application/zip', 'application/x-zip-compressed'],
        'rar' => ['application/x-rar', 'application/vnd.rar', 'application/x-rar-compressed'],
        '7z' => ['application/x-7z-compressed'],
        'docx' => ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/zip'],
        'xlsx' => ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/zip'],
        'pptx' => ['application/vnd.openxmlformats-officedocument.presentationml.presentation', 'application/zip'],
        'odt' => ['application/vnd.oasis.opendocument.text', 'application/zip'],
        'ods' => ['application/vnd.oasis.opendocument.spreadsheet', 'application/zip'],
        'odp' => ['application/vnd.oasis.opendocument.presentation', 'application/zip'],
    ];

    private const TEXT = [
        'txt', 'md', 'csv', 'json', 'xml', 'yml', 'yaml', 'ini', 'log',
        'py', 'c', 'h', 'cpp', 'hpp', 'cc', 'java', 'js', 'ts', 'html', 'htm', 'css', 'sql', 'ino', 'cs', 'go', 'rs', 'kt', 'rb', 'lua', 'sh',
    ];

    public function validate(string $attribute, mixed $value, Closure $fail): void
    {
        if (! $value instanceof UploadedFile || ! $value->isValid()) {
            return;
        }

        $name = Str::lower($value->getClientOriginalName());
        $extension = Str::lower($value->getClientOriginalExtension());

        if (self::isBlocked($name)) {
            $fail('Ese tipo de archivo no se acepta.');

            return;
        }

        if (isset(self::BINARY[$extension]) && ! in_array(self::detectedType($value), self::BINARY[$extension], true)) {
            $fail("El archivo no es un .{$extension} válido (su contenido es de otro tipo).");

            return;
        }

        if (in_array($extension, self::TEXT, true) && self::looksBinary($value)) {
            $fail("El archivo no es un .{$extension} de texto.");
        }
    }

    /** También frena nombres como "tarea.php.txt" o ".htaccess". */
    public static function isBlocked(string $name): bool
    {
        $parts = explode('.', Str::lower(basename($name)));
        array_shift($parts);

        return ($parts !== [] && array_intersect($parts, self::BLOCKED) !== []) || in_array(Str::lower(basename($name)), ['.htaccess', '.user.ini', '.htpasswd'], true);
    }

    /** El tipo según los primeros bytes del archivo (no el que manda el navegador). */
    private static function detectedType(UploadedFile $file): string
    {
        return (string) @(new finfo(FILEINFO_MIME_TYPE))->file($file->getRealPath());
    }

    private static function looksBinary(UploadedFile $file): bool
    {
        $handle = @fopen($file->getRealPath(), 'rb');
        if (! $handle) {
            return true;
        }
        $head = (string) fread($handle, 8192);
        fclose($handle);

        // UTF-16 (con BOM) es texto aunque tenga ceros.
        if (str_starts_with($head, "\xFF\xFE") || str_starts_with($head, "\xFE\xFF")) {
            return false;
        }

        return str_contains($head, "\0");
    }
}
