<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * D107: lo que hace falta para saber dónde se traba un alumno. Cada intento de una micro-misión (también los
 * fallos, que antes se quedaban en el navegador) y una fila por alumno, nodo y día que lo miró.
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::create('step_attempts', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->foreignId('node_step_id')->constrained()->cascadeOnDelete();
            // Repetidos de la micro-misión para contar rápido por nodo y por curso.
            $table->foreignId('node_id')->constrained()->cascadeOnDelete();
            $table->foreignId('course_id')->constrained()->cascadeOnDelete();
            $table->boolean('passed')->default(false);
            $table->string('kind', 20)->nullable();
            $table->string('answer', 500)->nullable();
            $table->timestamp('created_at')->index();

            $table->index(['user_id', 'course_id']);
            $table->index(['course_id', 'node_step_id']);
        });

        Schema::create('node_visits', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->foreignId('node_id')->constrained()->cascadeOnDelete();
            $table->foreignId('course_id')->constrained()->cascadeOnDelete();
            $table->date('visited_on');
            $table->unsignedSmallInteger('views')->default(1);
            $table->timestamp('first_at');
            $table->timestamp('last_at');

            $table->unique(['user_id', 'node_id', 'visited_on']);
            $table->index(['course_id', 'visited_on']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('node_visits');
        Schema::dropIfExists('step_attempts');
    }
};
