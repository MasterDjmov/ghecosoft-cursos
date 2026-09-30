<section class="w-full">
    @include('partials.settings-heading')

    <x-settings.layout heading="Avisos" subheading="Cómo te enterás de lo nuevo mientras tenés la plataforma abierta">
        <form wire:submit="save" class="my-6 flex w-full flex-col gap-6"
            x-data="{ permission: 'Notification' in window ? Notification.permission : 'unsupported' }"
            x-on:submit="if ($wire.alert_desktop && permission === 'default') Notification.requestPermission().then(p => permission = p)">
            <p class="text-sm text-ink-muted">
                Con la plataforma abierta (aunque sea en otra pestaña), la campanita se actualiza sola, la pestaña muestra cuántos avisos
                tenés sin leer y el ícono lleva un punto rojo.
            </p>

            <flux:switch wire:model="alert_sound" label="Sonar cuando llega algo nuevo"
                description="Un tono corto: una entrega para corregir, una corrección, un mensaje." />

            <div class="flex flex-col gap-2">
                <flux:switch wire:model="alert_desktop" label="Mostrar una notificación fuera del navegador"
                    description="Aparece aunque estés en otro programa. Al guardar, el navegador te pide permiso una sola vez." />
                <p x-show="permission === 'denied'" x-cloak class="flex items-start gap-2 text-sm text-warning">
                    <flux:icon name="exclamation-triangle" variant="micro" class="mt-0.5 shrink-0" />
                    El navegador tiene bloqueadas las notificaciones de esta página: habilitalas desde el candado de la barra de direcciones.
                </p>
                <p x-show="permission === 'unsupported'" x-cloak class="text-sm text-ink-muted">Este navegador no permite notificaciones.</p>
            </div>

            <div class="flex items-center gap-3">
                <flux:button variant="primary" type="submit">Guardar</flux:button>
                <flux:button type="button" variant="ghost" icon="speaker-wave" x-on:click="window.liveAlerts?.beep()">Probar el sonido</flux:button>
            </div>
        </form>
    </x-settings.layout>
</section>
