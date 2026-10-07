<?php

namespace App\Services;

use App\Enums\CoinReason;
use App\Models\Currency;
use App\Models\Mount;
use App\Models\User;
use Illuminate\Support\Facades\DB;
use InvalidArgumentException;

/**
 * Los establos (D91, JUEGO.md § 6): una montura por jugador. Se compra la especie en n1 y se mejora hasta n5;
 * cada nivel tiene precio y nivel mínimo. La especie es cosmética: se cambia gratis y conserva el nivel.
 */
class Stables
{
    public function __construct(private readonly Ledger $ledger) {}

    public function mountOf(User $user): ?Mount
    {
        return Mount::where('user_id', $user->id)->first();
    }

    /** @return array{reduction: int, price: int, min_level: int}|null el próximo nivel (o el primero), o null si ya es n5 */
    public function next(?Mount $mount): ?array
    {
        return config('game.mounts.levels.'.(($mount?->level ?? 0) + 1));
    }

    /** Comprar la primera (n1) o subir de nivel la que tiene. */
    public function buyOrUpgrade(User $user, ?string $species = null): Mount
    {
        return DB::transaction(function () use ($user, $species) {
            User::whereKey($user->id)->lockForUpdate()->first();
            $mount = $this->mountOf($user);
            $next = $this->next($mount);
            if (! $next) {
                throw new InvalidArgumentException('Tu montura ya está al máximo.');
            }
            if (Inventory::playerLevel($user) < $next['min_level']) {
                throw new InvalidArgumentException('Necesitás nivel '.$next['min_level'].'.');
            }
            if (! $mount && ! array_key_exists((string) $species, config('game.mounts.species'))) {
                throw new InvalidArgumentException('Elegí una especie.');
            }
            $level = ($mount?->level ?? 0) + 1;
            $this->ledger->debit($user, Currency::gold(), $next['price'], CoinReason::MountPurchase, $mount, null,
                ($mount ? $mount->name() : config('game.mounts.species.'.$species)).' n'.$level);

            if ($mount) {
                $mount->update(['level' => $level]);

                return $mount;
            }

            return Mount::create(['user_id' => $user->id, 'species' => $species, 'level' => 1]);
        });
    }

    public function changeSpecies(User $user, string $species): void
    {
        if (! array_key_exists($species, config('game.mounts.species'))) {
            throw new InvalidArgumentException('Esa especie no existe.');
        }
        $mount = $this->mountOf($user) ?? throw new InvalidArgumentException('Todavía no tenés montura.');
        $mount->update(['species' => $species]);
    }
}
