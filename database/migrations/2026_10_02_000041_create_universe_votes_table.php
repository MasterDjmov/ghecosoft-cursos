<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * «Quiero aprender esto» (D81): el voto de un alumno a un tema que ningún curso enseña o a un curso que
 * viene. Uno por alumno y por tema o curso; el docente ve quién votó qué.
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::create('universe_votes', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->string('target', 120); // «topic:css.posicion» o «course:12»
            $table->timestamps();
            $table->unique(['user_id', 'target']);
            $table->index('target');
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('universe_votes');
    }
};
