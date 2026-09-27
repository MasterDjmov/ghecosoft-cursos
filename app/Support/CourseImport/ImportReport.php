<?php

namespace App\Support\CourseImport;

/** Resultado de revisar o importar un curso: errores (frenan todo), avisos y qué cambió. */
class ImportReport
{
    /** @var list<string> */
    public array $errors = [];

    /** @var list<string> */
    public array $warnings = [];

    /** @var array<string, array{created: int, updated: int, unchanged: int}> */
    public array $counts = [];

    /** @var list<string> */
    public array $notes = [];

    public ?string $courseTitle = null;

    public ?string $courseUrl = null;

    public function error(string $message): void
    {
        $this->errors[] = $message;
    }

    public function warning(string $message): void
    {
        $this->warnings[] = $message;
    }

    public function note(string $message): void
    {
        $this->notes[] = $message;
    }

    /** @param  'created'|'updated'|'unchanged'  $result */
    public function count(string $entity, string $result): void
    {
        $this->counts[$entity] ??= ['created' => 0, 'updated' => 0, 'unchanged' => 0];
        $this->counts[$entity][$result]++;
    }

    public function ok(): bool
    {
        return $this->errors === [];
    }

    public function toArray(): array
    {
        return [
            'errors' => $this->errors,
            'warnings' => $this->warnings,
            'counts' => $this->counts,
            'notes' => $this->notes,
            'courseTitle' => $this->courseTitle,
            'courseUrl' => $this->courseUrl,
        ];
    }
}
