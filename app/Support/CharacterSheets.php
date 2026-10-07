<?php

namespace App\Support;

use Illuminate\Support\Collection;
use Illuminate\Support\Str;

/**
 * Las fichas de los personajes (D84) leídas de docs/historias/PERSONAJES.md, para Admin → Historia → Personajes:
 * cada «### Nombre» con sus renglones, la sección a la que pertenece y si todavía le falta la imagen. El .md
 * es la única fuente: se edita ahí y la pantalla lo muestra.
 */
class CharacterSheets
{
    /** Otro archivo de fichas (los tests usan uno propio para no depender de cómo está el .md real). */
    public static ?string $file = null;

    public static function path(): string
    {
        return self::$file ?? base_path('docs/historias/PERSONAJES.md');
    }

    /** El estilo común que va en todos los pedidos (lo que dice el .md arriba de todo). */
    public static function style(): string
    {
        return preg_match('/^\*\*Estilo común:\*\*\s*(.+)$/mu', self::text(), $m) ? trim($m[1]) : '';
    }

    /**
     * @return Collection<int, array{name: string, slug: string, section: string, missing: bool, body: string, protagonist: bool}>
     */
    public static function all(): Collection
    {
        $section = '';
        $sheets = [];
        $current = null;
        foreach (preg_split('/\R/u', self::text()) as $line) {
            if (preg_match('/^## (?:\d+\.\s*)?(.+)$/u', $line, $m)) {
                $current = null;
                $section = trim($m[1]);

                continue;
            }
            if (preg_match('/^### (.+)$/u', $line, $m)) {
                $heading = trim($m[1]);
                $missing = (bool) preg_match('/\*\(falta la imagen\)\*/u', $heading);
                $name = trim(preg_replace('/\s*\*\(.*?\)\*\s*/u', ' ', $heading));
                $sheets[] = ['name' => $name, 'slug' => Str::slug($name), 'section' => $section, 'missing' => $missing, 'body' => '',
                    'protagonist' => Str::startsWith($section, 'Los protagonistas')];
                $current = array_key_last($sheets);

                continue;
            }
            if ($current !== null && ! preg_match('/^---\s*$/', $line)) {
                $sheets[$current]['body'] .= $line."\n";
            }
        }

        return collect($sheets)
            ->map(fn (array $sheet) => [...$sheet, 'body' => trim($sheet['body'])])
            ->filter(fn (array $sheet) => $sheet['body'] !== '')
            ->values();
    }

    /** El pedido listo para pegar en Stitch: qué imágenes hacen falta, el estilo común y la ficha en texto plano. */
    public static function prompt(array $sheet): string
    {
        $images = $sheet['protagonist']
            ? 'cuerpo entero 896×1200, retrato circular y 6 variantes de aspecto'
            : 'cuerpo entero 896×1200 y retrato circular';
        $plain = trim(preg_replace(['/\*\*(.+?)\*\*/u', '/\*(.+?)\*/u', '/`(.+?)`/u', '/\[(.+?)\]\(.+?\)/u'], ['$1', '$1', '$1', '$1'], $sheet['body']));

        return "Personaje: {$sheet['name']}\nImágenes: {$images}.\nEstilo: ".self::style()."\nAspecto fijo (respetarlo siempre):\n{$plain}";
    }

    private static function text(): string
    {
        return is_file(self::path()) ? (string) file_get_contents(self::path()) : '';
    }
}
