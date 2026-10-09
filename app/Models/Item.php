<?php

namespace App\Models;

use App\Enums\ItemKind;
use App\Enums\ItemRarity;
use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Support\Facades\Storage;

/**
 * Un ítem del juego (D84 § 7, D90). Regla que no se rompe: un ítem nunca limita ni amplía lo que el alumno
 * puede escribir; solo afecta al juego (atributos, ataque, defensa, curación).
 */
#[Fillable(['code', 'name', 'description', 'kind', 'rarity', 'course_id', 'attack', 'defense', 'strength', 'dexterity', 'intelligence', 'luck', 'heal', 'price', 'min_level', 'in_shop', 'droppable', 'image_path', 'image_prompt'])]
class Item extends Model
{
    /** Estilo común de las imágenes de ítems (para generarlas siempre iguales). */
    public const IMAGE_STYLE = 'Ícono de ítem de juego RPG, cuadrado 1:1 (1024×1024), el objeto solo y centrado, en vista tres cuartos, sobre fondo oscuro liso con un brillo suave detrás; estilo anime/cómic cyber-arcana, con luz propia y detalles de neón del color de su mundo; sin texto ni personas.';

    /** Lado de la imagen chica de las grillas (thumbUrl). */
    public const THUMB_PX = 256;

    /** El que deja reacomodar los puntos del héroe una vez (D89). */
    public const RESPEC = 'pergamino-del-reinicio';

    /** Equipado, da una segunda vida en cada expedición (R02-N03). */
    public const TRACEBACK = 'amuleto-del-traceback';

    /** El del Imperio: la misma segunda vida (Java, R03-N04). */
    public const BELL = 'amuleto-de-la-campana';

    /** El de las Forjas: la misma segunda vida (C, R02-N04). */
    public const CORE_DUMP = 'amuleto-del-volcado';

    /** El de la Ciudadela: la misma segunda vida (C++, R05-N01). */
    public const CATCH = 'amuleto-del-catch';

    /** El de los Talleres: la misma segunda vida (HTML y CSS, R01-N05). */
    public const VALIDATOR = 'amuleto-del-validador';

    /** Los que dan la segunda vida en las expediciones. */
    public const SECOND_LIFE = [self::TRACEBACK, self::BELL, self::CORE_DUMP, self::CATCH, self::VALIDATOR];

    /** Termina al instante la expedición en camino; se gasta al usarlo (R03-N06). */
    public const HOURGLASS = 'reloj-de-arena';

    protected $attributes = [
        'rarity' => 'common', 'attack' => 0, 'defense' => 0, 'strength' => 0, 'dexterity' => 0, 'intelligence' => 0,
        'luck' => 0, 'heal' => 0, 'min_level' => 1, 'in_shop' => false, 'droppable' => false,
    ];

    protected function casts(): array
    {
        return [
            'kind' => ItemKind::class,
            'rarity' => ItemRarity::class,
            'attack' => 'integer', 'defense' => 'integer', 'strength' => 'integer', 'dexterity' => 'integer',
            'intelligence' => 'integer', 'luck' => 'integer', 'heal' => 'integer', 'price' => 'integer',
            'min_level' => 'integer', 'in_shop' => 'boolean', 'droppable' => 'boolean',
        ];
    }

    public function course(): BelongsTo
    {
        return $this->belongsTo(Course::class);
    }

    public function imageUrl(): ?string
    {
        return $this->image_path ? Storage::disk('public')->url($this->image_path) : null;
    }

    /**
     * La imagen chica (WebP de 256 px) para las grillas y los casilleros; la grande queda para la ficha.
     * Se arma la primera vez que se pide; si no se puede (sin GD o sin WebP), se usa la grande.
     */
    public function thumbUrl(): ?string
    {
        if (! $this->image_path) {
            return null;
        }
        $disk = Storage::disk('public');
        $thumb = 'item-thumbs/'.pathinfo($this->image_path, PATHINFO_FILENAME).'.webp';
        if (! $disk->exists($thumb) && ! self::makeThumb($disk->path($this->image_path), $disk->path($thumb))) {
            return $this->imageUrl();
        }

        return $disk->url($thumb);
    }

    private static function makeThumb(string $from, string $to): bool
    {
        if (! function_exists('imagewebp') || ! is_file($from) || ! ($image = @imagecreatefromstring((string) file_get_contents($from)))) {
            return false;
        }
        $small = imagescale($image, self::THUMB_PX, -1, IMG_BICUBIC);
        @mkdir(dirname($to), 0755, true);

        return $small !== false && imagewebp($small, $to, 82);
    }

    /** El pedido completo para generar la imagen: qué es, su rareza, lo que pidió el docente y el estilo común. */
    public function fullImagePrompt(): string
    {
        $glow = match ($this->rarity) {
            ItemRarity::Rare => 'brillo celeste',
            ItemRarity::Epic => 'brillo violeta intenso, con partículas',
            default => 'brillo gris tenue',
        };

        return trim(implode("\n", array_filter([
            "Ítem: {$this->name} ({$this->kind->label()}, {$this->rarity->label()}).",
            $this->image_prompt,
            $this->description ? "En el juego: {$this->description}" : null,
            "Rareza: {$glow}.",
            self::IMAGE_STYLE,
        ])));
    }

    public function isEquippable(): bool
    {
        return $this->kind->slot() !== null;
    }

    /** Sirve para el héroe de ese curso: es de su mundo o es común. */
    public function fitsCourse(?Course $course): bool
    {
        return $this->course_id === null || $this->course_id === $course?->id;
    }

    /**
     * Lo que da, para mostrar: «+3 ATQ · +1 FUE · cura 30».
     *
     * @return list<string>
     */
    public function bonuses(): array
    {
        $out = [];
        foreach (['attack' => 'ATQ', 'defense' => 'DEF', 'strength' => 'FUE', 'dexterity' => 'DES', 'intelligence' => 'INT', 'luck' => 'SUE'] as $field => $short) {
            if ($this->{$field} !== 0) {
                $out[] = ($this->{$field} > 0 ? '+' : '').$this->{$field}.' '.$short;
            }
        }
        if ($this->heal > 0) {
            $out[] = 'cura '.$this->heal;
        }

        return $out;
    }
}
