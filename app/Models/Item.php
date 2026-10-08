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

    /** El que deja reacomodar los puntos del héroe una vez (D89). */
    public const RESPEC = 'pergamino-del-reinicio';

    /** Equipado, da una segunda vida en cada expedición (R02-N03). */
    public const TRACEBACK = 'amuleto-del-traceback';

    /** El del Imperio: la misma segunda vida (Java, R03-N04). */
    public const BELL = 'amuleto-de-la-campana';

    /** El de las Forjas: la misma segunda vida (C, R02-N04). */
    public const CORE_DUMP = 'amuleto-del-volcado';

    /** Los que dan la segunda vida en las expediciones. */
    public const SECOND_LIFE = [self::TRACEBACK, self::BELL, self::CORE_DUMP];

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
