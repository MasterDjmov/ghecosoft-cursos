{{-- Una página de Mis Crónicas (D80): abierta (con quien habla o la imagen del fragmento) o bloqueada en
     silueta. La comparten el libro del alumno y la sala de guion (Admin → Historia). --}}
@if ($page['empty'] ?? false)
    <article class="flex gap-4 rounded-lg border border-dashed border-warning/40 bg-warning/5 p-4" data-test="chronicle-empty">
        <flux:icon name="pencil-square" class="mt-0.5 size-5 shrink-0 text-warning" />
        <div class="flex min-w-0 flex-col gap-1">
            <h3 class="font-medium text-white">{{ $page['title'] }}</h3>
            <p class="text-sm text-ink-muted">Este {{ term('node') }} no tiene crónica: el alumno no ve ninguna página acá. Escribila en el .md del curso (### Crónica) o colgale un fragmento.</p>
        </div>
    </article>
@elseif ($page['unlocked'])
    <article class="panel flex flex-col gap-4 p-5 {{ $page['kind'] === 'fragment' ? 'border-secondary/40' : '' }}" data-test="chronicle-page">
        @if ($page['image'])
            <img src="{{ $page['image'] }}" alt="" class="max-h-96 w-full rounded-lg object-cover">
        @endif
        <div class="flex gap-4">
            {{-- Quien habla: de cuerpo entero al costado (como una viñeta) o, si no hay, su retrato. --}}
            @if (! ($figure ?? null) && $portrait && $page['kind'] !== 'fragment')
                <img src="{{ $portrait }}" alt="" class="size-14 shrink-0 rounded-full object-cover ring-2 ring-secondary/50">
            @endif
            <div class="flex min-w-0 flex-1 flex-col gap-2">
                <h3 class="font-display text-lg font-semibold text-white">{{ $page['title'] }}</h3>
                <div class="markdown text-ink italic">{!! $page['html'] !!}</div>
            </div>
            @if ($figure ?? null)
                <img src="{{ $figure }}" alt="" loading="lazy" class="hidden h-56 w-40 shrink-0 self-end rounded-lg object-cover object-top ring-1 ring-secondary/30 sm:block" data-test="chronicle-figure">
                @if ($portrait)
                    <img src="{{ $portrait }}" alt="" class="size-12 shrink-0 rounded-full object-cover ring-2 ring-secondary/50 sm:hidden">
                @endif
            @endif
        </div>
    </article>
@else
    <article class="relative flex gap-4 overflow-hidden rounded-lg border border-dashed border-outline bg-surface-lowest/60 p-5" data-test="chronicle-locked">
        <div class="relative size-14 shrink-0">
            @if ($portrait)
                <img src="{{ $portrait }}" alt="" class="size-14 rounded-full object-cover opacity-30 blur-[2px] grayscale">
            @else
                <div class="size-14 rounded-full bg-surface-highest"></div>
            @endif
            <flux:icon name="lock-closed" class="absolute inset-0 m-auto size-5 text-ink-muted" />
        </div>
        <div class="flex min-w-0 flex-col gap-1">
            <h3 class="font-display text-lg font-semibold text-ink-muted">{{ $page['title'] }}</h3>
            <p class="text-sm text-ink-muted">{{ $page['missing'] }}</p>
            @if ($hint)
                <p class="text-sm text-warning/90 italic">{{ $hint }}</p>
            @endif
        </div>
    </article>
@endif
