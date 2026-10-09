@props(['expected' => ''])

{{-- El inspector de una micro-misión de HTML (D102): vive dentro de un x-data="codeRunner(...)" y muestra su
     informe (`output`, que arma resources/js/runners/inspector.js sin ejecutar la página), renglón por renglón,
     en verde lo que ya coincide con lo esperado y en ámbar lo que todavía no. --}}
@php($want = array_values(array_filter(array_map('trim', explode("\n", str_replace("\r\n", "\n", (string) $expected))), 'strlen')))
<div {{ $attributes->class('flex flex-col gap-1 bg-surface-lowest p-3') }} data-test="html-inspector"
    x-data="{ want: @js($want) }">
    <p class="tech-label flex items-center gap-1.5">
        <flux:icon name="magnifying-glass" variant="micro" /> Inspector
        <span class="font-normal normal-case text-ink-muted">· lee tu código sin ejecutarlo</span>
    </p>
    <ul class="flex flex-col gap-0.5 font-mono text-xs">
        <template x-for="(line, i) in (output || '').split('\n').filter((l) => l.trim() !== '')" :key="i">
            <li class="flex items-start gap-1.5" x-bind:class="line.trim() === want[i] ? 'text-success' : 'text-warning'">
                <span x-text="line.trim() === want[i] ? '✓' : '·'" aria-hidden="true"></span>
                <span class="min-w-0 break-words" x-text="line"></span>
            </li>
        </template>
    </ul>
</div>
