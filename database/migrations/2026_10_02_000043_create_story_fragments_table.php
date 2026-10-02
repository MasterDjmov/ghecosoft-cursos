<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * Fragmentos de Mis Crónicas (D80, etapa 2): trozos extra de historia (con imagen opcional) que el docente
 * agrega en Admin → Historia. Cuelgan de un lugar del libro y se abren con él: al completar un nodo, al
 * terminar una rama, al empezar o al terminar el curso. No tocan los .md de los cursos.
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::create('story_fragments', function (Blueprint $table) {
            $table->id();
            $table->foreignId('course_id')->constrained()->cascadeOnDelete();
            $table->foreignId('node_id')->nullable()->constrained()->cascadeOnDelete();
            $table->foreignId('branch_id')->nullable()->constrained()->cascadeOnDelete();
            $table->string('trigger', 30); // node_completed | branch_completed | course_started | course_completed
            $table->string('title');
            $table->text('body')->nullable();
            $table->string('image_path')->nullable();
            $table->unsignedInteger('position')->default(0);
            $table->timestamps();
            $table->index(['course_id', 'trigger']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('story_fragments');
    }
};
