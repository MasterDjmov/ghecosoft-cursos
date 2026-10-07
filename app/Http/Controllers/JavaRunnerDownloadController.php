<?php

namespace App\Http\Controllers;

use RuntimeException;
use Symfony\Component\HttpFoundation\BinaryFileResponse;
use ZipArchive;

/**
 * El paquete del Ejecutor de Java para la compu de cada uno (D85): scripts/JavaRunner.java, el lanzador de
 * Windows, el de Linux y Mac, y las instrucciones. Se arma al pedirlo, así siempre lleva la última versión.
 */
class JavaRunnerDownloadController extends Controller
{
    public function __invoke(): BinaryFileResponse
    {
        $zipPath = tempnam(sys_get_temp_dir(), 'ejecutor-java-');
        $zip = new ZipArchive;
        if ($zip->open($zipPath, ZipArchive::OVERWRITE) !== true) {
            throw new RuntimeException('No se pudo armar el paquete del ejecutor.');
        }
        $zip->addFile(base_path('scripts/JavaRunner.java'), 'ejecutor-java/JavaRunner.java');
        foreach (['Iniciar-ejecutor.bat', 'iniciar-ejecutor.sh', 'LEEME.txt'] as $file) {
            $zip->addFile(resource_path('java-runner/'.$file), 'ejecutor-java/'.$file);
        }
        // El lanzador de Linux y Mac, ejecutable.
        $zip->setExternalAttributesName('ejecutor-java/iniciar-ejecutor.sh', ZipArchive::OPSYS_UNIX, 0100755 << 16);
        $zip->close();

        return response()->download($zipPath, 'ejecutor-java.zip', ['Content-Type' => 'application/zip'])->deleteFileAfterSend();
    }
}
