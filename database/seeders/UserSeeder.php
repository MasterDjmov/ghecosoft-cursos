<?php

namespace Database\Seeders;

use App\Enums\Role;
use App\Models\User;
use Illuminate\Database\Seeder;

/**
 * Usuarios de DESARROLLO pedidos por el docente. Sus claves no cumplen la
 * regla de contraseñas a propósito (son de prueba): en producción el admin
 * se crea con `php artisan app:create-admin`.
 */
class UserSeeder extends Seeder
{
    public function run(): void
    {
        User::updateOrCreate(['username' => 'admin'], [
            'name' => 'Docente',
            'last_name' => 'GhecoSoft',
            'email' => 'admin@ghecosoft.test',
            'password' => 'admin123',
        ])->forceFill(['role' => Role::Admin, 'email_verified_at' => now()])->save();

        // Rol docente (D72): corrige y atiende a los alumnos de sus comisiones (DemoTeacherSeeder le arma una).
        User::updateOrCreate(['username' => 'docente'], [
            'name' => 'Docente',
            'last_name' => 'de Prueba',
            'email' => 'docente@ghecosoft.test',
            'password' => 'docente123',
        ])->forceFill(['role' => Role::Teacher, 'email_verified_at' => now()])->save();

        User::updateOrCreate(['username' => 'cliente'], [
            'name' => 'Cliente',
            'last_name' => 'de Prueba',
            'email' => 'cliente@ghecosoft.test',
            'password' => 'cliente123',
        ])->forceFill(['role' => Role::Student, 'email_verified_at' => now()])->save();
    }
}
