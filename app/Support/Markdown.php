<?php

namespace App\Support;

use League\CommonMark\GithubFlavoredMarkdownConverter;

/** Markdown de contenidos (nodos, consignas, descripciones) con GFM y el HTML escapado (D4). */
class Markdown
{
    public static function render(?string $text): string
    {
        if ($text === null || trim($text) === '') {
            return '';
        }

        static $converter = null;
        $converter ??= new GithubFlavoredMarkdownConverter([
            'html_input' => 'escape',
            'allow_unsafe_links' => false,
            'max_nesting_level' => 20,
        ]);

        return (string) $converter->convert($text);
    }
}
