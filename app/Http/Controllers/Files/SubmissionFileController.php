<?php

namespace App\Http\Controllers\Files;

use App\Http\Controllers\Controller;
use App\Models\Submission;
use Illuminate\Support\Facades\Storage;
use Symfony\Component\HttpFoundation\StreamedResponse;

/** Archivo adjunto de una entrega (disco privado). Siempre como descarga. */
class SubmissionFileController extends Controller
{
    public function __invoke(Submission $submission): StreamedResponse
    {
        $this->authorize('view', $submission);

        abort_unless($submission->file_path && Storage::disk('local')->exists($submission->file_path), 404);

        return Storage::disk('local')->download($submission->file_path, $submission->file_original_name, [
            'X-Content-Type-Options' => 'nosniff',
        ]);
    }
}
