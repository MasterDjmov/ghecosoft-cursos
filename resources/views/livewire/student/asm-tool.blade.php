<div class="mx-auto flex w-full max-w-5xl flex-col gap-6 p-4 sm:p-8">
    <header class="flex flex-col gap-1">
        <p class="tech-label">Herramientas</p>
        <h1 class="font-display text-2xl font-semibold text-white">El tablero del Gólem 8086</h1>
        <p class="text-sm text-ink-muted">
            Para practicar lo que quieras fuera de las micro-misiones. Corre acá mismo, en tu navegador, con la misma sintaxis de la cursada
            (MASM): lo que escribas también funciona en emu8086. Nada de lo que hagas acá se guarda ni cuenta para el curso.
        </p>
    </header>

    <x-code-runner :code="$starter" language="asm" name="practica" data-test="asm-tool" />

    <section class="panel flex flex-col gap-2 p-5 text-sm text-ink">
        <h2 class="font-display text-base font-semibold text-white">Lo que entiende el Gólem</h2>
        <ul class="list-disc space-y-1 ps-5 text-ink-muted">
            <li>Las órdenes del 8086: <code>mov add sub inc dec mul div cmp jmp</code>, los saltos condicionales, <code>loop</code>, <code>push pop call ret</code>, las de bits y las de cadenas.</li>
            <li>Las directivas de la cursada: <code>.model .stack .data .code</code>, <code>db dw dup ? equ offset byte ptr</code>, <code>proc/endp</code>, <code>macro/endm</code> y <code>end main</code>.</li>
            <li>Las interrupciones del curso: <code>INT 21h</code> (teclado y pantalla), <code>INT 10h</code> (cursor y colores) e <code>INT 16h</code>.</li>
            <li>Si usás una etiqueta <code>fin:</code>, al terminar el tablero te muestra cómo quedaron las palancas en ese momento.</li>
        </ul>
        @if ($course)
            <p class="text-xs text-ink-muted">Las explicaciones de cada orden están en el curso <a href="{{ route('student.course', $course) }}" wire:navigate class="text-primary-bright hover:underline">{{ $course->title }}</a>.</p>
        @endif
    </section>
</div>
