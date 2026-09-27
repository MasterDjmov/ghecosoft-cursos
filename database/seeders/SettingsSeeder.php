<?php

namespace Database\Seeders;

use App\Models\Currency;
use App\Models\Setting;
use Illuminate\Database\Seeder;

class SettingsSeeder extends Seeder
{
    public function run(): void
    {
        $settings = [
            'platform_name' => 'GhecoSoft-Code',
            'whatsapp_number' => '',
            'whatsapp_message' => 'Hola profe, soy {nombre}. Quiero inscribirme en {curso}.',
            'welcome_text' => 'Aprendé a programar avanzando por tu árbol de habilidades.',
        ];

        foreach ($settings as $key => $value) {
            Setting::updateOrCreate(['key' => $key], ['value' => $value]);
        }

        Currency::wildcard();
    }
}
