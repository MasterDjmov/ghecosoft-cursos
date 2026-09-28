<div class="flex flex-col gap-6">
    <x-auth-header title="Elegí tu clave" :description="'Hola, '.auth()->user()->name.'. Entraste con una clave provisoria: cambiala por una que solo sepas vos.'" />

    <form wire:submit="save" class="flex flex-col gap-5">
        <x-password-strength>
            <flux:input wire:model="password" label="Clave nueva" type="password" required autocomplete="new-password" viewable />
        </x-password-strength>

        <flux:input wire:model="password_confirmation" label="Repetí la clave" type="password" required autocomplete="new-password" viewable />

        <flux:button type="submit" variant="primary" class="w-full" data-test="change-password-button">Guardar y entrar</flux:button>
    </form>

    <form method="POST" action="{{ route('logout') }}" class="text-center">
        @csrf
        <flux:button type="submit" variant="ghost" size="sm">Salir</flux:button>
    </form>
</div>
