<?php

namespace App\Support;

use App\Models\Course;
use App\Models\User;

/**
 * Textos de historia del diccionario (story.course_intro, story.branch_completed,
 * story.course_completed…): el título es el "singular" y el texto largo, la "historia" (lore).
 */
class Story
{
    /** @return array{title: string, text: ?string, html: string}|null null si no hay historia cargada */
    public static function get(string $key, ?Course $course = null, ?User $user = null, bool $requireText = true): ?array
    {
        $term = app(Glossary::class)->resolve($key, $course);
        $text = Narrative::fill($term['lore'], $course, $user);

        if ($requireText && blank($text)) {
            return null;
        }

        return [
            'title' => (string) Narrative::fill($term['singular'], $course, $user),
            'text' => $text,
            'html' => Markdown::render($text),
        ];
    }
}
