{{-- Crónicas en Inglés (D106): la biblioteca de episodios. El alumno elige qué leer o practicar; cada
     episodio muestra su avance. Se abren sin monedas: el primero con el abono y el resto al terminar el anterior. --}}
@php
    use App\Services\TreeAccess;

    $done = $episodes->where('state', TreeAccess::STATE_COMPLETED)->count();
@endphp

<div class="mx-auto flex w-full max-w-6xl flex-col gap-6 p-4 sm:p-8" data-test="library">
    <header class="relative overflow-hidden rounded-2xl border border-outline">
        @if ($scene)
            <img src="{{ $scene }}" alt="" class="absolute inset-0 size-full object-cover opacity-40">
        @endif
        <div class="relative flex flex-col gap-4 bg-gradient-to-r from-surface via-surface/90 to-surface/40 p-6 sm:flex-row sm:items-center">
            <x-course-logo :course="$course" size="size-16" />
            <div class="flex min-w-0 flex-1 flex-col gap-1">
                <p class="tech-label">Biblioteca · {{ $course->title }}</p>
                <h1 class="font-display text-2xl font-semibold text-white">Elegí qué leer o practicar</h1>
                <p class="text-sm text-ink-muted"><span data-test="library-progress">{{ $done }} de {{ $episodes->count() }}</span> episodios terminados. Cada episodio se lee en inglés, se escucha y se practica: se comprueba solo.</p>
            </div>
            @if ($paidUntil)
                <x-subscription-countdown :until="$paidUntil" :total="$course->subscription_days" class="self-start sm:self-center" />
            @endif
        </div>
    </header>

    @if ($trial)
        <flux:callout icon="sparkles" color="cyan" data-test="trial-banner">
            <flux:callout.heading>Estás probando {{ $course->title }} gratis</flux:callout.heading>
            <flux:callout.text>
                El primer episodio se lee y se practica sin pagar. Para seguir con los demás,
                <flux:link :href="route('student.course', $course)" wire:navigate>pedí tu abono</flux:link> (el mes empieza a correr cuando se aprueba).
            </flux:callout.text>
        </flux:callout>
    @elseif (! $subscription && ! $staff)
        <flux:callout icon="clock" color="amber" data-test="expired-banner">
            <flux:callout.heading>Tu abono no está vigente</flux:callout.heading>
            <flux:callout.text>
                Podés releer y repasar los episodios que abriste. Para abrir episodios nuevos,
                <flux:link :href="route('student.course', $course)" wire:navigate>renová el abono</flux:link>.
            </flux:callout.text>
        </flux:callout>
    @endif

    {{-- Ada, la protagonista (D106): niña en Primaria, de 15 en Secundaria. Como en los otros cursos (D89), se toma el
         control desde acá; el oro de las misiones sube sus atributos y abre las expediciones. --}}
    @php
        $protagonist = app(\App\Services\Heroes::class)->protagonist($course);
    @endphp
    @if ($protagonist && auth()->user()->isStudent() && auth()->user()->can('play', $course) && ! app(\App\Services\Heroes::class)->heroOf(auth()->user(), $course))
        <a href="{{ route('student.hero', $course) }}" wire:navigate class="flex items-center gap-3 rounded-lg border border-warning/50 bg-warning/10 px-4 py-3 text-sm transition hover:bg-warning/15" data-test="take-control-prompt">
            <img src="{{ \App\Services\Heroes::lookUrl($protagonist, 1) }}" alt="" class="size-12 shrink-0 rounded-full object-cover">
            <span class="flex-1 text-ink"><strong class="text-warning">Tomá el control de {{ $protagonist['name'] }}</strong>: elegí su aspecto y repartí sus puntos. El oro que ganes en las misiones sube sus atributos.</span>
            <flux:icon name="chevron-right" variant="mini" class="text-warning" />
        </a>
    @endif

    {{-- Una temporada por región (D106): el tronco en orden y, abajo, sus ramas optativas. --}}
    @foreach ($seasons as $season)
        @php
            $trunk = $season['episodes']->reject(fn ($episode) => $episode['optional'])->values();
            $optional = $season['episodes']->where('optional', true)->values();
            $progress = $season['progress'];
        @endphp
        <section class="flex flex-col gap-4" wire:key="season-{{ $season['branch']->id }}" data-test="season">
            <div class="flex flex-wrap items-end justify-between gap-2 border-b border-outline pb-2">
                <div>
                    <p class="tech-label">Temporada {{ $loop->iteration }}</p>
                    <h2 class="font-display text-xl font-semibold text-white">{{ $season['branch']->title }}</h2>
                </div>
                @if ($progress)
                    <p class="text-sm text-ink-muted" data-test="season-progress">
                        {{ $progress['done'] }} de {{ $progress['total'] }} episodios
                        @unless ($loop->last)
                            · la siguiente se abre con {{ $progress['needed'] }}
                        @endunless
                    </p>
                @endif
            </div>
            <div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
                @foreach ($trunk as $episode)
                    @include('livewire.student.partials.episode-card', ['number' => $loop->iteration])
                @endforeach
            </div>
            @if ($optional->isNotEmpty())
                <p class="mt-2 text-sm text-ink-muted"><strong class="text-ink">Ramas:</strong> episodios cortos con la gente del lugar. Son optativos: suman palabras, oro y botín.</p>
                <div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
                    @foreach ($optional as $episode)
                        @include('livewire.student.partials.episode-card', ['number' => $loop->iteration])
                    @endforeach
                </div>
            @endif
        </section>
    @endforeach
</div>
