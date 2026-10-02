<?php

namespace App\Support;

use App\Models\Setting;
use Illuminate\Support\Facades\Cache;

/**
 * Cuántos mails puede mandar la plataforma (Configuración → Correo). El Gmail del docente tiene un límite
 * diario (~500) que comparte con su otra página: acá hay un interruptor, un tope propio por día y el
 * contador. Vale para todos los mails (avisos, recuperar la clave, verificar el correo): se cancelan en el
 * evento MessageSending (AppServiceProvider). Sin mail, los avisos siguen en la campanita.
 */
class MailBudget
{
    /** Apagado de fábrica: el docente lo prende cuando quiere que salgan mails. */
    public const DEFAULT_ENABLED = false;

    public const DEFAULT_LIMIT = 300;

    public static function enabled(): bool
    {
        return (bool) (int) Setting::get('mail_enabled', self::DEFAULT_ENABLED ? '1' : '0');
    }

    public static function limit(): int
    {
        return max(0, (int) Setting::get('mail_daily_limit', (string) self::DEFAULT_LIMIT));
    }

    private static function key(): string
    {
        return 'mail-sent:'.now()->toDateString();
    }

    public static function sentToday(): int
    {
        return (int) Cache::get(self::key(), 0);
    }

    public static function canSend(): bool
    {
        return self::enabled() && self::sentToday() < self::limit();
    }

    public static function record(): void
    {
        Cache::add(self::key(), 0, now()->addDays(2));
        Cache::increment(self::key());
    }

    /** Gmail avisó que se agotó su límite: no se intenta más hasta mañana. */
    public static function exhaust(): void
    {
        Cache::put(self::key(), max(self::limit(), self::sentToday()), now()->addDays(2));
    }
}
