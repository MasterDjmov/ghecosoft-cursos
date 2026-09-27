<section class="w-full">
    @include('partials.settings-heading')

    <x-settings.layout heading="Datos personales" subheading="Tu héroe, tu nombre, tu usuario y tus datos de contacto">
        {{-- D38: el héroe del alumno --}}
        <form wire:submit="saveHero" class="panel my-6 flex flex-col gap-4 p-5" data-test="hero-form">
            <div class="flex items-center gap-3">
                <span class="grid size-10 place-items-center rounded-full bg-secondary/20 text-secondary-bright"><flux:icon name="sparkles" variant="mini" /></span>
                <div>
                    <flux:heading>Tu héroe</flux:heading>
                    <flux:text class="text-sm">Así te llaman los personajes del curso, y así aparecés en el ranking y en tu CV.</flux:text>
                </div>
            </div>
            <flux:input wire:model="hero_name" label="Nombre del héroe" :placeholder="term('hero.name')" maxlength="20"
                description="De 3 a 20 letras o números. Es único en toda la plataforma: nadie más puede usarlo." />
            <div class="flex items-center justify-between gap-3">
                <flux:text class="text-sm italic">—Bien hecho, {{ $hero_name ?: term('hero.name') }}.</flux:text>
                <flux:button type="submit" variant="primary" icon="check">Guardar héroe</flux:button>
            </div>
        </form>

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
