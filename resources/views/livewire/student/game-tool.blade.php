<div @class(['mx-auto flex w-full max-w-5xl flex-col gap-6', 'p-4 sm:p-8' => ! $inWindow, 'p-3' => $inWindow])>
    <x-tool-header title="Juegos con SDL3 (prueba)" :in-window="$inWindow">
        El prototipo de la Ciudad Arcadia (D126): un juego en C con SDL3 que se edita y se juega acá mismo. Es el mismo
        archivo que compila con SDL3 de verdad en la compu.
    </x-tool-header>

    <x-code-runner :code="$starter" language="c" name="pong" keep="sdl-game" game download autocomplete data-test="game-tool" />

    <section class="panel flex flex-col gap-2 p-5 text-sm text-ink">
        <h2 class="font-display text-base font-semibold text-white">Para tener en cuenta</h2>
        <ul class="list-disc space-y-1 ps-5 text-ink-muted [&_code]:text-primary-bright [&_strong]:text-ink">
            <li><strong>Jugar</strong> compila tu código y abre la ventana del juego. Hacé clic en el juego para usar el teclado.</li>
            <li>El joystick o el control de consola se conecta por USB o Bluetooth: tocá un botón para que el navegador lo vea.</li>
            <li>Si el juego no llama nunca a <code>SDL_PollEvent</code>, <code>SDL_RenderPresent</code> ni <code>SDL_Delay</code>, se corta a los 3 segundos: es el Bucle Eterno.</li>
            <li>El texto de <code>SDL_RenderDebugText</code> es de 8 × 8 píxeles y no tiene tildes ni ñ (tampoco en SDL3 real).</li>
            <li>Anda en Chrome y en Edge actualizados.</li>
            <li><strong>Bajar</strong> te da el <code>.c</code>. En Linux, con SDL3 instalado: <code>gcc pong.c -o pong $(pkg-config --cflags --libs sdl3)</code>.</li>
        </ul>
    </section>
</div>
