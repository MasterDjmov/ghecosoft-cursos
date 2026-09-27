{{-- Medidor de seguridad: escucha el input de contraseña que tenga adentro. --}}
<div
    x-data="{
        pw: '',
        get checks() {
            return {
                length: this.pw.length >= 8,
                lower: /[a-z]/.test(this.pw),
                upper: /[A-Z]/.test(this.pw),
                number: /[0-9]/.test(this.pw),
            };
        },
        get score() {
            if (! this.pw) return 0;
            const passed = Object.values(this.checks).filter(Boolean).length;
            if (passed < 3) return 1;
            if (passed === 3) return 2;
            return this.pw.length >= 12 || /[^A-Za-z0-9]/.test(this.pw) ? 3 : 2;
        },
        get label() { return ['', 'Débil', 'Media', 'Fuerte'][this.score]; },
        get color() { return ['bg-surface-highest', 'bg-danger', 'bg-warning', 'bg-success'][this.score]; },
    }"
    x-on:input="if ($event.target.type === 'password' || $event.target.name === 'password') pw = $event.target.value"
    class="flex flex-col gap-2"
>
    {{ $slot }}

    <div class="flex items-center gap-2" aria-live="polite">
        <template x-for="i in 3" :key="i">
            <span class="h-1.5 flex-1 rounded-full transition-colors" :class="score >= i ? color : 'bg-surface-highest'"></span>
        </template>
        <span class="w-14 text-end text-xs text-ink-muted" x-text="label || 'Seguridad'"></span>
    </div>

    <ul class="grid grid-cols-2 gap-x-3 gap-y-1 text-xs">
        <li :class="checks.length ? 'text-success' : 'text-ink-muted'">✓ 8 caracteres o más</li>
        <li :class="checks.upper ? 'text-success' : 'text-ink-muted'">✓ Una mayúscula</li>
        <li :class="checks.lower ? 'text-success' : 'text-ink-muted'">✓ Una minúscula</li>
        <li :class="checks.number ? 'text-success' : 'text-ink-muted'">✓ Un número</li>
    </ul>
</div>
