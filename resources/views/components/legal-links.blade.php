{{-- D112: Términos, Privacidad y los botones de arrepentimiento y de baja (Defensa del Consumidor), en el pie de todas las páginas. --}}
<nav {{ $attributes->class('flex flex-wrap items-center justify-center gap-x-4 gap-y-1 text-xs text-ink-muted') }} aria-label="Legales" data-test="legal-links">
    <a href="{{ route('legal.withdrawal') }}" class="font-medium text-ink hover:text-primary-bright">Botón de arrepentimiento</a>
    <a href="{{ route('legal.cancellation') }}" class="hover:text-primary-bright">Botón de baja</a>
    <a href="{{ route('legal.terms') }}" class="hover:text-primary-bright">Términos y condiciones</a>
    <a href="{{ route('legal.privacy') }}" class="hover:text-primary-bright">Privacidad</a>
    <span>© {{ now()->year }} {{ config('legal.owner') }}</span>
</nav>
