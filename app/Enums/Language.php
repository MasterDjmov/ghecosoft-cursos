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
    // D106: un curso de inglés no ejecuta nada; english.js compara las respuestas en el navegador.
    case English = 'english';
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
            self::English => 'EN',
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
            self::English => 'Inglés',
            self::Other => 'Otro',
        };
    }

    /**
     * Lo que el alumno puede ejecutar en su navegador: Python (Pyodide en un Web Worker), HTML y CSS (una
     * vista previa en un iframe aislado, sin JavaScript ni red), SQL (SQLite en WebAssembly, en un Web Worker,
     * con una base vacía en memoria en cada ejecución), C (D98: Clang en WebAssembly, el mismo del docente,
     * con una carpeta vacía en memoria), C++ (D100: el mismo Clang con su encabezado precompilado) y PHP (D105:
     * PHP 8.3 en WebAssembly, el mismo del docente, sin red y con una carpeta vacía en cada ejecución). El resto,
     * solo quien corrige (D69).
     */
    public function runsForStudents(): bool
    {
        return in_array($this, [self::Python, self::Html, self::Sql, self::C, self::Cpp, self::Php], true);
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

    /**
     * D106: un curso que se comprueba solo (inglés). Sus nodos se completan al superar las micro-misiones (no hay
     * prácticas ni monedas del curso) y no cuenta para el CV, porque lo que se comprueba en el navegador se puede
     * trampear.
     */
    public function isSelfChecked(): bool
    {
        return $this === self::English;
    }

    /** Extensión del archivo en el editor. */
    public function extension(): string
    {
        return match ($this) {
            self::Python => 'py',
            self::JavaScript => 'js',
            self::TypeScript => 'ts',
            self::Arduino => 'ino',
            self::Other, self::English => 'txt',
            default => $this->value,
        };
    }
}
