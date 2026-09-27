<?php

namespace App\Livewire;

use Livewire\Component;

/** Campanita de la barra superior: avisos de solicitudes, entregas y comentarios. */
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

        return view('livewire.notifications-bell', [
            'unread' => $user->unreadNotifications()->count(),
            'items' => $user->notifications()->latest()->limit(8)->get(),
        ]);
    }
}
