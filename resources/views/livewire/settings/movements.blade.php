<section class="w-full">
    @include('partials.settings-heading')

    <x-settings.layout heading="Movimientos" subheading="Cada moneda y cada punto de experiencia que ganaste o gastaste, curso por curso." wide>
        <livewire:movement-feed :user="auth()->user()" />
    </x-settings.layout>
</section>
