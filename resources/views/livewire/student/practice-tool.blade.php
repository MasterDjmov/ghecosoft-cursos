<div @class(['mx-auto flex w-full max-w-5xl flex-col gap-6', 'p-4 sm:p-8' => ! $inWindow, 'p-3' => $inWindow])>
    <x-tool-header :title="'Practicar '.$tool['label']" :in-window="$inWindow">
        Para probar lo que quieras sin instalar nada. Lo que escribís queda en este navegador, por si volvés, y no cuenta para el curso.
    </x-tool-header>

    <x-code-runner :code="$tool['starter']" :language="$language" :name="$tool['name'] ?? 'practica'" :keep="$language" autocomplete data-test="practice-tool" />

    <section class="panel flex flex-col gap-2 p-5 text-sm text-ink">
        <h2 class="font-display text-base font-semibold text-white">Para tener en cuenta</h2>
        <ul class="list-disc space-y-1 ps-5 text-ink-muted [&_code]:text-primary-bright [&_strong]:text-ink">
            @foreach ($tool['notes'] as $note)
                <li>{!! $note !!}</li>
            @endforeach
            <li>Mientras escribís te sugiere palabras y estructuras: con <strong>Tab</strong> o <strong>Enter</strong> aceptás la que está marcada.</li>
        </ul>
    </section>
</div>
