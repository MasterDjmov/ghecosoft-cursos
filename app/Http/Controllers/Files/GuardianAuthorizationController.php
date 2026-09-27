<?php

namespace App\Http\Controllers\Files;

use App\Http\Controllers\Controller;
use App\Models\GuardianAuthorization;
use Illuminate\Support\Facades\Storage;
use Symfony\Component\HttpFoundation\StreamedResponse;

/** Nota de autorización de un menor (disco privado). */
class GuardianAuthorizationController extends Controller
{
    public function __invoke(GuardianAuthorization $authorization): StreamedResponse
    {
        $this->authorize('view', $authorization);

        abort_unless(Storage::disk('local')->exists($authorization->file_path), 404);

        return Storage::disk('local')->response($authorization->file_path, $authorization->original_name, [
            'X-Content-Type-Options' => 'nosniff',
            'Content-Security-Policy' => "default-src 'none'; img-src 'self'; style-src 'unsafe-inline'",
        ]);
    }
}
