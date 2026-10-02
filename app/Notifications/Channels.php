<?php

namespace App\Notifications;

use App\Support\MailBudget;

/** Siempre en la campanita; por mail solo si hay SMTP configurado (D15), y un mail que falla no rompe nada. */
class Channels
{
    /** @return list<string> */
    public static function for(): array
    {
        $mailer = config('mail.default');
        $smtp = $mailer === 'smtp' && filled(config('mail.mailers.smtp.host')) && config('mail.mailers.smtp.host') !== '127.0.0.1';

        // Con el correo apagado o el tope del día alcanzado (Configuración → Correo), solo la campanita.
        return $smtp && MailBudget::canSend() ? ['database', SafeMailChannel::class] : ['database'];
    }
}
