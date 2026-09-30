<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * Avisos en vivo (D62): cada usuario elige si suena un tono cuando llega un aviso
 * y si quiere la notificación del sistema (fuera del navegador).
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::table('users', function (Blueprint $table) {
            $table->boolean('alert_sound')->default(true)->after('cv_code');
            $table->boolean('alert_desktop')->default(false)->after('alert_sound');
        });
    }

    public function down(): void
    {
        Schema::table('users', function (Blueprint $table) {
            $table->dropColumn(['alert_sound', 'alert_desktop']);
        });
    }
};
