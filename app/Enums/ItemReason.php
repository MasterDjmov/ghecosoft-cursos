<?php

namespace App\Enums;

enum ItemReason: string
{
    case StepReward = 'step_reward';
    case ShopPurchase = 'shop_purchase';
    case Used = 'used';
    case Loot = 'loot';
    case ManualAdjustment = 'manual_adjustment';
    case Reversal = 'reversal';
    case CraftingCost = 'crafting_cost';
    case Crafted = 'crafted';

    public function label(): string
    {
        return match ($this) {
            self::StepReward => 'Micro-misión superada',
            self::ShopPurchase => 'Compra en la tienda',
            self::Used => 'Usado',
            self::Loot => 'Botín de expedición',
            self::ManualAdjustment => 'Ajuste del docente',
            self::Reversal => 'Corrección',
            self::CraftingCost => 'Usado en el taller',
            self::Crafted => 'Fabricado en el taller',
        };
    }
}
