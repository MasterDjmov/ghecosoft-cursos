<?php

namespace App\Http\Controllers;

use App\Models\User;
use App\Support\CvData;
use Illuminate\Http\Response;

/**
 * CV público: /cv/{usuario}. Se ve solo si el alumno lo compartió (y, si es
 * menor, con la autorización aprobada). Si no, "Este perfil es privado" sin
 * revelar ni el nombre. El dueño y el docente lo ven siempre (vista previa).
 */
class CvController extends Controller
{
    public function __invoke(string $username): Response
    {
        $user = User::where('username', $username)->first();
        $viewer = auth()->user();
        $isOwnerOrAdmin = $user && $viewer && ($viewer->id === $user->id || $viewer->isAdmin());

        if (! $user || ! $user->isStudent() || (! $user->hasPublicProfile() && ! $isOwnerOrAdmin)) {
            return response()->view('cv.private', [], 404);
        }

        return response()->view('cv.show', [
            ...CvData::for($user),
            'preview' => ! $user->hasPublicProfile(),
        ]);
    }
}
