<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\View\View;

/**
 * D113: «No quiero recibir más estos avisos», desde el link firmado del mail, sin entrar a la cuenta.
 * El link abre una confirmación (los lectores de correo abren los links solos) y el botón la guarda.
 */
class MuteAnnouncementsController extends Controller
{
    public function show(User $user): View
    {
        return view('legal.mute-announcements', ['user' => $user, 'muted' => $user->announcements_muted_at !== null]);
    }

    public function store(Request $request, User $user): View
    {
        if ($user->announcements_muted_at === null) {
            $user->forceFill(['announcements_muted_at' => now()])->save();
        }

        return view('legal.mute-announcements', ['user' => $user, 'muted' => true]);
    }
}
