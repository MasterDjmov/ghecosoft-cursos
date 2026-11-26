<?php

namespace App\Console\Commands;

use App\Models\Item;
use App\Models\NodeStep;
use App\Services\Inventory;
use App\Support\PracticeReferences;
use Illuminate\Console\Attributes\Description;
use Illuminate\Console\Attributes\Signature;
use Illuminate\Console\Command;
use Illuminate\Support\Str;

/**
 * Carga de una vez las imágenes de los ítems (lo mismo que subirlas una por una en Admin → Ítems).
 * Reconoce cada archivo por el código del ítem: vara-de-junco.jpg, vitral-de-iris.png… Los ítems que ya
 * tienen imagen no se tocan, salvo con --replace. El ítem de historia de una micro-misión («item: Fotograma
 * Congelado») se crea recién cuando alguien lo gana; si el archivo tiene su código (curso-nombre), se crea acá
 * para poder ponerle la imagen antes.
 */
#[Signature('app:item-images {path : Carpeta con las imágenes} {--apply : Guardar (sin esto, solo muestra qué haría)} {--replace : Reemplazar también las que ya tienen imagen}')]
#[Description('Carga las imágenes de los ítems por el código del ítem')]
class ItemImages extends Command
{
    public function handle(): int
    {
        $folder = rtrim((string) $this->argument('path'), '/');
        $images = collect(glob($folder.'/*.{jpg,jpeg,png,webp}', GLOB_BRACE))
            ->keyBy(fn ($path) => pathinfo($path, PATHINFO_FILENAME));
        if ($images->isEmpty()) {
            $this->error("No hay imágenes en {$folder}.");

            return self::FAILURE;
        }

        $items = Item::whereIn('code', $images->keys())->get()->keyBy('code');
        $stories = $this->storyItems($images->keys()->diff($items->keys())->all());
        $rows = [];
        $saved = 0;
        foreach ($images as $code => $path) {
            $item = $items[$code] ?? null;
            if (! $item && isset($stories[$code])) {
                if (! $this->option('apply')) {
                    $rows[] = [basename($path), $stories[$code]->item, 'ítem de historia: se crea con la imagen'];

                    continue;
                }
                $item = app(Inventory::class)->stepItem($stories[$code])[0];
            }
            if (! $item) {
                $rows[] = [basename($path), '—', 'no hay un ítem con ese código: se saltea'];

                continue;
            }
            if ($item->image_path && ! $this->option('replace')) {
                $rows[] = [basename($path), $item->name, 'ya tiene imagen: se saltea (--replace para cambiarla)'];

                continue;
            }
            if ($problem = PracticeReferences::check($path)) {
                $rows[] = [basename($path), $item->name, $problem.': se saltea'];

                continue;
            }

            $rows[] = [basename($path), $item->name, $item->image_path ? 'reemplaza la imagen' : 'imagen nueva'];
            if (! $this->option('apply')) {
                continue;
            }

            $item->update(['image_path' => PracticeReferences::store($path)]);
            $saved++;
        }

        $this->table(['Archivo', 'Ítem', ''], $rows);
        if ($this->option('apply')) {
            $this->info("Listo: {$saved} imágenes cargadas.");
        } else {
            $this->comment('Para guardar, repetí el comando con --apply.');
        }

        return self::SUCCESS;
    }

    /**
     * Las micro-misiones cuyo ítem de historia tendría alguno de esos códigos (el mismo que arma
     * Inventory::stepItem: el slug del curso y el del nombre).
     *
     * @param  list<string>  $codes
     * @return array<string, NodeStep>
     */
    private function storyItems(array $codes): array
    {
        if ($codes === []) {
            return [];
        }

        return NodeStep::whereNotNull('item')->where('item', '!=', '')->with('node.course')->get()->toBase()
            ->mapWithKeys(function (NodeStep $step) {
                $name = trim((string) preg_replace('/\s+x\d+$/iu', '', trim((string) $step->item)));

                return [Str::limit($step->node->course->slug.'-'.Str::slug($name), 80, '') => $step];
            })
            ->only($codes)
            ->all();
    }
}
