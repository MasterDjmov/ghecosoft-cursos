<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * D73: los comentarios guardados de cada docente («Bien, pero revisá los nombres de las variables»), para
 * insertarlos con un clic al corregir. Con curso, solo salen en ese curso; sin curso, en todos.
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::create('review_snippets', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->foreignId('course_id')->nullable()->constrained()->cascadeOnDelete();
            $table->text('body');
            $table->unsignedInteger('position')->default(0);
            $table->timestamps();
            $table->index(['user_id', 'position']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('review_snippets');
    }
};
