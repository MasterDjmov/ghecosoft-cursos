<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * Corrección asistida (D73): pruebas extra de una práctica (entrada → salida esperada), solo del docente.
 * La de ejemplo sigue en practices.sample_input / expected_output y es la que ve el alumno.
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::create('practice_tests', function (Blueprint $table) {
            $table->id();
            $table->foreignId('practice_id')->constrained()->cascadeOnDelete();
            $table->unsignedSmallInteger('position')->default(0);
            $table->string('name');
            $table->text('input')->nullable();
            $table->text('expected_output');
            $table->timestamps();

            $table->index(['practice_id', 'position']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('practice_tests');
    }
};
