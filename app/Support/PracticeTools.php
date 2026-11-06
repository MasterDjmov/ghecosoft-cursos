<?php

namespace App\Support;

use App\Enums\Language;
use App\Livewire\Student\JsTool;
use App\Models\Course;
use App\Models\User;

/**
 * Herramientas (D120): lugares para practicar lo que se quiera sin instalar nada. Cada lenguaje se habilita con el
 * abono vigente de un curso que lo usa (CoursePolicy::usePracticeTool); el staff los tiene todos. Se calcula en cada
 * request. El código corre donde siempre: en el navegador de quien lo usa (Java, con el ejecutor de su compu).
 */
class PracticeTools
{
    /**
     * Los que comparten la página de práctica, en el orden del menú. `courses`: los lenguajes de curso que lo
     * habilitan (SQL se practica en los cursos de PHP y de Java). `notes`: qué anda y qué no.
     */
    public const TOOLS = [
        'python' => [
            'label' => 'Python', 'icon' => 'code-bracket', 'courses' => ['python'],
            'notes' => [
                'Lo que lea <code>input()</code> se carga en la pestaña <strong>Entrada</strong>, una respuesta por línea.',
                'Anda la biblioteca estándar de Python. Las ventanas (<code>tkinter</code>, <code>pygame</code>) no.',
                'Si tu programa tarda más de 5 segundos, se corta: así un bucle infinito no te cuelga la página.',
            ],
            'starter' => <<<'CODE'
                # Probá lo que quieras y tocá Ejecutar (o Ctrl+Enter).
                nombre = input("¿Cómo te llamás? ")
                print(f"Hola, {nombre}")

                for numero in range(1, 4):
                    print(numero, "al cuadrado es", numero ** 2)
                CODE,
        ],
        'c' => [
            'label' => 'C', 'icon' => 'code-bracket', 'courses' => ['c'],
            'notes' => [
                'La primera vez tarda un poco, porque baja el compilador. Después queda guardado en tu navegador.',
                'Lo que lea <code>scanf</code> se carga en la pestaña <strong>Entrada</strong>, una respuesta por línea.',
                '<code>fopen</code> trabaja en una carpeta de mentira, vacía, que se borra al terminar.',
                'Es C moderno: <code>conio.h</code> y los gráficos de Turbo C no están.',
            ],
            'starter' => <<<'CODE'
                #include <stdio.h>

                int main(void) {
                    int edad;
                    printf("¿Cuántos años tenés? ");
                    scanf("%d", &edad);
                    printf("\nEl año que viene vas a tener %d.\n", edad + 1);
                    return 0;
                }
                CODE,
        ],
        'cpp' => [
            'label' => 'C++', 'icon' => 'code-bracket', 'courses' => ['cpp'],
            'notes' => [
                'La primera vez tarda un poco, porque baja el compilador. Después queda guardado en tu navegador.',
                'Lo que lea <code>cin</code> se carga en la pestaña <strong>Entrada</strong>, una respuesta por línea.',
                'Anda la biblioteca estándar (<code>vector</code>, <code>string</code>, <code>map</code>…). Las ventanas y los gráficos no.',
            ],
            'starter' => <<<'CODE'
                #include <iostream>
                #include <string>
                #include <vector>
                using namespace std;

                int main() {
                    vector<string> mochila = {"soga", "brújula", "pan"};
                    for (const string& cosa : mochila) {
                        cout << "Llevo: " << cosa << endl;
                    }
                    return 0;
                }
                CODE,
        ],
        'csharp' => [
            'label' => 'C#', 'icon' => 'code-bracket', 'courses' => ['csharp'],
            'notes' => [
                'La primera vez tarda un poco, porque baja el compilador. Después queda guardado en tu navegador.',
                'Lo que lea <code>Console.ReadLine()</code> se carga en la pestaña <strong>Entrada</strong>, una respuesta por línea.',
                'La consola, el teclado y la carpeta son de mentira: no hay internet y el programa se corta a los 5 segundos.',
            ],
            'starter' => <<<'CODE'
                using System;

                class Program
                {
                    static void Main()
                    {
                        Console.Write("¿Cómo te llamás? ");
                        string nombre = Console.ReadLine();
                        Console.WriteLine();
                        Console.WriteLine($"Hola, {nombre}");
                    }
                }
                CODE,
        ],
        'java' => [
            'label' => 'Java', 'icon' => 'code-bracket', 'courses' => ['java'], 'name' => 'Main',
            'notes' => [
                'Java es el único que no corre en el navegador: necesita el <strong>Ejecutor de Java</strong> abierto en tu compu (está en este mismo menú).',
                'Lo que lea <code>Scanner</code> se carga en la pestaña <strong>Entrada</strong>, una respuesta por línea.',
            ],
            'starter' => <<<'CODE'
                public class Main {
                    public static void main(String[] args) {
                        String[] mochila = {"soga", "brújula", "pan"};
                        for (String cosa : mochila) {
                            System.out.println("Llevo: " + cosa);
                        }
                    }
                }
                CODE,
        ],
        'php' => [
            'label' => 'PHP', 'icon' => 'code-bracket', 'courses' => ['php'],
            'notes' => [
                'Corre PHP 8.3 en tu navegador. La primera vez tarda un poco, porque lo baja.',
                'No hay internet ni conexión a MariaDB, y la carpeta está vacía en cada ejecución. Las consultas se practican en <strong>Practicar SQL</strong>.',
            ],
            'starter' => <<<'CODE'
                <?php
                $puestos = ['pescado' => 3, 'sal' => 0, 'redes' => 5];

                foreach ($puestos as $nombre => $cantidad) {
                    echo $cantidad > 0 ? "Hay $cantidad de $nombre\n" : "No queda $nombre\n";
                }
                CODE,
        ],
        'sql' => [
            'label' => 'SQL', 'icon' => 'circle-stack', 'courses' => ['php', 'java'],
            'notes' => [
                'Es SQLite: casi todo es igual a MariaDB, pero algunos tipos y funciones cambian.',
                'La base arranca vacía en cada ejecución, así que el programa tiene que crear sus tablas, como en el ejemplo.',
            ],
            'starter' => <<<'CODE'
                CREATE TABLE heroes (id INTEGER PRIMARY KEY, nombre TEXT, nivel INTEGER);
                INSERT INTO heroes (nombre, nivel) VALUES ('Mia', 3), ('Zed', 5), ('Nima', 1);

                SELECT nombre, nivel FROM heroes WHERE nivel > 1 ORDER BY nivel DESC;
                CODE,
        ],
        'html' => [
            'label' => 'HTML y CSS', 'icon' => 'window', 'courses' => ['html'],
            'notes' => [
                'La página se dibuja sola mientras escribís. Cada archivo tiene su solapa.',
                'Se dibuja en una caja cerrada, sin JavaScript ni formularios que se envíen. Las imágenes de internet no cargan.',
            ],
            'starter' => <<<'CODE'
                <!doctype html>
                <html lang="es">
                <head>
                  <meta charset="utf-8">
                  <title>Mi página</title>
                  <style>
                    body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; padding: 24px; }
                    h1 { color: #22d3ee; }
                  </style>
                </head>
                <body>
                  <h1>Hola</h1>
                  <p>Cambiá este texto y mirá cómo se dibuja.</p>
                </body>
                </html>
                CODE,
        ],
    ];

    /**
     * Las que son para todos los que iniciaron sesión, con o sin abono: son de consulta. Se abren en una ventana, se
     * pueden tener varias a la vez (`limit`) y solo se cierran con la cruz.
     *
     * @return list<array{key: string, label: string, icon: string, url: string, route: string, size: string, limit: int}>
     */
    public static function utilities(): array
    {
        return [
            ['key' => 'ascii', 'label' => 'Tabla ASCII', 'icon' => 'table-cells', 'url' => route('student.ascii'), 'route' => 'student.ascii', 'size' => '600x640', 'limit' => 3],
            ['key' => 'calculator', 'label' => 'Calculadora', 'icon' => 'calculator', 'url' => route('student.calculator'), 'route' => 'student.calculator', 'size' => '400x740', 'limit' => 3],
        ];
    }

    /** Los lenguajes de los cursos con los que este usuario puede practicar, una sola vez por request. */
    public static function allows(User $user, string $key): bool
    {
        $tool = self::TOOLS[$key] ?? null;
        if (! $tool) {
            return false;
        }

        return $user->isStaff() || Course::whereIn('language', $tool['courses'])->get()->contains(fn (Course $course) => $user->can('usePracticeTool', $course));
    }

    /**
     * Lo que va en la tarjeta de Herramientas de este usuario.
     *
     * @return list<array{key: string, label: string, icon: string, url: string, route: string, window: bool}>
     */
    public static function menu(User $user): array
    {
        $tools = [];
        foreach (self::TOOLS as $key => $tool) {
            if (self::allows($user, $key)) {
                $tools[] = ['key' => $key, 'label' => 'Practicar '.$tool['label'], 'icon' => $tool['icon'], 'url' => route('student.practice-tool', $key), 'route' => "student.practice-tool:{$key}", 'window' => true];
            }
        }
        if (JsTool::allowed($user)) {
            $tools[] = ['key' => 'js-tool', 'label' => 'La caja de la Feria', 'icon' => 'light-bulb', 'url' => route('student.js-tool'), 'route' => 'student.js-tool', 'window' => true];
        }
        if (Course::where('language', Language::Asm)->get()->contains(fn (Course $course) => $user->can('useAsmTool', $course))) {
            $tools[] = ['key' => 'asm-tool', 'label' => 'Gólem 8086', 'icon' => 'cpu-chip', 'url' => route('student.asm-tool'), 'route' => 'student.asm-tool', 'window' => true];
        }
        // El ejecutor es para instalar (D85): lo ve también quien pidió el curso y todavía no tiene el abono.
        $java = $user->isStaff() || Course::where('language', Language::Java)
            ->where(fn ($q) => $q->whereHas('subscriptions', fn ($s) => $s->where('user_id', $user->id))->orWhereHas('enrollmentRequests', fn ($r) => $r->where('user_id', $user->id)))
            ->exists();
        if ($java) {
            $tools[] = ['key' => 'java-runner', 'label' => 'Ejecutor de Java', 'icon' => 'command-line', 'url' => route('student.java-runner'), 'route' => 'student.java-runner', 'window' => false];
        }

        return $tools;
    }
}
