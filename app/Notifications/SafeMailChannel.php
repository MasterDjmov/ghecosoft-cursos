<?php

namespace App\Notifications;

use App\Support\MailBudget;
use Illuminate\Notifications\Channels\MailChannel;
use Illuminate\Notifications\Notification;
use Throwable;

/**
 * El mail de los avisos, sin romper la página: si el servidor de correo falla (Gmail sin conexión o con el
 * límite diario agotado), el aviso igual quedó en la campanita y el error va solo al registro.
 */
class SafeMailChannel extends MailChannel
{
    public function send($notifiable, Notification $notification)
    {
        try {
            return parent::send($notifiable, $notification);
        } catch (Throwable $e) {
            // «550 5.4.5 Daily user sending limit exceeded»: Gmail no acepta más por hoy.
            if (str_contains($e->getMessage(), '5.4.5') || str_contains(strtolower($e->getMessage()), 'sending limit')) {
                MailBudget::exhaust();
            }
            report($e);

            return null;
        }
    }
}
