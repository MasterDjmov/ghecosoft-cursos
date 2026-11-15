<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * D123: la ayuda que pidió un alumno en una micro-misión («¿Dónde toco?», «Comparemos», «Mostrame una línea», la
 * oferta de Gheco). Aparte de `step_attempts` para no mezclarla con los fallos de las estadísticas. `line` es la
 * línea de la solución que se le mostró (solo en `kind` = line).
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::create('step_helps', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->foreignId('node_step_id')->constrained()->cascadeOnDelete();
            $table->foreignId('course_id')->constrained()->cascadeOnDelete();
            $table->string('kind', 12);
            $table->unsignedSmallInteger('line')->nullable();
            $table->timestamp('created_at')->useCurrent();

            $table->index(['user_id', 'node_step_id']);
            $table->index(['user_id', 'course_id']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('step_helps');
    }
};
