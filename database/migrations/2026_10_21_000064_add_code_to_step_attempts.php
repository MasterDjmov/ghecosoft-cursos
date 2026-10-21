<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * D107: el código con el que el alumno falló una micro-misión, para que el docente lo vea en el Recorrido al lado
 * de la salida esperada y de la solución (y lo pueda ejecutar).
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::table('step_attempts', function (Blueprint $table) {
            $table->text('code')->nullable()->after('answer');
        });
    }

    public function down(): void
    {
        Schema::table('step_attempts', fn (Blueprint $table) => $table->dropColumn('code'));
    }
};
