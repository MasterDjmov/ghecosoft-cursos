<?php

namespace Database\Seeders;

use App\Models\Level;
use Illuminate\Database\Seeder;

class LevelSeeder extends Seeder
{
    public function run(): void
    {
        foreach ([1 => 0, 2 => 100, 3 => 250, 4 => 500, 5 => 1000, 6 => 1750, 7 => 2750] as $number => $xp) {
            Level::updateOrCreate(['number' => $number], ['xp_required' => $xp]);
        }
    }
}
