<x-layouts::auth :title="__('Register')">
    <div class="flex flex-col gap-6">
        <x-auth-header :title="__('Create an account')" :description="__('Enter your details below to create your account')" />

        @if (\App\Support\Maintenance::platform())
            <flux:callout icon="wrench-screwdriver" color="amber" data-test="maintenance-notice">
                <flux:callout.heading>Estamos en mantenimiento</flux:callout.heading>
                <flux:callout.text>{{ \App\Support\Maintenance::message() }} Por ahora no se pueden crear cuentas nuevas.</flux:callout.text>
            </flux:callout>
        @endif

        <x-auth-session-status class="text-center" :status="session('status')" />

        <form method="POST" action="{{ route('register.store') }}" class="flex flex-col gap-5">
            @csrf

            <div class="grid gap-5 sm:grid-cols-2">
                <flux:input name="name" :label="__('Name')" :value="old('name')" type="text" required autofocus autocomplete="given-name" placeholder="Tu nombre" />
                <flux:input name="last_name" label="Apellido" :value="old('last_name')" type="text" required autocomplete="family-name" placeholder="Tu apellido" />
            </div>

            <flux:input
                name="username"
                label="Usuario"
                :value="old('username')"
                type="text"
                required
                autocomplete="username"
                placeholder="kira_perez"
                description="Minúsculas, números, - y _. Es también el link de tu CV."
            />

            <div class="grid gap-5 sm:grid-cols-2">
                <flux:input name="email" label="Email (opcional)" :value="old('email')" type="email" autocomplete="email" placeholder="email@ejemplo.com"
                    description="Para recuperar la clave." />
                <flux:input name="phone" label="Teléfono (opcional)" :value="old('phone')" type="tel" autocomplete="tel" placeholder="+54 9 380 412-3456"
                    description="Para que el profe te escriba." />
            </div>

            <x-password-strength>
                <flux:input
                    name="password"
                    :label="__('Password')"
                    type="password"
                    required
                    autocomplete="new-password"
                    :placeholder="__('Password')"
                    viewable
                />
            </x-password-strength>

            <flux:input
                name="password_confirmation"
                :label="__('Confirm password')"
                type="password"
                required
                autocomplete="new-password"
                :placeholder="__('Confirm password')"
                viewable
            />

            <flux:button type="submit" variant="primary" class="w-full" data-test="register-user-button">
                {{ __('Create account') }}
            </flux:button>
        </form>

        <div class="space-x-1 text-center text-sm text-ink-muted">
            <span>{{ __('Already have an account?') }}</span>
            <flux:link :href="route('login')" wire:navigate>{{ __('Log in') }}</flux:link>
        </div>
    </div>
</x-layouts::auth>
