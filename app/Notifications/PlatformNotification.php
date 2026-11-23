<?php

namespace App\Notifications;

use App\Enums\Role;
use App\Models\Course;
use App\Models\User;
use App\Services\TeacherScope;
use App\Support\WhatsAppAlert;
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

    /** Los que además le llegan al WhatsApp del docente (CallMeBot): una cuenta nueva y un pedido de abono. */
    public const WHATSAPP = ['user.registered', 'request.new'];

    public function __construct(
        public readonly string $kind,
        public readonly string $title,
        public readonly string $body,
        public readonly string $url,
        public readonly string $icon = 'bell',
        // A quién le llega si el alumno contesta el mail (el docente que le escribió).
        public readonly ?string $replyTo = null,
        public readonly ?string $replyName = null,
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
        if (filled($this->replyTo)) {
            $mail->replyTo($this->replyTo, $this->replyName);
        }

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
        if (in_array($notification->kind, self::WHATSAPP, true)) {
            // El registro lleva el mail y el teléfono en el texto: al WhatsApp va solo el título (con el nombre).
            $extra = $notification->kind === 'request.new' ? "\n".$notification->body : '';
            WhatsAppAlert::queue('*'.$notification->title.'*'.$extra."\n".$notification->url);
        }

        \Illuminate\Support\Facades\Notification::send(
            User::where('role', Role::Admin)->get(),
            $notification,
        );
    }

    /** Lo de un alumno que no es de un curso (D124, Mis prácticas): a los administradores y a todos sus docentes. */
    public static function toStaffOf(self $notification, User $student): void
    {
        \Illuminate\Support\Facades\Notification::send(
            User::where('role', Role::Admin)->get()->merge(app(TeacherScope::class)->allTeachersOf($student))->unique('id'),
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
