<?php

namespace App\Enums;

enum CoinReason: string
{
    case EnrollmentGrant = 'enrollment_grant';
    case PracticeApproved = 'practice_approved';
    case NodeUnlock = 'node_unlock';
    case ManualAdjustment = 'manual_adjustment';
    case Reversal = 'reversal';

    public function label(): string
    {
        return match ($this) {
            self::EnrollmentGrant => 'Inscripción aprobada',
            self::PracticeApproved => 'Práctica aprobada',
            self::NodeUnlock => 'Nodo abierto',
            self::ManualAdjustment => 'Ajuste del docente',
            self::Reversal => 'Corrección',
        };
    }
}
