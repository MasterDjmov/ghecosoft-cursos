<?php

namespace Database\Seeders;

use App\Enums\Language;
use App\Enums\Modality;
use App\Enums\NodeType;
use App\Enums\PracticeEnvironment;
use App\Enums\SubmissionMode;
use App\Models\Badge;
use App\Models\Branch;
use App\Models\Course;
use App\Models\Currency;
use App\Models\GlossaryTerm;
use App\Models\Node;
use Illuminate\Database\Seeder;

/**
 * Curso demo de Python: raíz (clase 0) → rama Fundamentos (Comentarios →
 * Variables → Jefe) → rama Control (Condicionales → Bucles → Jefe), más un
 * extra que se paga con comodines.
 *
 * Economía: cada nodo cuesta 10 monedas del curso y sus obligatorias pagan
 * justo 10; cada optativa paga 3 comodines.
 */
class PythonDemoCourseSeeder extends Seeder
{
    private Course $course;

    public function run(): void
    {
        if (Course::where('slug', 'python')->exists()) {
            return;
        }

        $this->course = Course::create([
            'title' => 'Python desde cero',
            'slug' => 'python',
            'short_description' => 'Tu primera lengua: clara, legible y lista para todo.',
            'description' => "Aprendé Python desde el primer `print` hasta tus propios programas.\n\nCada tema es un nodo del árbol: leé la explicación, probá el ejemplo y resolvé las prácticas para ganar monedas y abrir el siguiente.",
            'language' => Language::Python,
            'is_published' => true,
            'position' => 1,
            'root_price' => 10,
            'subscription_days' => 30,
        ]);

        Currency::forCourse($this->course);
        $wildcard = Currency::wildcard();

        $this->course->cohorts()->create([
            'name' => 'Python – Clases individuales',
            'modality' => Modality::Virtual,
            'schedule_text' => 'A coordinar con el profe',
        ]);

        // Ejemplo del diccionario narrativo: en este curso la moneda se llama "escama".
        GlossaryTerm::create([
            'key' => 'coin.course',
            'course_id' => $this->course->id,
            'singular' => 'escama',
            'plural' => 'escamas',
            'gender' => 'f',
            'short_description' => 'La moneda del curso de Python: se gana aprobando prácticas obligatorias.',
        ]);

        $root = $this->node(null, null, NodeType::Root, 'Clase 0 · Preparar el entorno', 0, 10, [
            'chronicle' => "Cruzás el portal y caés de espaldas sobre el pasto del Valle. Una serpiente de escamas doradas te mira de cerca.\n\n—Antes de escribir tu primer hechizo —dice Ofidia—, necesitás tus herramientas.",
            'objectives' => "- Instalar Python y abrir el intérprete.\n- Ejecutar tu primer `print()`.\n- Leer tu primer pergamino de error (traceback).",
            'before_you_start' => 'Nada: este es el primer paso.',
            'use_cases' => 'Con Python se hacen páginas web, análisis de datos, inteligencia artificial, robots y juegos. Todo empieza con una línea como esta.',
            'common_errors' => "Si escribís `print(\"Hola\"` sin cerrar el paréntesis, aparece un **slime**:\n\n```\nSyntaxError: '(' was never closed\n```\n\nLeé la última línea del pergamino: te dice qué pasó y la flecha `^` te marca dónde.",
            'beast_key' => 'beast.slime',
            'self_check' => [
                ['question' => '¿Qué muestra print("Hola", "mundo")?', 'answer' => '`Hola mundo`: `print` separa los valores con un espacio.'],
                ['question' => '¿En qué línea del traceback está el tipo de error?', 'answer' => 'En la última.'],
            ],
            'teacher_solutions' => "Tu primer programa: print(\"Kira\")\nprint(\"La Rioja\")\n\nTiempo estimado de la clase: 60 minutos.",
            'content' => "## Bienvenida\n\nAntes de escribir tu primer programa, preparamos las herramientas.\n\n1. Instalá **Python 3** desde python.org (o verificá con `python3 --version`).\n2. Abrí una terminal y escribí `python3`: aparece el **REPL** (`>>>`).\n3. Probá `print(\"Hola, mundo\")`.",
            'example_code' => "print(\"Hola, mundo\")\nprint(\"Mi primer programa en Python\")",
            'expected_output' => "Hola, mundo\nMi primer programa en Python",
        ], [
            ['Instalá Python', 'Instalá Python 3 y verificá la versión con `python3 --version`. Marcá la práctica como completada cuando lo tengas.', true, SubmissionMode::None, 0, 5, ['environment' => PracticeEnvironment::Local]],
            ['Tu primer programa', 'Escribí un programa que muestre tu nombre y tu ciudad en dos líneas.', true, SubmissionMode::Code, 5, 10, [
                'approval_criteria' => "- Usa `print()` dos veces.\n- Muestra el nombre en la primera línea y la ciudad en la segunda.",
                'reference_solution' => "print(\"Kira\")\nprint(\"La Rioja\")",
            ]],
            ['Pedile datos al usuario', 'Pedí el nombre con `input()` y saludá: `Hola, <nombre>`.', true, SubmissionMode::Code, 5, 10, [
                'sample_input' => 'Kira',
                'expected_output' => 'Hola, Kira',
                'approval_criteria' => "- Lee el nombre con `input()`.\n- Muestra exactamente `Hola, ` seguido del nombre.",
                'reference_solution' => "nombre = input()\nprint(\"Hola,\", nombre)",
            ]],
            ['Saludo decorado', 'Mostrá el saludo dentro de un marco hecho con `*`.', false, SubmissionMode::Code, 3, 15],
        ]);

        $fundamentals = Branch::create(['course_id' => $this->course->id, 'title' => 'Fundamentos', 'position' => 1]);

        $comments = $this->node($fundamentals, $root, NodeType::Topic, 'Comentarios', 1, 10, [
            'content' => "## Comentarios\n\nUn comentario empieza con `#` y Python lo ignora: es para las personas que leen tu código.\n\n```python\n# Esto es un comentario\nprint(\"Esto sí se ejecuta\")\n```",
            'example_code' => "# Calcula el oro de la heroína\noro = 15  # oro inicial\nprint(oro)",
            'expected_output' => '15',
        ], $this->standardPractices('comentarios'));

        $variables = $this->node($fundamentals, $comments, NodeType::Topic, 'Variables', 2, 10, [
            'chronicle' => "En la posada, Bron cuenta su oro con los dedos y se equivoca cada vez.\n\n—Necesitás un lugar donde guardar ese número —le decís. Mia sonríe: sabe cómo se llama eso.",
            'objectives' => "- Guardar un valor con un nombre.\n- Cambiarlo y volver a mostrarlo.",
            'before_you_start' => 'Saber usar `print()` (Clase 0) y escribir comentarios (Comentarios).',
            'use_cases' => 'Un carrito de compras guarda el total en una variable; un juego guarda la vida del personaje.',
            'common_errors' => "Usar una variable antes de crearla despierta a un **esqueleto**:\n\n```\nNameError: name 'oro' is not defined\n```",
            'beast_key' => 'beast.skeleton',
            'self_check' => [
                ['question' => 'Si oro = 5 y después oro = oro + 1, ¿cuánto vale oro?', 'answer' => '6'],
            ],
            'content' => "## Variables\n\nUna variable es un **nombre que apunta a un valor**. El `=` no significa \"es igual\": significa \"que este nombre apunte a este valor\".",
            'example_code' => "oro = 15\noro = oro + 10\nprint(f\"Tenés {oro} monedas\")",
            'expected_output' => 'Tenés 25 monedas',
        ], $this->standardPractices('variables'));

        $slimeBadge = Badge::create(['code' => 'rey_slime', 'course_id' => $this->course->id, 'name' => 'Cazador de slimes', 'description' => 'Venciste al Rey Slime.']);
        $golemBadge = Badge::create(['code' => 'golem_bucle', 'course_id' => $this->course->id, 'name' => 'Rompe-bucles', 'description' => 'Venciste al Golem del Bucle.']);

        $boss1 = $this->node($fundamentals, $variables, NodeType::Boss, 'Jefe: el Rey Slime', 3, 10, [
            'badge_id' => $slimeBadge->id,
            'content' => "## ¡El Rey Slime!\n\nProyecto del bloque: una **ficha de personaje** que pide datos, hace cuentas y muestra un resumen prolijo.",
        ], [
            ['Ficha de personaje', 'Pedí nombre, clase, nivel y oro. Mostrá la ficha y cuánto oro le falta para 100.', true, SubmissionMode::Code, 10, 50],
        ]);

        $control = Branch::create(['course_id' => $this->course->id, 'title' => 'Control', 'position' => 2]);

        $conditionals = $this->node($control, $boss1, NodeType::Topic, 'Condicionales', 1, 10, [
            'content' => "## Condicionales\n\n`if`, `elif` y `else` eligen qué parte del código se ejecuta según una condición.",
            'example_code' => "vida = 30\nif vida > 50:\n    print(\"Estás bien\")\nelif vida > 0:\n    print(\"Cuidado\")\nelse:\n    print(\"Game over\")",
            'expected_output' => 'Cuidado',
        ], $this->standardPractices('condicionales'));

        $loops = $this->node($control, $conditionals, NodeType::Topic, 'Bucles', 2, 10, [
            'content' => "## Bucles\n\n`for` repite para cada elemento; `while` repite mientras la condición sea verdadera.",
            'example_code' => "for oleada in range(1, 4):\n    print(f\"Oleada {oleada}\")",
            'expected_output' => "Oleada 1\nOleada 2\nOleada 3",
        ], $this->standardPractices('bucles'));

        $this->node($control, $loops, NodeType::Boss, 'Jefe: el Golem del Bucle', 3, 10, [
            'badge_id' => $golemBadge->id,
            'content' => "## ¡El Golem del Bucle!\n\nProyecto del bloque: un **menú de consola** que se repite hasta que el usuario elige salir.",
        ], [
            ['Menú de la posada', 'Mostrá un menú con 3 opciones y repetilo hasta que elijan "Salir".', true, SubmissionMode::Code, 10, 50],
        ]);

        $extras = Branch::create(['course_id' => $this->course->id, 'title' => 'Extras', 'position' => 99, 'is_extra' => true]);

        $this->node($extras, $variables, NodeType::Extra, 'Extra: f-strings a fondo', 1, 3, [
            'content' => "## f-strings a fondo\n\nFormato de números, alineación y relleno: `f\"{precio:>8.2f}\"`.",
            'example_code' => "precio = 1234.5\nprint(f\"[{precio:>10.2f}]\")",
            'expected_output' => '[   1234.50]',
            'price_currency_id' => $wildcard->id,
        ], [
            ['Ticket alineado', 'Mostrá un ticket con 3 productos y sus precios alineados a la derecha.', false, SubmissionMode::Code, 3, 15],
        ]);
    }

    /**
     * @param  list<array{0: string, 1: string, 2: bool, 3: SubmissionMode, 4: int, 5: int, 6?: array<string, mixed>}>  $practices
     */
    private function node(?Branch $branch, ?Node $parent, NodeType $type, string $title, int $position, int $price, array $fields, array $practices): Node
    {
        $node = Node::create([
            'course_id' => $this->course->id,
            'branch_id' => $branch?->id,
            'parent_id' => $parent?->id,
            'type' => $type,
            'title' => $title,
            'position' => $position,
            'price' => $price,
            'example_language' => isset($fields['example_code']) ? 'python' : null,
            ...$fields,
        ]);

        foreach ($practices as $index => $practice) {
            [$practiceTitle, $instructions, $required, $mode, $coins, $xp] = $practice;
            $node->practices()->create([
                'title' => $practiceTitle,
                'instructions' => $instructions,
                'is_required' => $required,
                'submission_mode' => $mode,
                'allowed_extensions' => $mode === SubmissionMode::Code ? null : 'py,txt,zip',
                'coin_reward' => $coins,
                'xp_reward' => $xp,
                'position' => $index + 1,
                ...($practice[6] ?? []),
            ]);
        }

        return $node;
    }

    /** 3 obligatorias (3 + 3 + 4 = 10 monedas del curso) + 1 optativa (3 comodines). */
    private function standardPractices(string $topic): array
    {
        return [
            ['Misión 1', "Resolvé la primera misión de {$topic}.", true, SubmissionMode::Code, 3, 10],
            ['Misión 2', "Resolvé la segunda misión de {$topic}.", true, SubmissionMode::Code, 3, 10],
            ['Misión 3', "Resolvé la tercera misión de {$topic}.", true, SubmissionMode::Code, 4, 10],
            ['Encargo del Gremio', "Un ejercicio de {$topic} fuera del mundo de los juegos.", false, SubmissionMode::Code, 3, 15],
        ];
    }
}
