<?php

namespace App\Enums;

enum XpReason: string
{
    case PracticeApproved = 'practice_approved';
    case StepCompleted = 'step_completed';
    case NodeCompleted = 'node_completed';
    case BossDefeated = 'boss_defeated';
    case SpokeAloud = 'spoke_aloud';
    case ManualAdjustment = 'manual_adjustment';
    case Reversal = 'reversal';

    public function label(): string
    {
        return match ($this) {
            self::PracticeApproved => 'Práctica aprobada',
            self::StepCompleted => 'Micro-misión superada',
            self::NodeCompleted => 'Nodo completado',
            self::BossDefeated => 'Jefe vencido',
            self::SpokeAloud => 'Lo dijo en voz alta',
            self::ManualAdjustment => 'Ajuste del docente',
            self::Reversal => 'Corrección',
        };
    }
}
