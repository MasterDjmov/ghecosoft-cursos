<div @class(['mx-auto flex w-full max-w-5xl flex-col gap-6', 'p-4 sm:p-8' => ! $inWindow, 'p-3' => $inWindow])>
    @if ($saved)
        @include('livewire.student.partials.saved-header', ['toolLabel' => 'Practicar '.$tool['label']])
    @else
        <x-tool-header :title="'Practicar '.$tool['label']" :in-window="$inWindow">
            Para probar lo que quieras sin instalar nada. Lo que escribís queda en este navegador, por si volvés, y no cuenta para el curso.
            Con <strong class="text-ink">Guardar</strong> queda en <a href="{{ route('student.saved-practices') }}" wire:navigate class="text-primary-bright hover:underline">Mis prácticas</a>, para seguirla cuando quieras (y desde otra compu).
        </x-tool-header>
    @endif

    {{-- Una guardada se abre con lo guardado (no con lo que quedó en el navegador). --}}
    <x-code-runner :code="$saved?->code ?? $tool['starter']" :stdin="(string) $saved?->stdin" :show-stdin="filled($saved?->stdin)" :language="$language"
        :name="$saved ? \Illuminate\Support\Str::beforeLast($saved->fileName(), '.') : ($tool['name'] ?? 'practica')"
        :keep="$saved ? null : $language" autocomplete download data-test="practice-tool" wire:key="runner-{{ $saved?->id ?? 'nueva' }}">
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
        <h2 class="font-display text-base font-semibold text-white">Para tener en cuenta</h2>
        <ul class="list-disc space-y-1 ps-5 text-ink-muted [&_code]:text-primary-bright [&_strong]:text-ink">
            @foreach ($tool['notes'] as $note)
                <li>{!! $note !!}</li>
            @endforeach
            <li>Mientras escribís te sugiere palabras y estructuras: con <strong>Tab</strong> o <strong>Enter</strong> aceptás la que está marcada.</li>
            <li><strong>Bajar</strong> te da el archivo para abrirlo en tu compu; <strong>Guardar</strong> lo deja en Mis prácticas.</li>
        </ul>
    </section>
</div>
