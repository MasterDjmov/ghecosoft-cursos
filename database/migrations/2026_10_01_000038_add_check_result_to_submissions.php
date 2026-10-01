<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * Corrección asistida (D73): lo que dieron las pruebas al correrlas en el navegador de quien corrige
 * ({"passed": 3, "total": 4, "at": "..."}). Es una ayuda para la bandeja, no una nota: el alumno no la ve.
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::table('submissions', function (Blueprint $table) {
            $table->json('check_result')->nullable()->after('file_original_name');
        });
    }

    public function down(): void
    {
        Schema::table('submissions', function (Blueprint $table) {
            $table->dropColumn('check_result');
        });
    }
};
