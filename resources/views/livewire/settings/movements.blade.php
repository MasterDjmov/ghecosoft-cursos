<section class="w-full">
    @include('partials.settings-heading')

    <x-settings.layout heading="Movimientos" subheading="Cada moneda y cada punto de experiencia que ganaste o gastaste." wide>
        <x-movements :coins="$coins" :xp="$xp" />
    </x-settings.layout>
</section>
