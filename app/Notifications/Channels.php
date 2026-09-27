<?php

namespace App\Notifications;

/** Siempre en la campanita; por mail solo si hay SMTP configurado (D15). */
class Channels
{
    /** @return list<string> */
    public static function for(): array
    {
        $mailer = config('mail.default');
        $smtp = $mailer === 'smtp' && filled(config('mail.mailers.smtp.host')) && config('mail.mailers.smtp.host') !== '127.0.0.1';

        return $smtp ? ['database', 'mail'] : ['database'];
    }
}
