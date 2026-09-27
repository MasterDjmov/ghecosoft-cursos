<?php

namespace App\Enums;

enum Language: string
{
    case Python = 'python';
    case C = 'c';
    case Cpp = 'cpp';
    case Java = 'java';
    case JavaScript = 'javascript';
    case TypeScript = 'typescript';
    case Php = 'php';
    case Sql = 'sql';
    case Arduino = 'arduino';
    case Other = 'other';

    /** Abreviatura para íconos chicos. */
    public function short(): string
    {
        return match ($this) {
            self::Python => 'Py',
            self::Cpp => 'C++',
            self::Java => 'Jv',
            self::JavaScript => 'JS',
            self::TypeScript => 'TS',
            self::Php => 'PHP',
            self::Sql => 'SQL',
            self::Arduino => 'Ino',
            self::C => 'C',
            self::Other => '</>',
        };
    }

    public function label(): string
    {
        return match ($this) {
            self::Python => 'Python',
            self::C => 'C',
            self::Cpp => 'C++',
            self::Java => 'Java',
            self::JavaScript => 'JavaScript',
            self::TypeScript => 'TypeScript',
            self::Php => 'PHP',
            self::Sql => 'SQL',
            self::Arduino => 'Arduino',
            self::Other => 'Otro',
        };
    }
}
