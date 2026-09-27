<section class="w-full">
    @include('partials.settings-heading')

    <x-settings.layout heading="Datos personales" subheading="Tu nombre, tu usuario y tus datos de contacto">
        <form wire:submit="updateProfileInformation" class="my-6 w-full space-y-6">
            <div class="grid gap-6 sm:grid-cols-2">
                <flux:input wire:model="name" :label="__('Name')" type="text" required autocomplete="given-name" />
                <flux:input wire:model="last_name" label="Apellido" type="text" required autocomplete="family-name" />
            </div>

            <flux:input wire:model="username" label="Usuario" type="text" required autocomplete="username"
                description="También es el link de tu CV: /cv/{{ $username ?: 'tu_usuario' }}" />

            <flux:input wire:model="email" :label="__('Email')" type="email" required autocomplete="email" />

            <div class="grid gap-6 sm:grid-cols-2">
                <flux:input wire:model="phone" label="Teléfono (opcional)" type="tel" autocomplete="tel" />
                <flux:input wire:model="birth_date" label="Fecha de nacimiento (opcional)" type="date" />
            </div>

            <flux:input wire:model="dni" label="DNI (opcional)" type="text" inputmode="numeric"
                description="Solo números. Se usará si más adelante la plataforma emite certificados." />

            <flux:button variant="primary" type="submit">{{ __('Save') }}</flux:button>
        </form>
    </x-settings.layout>
</section>
