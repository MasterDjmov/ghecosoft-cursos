<?php

namespace App\Enums;

enum ItemKind: string
{
    case Weapon = 'weapon';
    case Armor = 'armor';
    case Accessory = 'accessory';
    case Potion = 'potion';
    case Material = 'material';
    case Story = 'story';
    case Special = 'special';

    public function label(): string
    {
        return match ($this) {
            self::Weapon => 'Arma',
            self::Armor => 'Ropa',
            self::Accessory => 'Accesorio',
            self::Potion => 'Poción',
            self::Material => 'Material',
            self::Story => 'De la historia',
            self::Special => 'Especial',
        };
    }

    public function plural(): string
    {
        return match ($this) {
            self::Weapon => 'Armas',
            self::Armor => 'Ropa',
            self::Accessory => 'Accesorios',
            self::Potion => 'Pociones',
            self::Material => 'Materiales',
            self::Story => 'De la historia',
            self::Special => 'Especiales',
        };
    }

    /** La columna del héroe donde se equipa, o null si no se equipa. */
    public function slot(): ?string
    {
        return match ($this) {
            self::Weapon => 'weapon_item_id',
            self::Armor => 'armor_item_id',
            self::Accessory => 'accessory_item_id',
            default => null,
        };
    }

    public function icon(): string
    {
        return match ($this) {
            self::Weapon => 'bolt',
            self::Armor => 'shield-check',
            self::Accessory => 'sparkles',
            self::Potion => 'beaker',
            self::Material => 'cube',
            self::Story => 'book-open',
            self::Special => 'star',
        };
    }

    /** @return list<string> las columnas de equipo del héroe, en orden */
    public static function slots(): array
    {
        return ['weapon_item_id', 'armor_item_id', 'accessory_item_id'];
    }

    public static function forSlot(string $slot): self
    {
        return match ($slot) {
            'weapon_item_id' => self::Weapon,
            'armor_item_id' => self::Armor,
            'accessory_item_id' => self::Accessory,
        };
    }
}
