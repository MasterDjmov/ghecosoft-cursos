<div @class(['mx-auto flex w-full max-w-5xl flex-col gap-6', 'p-4 sm:p-8' => ! $inWindow, 'p-3' => $inWindow]) x-data="{ open: 'consola' }">
    <x-tool-header title="La caja de la Feria" :in-window="$inWindow">
        JavaScript para practicar lo que quieras. Corre acá mismo, en tu navegador, dentro de una caja: no tiene internet, no ve tu sesión
        y todo lo que toca es de mentira (el reloj, las cookies, el almacenamiento y el Puerto de Elefa), y se borra al terminar.
        Tu código queda en este navegador, por si volvés, y no cuenta para el curso.
    </x-tool-header>

    <nav class="flex flex-wrap gap-2" aria-label="Ejemplos">
        @foreach ($examples as $key => $example)
            <button type="button" x-on:click="open = '{{ $key }}'" data-test="js-example-{{ $key }}"
                class="rounded-full border px-3 py-1 text-sm transition"
                x-bind:class="open === '{{ $key }}' ? 'border-primary-bright bg-primary/15 text-white' : 'border-outline text-ink-muted hover:text-ink'">
                {{ $example['title'] }}
            </button>
        @endforeach
    </nav>

    @foreach ($examples as $key => $example)
        <section x-show="open === '{{ $key }}'" @if (! $loop->first) x-cloak @endif class="flex flex-col gap-3">
            <p class="text-sm text-ink-muted">{{ $example['about'] }}</p>
            <x-code-runner :code="$example['code']" language="javascript" name="feria" :keep="'js-'.$key" autocomplete
                :checks="isset($example['page']) ? json_encode(['page' => $example['page']], JSON_UNESCAPED_UNICODE) : null" data-test="js-tool" />
        </section>
    @endforeach

    <section class="panel flex flex-col gap-2 p-5 text-sm text-ink">
        <h2 class="font-display text-base font-semibold text-white">Lo que hay en la caja</h2>
        <ul class="list-disc space-y-1 ps-5 text-ink-muted">
            <li><strong class="text-ink">La consola</strong>, como la de Node: <code>console.log</code>, <code>table</code>, <code>group</code>, <code>count</code>, <code>time</code>. Los errores te dicen la línea y qué quieren decir.</li>
            <li><strong class="text-ink">El reloj de la caja:</strong> <code>setTimeout</code>, <code>setInterval</code>, <code>requestAnimationFrame</code>, <code>Date</code> y <code>performance.now()</code> avanzan juntos; arranca el 2 de marzo de 2026 a las 21 h. <code>Math.random()</code> da siempre la misma serie.</li>
            <li><strong class="text-ink">El Puerto de Elefa:</strong> <code>fetch('/puerto/…')</code> contesta <code>hola</code>, <code>puestos</code>, <code>puestos/1</code>, <code>heroes</code>, <code>clima</code>, <code>mensajes</code> (también POST), <code>lento</code> (3 s), <code>error</code> (500), <code>roto</code> (JSON cortado), <code>texto</code>, <code>eco</code>, <code>fichas?pagina=2</code> y la sesión (<code>login</code> con nima / luciernaga, <code>perfil</code>, <code>salir</code>). Con <code>?demora=ms</code> cambia cuánto tarda y con <code>?falla=1</code> falla.</li>
            <li><strong class="text-ink">Cookies, localStorage y sessionStorage</strong> de mentira: se ven en el Tablero y se borran al terminar.</li>
            <li><strong class="text-ink">alert, confirm y prompt:</strong> las respuestas salen de la pestaña Entrada, una por línea.</li>
            <li><strong class="text-ink">Un tope:</strong> si un bucle no termina, la caja lo corta (como al Gólem) y te avisa.</li>
        </ul>
        @if ($course && ! $inWindow)
            <p class="text-xs text-ink-muted">Las explicaciones están en el curso <a href="{{ route('student.course', $course) }}" wire:navigate class="text-primary-bright hover:underline">{{ $course->title }}</a>.</p>
        @endif
    </section>
</div>
