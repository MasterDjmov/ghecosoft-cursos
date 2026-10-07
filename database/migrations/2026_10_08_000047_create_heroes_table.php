<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * El protagonista de cada curso en manos de un jugador (D84/D89): el aspecto que eligió entre las
 * 6 variantes y los 4 atributos (24 puntos repartidos al empezar, cada uno entre 4 y 12; después
 * se suben con oro).
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::create('heroes', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->foreignId('course_id')->constrained()->cascadeOnDelete();
            $table->unsignedTinyInteger('look')->default(1);
            $table->unsignedSmallInteger('strength');
            $table->unsignedSmallInteger('dexterity');
            $table->unsignedSmallInteger('intelligence');
            $table->unsignedSmallInteger('luck');
            $table->timestamps();

            $table->unique(['user_id', 'course_id']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('heroes');
    }
};
