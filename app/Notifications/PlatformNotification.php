<?php

namespace App\Notifications;

use App\Enums\Role;
use App\Models\User;
use Illuminate\Notifications\Messages\MailMessage;
use Illuminate\Notifications\Notification;

/**
 * Aviso simple de la plataforma: título, texto y link. Todas las
 * notificaciones (solicitudes, entregas, comentarios) usan esta forma.
 */
class PlatformNotification extends Notification
{
    public function __construct(
        public readonly string $kind,
        public readonly string $title,
        public readonly string $body,
        public readonly string $url,
        public readonly string $icon = 'bell',
    ) {}

    public function via(object $notifiable): array
    {
        return Channels::for();
    }

    /** @return array<string, string> */
    public function toArray(object $notifiable): array
    {
        return [
            'kind' => $this->kind,
            'title' => $this->title,
            'body' => $this->body,
            'url' => $this->url,
            'icon' => $this->icon,
        ];
    }

    public function toMail(object $notifiable): MailMessage
    {
        return (new MailMessage)
            ->subject($this->title)
            ->greeting('Hola, '.$notifiable->name)
            ->line($this->body)
            ->action('Ver en la plataforma', $this->url);
    }

    /** Avisa a todos los docentes. */
    public static function toAdmins(self $notification): void
    {
        \Illuminate\Support\Facades\Notification::send(
            User::where('role', Role::Admin)->get(),
            $notification,
        );
    }
}
