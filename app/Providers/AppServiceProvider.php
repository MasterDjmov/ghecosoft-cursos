<?php

namespace App\Providers;

use App\Http\Middleware\EnsureCourseOpen;
use App\Http\Middleware\EnsurePasswordChanged;
use App\Models\User;
use App\Support\MailBudget;
use App\Support\TrustedProxies;
use Carbon\CarbonImmutable;
use Illuminate\Mail\Events\MessageSending;
use Illuminate\Mail\Events\MessageSent;
use Illuminate\Support\Facades\Date;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Event;
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

        // También en las acciones de Livewire: con clave provisoria no se hace nada más, y un curso en
        // mantenimiento (D86) frena también las páginas que ya estaban abiertas.
        Livewire::addPersistentMiddleware([EnsurePasswordChanged::class, EnsureCourseOpen::class]);

        // El correo real (SMTP del docente) con interruptor y tope por día: lo que no corresponde no sale.
        Event::listen(MessageSending::class, fn () => config('mail.default') === 'smtp' && ! MailBudget::canSend() ? false : null);
        Event::listen(MessageSent::class, fn () => config('mail.default') === 'smtp' ? MailBudget::record() : null);
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

        // Detrás de Cloudflare: la IP real del alumno (límites de intentos) y el HTTPS.
        TrustedProxies::apply();

        // Regla pedida para la plataforma: mínimo 8, mayúscula, minúscula y número.
        Password::defaults(fn (): Password => Password::min(8)->mixedCase()->numbers());
    }
}
