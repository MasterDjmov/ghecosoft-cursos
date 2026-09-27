<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;

/**
 * Datos mínimos para producción: configuración, moneda comodín y niveles.
 * No crea usuarios (el admin se crea con `php artisan app:create-admin`).
 */
class ProductionSeeder extends Seeder
{
    public function run(): void
    {
        $this->call([
            SettingsSeeder::class,
            LevelSeeder::class,
        ]);
    }
}
