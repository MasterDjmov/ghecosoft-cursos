{{-- Herramientas → Ejecutor de Java (D85): Java corre en la compu del alumno, nunca en el servidor. --}}
@php($step = 'grid size-8 shrink-0 place-items-center rounded-full bg-primary/15 font-mono text-sm font-bold text-primary-bright')
<div class="mx-auto flex w-full max-w-3xl flex-col gap-6 p-4 sm:p-8">
    <header class="flex flex-col gap-1">
        <p class="tech-label">Herramientas</p>
        <h1 class="font-display text-2xl font-semibold text-white sm:text-3xl">Ejecutor de Java</h1>
        <p class="text-ink-muted">Para que el botón <strong class="text-ink">Ejecutar</strong> funcione en los cursos de Java, tu código corre en <strong class="text-ink">tu compu</strong>, con un programa chico abierto. Se instala una sola vez. Sin él podés escribir y entregar igual: el profe lo ejecuta al corregir.</p>
    </header>

    <section class="panel flex gap-4 p-5">
        <span class="{{ $step }}">1</span>
        <div class="flex flex-col gap-2">
            <h2 class="font-medium text-white">Instalá Java (el JDK 21)</h2>
            <ul class="flex list-disc flex-col gap-1 ps-5 text-sm text-ink-muted">
                <li><strong class="text-ink">Windows:</strong> entrá a <a href="https://adoptium.net/es/temurin/releases/?version=21" target="_blank" rel="noopener" class="text-primary-bright hover:underline">adoptium.net</a>, bajá <em>Temurin 21 (LTS)</em> para Windows, el archivo <strong class="text-ink">.msi</strong>, e instalalo dejando marcada la opción <em>Add to PATH</em>.</li>
                <li><strong class="text-ink">Ubuntu o Debian:</strong> en una terminal, <code class="font-mono text-ink">sudo apt install openjdk-21-jdk</code></li>
                <li><strong class="text-ink">Mac:</strong> en la misma página, el instalador <strong class="text-ink">.pkg</strong>.</li>
            </ul>
            <p class="text-xs text-ink-muted">Si ya tenés Java 17 o más nuevo (el JDK, no solo el JRE), saltá este paso.</p>
        </div>
    </section>

    <section class="panel flex gap-4 p-5">
        <span class="{{ $step }}">2</span>
        <div class="flex flex-col gap-3">
            <h2 class="font-medium text-white">Bajá el ejecutor y descomprimilo</h2>
            <p class="text-sm text-ink-muted">Es una carpeta con el ejecutor, el lanzador para Windows, el de Linux y Mac, y un LEEME. Descomprimila en un lugar fácil de encontrar, por ejemplo el Escritorio.</p>
            <flux:button icon="arrow-down-tray" variant="primary" class="self-start" :href="route('student.java-runner.download')" data-test="java-runner-download">Bajar el ejecutor (.zip)</flux:button>
        </div>
    </section>

    <section class="panel flex gap-4 p-5">
        <span class="{{ $step }}">3</span>
        <div class="flex flex-col gap-2">
            <h2 class="font-medium text-white">Abrilo cada vez que vayas a practicar</h2>
            <ul class="flex list-disc flex-col gap-1 ps-5 text-sm text-ink-muted">
                <li><strong class="text-ink">Windows:</strong> doble clic en <code class="font-mono text-ink">Iniciar-ejecutor.bat</code>. Si aparece «Windows protegió su PC», tocá <em>Más información</em> → <em>Ejecutar de todas formas</em>.</li>
                <li><strong class="text-ink">Linux y Mac:</strong> en una terminal, dentro de la carpeta: <code class="font-mono text-ink">sh iniciar-ejecutor.sh</code></li>
            </ul>
            <p class="text-sm text-ink-muted">Se abre una ventana negra que dice <em>Ejecutor de Java listo</em>. <strong class="text-ink">Dejala abierta</strong> mientras practicás; al cerrarla, deja de funcionar.</p>
        </div>
    </section>

    <section class="panel flex gap-4 p-5" x-data="{
            state: 'idle', java: '',
            async probe() {
                this.state = 'probing';
                try {
                    const r = await fetch(@js($runnerUrl).replace(/\/+$/, '') + '/ping', { signal: AbortSignal.timeout(8000) });
                    const data = await r.json();
                    this.java = data.java ?? '';
                    this.state = data.ok ? 'ok' : 'fail';
                } catch (e) { this.state = 'fail'; }
            },
        }">
        <span class="{{ $step }}">4</span>
        <div class="flex min-w-0 flex-col gap-3">
            <h2 class="font-medium text-white">Probá la conexión</h2>
            <p class="text-sm text-ink-muted">La primera vez, el navegador pregunta si este sitio puede acceder a <em>dispositivos de tu red local</em>: tocá <strong class="text-ink">Permitir</strong>. Es tu propia compu.</p>
            <flux:button icon="signal" class="self-start" x-on:click="probe" x-bind:disabled="state === 'probing'" data-test="java-runner-probe">
                <span x-text="state === 'probing' ? 'Probando…' : 'Probar conexión'">Probar conexión</span>
            </flux:button>
            <flux:callout icon="check-circle" color="emerald" x-show="state === 'ok'" x-cloak>
                <flux:callout.text>¡Listo! El ejecutor responde (<span x-text="'Java ' + java"></span>). Ya podés tocar <strong>Ejecutar</strong> en los cursos de Java.</flux:callout.text>
            </flux:callout>
            <flux:callout icon="exclamation-triangle" color="amber" x-show="state === 'fail'" x-cloak>
                <flux:callout.text>
                    No responde. Revisá que la ventana del ejecutor esté abierta y diga <em>listo</em>.
                    Si rechazaste el permiso: candado a la izquierda de la dirección → <em>Configuración del sitio</em> → <em>Acceso a la red local</em> → <em>Permitir</em>, y recargá.
                    Si usás una extensión que cambia los encabezados (como <em>CORS Unblock</em>), apagala para este sitio.
                </flux:callout.text>
            </flux:callout>
        </div>
    </section>

    <flux:callout icon="shield-check" color="zinc">
        <flux:callout.text>
            <strong>¿Es seguro?</strong> El ejecutor escucha solo dentro de tu compu (127.0.0.1) y solo atiende a esta plataforma. Compila y ejecuta el código que vos escribís en el editor, con un límite de tiempo, como si lo corrieras vos en una terminal. Nada de tu compu se sube a la plataforma: solo vuelve la salida del programa.
        </flux:callout.text>
    </flux:callout>
</div>
