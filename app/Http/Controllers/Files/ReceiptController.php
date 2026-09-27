<?php

namespace App\Http\Controllers\Files;

use App\Http\Controllers\Controller;
use App\Models\EnrollmentRequest;
use Illuminate\Support\Facades\Storage;
use Symfony\Component\HttpFoundation\StreamedResponse;

/** Comprobante de pago de una solicitud (disco privado). */
class ReceiptController extends Controller
{
    public function __invoke(EnrollmentRequest $request): StreamedResponse
    {
        $this->authorize('view', $request);

        abort_unless($request->receipt_path && Storage::disk('local')->exists($request->receipt_path), 404);

        // Imágenes y PDF se muestran en el navegador; el resto se descarga.
        return Storage::disk('local')->response($request->receipt_path, $request->receipt_original_name, [
            'X-Content-Type-Options' => 'nosniff',
            'Content-Security-Policy' => "default-src 'none'; img-src 'self'; style-src 'unsafe-inline'",
        ]);
    }
}
