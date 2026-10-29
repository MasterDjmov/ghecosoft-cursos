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

            {{-- D114: la fecha dice quién es menor; con menos de 13, su adulto responsable tiene que estar de acuerdo. --}}
            <div class="flex flex-col gap-3"
                x-data="{ birth: @js(old('birth_date', '')), get young() { if (! this.birth) return false; const b = new Date(this.birth + 'T00:00'), t = new Date(); let age = t.getFullYear() - b.getFullYear(); if (t < new Date(t.getFullYear(), b.getMonth(), b.getDate())) age--; return age < {{ \App\Models\User::GUARDIAN_CONSENT_AGE }}; } }">
                <flux:input name="birth_date" label="Fecha de nacimiento" :value="old('birth_date')" type="date" required x-model="birth"
                    :max="now()->subDay()->format('Y-m-d')" description="Para saber si sos menor y cuidar tus datos como corresponde." data-test="register-birth-date" />

                <div x-show="young" x-cloak class="flex flex-col gap-1">
                    <label class="flex items-start gap-2 text-sm text-ink">
                        <input type="checkbox" name="guardian_consent" value="1" @checked(old('guardian_consent')) x-bind:required="young" class="mt-0.5 size-4 shrink-0 accent-primary" data-test="register-guardian-consent">
                        <span>Mi mamá, mi papá o mi tutor sabe que me registro y está de acuerdo.</span>
                    </label>
                    <flux:error name="guardian_consent" />
                </div>
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

            {{-- D112: consentimiento informado (Ley 25.326, art. 5 y 6). --}}
            <div class="flex flex-col gap-1">
                <label class="flex items-start gap-2 text-sm text-ink">
                    <input type="checkbox" name="terms" value="1" @checked(old('terms')) required class="mt-0.5 size-4 shrink-0 accent-primary" data-test="register-terms">
                    <span>
                        Leí y acepto los <a href="{{ route('legal.terms') }}" target="_blank" class="text-primary-bright hover:underline">Términos y condiciones</a>
                        y la <a href="{{ route('legal.privacy') }}" target="_blank" class="text-primary-bright hover:underline">Política de privacidad</a>.
                        Si sos menor, leelos con tu adulto responsable.
                    </span>
                </label>
                <flux:error name="terms" />
            </div>

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
