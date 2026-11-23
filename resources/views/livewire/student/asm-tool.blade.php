<div @class(['mx-auto flex w-full max-w-5xl flex-col gap-6', 'p-4 sm:p-8' => ! $inWindow, 'p-3' => $inWindow])>
    @if ($saved)
        @include('livewire.student.partials.saved-header', ['toolLabel' => 'Gólem 8086'])
    @else
        <x-tool-header title="El tablero del Gólem 8086" :in-window="$inWindow">
            Para practicar lo que quieras fuera de las micro-misiones. Corre acá mismo, en tu navegador, con la misma sintaxis de este curso
            (MASM): lo que escribas también funciona en emu8086. Lo que escribís queda en este navegador, por si volvés, y no cuenta para el curso.
            Con <strong class="text-ink">Guardar</strong> queda en <a href="{{ route('student.saved-practices') }}" wire:navigate class="text-primary-bright hover:underline">Mis prácticas</a>.
        </x-tool-header>
    @endif

    <x-code-runner :code="$saved?->code ?? $starter" :stdin="(string) $saved?->stdin" language="asm"
        :name="$saved ? \Illuminate\Support\Str::beforeLast($saved->fileName(), '.') : 'practica'" :keep="$saved ? null : 'asm'"
        autocomplete download data-test="asm-tool" wire:key="runner-{{ $saved?->id ?? 'nueva' }}">
        <x-slot:actions>
            @include('livewire.student.partials.saved-actions')
        </x-slot:actions>
        <x-slot:footer>
            @if ($canConsult)
                @include('livewire.student.partials.saved-chat')
            @elseif (! $saved)
                @include('livewire.student.partials.saved-chat-hint')
            @endif
        </x-slot:footer>
    </x-code-runner>

    <section class="panel flex flex-col gap-2 p-5 text-sm text-ink">
        <h2 class="font-display text-base font-semibold text-white">Lo que entiende el Gólem</h2>
        <ul class="list-disc space-y-1 ps-5 text-ink-muted">
            <li>Las órdenes del 8086: <code>mov add sub inc dec mul div cmp jmp</code>, los saltos condicionales, <code>loop</code>, <code>push pop call ret</code>, las de bits y las de cadenas.</li>
            <li>Las directivas de este curso: <code>.model .stack .data .code</code>, <code>db dw dup ? equ offset byte ptr</code>, <code>proc/endp</code>, <code>macro/endm</code> y <code>end main</code>.</li>
            <li>Las interrupciones del curso: <code>INT 21h</code> (teclado y pantalla), <code>INT 10h</code> (cursor y colores) e <code>INT 16h</code>.</li>
            <li>Si usás una etiqueta <code>fin:</code>, al terminar el tablero te muestra cómo quedaron las palancas en ese momento.</li>
        </ul>
        @if ($course && ! $inWindow)
            <p class="text-xs text-ink-muted">Las explicaciones de cada orden están en el curso <a href="{{ route('student.course', $course) }}" wire:navigate class="text-primary-bright hover:underline">{{ $course->title }}</a>.</p>
        @endif
    </section>
</div>
