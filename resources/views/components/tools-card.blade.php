{{-- Herramientas (D120): la calculadora y la tabla son para todos; lo que se puede practicar sin instalar nada, según los cursos de cada uno. --}}
@php($tools = \App\Support\PracticeTools::menu(auth()->user()))
<flux:separator variant="subtle" class="my-2" />
<div class="rounded-xl border border-primary/30 bg-primary/5 p-1" data-test="menu-tools">
    <flux:sidebar.group heading="Herramientas" class="grid">
        @foreach (\App\Support\PracticeTools::utilities() as $tool)
            {{-- Un clic abre (o trae adelante) su ventana flotante; el + abre otra más. --}}
            <div class="group relative grid">
                <flux:sidebar.item :icon="$tool['icon']" :href="$tool['url']" :current="request()->routeIs($tool['route'])"
                    data-tool-window="{{ $tool['url'] }}" data-tool-title="{{ $tool['label'] }}" data-tool-limit="{{ $tool['limit'] }}" data-tool-size="{{ $tool['size'] }}" data-test="menu-{{ $tool['key'] }}">
                    {{ $tool['label'] }}
                </flux:sidebar.item>
                <button type="button" data-tool-window="{{ $tool['url'] }}" data-tool-title="{{ $tool['label'] }}" data-tool-limit="{{ $tool['limit'] }}" data-tool-size="{{ $tool['size'] }}" data-tool-new title="Abrir otra ventana" aria-label="Abrir otra ventana de {{ $tool['label'] }}"
                    class="absolute end-1 top-1/2 grid size-6 -translate-y-1/2 place-items-center rounded text-ink-muted opacity-60 transition hover:bg-surface-high hover:text-ink hover:opacity-100">
                    <flux:icon name="plus" variant="micro" />
                </button>
            </div>
        @endforeach
        @foreach ($tools as $tool)
            @php($current = str_contains($tool['route'], ':') ? request()->routeIs('student.practice-tool') && request()->route('language') === $tool['key'] : request()->routeIs($tool['route']))
            <div class="group relative grid">
                <flux:sidebar.item :icon="$tool['icon']" :href="$tool['url']" :current="$current" wire:navigate data-test="menu-{{ $tool['key'] }}">
                    {{ $tool['label'] }}
                </flux:sidebar.item>
                @if ($tool['window'])
                    <button type="button" data-tool-window="{{ $tool['url'] }}" data-tool-title="{{ $tool['label'] }}" title="Abrir en ventana" aria-label="Abrir {{ $tool['label'] }} en ventana"
                        class="absolute end-1 top-1/2 grid size-6 -translate-y-1/2 place-items-center rounded text-ink-muted opacity-60 transition hover:bg-surface-high hover:text-ink hover:opacity-100">
                        <flux:icon name="arrow-top-right-on-square" variant="micro" />
                    </button>
                @endif
            </div>
        @endforeach
    </flux:sidebar.group>
</div>
