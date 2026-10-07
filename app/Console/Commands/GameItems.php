<?php

namespace App\Console\Commands;

use App\Models\Course;
use App\Models\Item;
use Illuminate\Console\Command;

/**
 * Los ítems de ejemplo del juego (D90): crea los que faltan y nunca toca los que ya están (el docente los
 * edita y les pone imagen desde Admin → Juego → Ítems). Lo corre deploy.sh en cada actualización.
 */
class GameItems extends Command
{
    protected $signature = 'app:game-items';

    protected $description = 'Crea los ítems de ejemplo del juego que falten (no modifica los existentes)';

    /**
     * Por mundo (slug del curso; null = común). Cada fila: code, name, kind, rarity, bonos, price (null = no
     * se vende), min_level, droppable, description.
     */
    public const CATALOG = [
        'python' => [
            // Armas
            ['code' => 'vara-de-junco', 'name' => 'Vara de Junco', 'kind' => 'weapon', 'rarity' => 'common', 'attack' => 2, 'price' => 120, 'min_level' => 1, 'droppable' => true, 'description' => 'Un junco del río, recto y liviano. Para empezar alcanza.'],
            ['code' => 'pluma-de-la-copista', 'name' => 'Pluma de la Copista', 'kind' => 'weapon', 'rarity' => 'common', 'attack' => 3, 'intelligence' => 1, 'price' => 300, 'min_level' => 3, 'droppable' => true, 'description' => 'Escribe runas tan derechas que hasta cortan.'],
            ['code' => 'baculo-del-interprete', 'name' => 'Báculo del Intérprete', 'kind' => 'weapon', 'rarity' => 'rare', 'attack' => 5, 'intelligence' => 2, 'price' => 900, 'min_level' => 6, 'droppable' => true, 'description' => 'Lee cada línea en voz alta antes de lanzarla.'],
            ['code' => 'daga-del-indice-cero', 'name' => 'Daga del Índice Cero', 'kind' => 'weapon', 'rarity' => 'rare', 'attack' => 6, 'dexterity' => 2, 'price' => 1200, 'min_level' => 8, 'droppable' => true, 'description' => 'Siempre empieza a contar desde cero, y siempre acierta al primero.'],
            ['code' => 'cetro-de-la-espiral', 'name' => 'Cetro de la Espiral', 'kind' => 'weapon', 'rarity' => 'epic', 'attack' => 9, 'intelligence' => 4, 'droppable' => true, 'description' => 'Tiene la forma del portal verde. Nadie sabe quién lo talló.'],
            // Ropa
            ['code' => 'tunica-de-aprendiz', 'name' => 'Túnica de Aprendiz', 'kind' => 'armor', 'rarity' => 'common', 'defense' => 2, 'price' => 100, 'min_level' => 1, 'droppable' => true, 'description' => 'La que usan todos los aprendices del Valle.'],
            ['code' => 'capa-del-valle', 'name' => 'Capa del Valle', 'kind' => 'armor', 'rarity' => 'common', 'defense' => 3, 'dexterity' => 1, 'price' => 280, 'min_level' => 3, 'droppable' => true, 'description' => 'Verde como el río; no se moja.'],
            ['code' => 'chaleco-de-escamas', 'name' => 'Chaleco de Escamas', 'kind' => 'armor', 'rarity' => 'rare', 'defense' => 5, 'strength' => 1, 'price' => 850, 'min_level' => 6, 'droppable' => true, 'description' => 'Escamas del Valle cosidas una por una.'],
            ['code' => 'tunica-runica', 'name' => 'Túnica Rúnica', 'kind' => 'armor', 'rarity' => 'rare', 'defense' => 6, 'intelligence' => 2, 'price' => 1300, 'min_level' => 9, 'droppable' => true, 'description' => 'Sus runas se encienden cuando el código corre sin errores.'],
            ['code' => 'manto-de-ofidia', 'name' => 'Manto de Ofidia', 'kind' => 'armor', 'rarity' => 'epic', 'defense' => 9, 'intelligence' => 3, 'luck' => 1, 'droppable' => true, 'description' => 'Una escama del vestido de la guardiana, convertida en manto.'],
            // Accesorios
            ['code' => 'anillo-del-bucle', 'name' => 'Anillo del Bucle', 'kind' => 'accessory', 'rarity' => 'common', 'dexterity' => 1, 'luck' => 1, 'price' => 150, 'min_level' => 2, 'droppable' => true, 'description' => 'Da vueltas en el dedo sin parar, pero sabe cuándo frenar.'],
            ['code' => 'amuleto-del-traceback', 'name' => 'Amuleto del Traceback', 'kind' => 'accessory', 'rarity' => 'rare', 'defense' => 2, 'strength' => 1, 'price' => 700, 'min_level' => 5, 'droppable' => true, 'description' => 'Se lee de abajo hacia arriba, como los errores.'],
            ['code' => 'colgante-de-la-sangria', 'name' => 'Colgante de la Sangría', 'kind' => 'accessory', 'rarity' => 'rare', 'intelligence' => 2, 'price' => 900, 'min_level' => 7, 'droppable' => true, 'description' => 'Cuatro espacios exactos entre cada piedra.'],
            ['code' => 'ojo-del-depurador', 'name' => 'Ojo del Depurador', 'kind' => 'accessory', 'rarity' => 'epic', 'intelligence' => 2, 'luck' => 3, 'droppable' => true, 'description' => 'Ve el error antes de que pase.'],
            // De la historia (los dan las micro-misiones; algunos sirven en el juego)
            ['code' => 'espiral-de-junco', 'name' => 'Espiral de Junco', 'kind' => 'accessory', 'rarity' => 'common', 'dexterity' => 1, 'luck' => 1, 'description' => 'La encontraste al salir del Laberinto de las Siete Salas.'],
            ['code' => 'espejo-del-troll', 'name' => 'Espejo del Troll', 'kind' => 'accessory', 'rarity' => 'rare', 'defense' => 3, 'luck' => 2, 'description' => 'Lo que quedó del troll: muestra si dos cosas son la misma o solo iguales.'],
            ['code' => 'pocion-de-curacion', 'name' => 'Poción de Curación', 'kind' => 'potion', 'rarity' => 'common', 'heal' => 40, 'price' => 30, 'min_level' => 1, 'description' => 'El hechizo de curación escrito una sola vez, embotellado. En las expediciones se toma sola si la vida baja mucho.'],
            ['code' => 'bolsa-de-cuero', 'name' => 'Bolsa de cuero', 'kind' => 'story', 'description' => 'La primera bolsa de Mia, del puesto de Baldo: acá guarda el oro.'],
            ['code' => 'llave-del-puente', 'name' => 'Llave del Puente', 'kind' => 'story', 'description' => 'El Guardián del Puente del Juicio la dejó caer en tu mano.'],
            ['code' => 'morral-de-la-posada', 'name' => 'Morral de la Posada', 'kind' => 'story', 'description' => 'Para llevar lo de toda la compañía.'],
            ['code' => 'el-bestiario', 'name' => 'El Bestiario', 'kind' => 'story', 'description' => 'Regalo del Ermitaño: cada criatura del Valle, con su vida, su ataque y su debilidad.'],
            ['code' => 'cofre-de-los-ecos', 'name' => 'Cofre de los Ecos', 'kind' => 'story', 'description' => 'Del tamaño de una nuez. Si lo acercás al oído, repite lo último que dijiste.'],
            ['code' => 'estante-portatil', 'name' => 'Estante Portátil', 'kind' => 'story', 'description' => 'Para ordenar el pergamino en tomos.'],
            // Materiales de las expediciones (para el crafteo, más adelante)
            ['code' => 'baba-de-slime', 'name' => 'Baba de Slime', 'kind' => 'material', 'rarity' => 'common', 'description' => 'Pegajosa. Huele a comilla sin cerrar.'],
            ['code' => 'diente-de-goblin', 'name' => 'Diente de Goblin', 'kind' => 'material', 'rarity' => 'common', 'description' => 'Un goblin lo perdió mezclando tipos.'],
            ['code' => 'hueso-de-esqueleto', 'name' => 'Hueso de Esqueleto', 'kind' => 'material', 'rarity' => 'common', 'description' => 'De un nombre sin cuerpo.'],
            ['code' => 'colmillo-de-orco', 'name' => 'Colmillo de Orco', 'kind' => 'material', 'rarity' => 'common', 'description' => 'Del que pidió el índice que no estaba.'],
            ['code' => 'musgo-de-troll', 'name' => 'Musgo de Troll', 'kind' => 'material', 'rarity' => 'rare', 'description' => 'Crece debajo de los puentes entre variables.'],
            ['code' => 'garra-de-ogro', 'name' => 'Garra de Ogro', 'kind' => 'material', 'rarity' => 'rare', 'description' => 'El ogro no da error: da esto.'],
        ],
        null => [
            ['code' => 'pocion-grande', 'name' => 'Poción Grande', 'kind' => 'potion', 'rarity' => 'rare', 'heal' => 90, 'price' => 80, 'min_level' => 6, 'description' => 'Sirve en cualquier mundo.'],
            ['code' => Item::RESPEC, 'name' => 'Pergamino del Reinicio', 'kind' => 'special', 'rarity' => 'epic', 'price' => 1500, 'min_level' => 5, 'description' => 'Al usarlo sobre un héroe, deja reacomodar sus puntos del principio una vez.'],
        ],
    ];

    public function handle(): int
    {
        $created = 0;
        foreach (self::CATALOG as $slug => $rows) {
            $course = $slug ? Course::where('slug', $slug)->first() : null;
            if ($slug && ! $course) {
                $this->warn("No está el curso «{$slug}»: salteo sus ítems.");

                continue;
            }
            foreach ($rows as $row) {
                $item = Item::firstOrCreate(['code' => $row['code']], [
                    ...$row,
                    'course_id' => $course?->id,
                    'in_shop' => isset($row['price']),
                    'droppable' => $row['droppable'] ?? false,
                ]);
                $created += (int) $item->wasRecentlyCreated;
            }
        }
        $this->info("Ítems de ejemplo: {$created} nuevos.");

        return self::SUCCESS;
    }
}
