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
            ['code' => 'amuleto-del-traceback', 'name' => 'Amuleto del Traceback', 'kind' => 'accessory', 'rarity' => 'rare', 'defense' => 2, 'strength' => 1, 'price' => 700, 'min_level' => 5, 'droppable' => true, 'description' => 'Se lee de abajo hacia arriba, como los errores. Equipado, en cada expedición te levanta una vez con la mitad de la vida.'],
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
            ['code' => 'notas-del-viajero', 'name' => 'Notas del Viajero', 'kind' => 'story', 'description' => 'Hojas a medio borrar del Sótano del Bastión, con la marca del vitral.'],
            ['code' => 'pluma-del-archivista', 'name' => 'Pluma del Archivista', 'kind' => 'weapon', 'rarity' => 'rare', 'attack' => 7, 'intelligence' => 3, 'description' => 'Lo que quedó del Archivista Corrupto: una pluma de plata que todavía escribe sola.'],
            ['code' => 'pieza-de-vitral', 'name' => 'Pieza de Vitral', 'kind' => 'story', 'description' => 'Plomo y vidrio de colores. No es de ningún reloj, pero encaja en uno.'],
            ['code' => 'escudo-de-las-aserciones', 'name' => 'Escudo de las Aserciones', 'kind' => 'armor', 'rarity' => 'rare', 'defense' => 7, 'strength' => 1, 'description' => 'Del Gremio de Artífices: lo que se prueba, aguanta.'],
            ['code' => 'reloj-de-arena', 'name' => 'Reloj de Arena', 'kind' => 'special', 'rarity' => 'rare', 'price' => 200, 'min_level' => 5, 'description' => 'Termina al instante la expedición que está en camino. Se gasta al usarlo.'],
            ['code' => 'tunica-encendida', 'name' => 'Túnica Encendida', 'kind' => 'armor', 'rarity' => 'epic', 'defense' => 11, 'intelligence' => 4, 'luck' => 2, 'description' => 'La túnica de Mia con todas sus runas encendidas, de los pies a la capucha.'],
            ['code' => 'estante-portatil', 'name' => 'Estante Portátil', 'kind' => 'story', 'description' => 'Para ordenar el pergamino en tomos.'],
            // Materiales de las expediciones (para el crafteo, más adelante)
            ['code' => 'baba-de-slime', 'name' => 'Baba de Slime', 'kind' => 'material', 'rarity' => 'common', 'description' => 'Pegajosa. Huele a comilla sin cerrar.'],
            ['code' => 'diente-de-goblin', 'name' => 'Diente de Goblin', 'kind' => 'material', 'rarity' => 'common', 'description' => 'Un goblin lo perdió mezclando tipos.'],
            ['code' => 'hueso-de-esqueleto', 'name' => 'Hueso de Esqueleto', 'kind' => 'material', 'rarity' => 'common', 'description' => 'De un nombre sin cuerpo.'],
            ['code' => 'colmillo-de-orco', 'name' => 'Colmillo de Orco', 'kind' => 'material', 'rarity' => 'common', 'description' => 'Del que pidió el índice que no estaba.'],
            ['code' => 'musgo-de-troll', 'name' => 'Musgo de Troll', 'kind' => 'material', 'rarity' => 'rare', 'description' => 'Crece debajo de los puentes entre variables.'],
            ['code' => 'garra-de-ogro', 'name' => 'Garra de Ogro', 'kind' => 'material', 'rarity' => 'rare', 'description' => 'El ogro no da error: da esto.'],
            ['code' => 'escama-de-dragon', 'name' => 'Escama de Dragón', 'kind' => 'material', 'rarity' => 'epic', 'description' => 'De las cabezas sueltas de la Hidra y de lo que vigila los lugares más altos del Valle.'],
            // Solo se fabrican en el taller (D93)
            ['code' => 'anillo-de-colmillos', 'name' => 'Anillo de Colmillos', 'kind' => 'accessory', 'rarity' => 'rare', 'defense' => 1, 'strength' => 2, 'luck' => 1, 'description' => 'El Anillo del Bucle, con cinco colmillos de orco engarzados.'],
            ['code' => 'pluma-del-juicio', 'name' => 'Pluma del Juicio', 'kind' => 'weapon', 'rarity' => 'rare', 'attack' => 6, 'intelligence' => 3, 'description' => 'La Pluma de la Copista, endurecida con dientes y huesos: escribe y corta.'],
            ['code' => 'capa-de-musgo', 'name' => 'Capa de Musgo', 'kind' => 'armor', 'rarity' => 'rare', 'defense' => 5, 'dexterity' => 2, 'description' => 'La Capa del Valle, forrada con musgo de troll: nada la atraviesa fácil.'],
            ['code' => 'baculo-de-la-garra', 'name' => 'Báculo de la Garra', 'kind' => 'weapon', 'rarity' => 'epic', 'attack' => 10, 'intelligence' => 4, 'description' => 'El Báculo del Intérprete, con garras de ogro y escamas de dragón.'],
        ],
        'java' => [
            // Armas
            ['code' => 'ganzua-de-bronce', 'name' => 'Ganzúa de Bronce', 'kind' => 'weapon', 'rarity' => 'common', 'attack' => 2, 'price' => 120, 'min_level' => 1, 'droppable' => true, 'description' => 'En el Imperio no abre nada, pero pincha.'],
            ['code' => 'baston-del-aduanero', 'name' => 'Bastón del Aduanero', 'kind' => 'weapon', 'rarity' => 'common', 'attack' => 3, 'strength' => 1, 'price' => 300, 'min_level' => 3, 'droppable' => true, 'description' => 'Con él se marca lo que no está declarado.'],
            ['code' => 'sello-cortante', 'name' => 'Sello Cortante', 'kind' => 'weapon', 'rarity' => 'rare', 'attack' => 5, 'intelligence' => 2, 'price' => 900, 'min_level' => 6, 'droppable' => true, 'description' => 'Un sello de bronce con el borde afilado: aprueba o corta.'],
            ['code' => 'estoque-del-casting', 'name' => 'Estoque del Casting', 'kind' => 'weapon', 'rarity' => 'rare', 'attack' => 6, 'dexterity' => 2, 'price' => 1200, 'min_level' => 8, 'droppable' => true, 'description' => 'Convierte lo que toca al tipo que hace falta.'],
            ['code' => 'compas-de-kaffa', 'name' => 'Compás de Kaffa', 'kind' => 'weapon', 'rarity' => 'epic', 'attack' => 9, 'intelligence' => 4, 'droppable' => true, 'description' => 'Con este compás se trazaron los planos de la capital.'],
            // Ropa
            ['code' => 'capa-de-viajero', 'name' => 'Capa de Viajero', 'kind' => 'armor', 'rarity' => 'common', 'defense' => 2, 'price' => 100, 'min_level' => 1, 'droppable' => true, 'description' => 'La que llevan los que hacen fila en la Aduana.'],
            ['code' => 'chaqueta-de-la-aduana', 'name' => 'Chaqueta de la Aduana', 'kind' => 'armor', 'rarity' => 'common', 'defense' => 3, 'dexterity' => 1, 'price' => 280, 'min_level' => 3, 'droppable' => true, 'description' => 'Azul, de cuello alto y botones de bronce. Nadia diría que no es para cualquiera.'],
            ['code' => 'armadura-de-los-moldes', 'name' => 'Armadura de los Moldes', 'kind' => 'armor', 'rarity' => 'rare', 'defense' => 5, 'strength' => 1, 'price' => 850, 'min_level' => 6, 'droppable' => true, 'description' => 'Salió entera del molde, sin una pieza de menos.'],
            ['code' => 'gabardina-encapsulada', 'name' => 'Gabardina Encapsulada', 'kind' => 'armor', 'rarity' => 'rare', 'defense' => 6, 'intelligence' => 2, 'price' => 1300, 'min_level' => 9, 'droppable' => true, 'description' => 'Lo de adentro no se toca desde afuera.'],
            ['code' => 'manto-imperial', 'name' => 'Manto Imperial', 'kind' => 'armor', 'rarity' => 'epic', 'defense' => 9, 'intelligence' => 3, 'luck' => 1, 'droppable' => true, 'description' => 'Bordado con los planos de todas las catedrales del Imperio.'],
            // Accesorios
            ['code' => 'taza-de-cafe', 'name' => 'Taza de Café', 'kind' => 'accessory', 'rarity' => 'common', 'dexterity' => 1, 'luck' => 1, 'price' => 150, 'min_level' => 2, 'droppable' => true, 'description' => 'Siempre caliente. Kaffa tiene una igual.'],
            ['code' => 'anillo-del-punto-y-coma', 'name' => 'Anillo del Punto y Coma', 'kind' => 'accessory', 'rarity' => 'rare', 'defense' => 2, 'strength' => 1, 'price' => 700, 'min_level' => 5, 'droppable' => true, 'description' => 'Nunca te olvidás de cerrar una instrucción.'],
            ['code' => 'monoculo-del-compilador', 'name' => 'Monóculo del Compilador', 'kind' => 'accessory', 'rarity' => 'rare', 'intelligence' => 2, 'price' => 900, 'min_level' => 7, 'droppable' => true, 'description' => 'Ve el error antes de ejecutar.'],
            ['code' => 'sello-imperial', 'name' => 'Sello Imperial', 'kind' => 'accessory', 'rarity' => 'epic', 'intelligence' => 2, 'luck' => 3, 'droppable' => true, 'description' => 'El que lo lleva pasa cualquier Aduana.'],
            // Pociones y de la historia
            ['code' => 'cafe-fuerte', 'name' => 'Café Fuerte', 'kind' => 'potion', 'rarity' => 'common', 'heal' => 40, 'price' => 30, 'min_level' => 1, 'description' => 'Una taza bien cargada. En las expediciones se toma sola si la vida baja mucho.'],
            ['code' => 'sello-de-entrada', 'name' => 'Sello de Entrada', 'kind' => 'accessory', 'rarity' => 'rare', 'defense' => 1, 'intelligence' => 2, 'luck' => 1, 'description' => 'Te lo dio el Centinela de la Aduana: ya no sos un colado, estás declarado.'],
            ['code' => 'llave-del-vitral', 'name' => 'Llave del Vitral', 'kind' => 'story', 'description' => 'Plomo y vidrios de colores, con una etiqueta: «para quien llegue». No entra en ninguna cerradura del Imperio… todavía.'],
        ],
        null => [
            ['code' => 'pocion-grande', 'name' => 'Poción Grande', 'kind' => 'potion', 'rarity' => 'rare', 'heal' => 90, 'price' => 80, 'min_level' => 6, 'description' => 'Sirve en cualquier mundo.'],
            ['code' => Item::RESPEC, 'name' => 'Pergamino del Reinicio', 'kind' => 'special', 'rarity' => 'epic', 'price' => 1500, 'min_level' => 5, 'description' => 'Al usarlo sobre un héroe, deja reacomodar sus puntos del principio una vez.'],
        ],
    ];

    /**
     * El pedido de imagen de cada ítem de ejemplo (cómo es el objeto); se completa en los que no tienen uno,
     * nunca pisa lo que escribió el docente. El estilo común lo suma Item::fullImagePrompt().
     */
    public const PROMPTS = [
        // Python: el Valle de la Serpiente (neón verde y cian)
        'vara-de-junco' => 'Una vara recta de junco verde del río, atada con cordel en la empuñadura, con una runa pequeña que brilla en la punta.',
        'pluma-de-la-copista' => 'Una pluma larga de escribir, violeta y lila, con punta de metal afilada como un estilete y una cinta de texto holográfico enroscada.',
        'baculo-del-interprete' => 'Un báculo de madera oscura coronado por una serpiente de piedra que sostiene un cristal verde; líneas de código flotan alrededor del cristal.',
        'daga-del-indice-cero' => 'Una daga fina de acero oscuro con un «0» grabado en la hoja que brilla en cian; guardia con forma de corchetes [ ].',
        'cetro-de-la-espiral' => 'Un cetro de plata con una espiral de luz verde en la punta, como un portal en miniatura que gira; escamas grabadas en el mango.',
        'tunica-de-aprendiz' => 'Una túnica sencilla de aprendiz, gris oscuro, doblada con prolijidad, con un borde verde apagado y una runa cosida en el pecho.',
        'capa-del-valle' => 'Una capa verde musgo con capucha, flotando como si la moviera el viento, con gotas de agua que resbalan sin mojarla.',
        'chaleco-de-escamas' => 'Un chaleco de cuero cubierto de escamas verdes superpuestas, cosidas una por una, con remaches de bronce.',
        'tunica-runica' => 'Una túnica larga azul oscuro con runas bordadas en hilo de luz cian que se encienden en hileras, colgada de un perchero de bronce.',
        'manto-de-ofidia' => 'Un manto amplio de escamas esmeralda y doradas, con una gran escama brillante en el broche, que ondula como el cuerpo de una serpiente.',
        'anillo-del-bucle' => 'Un anillo de plata con forma de flecha circular que vuelve sobre sí misma, con una piedrita verde que gira despacio.',
        'amuleto-del-traceback' => 'Un amuleto con forma de pergamino enroscado colgado de una cadena, con una línea de traceback grabada que brilla en violeta de abajo hacia arriba.',
        'colgante-de-la-sangria' => 'Un colgante con cuatro piedras cian alineadas a la misma distancia exacta, en un marco de plata rectangular.',
        'ojo-del-depurador' => 'Un monóculo dorado con un ojo de luz violeta en el lente, rodeado de pequeños engranajes y un insecto de metal posado en el borde.',
        'espiral-de-junco' => 'Una espiral tejida con junco verde, del tamaño de una mano, con una lucecita en el centro.',
        'espejo-del-troll' => 'Un espejo de mano ovalado, con marco de piedra cubierto de musgo, que refleja dos imágenes iguales desfasadas.',
        'pocion-de-curacion' => 'Un frasco redondo de vidrio con líquido verde luminoso, tapón de corcho y una etiqueta con una cruz.',
        'bolsa-de-cuero' => 'Una bolsita de cuero marrón atada con cordón, con algunas monedas de oro asomando.',
        'llave-del-puente' => 'Una llave grande de piedra negra con la cabeza en forma de serpiente enroscada y ojos verdes de musgo.',
        'morral-de-la-posada' => 'Un morral de lona gastado con muchas correas y parches, con una jarrita colgando del costado.',
        'el-bestiario' => 'Un libro grueso de tapas de cuero verde con dibujos de criaturas en relieve y un monóculo de luz cian apoyado encima.',
        'cofre-de-los-ecos' => 'Un cofrecito del tamaño de una nuez, de bronce, con ondas de sonido talladas en la tapa que vibran en cian.',
        'estante-portatil' => 'Un estante plegable de madera clara, abierto en tres tomos, con tiras de luz que separan cada libro.',
        'notas-del-viajero' => 'Un manojo de hojas viejas, húmedas y a medio borrar, atadas con un hilo, con la marca de agua de un pequeño vitral.',
        'pluma-del-archivista' => 'Una pluma de plata que escribe sola en el aire una línea de tinta violeta; restos de papel picado flotando alrededor.',
        'pieza-de-vitral' => 'Un fragmento de vitral de plomo y vidrios de colores, del tamaño de una moneda grande, que proyecta luces de colores.',
        'escudo-de-las-aserciones' => 'Un escudo redondo de bronce con una gran marca de verificación grabada en el centro que brilla en verde; remaches como engranajes.',
        'reloj-de-arena' => 'Un reloj de arena chiquito de bronce y vidrio, con arena verde luminosa que cae hacia arriba.',
        'tunica-encendida' => 'Una túnica de maga violeta oscura con todas sus runas encendidas en violeta brillante, de los pies a la capucha, que flota con luz propia.',
        'baba-de-slime' => 'Un frasquito con una gota de baba verde pegajosa y translúcida, con burbujas adentro.',
        'diente-de-goblin' => 'Un diente amarillento y puntiagudo de goblin, con una monedita pegada.',
        'hueso-de-esqueleto' => 'Un hueso blanco con runas apagadas grabadas, partido en una punta.',
        'colmillo-de-orco' => 'Un colmillo grande y curvo de orco, con una muesca en la base.',
        'musgo-de-troll' => 'Un puñado de musgo verde oscuro con pequeñas piedras incrustadas, que brilla apenas.',
        'garra-de-ogro' => 'Una garra gruesa y gris de ogro, con la uña rota.',
        'escama-de-dragon' => 'Una escama grande de dragón, verde oscuro iridiscente, con bordes que brillan como brasas.',
        'anillo-de-colmillos' => 'Un anillo de plata grueso con cinco colmillos pequeños de orco engarzados alrededor de una piedra verde.',
        'pluma-del-juicio' => 'Una pluma de escribir violeta con la punta de diente afilado y el cañón reforzado con anillos de hueso tallado.',
        'capa-de-musgo' => 'Una capa verde con capucha, forrada por dentro con musgo de troll que brilla apenas, con piedritas incrustadas.',
        'baculo-de-la-garra' => 'Un báculo de madera oscura con una serpiente de piedra en la punta, rodeada de tres garras de ogro y escamas de dragón que brillan como brasas.',
        // Java: el Imperio de las Clases (dorado de las catedrales y rojo de Zed)
        'ganzua-de-bronce' => 'Una ganzúa larga de bronce con el mango envuelto en cuero negro y un brillo rojo en la punta.',
        'baston-del-aduanero' => 'Un bastón de madera oscura con puntera y empuñadura de bronce, con el escudo de la Aduana grabado.',
        'sello-cortante' => 'Un sello de bronce grande, de mango largo, con el borde afilado como una hoja y la palabra «APROBADO» en relieve.',
        'estoque-del-casting' => 'Un estoque fino de acero con la guarda en forma de paréntesis ( ) y runas doradas en la hoja.',
        'compas-de-kaffa' => 'Un compás de arquitecto enorme, de bronce y oro, con una punta que deja una estela de luz dorada.',
        'capa-de-viajero' => 'Una capa marrón gastada de viajero, con capucha y un parche con el sello de la Aduana.',
        'chaqueta-de-la-aduana' => 'Una chaqueta azul oscuro de cuello alto con botones de bronce y vivos dorados, doblada con prolijidad.',
        'armadura-de-los-moldes' => 'Una armadura de placas gris acero, perfecta y simétrica, con las marcas del molde todavía visibles.',
        'gabardina-encapsulada' => 'Una gabardina negra larga con candados dorados pequeños en los bolsillos y el cuello alto.',
        'manto-imperial' => 'Un manto rojo profundo con planos de catedrales bordados en hilo de oro que brillan.',
        'taza-de-cafe' => 'Una taza de cerámica blanca con borde dorado, café humeante y un hilo de vapor que dibuja un engranaje.',
        'anillo-del-punto-y-coma' => 'Un anillo de bronce con un punto y coma ; de rubí engarzado.',
        'monoculo-del-compilador' => 'Un monóculo dorado con el lente rojo, que proyecta una línea de código marcada en rojo.',
        'sello-imperial' => 'Un sello de lacre dorado con el escudo del Imperio, colgado de una cadena fina.',
        'cafe-fuerte' => 'Un vaso de vidrio grueso con café negro humeante y una franja dorada, con una etiqueta con una cruz.',
        'sello-de-entrada' => 'Un sello de bronce antiguo con mango de piedra gris y la palabra «DECLARADO» en relieve, con un brillo azul en el borde.',
        'llave-del-vitral' => 'Una llave antigua de plomo con la cabeza hecha de vidrios de colores, como un vitral pequeño, con una etiqueta de papel atada.',
        // Comunes (sirven en cualquier mundo)
        'pocion-grande' => 'Un frasco grande de vidrio facetado con líquido rojo y dorado luminoso, tapón lacrado.',
        Item::RESPEC => 'Un pergamino enrollado con sello de cera dorado, del que salen flechas de luz que vuelven al centro.',
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
                if (! $item->image_prompt && isset(self::PROMPTS[$item->code])) {
                    $item->update(['image_prompt' => self::PROMPTS[$item->code]]);
                }
            }
        }
        $this->info("Ítems de ejemplo: {$created} nuevos.");

        return self::SUCCESS;
    }
}
