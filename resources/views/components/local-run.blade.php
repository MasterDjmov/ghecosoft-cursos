@props([
    'code' => '',
    'stdin' => '',
    'language' => 'java',
    'name' => 'main',
])

@php
    // Lenguajes que el docente prueba en su compu (D67): Java no tiene un compilador libre y completo
    // para el navegador. Se arma todo acá, en el navegador: no hay descarga desde el servidor.
    $class = preg_match('/public\s+(?:(?:final|abstract)\s+)*class\s+(\w+)/', (string) $code, $m) ? $m[1] : 'Main';
    $file = $class.'.java';
    $dir = '/tmp/ghecosoft/'.$name;
    $stdin = str_replace("\r\n", "\n", (string) $stdin);
    $input = trim($stdin) === '' ? ' < /dev/null' : " <<'FIN_ENTRADA'\n".rtrim($stdin, "\n")."\nFIN_ENTRADA";
    $command = "mkdir -p {$dir} && cd {$dir} && cat > {$file} <<'FIN_CODIGO'\n".rtrim(str_replace("\r\n", "\n", (string) $code), "\n")
        ."\nFIN_CODIGO\njavac -encoding UTF-8 -d . {$file} && java -cp . {$class}{$input}\n";
@endphp

<div {{ $attributes->class('flex flex-col gap-2 rounded-lg border border-outline bg-surface-low p-3') }} data-test="local-run"
    x-data="{
        copied: false,
        async copy() {
            try { await navigator.clipboard.writeText(@js($command)); this.copied = true; setTimeout(() => this.copied = false, 1500) } catch (e) {}
        },
        download() {
            const url = URL.createObjectURL(new Blob([@js((string) $code)], { type: 'text/x-java' }));
            const a = Object.assign(document.createElement('a'), { href: url, download: @js($file) });
            a.click();
            URL.revokeObjectURL(url);
        },
    }">
    <p class="flex items-center gap-2 text-sm text-ink">
        <flux:icon name="command-line" variant="micro" class="text-primary-bright" />
        Probalo en tu compu: pegá el comando en la terminal (lo compila en <code class="font-mono text-xs">{{ $dir }}</code> y lo corre con la entrada de ejemplo).
    </p>
    <div class="flex flex-wrap gap-2">
        <flux:button size="sm" variant="primary" icon="clipboard" x-on:click="copy">
            <span x-text="copied ? '¡Copiado!' : 'Copiar comando'">Copiar comando</span>
        </flux:button>
        <flux:button size="sm" icon="arrow-down-tray" x-on:click="download">Descargar {{ $file }}</flux:button>
    </div>
    <details class="text-xs">
        <summary class="cursor-pointer text-ink-muted">Ver el comando</summary>
        <pre class="mt-2 max-h-60 overflow-auto rounded-md border border-outline bg-[#05070d] p-2 font-mono whitespace-pre text-ink-muted">{{ $command }}</pre>
    </details>
</div>
