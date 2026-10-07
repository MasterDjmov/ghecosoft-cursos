<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * Expediciones (D91): el héroe sale a un lugar del mapa por 5, 15 o 30 minutos; al volver, el servidor calcula
 * la exploración y las peleas (`log`) y paga el botín (`rewards`). Sin cron: se resuelve cuando el jugador
 * vuelve a mirar. Y la montura del jugador (una, de la especie que elija, nivel 1 a 5).
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::create('expeditions', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->foreignId('hero_id')->constrained()->cascadeOnDelete();
            $table->foreignId('course_id')->constrained()->cascadeOnDelete();
            $table->string('place', 60);
            $table->string('length', 10);
            $table->timestamp('started_at');
            $table->timestamp('ends_at');
            $table->timestamp('resolved_at')->nullable();
            $table->boolean('won')->nullable();
            $table->json('log')->nullable();
            $table->json('rewards')->nullable();
            $table->timestamps();

            $table->index(['user_id', 'started_at']);
        });

        Schema::create('mounts', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->unique()->constrained()->cascadeOnDelete();
            $table->string('species', 40);
            $table->unsignedTinyInteger('level')->default(1);
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('mounts');
        Schema::dropIfExists('expeditions');
    }
};
