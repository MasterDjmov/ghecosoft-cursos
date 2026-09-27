<?php

namespace App\Http\Controllers\Files;

use App\Enums\ResourceType;
use App\Http\Controllers\Controller;
use App\Models\NodeResource;
use Illuminate\Support\Facades\Storage;
use Symfony\Component\HttpFoundation\StreamedResponse;

/** Descarga de archivos de un nodo (disco privado). */
class NodeResourceController extends Controller
{
    public function __invoke(NodeResource $resource): StreamedResponse
    {
        $this->authorize('view', $resource);

        abort_unless($resource->type === ResourceType::File && Storage::disk('local')->exists($resource->file_path), 404);

        return Storage::disk('local')->download($resource->file_path, $resource->original_name, [
            'X-Content-Type-Options' => 'nosniff',
        ]);
    }
}
