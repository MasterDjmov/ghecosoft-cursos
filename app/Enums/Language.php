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
    case Html = 'html';
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
            self::Html => 'HTML',
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
            self::Html => 'HTML y CSS',
            self::Sql => 'SQL',
            self::Arduino => 'Arduino',
            self::Other => 'Otro',
        };
    }

    /**
     * Lo que el alumno puede ejecutar en su navegador: Python (Pyodide en un Web Worker) y HTML y CSS (una
     * vista previa en un iframe aislado, sin JavaScript ni red). El resto, solo quien corrige (D66–D69).
     */
    public function runsForStudents(): bool
    {
        return in_array($this, [self::Python, self::Html], true);
    }

    /**
     * Lo que corre con el ejecutor local en la compu de quien lo usa (D85): Java, con scripts/JavaRunner.java
     * abierto. Lo usan el docente al corregir y el alumno para probar su propio código; nunca el servidor.
     */
    public function runsOnLocalRunner(): bool
    {
        return $this === self::Java;
    }

    /** Lo que el alumno puede ejecutar: en el navegador o con el ejecutor de su compu. */
    public function studentCanRun(): bool
    {
        return $this->runsForStudents() || $this->runsOnLocalRunner();
    }

    /** Extensión del archivo en el editor. */
    public function extension(): string
    {
        return match ($this) {
            self::Python => 'py',
            self::JavaScript => 'js',
            self::TypeScript => 'ts',
            self::Arduino => 'ino',
            self::Other => 'txt',
            default => $this->value,
        };
    }
}
