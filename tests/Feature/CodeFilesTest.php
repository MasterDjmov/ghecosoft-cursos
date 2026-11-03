<?php

use App\Support\CodeFiles;

// D116: los ejemplos de varios archivos se ven en solapas, una por archivo.

test('un ejemplo con `nombre` y su bloque se separa en archivos, con la explicación arriba de cada uno', function () {
    $code = "Primero la tabla.\n\n`schema.sql`\n\n```sql\nCREATE TABLE t (x INT);\n```\n\n`src/Main.java`\n```java\nclass Main {}\n```\n\nCon la aplicación corriendo:\n\n```bash\ncurl localhost:8080\n```";

    $split = CodeFiles::split($code, 'java', 'ejemplo', 'java');

    expect(array_column($split['files'], 'name'))->toBe(['schema.sql', 'src/Main.java', 'terminal'])
        ->and(array_column($split['files'], 'language'))->toBe(['sql', 'java', null])
        ->and($split['files'][0]['note'])->toBe('Primero la tabla.')
        ->and($split['files'][1]['text'])->toBe('class Main {}')
        ->and($split['files'][2]['note'])->toBe('Con la aplicación corriendo:')
        // Un solo archivo de Java: ese es el que se ejecuta.
        ->and($split['run'])->toBe(1);
});

test('con varios archivos del lenguaje del curso no se ejecuta; sin bloques no se separa', function () {
    $code = "`dado.h`\n```c\nint tirar(void);\n```\n\n`main.c`\n```c\nint main(void) { return 0; }\n```";

    expect(CodeFiles::split($code, 'c')['run'])->toBeNull()
        ->and(CodeFiles::split('int main(void) { return 0; }', 'c'))->toBeNull();
});

test('los archivos simulados con comentarios se separan y vuelven exactos; con sangría no son archivos', function () {
    $code = "#include <stdio.h>\n\n/* ===== dado.h ===== */\nint tirar(void);\n\n/* ===== main.c ===== */\nint main(void)\n{\n    /* --- math.h: no es un archivo --- */\n    return tirar();\n}";

    $split = CodeFiles::split($code, 'c');

    expect(array_column($split['files'], 'name'))->toBe(['dado.h', 'main.c'])
        ->and($split['run'])->toBe(-1)
        ->and(implode("\n", array_column($split['files'], 'text')))->toBe($code)
        ->and(CodeFiles::split("int main(void)\n{\n    /* --- math.h --- */\n    /* --- ctype.h --- */\n}", 'c'))->toBeNull();
});

test('el ejemplo de varios archivos llega al visor del alumno en solapas', function () {
    $made = makeCourse(['language' => 'c']);
    $student = studentWithRootOpen($made);
    $made['root']->update(['example_code' => "`dado.h`\n```c\nint tirar(void);\n```\n\n`main.c`\n```c\nint main(void) { return 0; }\n```"]);

    $this->actingAs($student)->get(route('student.node', [$made['course'], $made['root']]))
        ->assertOk()
        ->assertSee('data-test="code-file-tabs"', false)
        ->assertSee('dado.h', false);
});
