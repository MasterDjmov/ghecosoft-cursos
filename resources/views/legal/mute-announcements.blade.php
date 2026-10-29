{{-- D113: baja de los mails que no son de la cuenta («Avisame»); se llega por el link firmado del mail. --}}
<x-layouts::legal title="Avisos por mail">
    <article class="markdown" data-test="mute-announcements">
        <h1>Avisos por mail</h1>

        @if ($muted)
            <p data-test="announcements-muted">
                Listo, {{ $user->name }}: no te mandamos más por mail los avisos de cursos nuevos («Avisame»). Si entrás a la plataforma, los seguís
                viendo en la campanita.
            </p>
            <p>Los mails de tu cuenta (entregas, pagos, abono) siguen llegando, porque son parte del servicio.</p>
        @else
            <p>
                {{ $user->name }}, si confirmás, no te mandamos más por mail los avisos de cursos nuevos («Avisame»). Los mails de tu cuenta
                (entregas, pagos, abono) siguen llegando.
            </p>
            <form method="POST" action="{{ request()->fullUrl() }}">
                @csrf
                <flux:button type="submit" variant="primary" data-test="mute-announcements-button">No quiero recibir más estos avisos</flux:button>
            </form>
        @endif
    </article>
</x-layouts::legal>
