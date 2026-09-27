<?php

namespace App\Enums;

enum XpReason: string
{
    case PracticeApproved = 'practice_approved';
    case NodeCompleted = 'node_completed';
    case BossDefeated = 'boss_defeated';
    case ManualAdjustment = 'manual_adjustment';
    case Reversal = 'reversal';

    public function label(): string
    {
        return match ($this) {
            self::PracticeApproved => 'Práctica aprobada',
            self::NodeCompleted => 'Nodo completado',
            self::BossDefeated => 'Jefe vencido',
            self::ManualAdjustment => 'Ajuste del docente',
            self::Reversal => 'Corrección',
        };
    }
}
