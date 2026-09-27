<?php

namespace App\Support;

use App\Models\Node;
use App\Models\User;
use App\Services\Ledger;
use App\Services\TreeAccess;

/** Traduce los motivos de TreeAccess::unlockBlockers() a frases para el alumno. */
class UnlockMessages
{
    /** @return list<string> */
    public static function for(User $user, Node $node, ?array $blockers = null): array
    {
        $access = app(TreeAccess::class);
        $blockers ??= $access->unlockBlockers($user, $node);
        $course = $node->course;

        return array_values(array_filter(array_map(function (string $blocker) use ($user, $node, $course, $access) {
            return match ($blocker) {
                TreeAccess::BLOCK_UNPUBLISHED => 'Todavía no está disponible.',
                TreeAccess::BLOCK_NO_SUBSCRIPTION => 'Tu abono no está vigente: renovalo para seguir abriendo.',
                TreeAccess::BLOCK_ROOT_CLOSED => 'Primero abrí «'.$course->rootNode?->title.'».',
                TreeAccess::BLOCK_PARENT_INCOMPLETE => 'Aprobá las '.term('practice', $course, 2).' obligatorias de «'.$node->parent?->title.'».',
                TreeAccess::BLOCK_REQUIREMENTS_INCOMPLETE => self::missingRequirements($user, $node, $access),
                TreeAccess::BLOCK_INSUFFICIENT_FUNDS => self::missingFunds($user, $node, $access),
                default => null,
            };
        }, $blockers)));
    }

    /** "Aprobá también las obligatorias de «X» y de «Y»." */
    private static function missingRequirements(User $user, Node $node, TreeAccess $access): ?string
    {
        $titles = collect($access->incompleteRequirements($user, $node))->map(fn (Node $required) => '«'.$required->title.'»');
        if ($titles->isEmpty()) {
            return null;
        }

        return 'Aprobá también las '.term('practice', $node->course, 2).' obligatorias de '.$titles->join(', de ', ' y de ').'.';
    }

    private static function missingFunds(User $user, Node $node, TreeAccess $access): string
    {
        $currency = $access->paymentCurrency($node);
        $missing = $node->price - app(Ledger::class)->balance($user, $currency);
        $name = $currency->is_wildcard ? term('coin.wildcard', null, $missing) : term('coin.course', $node->course, $missing);

        return "Te faltan {$missing} {$name}.";
    }

    /** "10 escamas" / "3 comodines" según con qué se paga el nodo. */
    public static function price(Node $node): string
    {
        $currency = app(TreeAccess::class)->paymentCurrency($node);

        return $node->price.' '.($currency->is_wildcard
            ? term('coin.wildcard', null, $node->price)
            : term('coin.course', $node->course, $node->price));
    }
}
