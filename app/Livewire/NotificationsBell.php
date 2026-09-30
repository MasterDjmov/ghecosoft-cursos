<?php

namespace App\Livewire;

use Livewire\Component;

/** Campanita de la barra superior: avisos de solicitudes, entregas, comentarios y mensajes (en vivo, D62). */
class NotificationsBell extends Component
{
    public function open(string $id)
    {
        $notification = auth()->user()->notifications()->findOrFail($id);
        $notification->markAsRead();

        $url = $notification->data['url'] ?? route('home');

        // Solo links de la propia plataforma.
        return str_starts_with($url, url('/')) ? $this->redirect($url, navigate: true) : null;
    }

    public function markAllRead(): void
    {
        auth()->user()->unreadNotifications->markAsRead();
    }

    public function render()
    {
        $user = auth()->user();
        $unread = $user->unreadNotifications()->count();
        $newest = $user->unreadNotifications()->latest()->first();

        // Avisos en vivo (D62): el navegador pone la cantidad en la pestaña y, si el aviso es nuevo,
        // suena y muestra la notificación del sistema según las preferencias del usuario.
        $this->dispatch('live-alerts',
            user: $user->id,
            unread: $unread,
            newest: $newest ? [
                'id' => $newest->id,
                'title' => $newest->data['title'] ?? 'Aviso nuevo',
                'body' => $newest->data['body'] ?? '',
                'url' => $newest->data['url'] ?? route('home'),
            ] : null,
            sound: $user->alert_sound,
            desktop: $user->alert_desktop,
        );

        return view('livewire.notifications-bell', [
            'unread' => $unread,
            'items' => $user->notifications()->latest()->limit(8)->get(),
        ]);
    }
}
