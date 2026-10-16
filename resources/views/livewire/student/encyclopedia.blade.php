{{-- La Gran Enciclopedia del Código (D104): portada con las 8 secciones; adentro, fichas en tarjetas que se abren en un modal. --}}
@php
    use App\Livewire\Student\Encyclopedia as Page;
    // Dónde están las 8 tarjetas pintadas en la portada (porcentajes de la imagen de 1376×768).
    $spots = [
        'clases' => [29.5, 16.9], \App\Support\Encyclopedia::MASTERS => [40.0, 16.9], \App\Support\Encyclopedia::BESTIARY => [50.4, 16.9], 'monturas' => [60.8, 16.9],
        'monedas' => [29.5, 32.3], 'artefactos' => [40.0, 32.3], 'reinos' => [50.4, 32.3], 'hechizos' => [60.8, 32.3],
    ];
@endphp
<div class="relative min-h-full">
    {{-- La biblioteca limpia (sin letras) ocupa toda el área de fondo en todas las pantallas; la portada va encima. --}}
    <div class="pointer-events-none fixed inset-0 -z-10" style="background: url('{{ asset('img/enciclopedia/fondo-biblioteca.webp') }}') center / cover no-repeat"></div>
    <div @class(['pointer-events-none fixed inset-0 -z-10 bg-gradient-to-b', 'from-[#05070d]/55 via-[#05070d]/35 to-[#05070d]/70' => $section === '', 'from-[#05070d]/70 via-[#05070d]/60 to-[#05070d]/80' => $section !== ''])></div>

    <div @class(['mx-auto flex w-full flex-col gap-6 p-4 sm:p-8', 'max-w-6xl' => $section !== ''])>
        @if ($section === '')
            <header class="flex flex-col gap-1">
                <p class="tech-label">Juego</p>
                <h1 class="font-display text-2xl font-semibold text-white sm:text-3xl">La Gran Enciclopedia del Código</h1>
                <p class="text-ink-muted">Todo el universo: quién es quién, qué criaturas hay y dónde aparecen. Lo que todavía no conociste está en sombra, con la pista de dónde encontrarlo.</p>
            </header>

            {{-- Portada: las tarjetas pintadas son los botones (en la compu). --}}
            <div class="relative hidden overflow-hidden rounded-xl border border-outline shadow-2xl md:block" data-test="encyclopedia-cover">
                <img src="{{ asset('img/enciclopedia/portada.webp') }}" alt="La Gran Enciclopedia del Código" class="block w-full">
                @foreach ($spots as $key => [$left, $top])
                    @php($ready = in_array($key, Page::SECTIONS_READY, true))
                    <button type="button" @disabled(! $ready) wire:click="show('{{ $key }}')" title="{{ Page::SECTIONS[$key] }}{{ $ready ? '' : ' · próximamente' }}"
                        class="group absolute rounded-md transition {{ $ready ? 'cursor-pointer hover:bg-cyan-300/15 hover:ring-2 hover:ring-cyan-300/80' : 'cursor-default' }}"
                        style="left: {{ $left }}%; top: {{ $top }}%; width: 9.7%; height: 13.9%" data-test="cover-{{ $key }}">
                        @if (isset($counts[$key]))
                            <span class="absolute -top-2 -right-2 rounded-full border border-cyan-300/60 bg-[#05070d]/90 px-1.5 font-mono text-[11px] text-cyan-200">{{ $counts[$key]['discovered'] }}/{{ $counts[$key]['total'] }}</span>
                        @elseif (! $ready)
                            <span class="absolute -top-2 -right-2 rounded-full border border-outline bg-[#05070d]/90 px-1.5 text-[10px] text-ink-muted">Pronto</span>
                        @endif
                    </button>
                @endforeach
            </div>

            {{-- En el celular: la portada de adorno y las secciones en botones. --}}
            <img src="{{ asset('img/enciclopedia/portada.webp') }}" alt="" class="block w-full rounded-xl border border-outline md:hidden">
            <div class="grid grid-cols-2 gap-3 md:hidden">
                @foreach (Page::SECTIONS as $key => $title)
                    @php($ready = in_array($key, Page::SECTIONS_READY, true))
                    <button type="button" @disabled(! $ready) wire:click="show('{{ $key }}')"
                        class="panel flex items-center justify-between gap-2 px-3 py-3 text-left {{ $ready ? 'hover:border-cyan-300/60' : 'opacity-50' }}">
                        <span class="font-medium text-white">{{ $title }}</span>
                        <span class="font-mono text-xs text-ink-muted">{{ isset($counts[$key]) ? $counts[$key]['discovered'].'/'.$counts[$key]['total'] : ($ready ? '' : 'Pronto') }}</span>
                    </button>
                @endforeach
            </div>
        @else
            <header class="flex flex-col gap-3">
                <button type="button" wire:click="back" class="inline-flex items-center gap-1.5 self-start text-sm text-ink-muted hover:text-white" data-test="encyclopedia-back">
                    <flux:icon name="chevron-left" variant="micro" /> La Gran Enciclopedia
                </button>
                <div class="flex flex-wrap items-end justify-between gap-3">
                    <div>
                        <h1 class="font-display text-2xl font-semibold text-white sm:text-3xl">{{ Page::SECTIONS[$section] }}</h1>
                        <p class="text-ink-muted">
                            {{ $counts[$section]['discovered'] }} de {{ $counts[$section]['total'] }} descubiertos.
                            {{ match ($section) {
                                \App\Support\Encyclopedia::BESTIARY => 'Cada criatura es un error de programación: conocelas para vencerlas.',
                                \App\Support\EncyclopediaItems::ARTIFACTS => 'Todo lo que se puede conseguir en el universo, y dónde.',
                                \App\Support\EncyclopediaItems::COINS => 'Cómo se gana cada moneda y para qué sirve.',
                                default => 'Los que te vas cruzando en la historia.',
                            } }}
                        </p>
                    </div>
                    <div class="flex flex-wrap items-center gap-2">
                        <flux:input wire:model.live.debounce.300ms="search" icon="magnifying-glass" placeholder="Buscar por nombre" size="sm" class="w-48" data-test="encyclopedia-search" />
                        <flux:select wire:model.live="course" size="sm" class="w-44" data-test="encyclopedia-course">
                            <flux:select.option value="">Todos los mundos</flux:select.option>
                            @foreach ($courses as $option)
                                <flux:select.option value="{{ $option->slug }}">{{ \Illuminate\Support\Str::before($option->title, ':') }}</flux:select.option>
                            @endforeach
                        </flux:select>
                    </div>
                </div>
            </header>

            @forelse ($groups as $group => $items)
                <section class="flex flex-col gap-3" wire:key="group-{{ \Illuminate\Support\Str::slug($group) }}">
                    <h2 class="font-display text-lg font-semibold text-white">{{ $group }}</h2>
                    <div class="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-5">
                        @foreach ($items as $item)
                            <button type="button" wire:click="open('{{ $item['key'] }}')" wire:key="entry-{{ $item['key'] }}" data-test="entry-{{ $item['key'] }}"
                                class="panel group flex flex-col items-center gap-2 p-3 text-center transition hover:-translate-y-0.5 hover:border-cyan-300/60">
                                <div @class(['relative grid aspect-square w-full place-items-center overflow-hidden rounded-xl bg-[#05070d]', isset($item['rarity']) ? 'border-2 '.$item['rarity']->classes() : ''])>
                                    @if (isset($item['currency']))
                                        <x-coin-icon :currency="$item['currency']" size="size-2/3!" :class="$item['discovered'] ? '' : 'blur-[3px] brightness-[0.4] grayscale'" />
                                    @elseif ($item['portrait'])
                                        <img src="{{ $item['portrait'] }}" alt="" loading="lazy"
                                            @class(['size-full object-cover transition', 'blur-[3px] brightness-[0.4] grayscale' => ! $item['discovered'], 'group-hover:scale-105' => $item['discovered']])>
                                    @endif
                                    @unless ($item['discovered'])
                                        <span class="absolute inset-0 grid place-items-center font-display text-4xl font-bold text-cyan-200/70">?</span>
                                    @endunless
                                    @if ($item['defeated'])
                                        <span class="absolute right-1 bottom-1 rounded bg-success/90 px-1.5 text-[10px] font-semibold text-[#05070d]" data-test="defeated-{{ $item['key'] }}">Vencido</span>
                                    @elseif ($item['boss'])
                                        <span class="absolute right-1 bottom-1 rounded bg-danger/80 px-1.5 text-[10px] font-semibold text-white">Jefe</span>
                                    @endif
                                </div>
                                <span class="text-sm font-medium leading-tight {{ $item['discovered'] ? 'text-white' : 'text-ink-muted' }}">{{ $item['name'] }}</span>
                                @if ($item['discovered'] && ($item['subtitle'] ?? null))
                                    <span @class(['text-[11px] leading-tight', isset($item['rarity']) ? $item['rarity']->classes() : 'text-ink-muted'])>{{ $item['subtitle'] }}</span>
                                @endif
                                @unless ($item['discovered'])
                                    <span class="text-[11px] leading-tight text-ink-muted">{{ $item['where'] }}</span>
                                @endunless
                            </button>
                        @endforeach
                    </div>
                </section>
            @empty
                <p class="text-ink-muted">No hay nada con ese nombre.</p>
            @endforelse
        @endif
    </div>

    {{-- La ficha: un solo modal que se llena con la elegida (lo no descubierto, sin su texto). --}}
    <flux:modal name="encyclopedia-entry" class="w-full max-w-3xl" data-test="encyclopedia-modal">
        @if ($entry)
            <div class="flex flex-col gap-5 sm:flex-row">
                <div @class(['relative mx-auto grid w-full max-w-60 shrink-0 place-items-center overflow-hidden rounded-xl border bg-[#05070d] sm:mx-0', isset($entry['rarity']) ? 'border-2 '.$entry['rarity']->classes() : 'border-outline', 'aspect-square' => $entry['square'] ?? false])>
                    @if (isset($entry['currency']))
                        <x-coin-icon :currency="$entry['currency']" size="size-3/4!" :class="$entry['discovered'] ? '' : 'blur-[4px] brightness-[0.4] grayscale'" />
                    @elseif ($image = $entry['discovered'] ? ($entry['figure'] ?? $entry['portrait']) : $entry['portrait'])
                        <img src="{{ $image }}" alt="{{ $entry['discovered'] ? $entry['name'] : '' }}" @class(['w-full', 'blur-[4px] brightness-[0.4] grayscale' => ! $entry['discovered']])>
                    @endif
                    @unless ($entry['discovered'])
                        <span class="absolute inset-0 grid place-items-center font-display text-6xl font-bold text-cyan-200/70">?</span>
                    @endunless
                </div>
                @if (! empty($entry['gallery']))
                    {{-- Los niveles de una montura, de n1 a n5. --}}
                    <div class="flex gap-1.5 sm:order-last sm:flex-col" data-test="entry-gallery">
                        @foreach ($entry['gallery'] as $shot)
                            <figure class="flex flex-col items-center gap-0.5">
                                <img src="{{ $shot['url'] }}" alt="{{ $entry['name'] }} {{ $shot['label'] }}" loading="lazy" class="size-14 rounded-lg border border-outline object-cover">
                                <figcaption class="font-mono text-[10px] text-ink-muted">{{ $shot['label'] }}</figcaption>
                            </figure>
                        @endforeach
                    </div>
                @endif
                <div class="flex min-w-0 flex-1 flex-col gap-3">
                    <div>
                        <p class="tech-label">{{ $entry['group'] }}</p>
                        <flux:heading size="xl">{{ $entry['name'] }}</flux:heading>
                        @if ($entry['discovered'] && ($entry['subtitle'] ?? null))
                            <p @class(['text-xs tracking-wide uppercase', isset($entry['rarity']) ? $entry['rarity']->classes() : 'text-ink-muted'])>{{ $entry['subtitle'] }}</p>
                        @endif
                        @if ($entry['defeated'])
                            <p class="text-sm font-semibold text-success">Lo venciste</p>
                        @elseif ($entry['boss'])
                            <p class="text-sm text-danger">Jefe</p>
                        @endif
                    </div>
                    @if ($entry['discovered'])
                        <dl class="flex flex-col gap-2 text-sm" data-test="entry-fields">
                            @foreach ($entry['fields'] as $label => $text)
                                @if ($label === 'Frase')
                                    <blockquote class="border-l-2 border-cyan-300/70 pl-3 italic text-cyan-100">{!! \App\Support\Markdown::render($text) !!}</blockquote>
                                @else
                                    <div>
                                        <dt class="text-xs tracking-wide text-ink-muted uppercase">{{ $label }}</dt>
                                        <dd class="markdown text-ink">{!! \App\Support\Markdown::render($text) !!}</dd>
                                    </div>
                                @endif
                            @endforeach
                        </dl>
                        @if ($entry['where'])
                            <p class="text-xs text-ink-muted">Aparece en {{ $entry['where'] }}.</p>
                        @endif
                        @include('livewire.student.partials.encyclopedia-sources')
                    @else
                        <p class="text-ink-muted" data-test="entry-locked">{{ match ($entry['section']) {
                            \App\Support\Encyclopedia::BESTIARY => 'Todavía no te enfrentaste a esta criatura. Su historia se abre cuando llegues.',
                            \App\Support\EncyclopediaItems::ARTIFACTS => 'Todavía no lo conseguiste. Cuando lo tengas, vas a ver qué hace.',
                            \App\Support\EncyclopediaItems::COINS => 'Todavía no la ganaste: se abre cuando empieces ese mundo.',
                            \App\Support\EncyclopediaWorlds::MOUNTS => 'Todavía no es tuya. Cuando la tengas, vas a ver cómo es y cómo crece.',
                            \App\Support\EncyclopediaWorlds::REALMS => 'Todavía no llegaste a esta región. Su mapa y sus lugares se abren cuando la empieces.',
                            default => 'Todavía no te cruzaste con este personaje. Su historia se abre cuando llegues.',
                        } }}</p>
                        @if ($entry['where'])
                            <p class="flex items-start gap-1.5 text-sm text-cyan-200"><flux:icon name="map-pin" variant="micro" class="mt-0.5 shrink-0" /> Aparece en {{ $entry['where'] }}.</p>
                        @endif
                        @include('livewire.student.partials.encyclopedia-sources')
                    @endif
                </div>
            </div>
        @endif
    </flux:modal>
</div>
