<?php

namespace Database\Seeders;

use App\Enums\XpReason;
use App\Models\User;
use App\Services\Ledger;
use App\Services\Ranking;
use Illuminate\Database\Seeder;

/** Demo: alumnos con perfil público y XP, para ver el top 10 de la landing. Solo en local. */
class DemoHeroesSeeder extends Seeder
{
    public function run(Ledger $ledger): void
    {
        $heroes = [
            ['Luna', 'Roja', 'Luna Roja', 980], ['Tomás', 'Vera', 'Byte Salvaje', 870], ['Ana', 'Sosa', 'Pixelia', 760],
            ['Juan', 'Díaz', 'Kernel', 640], ['Sofía', 'Luna', null, 520], ['Mateo', 'Ruiz', 'Zafiro', 430],
            ['Valen', 'Paz', 'Lambda', 310], ['Emi', 'Toro', 'Nébula', 220], ['Cami', 'Gil', 'Rayo', 150],
            ['Fede', 'Ortiz', 'Ciclón', 90], ['Rocío', 'Mena', 'Aurora', 40],
        ];

        foreach ($heroes as $i => [$name, $lastName, $hero, $xp]) {
            $username = 'demo_heroe_'.($i + 1);
            if (User::where('username', $username)->exists()) {
                continue;
            }
            $user = User::create([
                'name' => $name, 'last_name' => $lastName, 'username' => $username, 'password' => 'Demo12345',
                'hero_name' => $hero, 'cv_public' => true, 'birth_date' => now()->subYears(20 + $i),
            ]);
            $ledger->addXp($user, $xp, XpReason::ManualAdjustment, note: 'Demo del top de la landing');
        }

        Ranking::forget();
    }
}
