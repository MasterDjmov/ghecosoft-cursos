<?php

namespace App\Notifications;

use App\Enums\Role;
use App\Models\Course;
use App\Models\User;
use App\Services\TeacherScope;
use Illuminate\Notifications\Messages\MailMessage;
use Illuminate\Notifications\Notification;
use Illuminate\Support\Facades\URL;

/**
 * Aviso simple de la plataforma: título, texto y link. Todas las
 * notificaciones (solicitudes, entregas, comentarios) usan esta forma.
 */
class PlatformNotification extends Notification
{
    /** Avisos que no son de la cuenta (D113): el mail lleva el link de baja y, con la baja, quedan solo en la campanita. */
    public const ANNOUNCEMENTS = ['course.released'];

    public function __construct(
        public readonly string $kind,
        public readonly string $title,
        public readonly string $body,
        public readonly string $url,
        public readonly string $icon = 'bell',
    ) {}

    public function via(object $notifiable): array
    {
        // Sin email (D36), o con la baja de los anuncios (D113), el aviso queda solo en la campanita.
        if (blank($notifiable->email ?? null) || ($this->isAnnouncement() && $notifiable->announcements_muted_at !== null)) {
            return ['database'];
        }

        return Channels::for();
    }

    public function isAnnouncement(): bool
    {
        return in_array($this->kind, self::ANNOUNCEMENTS, true);
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
        $mail = (new MailMessage)
            ->subject($this->title)
            ->greeting('Hola, '.$notifiable->name)
            ->line($this->body)
            ->action('Ver en la plataforma', $this->url);

        // D113: quién lo manda y cómo dejar de recibirlo, en todo mail que no es de la cuenta.
        if ($this->isAnnouncement()) {
            $mail->line('Te llega porque pediste «Avisame» en '.config('app.name').', de '.config('legal.owner').' ('.config('legal.email').').')
                ->line('[No quiero recibir más estos avisos]('.URL::signedRoute('announcements.mute', $notifiable).')');
        }

        return $mail;
    }

    /** Avisa a los administradores (pagos, cuentas, privacidad). */
    public static function toAdmins(self $notification): void
    {
        \Illuminate\Support\Facades\Notification::send(
            User::where('role', Role::Admin)->get(),
            $notification,
        );
    }

    /** Lo de un alumno en un curso (entregas, consultas): a los administradores y a sus docentes (D72). */
    public static function toStaff(self $notification, User $student, Course $course): void
    {
        \Illuminate\Support\Facades\Notification::send(
            User::where('role', Role::Admin)->get()->merge(app(TeacherScope::class)->teachersOf($student, $course))->unique('id'),
            $notification,
        );
    }
}
