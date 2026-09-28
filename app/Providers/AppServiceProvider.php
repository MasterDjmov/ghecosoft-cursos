<?php

namespace App\Providers;

use App\Http\Middleware\EnsurePasswordChanged;
use App\Models\User;
use Carbon\CarbonImmutable;
use Illuminate\Support\Facades\Date;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Gate;
use Illuminate\Support\Facades\URL;
use Illuminate\Support\ServiceProvider;
use Illuminate\Validation\Rules\Password;
use Livewire\Livewire;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        //
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        $this->configureDefaults();

        // El docente puede ver y hacer todo; las Policies solo deciden por los alumnos.
        Gate::before(fn (User $user) => $user->isAdmin() ? true : null);

        // También en las acciones de Livewire: con clave provisoria no se hace nada más.
        Livewire::addPersistentMiddleware([EnsurePasswordChanged::class]);
    }

    /**
     * Configure default behaviors for production-ready applications.
     */
    protected function configureDefaults(): void
    {
        Date::use(CarbonImmutable::class);

        DB::prohibitDestructiveCommands(
            app()->isProduction(),
        );

        // En el servidor todo va por HTTPS (AutoSSL de cPanel).
        URL::forceHttps(app()->isProduction());

        // Regla pedida para la plataforma: mínimo 8, mayúscula, minúscula y número.
        Password::defaults(fn (): Password => Password::min(8)->mixedCase()->numbers());
    }
}
