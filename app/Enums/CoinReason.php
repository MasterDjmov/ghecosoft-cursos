<?php

namespace App\Enums;

enum CoinReason: string
{
    case EnrollmentGrant = 'enrollment_grant';
    case PracticeApproved = 'practice_approved';
    case NodeUnlock = 'node_unlock';
    case ManualAdjustment = 'manual_adjustment';
    case Reversal = 'reversal';
    // Oro (D89).
    case StepCompleted = 'step_completed';
    case StatUpgrade = 'stat_upgrade';
    case ShopPurchase = 'shop_purchase';
    case MountPurchase = 'mount_purchase';
    case ExpeditionLoot = 'expedition_loot';

    public function label(): string
    {
        return match ($this) {
            self::StepCompleted => 'Micro-misión superada',
            self::StatUpgrade => 'Atributo mejorado',
            self::ShopPurchase => 'Compra en la tienda',
            self::MountPurchase => 'Montura',
            self::ExpeditionLoot => 'Botín de expedición',
            self::EnrollmentGrant => 'Inscripción aprobada',
            self::PracticeApproved => 'Práctica aprobada',
            self::NodeUnlock => 'Nodo abierto',
            self::ManualAdjustment => 'Ajuste del docente',
            self::Reversal => 'Corrección',
        };
    }
}
