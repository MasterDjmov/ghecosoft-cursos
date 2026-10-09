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
            // Solo se fabrican en el taller (D93)
            ['code' => 'taza-encantada', 'name' => 'Taza Encantada', 'kind' => 'accessory', 'rarity' => 'rare', 'defense' => 1, 'dexterity' => 2, 'luck' => 1, 'description' => 'La Taza de Café con cinco colmillos de orco de asa: el café nunca se enfría.'],
            ['code' => 'sello-dentado', 'name' => 'Sello Dentado', 'kind' => 'weapon', 'rarity' => 'rare', 'attack' => 6, 'intelligence' => 3, 'description' => 'El Bastón del Aduanero con dientes y huesos en la punta: sella y muerde.'],
            ['code' => 'chaqueta-forrada', 'name' => 'Chaqueta Forrada', 'kind' => 'armor', 'rarity' => 'rare', 'defense' => 5, 'dexterity' => 2, 'description' => 'La Chaqueta de la Aduana forrada con musgo de troll: nada la atraviesa fácil.'],
            ['code' => 'estoque-de-la-garra', 'name' => 'Estoque de la Garra', 'kind' => 'weapon', 'rarity' => 'epic', 'attack' => 10, 'dexterity' => 4, 'description' => 'El Estoque del Casting con garras de ogro y escamas de dragón: convierte y corta.'],
            ['code' => 'llave-maestra', 'name' => 'Llave Maestra', 'kind' => 'weapon', 'rarity' => 'epic', 'attack' => 11, 'intelligence' => 4, 'luck' => 2, 'description' => 'La ganzúa de Zed, transformada al vencer al Dragón del Imperio: abre las puertas que se abren con contratos.'],
            ['code' => 'remo-de-las-corrientes', 'name' => 'Remo de las Corrientes', 'kind' => 'weapon', 'rarity' => 'epic', 'attack' => 9, 'dexterity' => 3, 'strength' => 1, 'description' => 'Lo soltó el Leviatán de los Datos: con él, las corrientes del río te obedecen.'],
            ['code' => 'vitral-del-viajero', 'name' => 'Vitral del Viajero', 'kind' => 'story', 'description' => 'Lo hizo el Vidriero y viajaba en la barcaza Ceibo. La etiqueta dice: «para la ventana más alta de la Torre del Arquitecto».'],
            ['code' => 'amuleto-de-la-campana', 'name' => 'Amuleto de la Campana', 'kind' => 'accessory', 'rarity' => 'rare', 'defense' => 2, 'strength' => 1, 'price' => 700, 'min_level' => 5, 'droppable' => true, 'description' => 'Una campanita de bronce: para que escuches siempre las alarmas. Equipado, en cada expedición te levanta una vez con la mitad de la vida.'],
            ['code' => 'linterna-del-espectro', 'name' => 'Linterna del Espectro', 'kind' => 'accessory', 'rarity' => 'epic', 'defense' => 2, 'intelligence' => 3, 'luck' => 2, 'description' => 'La dejó el Espectro Nulo al apagarse: ilumina donde algo debería estar.'],
            ['code' => 'guantes-del-artesano', 'name' => 'Guantes del Artesano', 'kind' => 'accessory', 'rarity' => 'rare', 'defense' => 2, 'strength' => 1, 'dexterity' => 1, 'description' => 'Te los dio la Maestra de Moldes al vencer a la Quimera: sos aprendiz de la Academia.'],
            ['code' => 'sello-de-entrada', 'name' => 'Sello de Entrada', 'kind' => 'accessory', 'rarity' => 'rare', 'defense' => 1, 'intelligence' => 2, 'luck' => 1, 'description' => 'Te lo dio el Centinela de la Aduana: ya no sos un colado, estás declarado.'],
            ['code' => 'llave-del-vitral', 'name' => 'Llave del Vitral', 'kind' => 'story', 'description' => 'Plomo y vidrios de colores, con una etiqueta: «para quien llegue». No entra en ninguna cerradura del Imperio… todavía.'],
        ],
        'c' => [
            // Las Forjas (docs/historias/c.md): el carro de Chispa. Armas
            ['code' => 'espada-de-practica', 'name' => 'Espada de Práctica', 'kind' => 'weapon', 'rarity' => 'common', 'attack' => 2, 'price' => 120, 'min_level' => 1, 'droppable' => true, 'description' => 'Hierro sin templar, para aprender a medir el golpe. Chispa jura que es «casi nueva».'],
            ['code' => 'martillo-de-aprendiz', 'name' => 'Martillo de Aprendiz', 'kind' => 'weapon', 'rarity' => 'common', 'attack' => 3, 'strength' => 1, 'price' => 300, 'min_level' => 3, 'droppable' => true, 'description' => 'En la Forja cada uno tiene el suyo y nadie presta el propio. Este es tuyo.'],
            ['code' => 'sable-del-desborde', 'name' => 'Sable del Desborde', 'kind' => 'weapon', 'rarity' => 'rare', 'attack' => 5, 'intelligence' => 2, 'price' => 900, 'min_level' => 6, 'droppable' => true, 'description' => 'Corta hasta 255. Al 256, vuelve a cero.'],
            ['code' => 'florete-del-puntero', 'name' => 'Florete del Puntero', 'kind' => 'weapon', 'rarity' => 'rare', 'attack' => 6, 'dexterity' => 2, 'price' => 1200, 'min_level' => 8, 'droppable' => true, 'description' => 'Apunta exacto a la dirección. Nunca a NULL.'],
            ['code' => 'martillo-de-ferrum', 'name' => 'Martillo de Ferrum', 'kind' => 'weapon', 'rarity' => 'epic', 'attack' => 9, 'intelligence' => 4, 'droppable' => true, 'description' => 'Una copia del de Maese Ferrum, forjada por él mismo. El original no se presta.'],
            // Ropa
            ['code' => 'delantal-de-cuero', 'name' => 'Delantal de Cuero', 'kind' => 'armor', 'rarity' => 'common', 'defense' => 2, 'price' => 100, 'min_level' => 1, 'droppable' => true, 'description' => 'El de todos los aprendices de la Forja, con un bolsillo para la tiza.'],
            ['code' => 'chaleco-de-minero', 'name' => 'Chaleco de Minero', 'kind' => 'armor', 'rarity' => 'common', 'defense' => 3, 'dexterity' => 1, 'price' => 280, 'min_level' => 3, 'droppable' => true, 'description' => 'Reforzado como el de Hulda: las vagonetas no perdonan.'],
            ['code' => 'cota-alineada', 'name' => 'Cota Alineada', 'kind' => 'armor', 'rarity' => 'rare', 'defense' => 5, 'strength' => 1, 'price' => 850, 'min_level' => 6, 'droppable' => true, 'description' => 'Cada anillo en su lugar y ni un byte de relleno de más.'],
            ['code' => 'capa-ignifuga', 'name' => 'Capa Ignífuga', 'kind' => 'armor', 'rarity' => 'rare', 'defense' => 6, 'intelligence' => 2, 'price' => 1300, 'min_level' => 9, 'droppable' => true, 'description' => 'Pasa entre la lava sin chamuscarse. Tizón la midió dos veces.'],
            ['code' => 'armadura-de-la-fragua', 'name' => 'Armadura de la Fragua', 'kind' => 'armor', 'rarity' => 'epic', 'defense' => 9, 'intelligence' => 3, 'luck' => 1, 'droppable' => true, 'description' => 'Templada placa por placa en la fragua más honda.'],
            // Accesorios
            ['code' => 'calibre-de-bronce', 'name' => 'Calibre de Bronce', 'kind' => 'accessory', 'rarity' => 'common', 'dexterity' => 1, 'luck' => 1, 'price' => 150, 'min_level' => 2, 'droppable' => true, 'description' => 'Como el de Tizón. Lo vas a terminar usando para medir la sopa.'],
            ['code' => 'anillo-del-sizeof', 'name' => 'Anillo del sizeof', 'kind' => 'accessory', 'rarity' => 'rare', 'defense' => 2, 'strength' => 1, 'price' => 700, 'min_level' => 5, 'droppable' => true, 'description' => 'Sabe cuánto pesa cada cosa antes de levantarla.'],
            ['code' => 'antiparras-del-depurador', 'name' => 'Antiparras del Depurador', 'kind' => 'accessory', 'rarity' => 'rare', 'intelligence' => 2, 'price' => 900, 'min_level' => 7, 'droppable' => true, 'description' => 'Ven el comportamiento indefinido antes de que pase.'],
            ['code' => 'sello-del-yunque', 'name' => 'Sello del Yunque', 'kind' => 'accessory', 'rarity' => 'epic', 'intelligence' => 2, 'luck' => 3, 'droppable' => true, 'description' => 'Dos golpes en el yunque grabados en bronce: el aplauso de Ferrum.'],
            // Pociones
            ['code' => 'sopa-de-tizon', 'name' => 'Sopa de Tizón', 'kind' => 'potion', 'rarity' => 'common', 'heal' => 40, 'price' => 30, 'min_level' => 1, 'description' => 'Medida al mililitro. En las expediciones se toma sola si la vida baja mucho.'],
            // Solo se fabrican en el taller (D93)
            ['code' => 'calibre-afilado', 'name' => 'Calibre Afilado', 'kind' => 'accessory', 'rarity' => 'rare', 'defense' => 1, 'dexterity' => 2, 'luck' => 1, 'description' => 'El Calibre de Bronce con puntas de colmillo de orco: mide y pincha.'],
            ['code' => 'martillo-dentado', 'name' => 'Martillo Dentado', 'kind' => 'weapon', 'rarity' => 'rare', 'attack' => 6, 'intelligence' => 3, 'description' => 'El Martillo de Aprendiz con dientes de goblin y huesos en la cabeza: cada golpe deja marca.'],
            ['code' => 'chaleco-acolchado', 'name' => 'Chaleco Acolchado', 'kind' => 'armor', 'rarity' => 'rare', 'defense' => 5, 'dexterity' => 2, 'description' => 'El Chaleco de Minero forrado con musgo de troll: ni una piedra lo atraviesa.'],
            ['code' => 'florete-de-la-garra', 'name' => 'Florete de la Garra', 'kind' => 'weapon', 'rarity' => 'epic', 'attack' => 10, 'dexterity' => 4, 'description' => 'El Florete del Puntero con garras de ogro y escamas de dragón: apunta y corta.'],
            // Lo que gana Kira en la historia
            ['code' => 'espada-rajada', 'name' => 'Espada Rajada', 'kind' => 'story', 'description' => 'La espada de aprendiz de Kira, rajada de punta a mango contra un portón que se abría tirando.'],
            ['code' => 'espada-reforjada', 'name' => 'Espada Reforjada', 'kind' => 'weapon', 'rarity' => 'rare', 'attack' => 6, 'strength' => 2, 'description' => 'Maese Ferrum la reforjó al caer el Gólem de Escoria: «La próxima la forjás vos».'],
            ['code' => Item::CORE_DUMP, 'name' => 'Amuleto del Volcado', 'kind' => 'accessory', 'rarity' => 'rare', 'defense' => 2, 'strength' => 1, 'price' => 700, 'min_level' => 5, 'droppable' => true, 'description' => 'Hulda te lo colgó al cuello después de tu primera caída: guarda lo que pasó antes de cada golpe. Equipado, en cada expedición te levanta una vez con la mitad de la vida.'],
            ['code' => 'hilo-de-las-direcciones', 'name' => 'Hilo de las Direcciones', 'kind' => 'accessory', 'rarity' => 'rare', 'dexterity' => 2, 'intelligence' => 1, 'luck' => 1, 'description' => 'Un hilo de cobre de la tela de la Araña: siempre sabe adónde va.'],
            ['code' => 'lampara-del-minero', 'name' => 'Lámpara del Minero', 'kind' => 'accessory', 'rarity' => 'epic', 'defense' => 2, 'intelligence' => 3, 'luck' => 2, 'description' => 'Te la regaló Hulda al vencer a la Sanguijuela: con su luz, nada se te esconde.'],
            ['code' => 'libro-de-registros-de-plomo', 'name' => 'Libro de Registros de Plomo', 'kind' => 'story', 'description' => 'Estaba en el último cajón del Guardián del Archivo: las medidas exactas del marco que encargó el Vidriero. En la última página: «Fundido bajo la Montaña».'],
            ['code' => 'hoja-templada', 'name' => 'Hoja Templada', 'kind' => 'weapon', 'rarity' => 'legendary', 'attack' => 12, 'strength' => 3, 'dexterity' => 2, 'description' => 'La espada que Kira forjó ella misma frente al Dragón bajo la Montaña, midiendo cada grado.'],
            ['code' => 'matriz-del-marco', 'name' => 'Matriz del Marco', 'kind' => 'story', 'description' => 'El molde de plomo de un vitral enorme que dejó el Vidriero bajo la Montaña, con la inscripción «para quien llegue». El mismo marco que espera en la torre más alta del Imperio.'],
        ],
        'cpp' => [
            // La Ciudadela (docs/historias/cpp.md): lo que gana Bron en la historia. La tienda y las recetas se
            // suman cuando estén sus imágenes y el mapa.
            ['code' => 'llave-mellada', 'name' => 'Llave Mellada', 'kind' => 'story', 'description' => 'La llave inglesa cian de Bron, mellada contra el engranaje 47 del portón de la Ciudadela. Faltaban 153.'],
            ['code' => 'engranaje-de-laton', 'name' => 'Engranaje de Latón', 'kind' => 'accessory', 'rarity' => 'rare', 'defense' => 2, 'strength' => 1, 'intelligence' => 1, 'description' => 'El corazón del Autómata de Latón: lo venciste con un plan, no con la llave.'],
            ['code' => 'llave-ajustable', 'name' => 'Llave Ajustable', 'kind' => 'weapon', 'rarity' => 'rare', 'attack' => 6, 'strength' => 1, 'dexterity' => 1, 'description' => 'Tesla le agregó a tu llave una tuerca que se corre al caer la Quimera: una llave para muchas tuercas, como un buen constructor.'],
            ['code' => Item::CATCH, 'name' => 'Amuleto del Catch', 'kind' => 'accessory', 'rarity' => 'rare', 'defense' => 2, 'strength' => 1, 'price' => 700, 'min_level' => 5, 'droppable' => true, 'description' => 'Una red de bronce chiquita: la que te atajó cuando se rompió el andamio. Equipado, en cada expedición te levanta una vez con la mitad de la vida.'],
            ['code' => 'espejo-del-mimico', 'name' => 'Espejo del Mímico', 'kind' => 'accessory', 'rarity' => 'epic', 'defense' => 1, 'intelligence' => 3, 'luck' => 3, 'description' => 'Lo dejó el Mímico al caer: refleja lo que tenés, no lo que sos.'],
            ['code' => 'catalogo-de-plantillas', 'name' => 'Catálogo de Plantillas', 'kind' => 'story', 'description' => 'Lo soltó el Kraken en los sótanos de la Gran Biblioteca. En la página de las bisagras del Vidriero dice: «plantilla, para cualquier marco».'],
            ['code' => 'engranaje-del-portal', 'name' => 'Engranaje del Portal', 'kind' => 'story', 'description' => 'Le colgaba del cuello al Minotauro del Laberinto. Tiene los mismos dientes que las bisagras del Vidriero, y no encaja en ninguna máquina de la Ciudadela.'],
            ['code' => 'llave-universal', 'name' => 'Llave Universal', 'kind' => 'weapon', 'rarity' => 'legendary', 'attack' => 12, 'strength' => 2, 'intelligence' => 3, 'description' => 'Bron dibujó su plano frente a la Gárgola de los Vitrales y Tesla la construyó en el torno: se ajusta a cualquier tuerca de la Ciudadela, como una plantilla.'],
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
        'taza-encantada' => 'Una taza de café humeante de porcelana azul con un asa hecha de cinco colmillos de orco curvados y un vapor que brilla.',
        'sello-dentado' => 'Un bastón de aduanero de madera oscura con un sello de bronce en la punta rodeado de dientes de goblin y pequeños huesos.',
        'chaqueta-forrada' => 'Una chaqueta azul de cuello alto con botones de bronce, forrada por dentro con musgo verde de troll que asoma por los bordes.',
        'estoque-de-la-garra' => 'Un estoque fino y largo con la guarnición hecha de garras de ogro y la hoja cubierta de escamas de dragón que brillan.',
        'llave-maestra' => 'Una llave maestra dorada y larga, con dientes que parecen engranajes y un mango que todavía conserva la forma de una ganzúa vieja, con un brillo cálido.',
        'remo-de-las-corrientes' => 'Un remo largo de madera clara con vetas de luz celeste que se mueven como corrientes de agua, con la pala grabada con olas.',
        'vitral-del-viajero' => 'Un vitral redondo de colores en un marco de plomo, envuelto a medias en una lona gastada, con una etiqueta de papel atada con un hilo.',
        'amuleto-de-la-campana' => 'Un amuleto con forma de campanita de bronce colgada de un cordón de cuero, con un brillo dorado que vibra como si sonara.',
        'linterna-del-espectro' => 'Una linterna antigua de hierro negro con vidrios esmerilados y una llama azul fría adentro, que proyecta un haz de luz pálida.',
        'guantes-del-artesano' => 'Un par de guantes de cuero marrón gastado con remaches y nudillos de bronce, y el sello de la Academia de los Moldes grabado en el dorso.',
        'sello-de-entrada' => 'Un sello de bronce antiguo con mango de piedra gris y la palabra «DECLARADO» en relieve, con un brillo azul en el borde.',
        'llave-del-vitral' => 'Una llave antigua de plomo con la cabeza hecha de vidrios de colores, como un vitral pequeño, con una etiqueta de papel atada.',
        // Las Forjas (C)
        'espada-rajada' => 'Una espada de aprendiz con una grieta que la atraviesa de punta a mango, con líneas cian apagadas en la hoja.',
        'espada-reforjada' => 'Una espada de acero oscuro recién reforjada, con la marca del martillo en la hoja y un brillo naranja de fragua en el filo.',
        Item::CORE_DUMP => 'Un amuleto con forma de gota de lava solidificada colgado de una cadena de hierro, con números chiquitos grabados que brillan en naranja.',
        'hilo-de-las-direcciones' => 'Un ovillo de hilo de cobre brillante con una punta que se estira sola señalando hacia un costado, con destellos cian.',
        'lampara-del-minero' => 'Una lámpara de minero de hierro y bronce con un vidrio grueso y una luz cian intensa adentro, con un gancho para colgar.',
        'libro-de-registros-de-plomo' => 'Un libro grueso con tapas de plomo gris y una cadena de hierro, entreabierto, con medidas y planos de un marco en las páginas.',
        // C: las Forjas de Hierro (naranja fragua, hierro y bronce)
        'espada-de-practica' => 'Una espada corta de hierro sin templar, gris opaco, con la empuñadura envuelta en cuero gastado y una etiqueta de precio de cartón atada con hilo.',
        'martillo-de-aprendiz' => 'Un martillo de herrero chico con cabeza de hierro negro y mango de madera, con las iniciales del dueño marcadas a fuego.',
        'sable-del-desborde' => 'Un sable curvo de acero con el número 255 grabado en la hoja, que brilla en naranja, y un 0 en cian cerca de la punta.',
        'florete-del-puntero' => 'Un florete fino de acero con una flecha grabada en la hoja que brilla en cian y una guardia de bronce con forma de asterisco.',
        'martillo-de-ferrum' => 'Un martillo de forja enorme de hierro negro con runas de enano que brillan en naranja, y un mango de roble con bandas de bronce.',
        'delantal-de-cuero' => 'Un delantal de herrero de cuero marrón con quemaduras chiquitas, un bolsillo con una tiza blanca y correas de bronce.',
        'chaleco-de-minero' => 'Un chaleco de cuero grueso reforzado con placas de hierro, con polvo de roca y un gancho para el farol.',
        'cota-alineada' => 'Una cota de malla de anillos de acero perfectamente alineados en filas, sin huecos, que brilla con un reflejo naranja.',
        'capa-ignifuga' => 'Una capa gris ceniza con bordes de hilo de bronce, con brasas que le caen encima y se apagan sin quemarla.',
        'armadura-de-la-fragua' => 'Una armadura de placas de hierro negro con vetas de lava naranja entre las placas, humeante, sobre un soporte de forja.',
        'calibre-de-bronce' => 'Un calibre de herrero de bronce pulido con marcas de medida grabadas, colgado de un cordón de cuero.',
        'anillo-del-sizeof' => 'Un anillo grueso de hierro con un pequeño número grabado y una piedra naranja que parece una pesa.',
        'antiparras-del-depurador' => 'Unas antiparras de herrero de bronce con lentes cian que muestran líneas de código y un punto rojo de alerta.',
        'sello-del-yunque' => 'Un sello redondo de bronce con un yunque y dos martillos grabados, que brilla con chispas naranjas.',
        'sopa-de-tizon' => 'Un cuenco de hierro con sopa humeante y un calibre de bronce chiquito apoyado en el borde, midiéndola.',
        'calibre-afilado' => 'Un calibre de bronce con las puntas reemplazadas por dos colmillos de orco curvos y afilados.',
        'martillo-dentado' => 'Un martillo de aprendiz con la cabeza rodeada de dientes de goblin y pequeños huesos atados con alambre.',
        'chaleco-acolchado' => 'Un chaleco de minero de cuero con forro de musgo verde de troll que asoma por las costuras.',
        'florete-de-la-garra' => 'Un florete fino de acero con garras de ogro en la guardia y escamas de dragón rojas en la hoja.',
        'hoja-templada' => 'Una espada larga y fina de acero templado con un filo que brilla en cian y una empuñadura envuelta en cuero, con vapor saliendo de la hoja.',
        'matriz-del-marco' => 'Un molde de plomo enorme con la forma de un marco de vitral redondo, con la inscripción «para quien llegue» grabada en el borde.',
        // La Ciudadela (C++)
        'llave-mellada' => 'Una llave inglesa grande de color cian con la boca mellada y un diente de engranaje de bronce todavía trabado adentro.',
        'engranaje-de-laton' => 'Un engranaje de latón pulido del tamaño de una mano, con una ventanita en el centro donde late una luz cian como un corazón de vapor.',
        'llave-ajustable' => 'Una llave inglesa cian con una tuerca de bronce que corre a lo largo del mango para ajustar la boca, con marcas de medida grabadas.',
        Item::CATCH => 'Un amuleto con forma de red tejida en hilo de bronce, colgado de una cadena fina, con nudos que brillan en cian.',
        'espejo-del-mimico' => 'Un espejo de mano ovalado con marco de cera gris que se derrite apenas, y un reflejo levemente distinto al de afuera.',
        'catalogo-de-plantillas' => 'Un libro grande con tapas de bronce y engranajes en el lomo, abierto en un plano de dos bisagras con medidas que no cierran.',
        'engranaje-del-portal' => 'Un engranaje enorme de bronce oscuro con dientes de formas raras, atado a una cadena cortada, con un brillo de vitral entre los dientes.',
        'llave-universal' => 'Una llave inglesa legendaria de bronce y cian con una boca hecha de piezas que se reacomodan solas, rodeada de líneas de plano luminosas.',
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
