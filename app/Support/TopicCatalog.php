<?php

namespace App\Support;

/**
 * El catálogo de temas del universo (cursos/temas.md, D70): familias con su alcance
 * (lenguaje | compartido) y sus temas en orden, de lo básico a lo avanzado.
 */
class TopicCatalog
{
    public const SCOPE_LANGUAGE = 'lenguaje';

    public const SCOPE_SHARED = 'compartido';

    /** @var array<string, array{families: array, topics: array}> */
    private static array $loaded = [];

    public static function path(): string
    {
        return base_path('cursos/temas.md');
    }

    /**
     * @return array<string, array{key: string, title: string, scope: string, topics: list<string>}>
     */
    public static function families(): array
    {
        return self::load()['families'];
    }

    /**
     * @return array<string, array{key: string, family: string, title: string, description: string, order: int}>
     */
    public static function topics(): array
    {
        return self::load()['topics'];
    }

    public static function has(string $key): bool
    {
        return isset(self::topics()[$key]);
    }

    /** @return array{families: array, topics: array} */
    private static function load(): array
    {
        $path = self::path();
        $stamp = is_file($path) ? $path.'@'.filemtime($path) : 'none';

        return self::$loaded[$stamp] ??= self::parse(is_file($path) ? (string) file_get_contents($path) : '');
    }

    /** @return array{families: array, topics: array} */
    public static function parse(string $markdown): array
    {
        $families = [];
        $topics = [];
        $family = null;
        $order = 0;

        foreach (preg_split('/\R/', $markdown) as $line) {
            if (preg_match('/^##\s+([a-z0-9-]+)\s+·\s+(.+)$/u', $line, $m)) {
                $family = $m[1];
                $families[$family] = ['key' => $family, 'title' => trim($m[2]), 'scope' => self::SCOPE_LANGUAGE, 'topics' => []];
            } elseif ($family && preg_match('/^alcance:\s*(\w+)/u', $line, $m)) {
                $families[$family]['scope'] = $m[1] === self::SCOPE_SHARED ? self::SCOPE_SHARED : self::SCOPE_LANGUAGE;
            } elseif ($family && preg_match('/^-\s+([a-z0-9-]+\.[a-z0-9-]+)\s+·\s+([^·]+?)(?:\s+·\s+(.+))?$/u', $line, $m)) {
                $topics[$m[1]] = ['key' => $m[1], 'family' => $family, 'title' => trim($m[2]), 'description' => trim($m[3] ?? ''), 'order' => $order++];
                $families[$family]['topics'][] = $m[1];
            }
        }

        return ['families' => $families, 'topics' => $topics];
    }
}
