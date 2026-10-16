<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * Desde dónde entran los alumnos (celular, tablet o compu; sistema y navegador): una fila por alumno, día y
 * dispositivo. Se junta ahora; las pantallas con las métricas vienen con las estadísticas (D107 fase 2).
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::create('user_accesses', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->date('accessed_on');
            $table->string('device', 10);
            $table->string('os', 20);
            $table->string('browser', 20);
            $table->unsignedInteger('requests')->default(1);
            $table->timestamp('first_at');
            $table->timestamp('last_at');

            $table->unique(['user_id', 'accessed_on', 'device', 'os', 'browser'], 'user_accesses_unique');
            $table->index(['accessed_on', 'device']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('user_accesses');
    }
};
