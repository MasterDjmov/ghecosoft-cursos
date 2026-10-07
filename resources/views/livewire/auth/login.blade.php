<x-layouts::auth :title="__('Log in')">
    <div class="flex flex-col gap-6">
        <x-auth-header :title="__('Log in to your account')" :description="__('Enter your email and password below to log in')" />

        @if (\App\Support\Maintenance::platform())
            {{-- Plataforma en mantenimiento (D86): solo entra el administrador. --}}
            <flux:callout icon="wrench-screwdriver" color="amber" data-test="maintenance-notice">
                <flux:callout.heading>Estamos en mantenimiento</flux:callout.heading>
                <flux:callout.text>{{ \App\Support\Maintenance::message() }}</flux:callout.text>
            </flux:callout>
        @else
            <x-auth-session-status class="text-center" :status="session('status')" />
        @endif

        @if ($notice = session()->pull(\App\Services\SingleSession::NOTICE_KEY))
            <flux:callout icon="shield-exclamation" color="amber" data-test="auth-notice">
                <flux:callout.text>{{ $notice }}</flux:callout.text>
            </flux:callout>
        @endif

        <x-passkey-verify />

        <form method="POST" action="{{ route('login.store') }}" class="flex flex-col gap-6">
            @csrf

            <flux:input
                name="login"
                label="Usuario o email"
                :value="old('login')"
                type="text"
                required
                autofocus
                autocomplete="username"
                placeholder="tu_usuario o email@ejemplo.com"
            />

            <div class="relative">
                <flux:input
                    name="password"
                    :label="__('Password')"
                    type="password"
                    required
                    autocomplete="current-password"
                    :placeholder="__('Password')"
                    viewable
                />

                @if (Route::has('password.request'))
                    <flux:link class="absolute top-0 end-0 text-sm" :href="route('password.request')" wire:navigate>
                        {{ __('Forgot your password?') }}
                    </flux:link>
                @endif
            </div>

            <flux:checkbox name="remember" :label="__('Remember me')" :checked="old('remember')" />

            <flux:button variant="primary" type="submit" class="w-full" data-test="login-button">
                {{ __('Log in') }}
            </flux:button>
        </form>

        <x-teacher-contact />

        <div class="space-x-1 text-center text-sm text-ink-muted">
            <span>{{ __('Don\'t have an account?') }}</span>
            <flux:link :href="route('register')" wire:navigate>{{ __('Sign up') }}</flux:link>
        </div>
    </div>
</x-layouts::auth>
