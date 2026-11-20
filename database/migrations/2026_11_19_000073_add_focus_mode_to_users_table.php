<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * D123, fase 3: el modo enfoque (docs/AYUDA.md § 5). Lo prende el alumno en su perfil o el docente desde su ficha;
 * no se guarda ningún motivo.
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::table('users', function (Blueprint $table) {
            $table->boolean('focus_mode')->default(false)->after('alert_desktop');
        });
    }

    public function down(): void
    {
        Schema::table('users', function (Blueprint $table) {
            $table->dropColumn('focus_mode');
        });
    }
};
