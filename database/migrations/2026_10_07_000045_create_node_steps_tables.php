<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * Micro-misiones (D84 § 3): pasos cortos dentro de un nodo, con escena, pista de Gheco, desafío y recompensa.
 * Se comprueban solas en el navegador del alumno (salida esperada) y solo dan premios de juego.
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::create('node_steps', function (Blueprint $table) {
            $table->id();
            $table->foreignId('node_id')->constrained()->cascadeOnDelete();
            $table->string('code');
            $table->unsignedSmallInteger('position')->default(0);
            $table->string('title');
            $table->string('place')->nullable();
            $table->string('characters')->nullable();
            $table->string('creature')->nullable();
            $table->string('card_title')->nullable();
            $table->string('card_body', 500)->nullable();
            $table->unsignedSmallInteger('xp_reward')->default(0);
            $table->unsignedSmallInteger('gold_reward')->default(0);
            $table->string('item')->nullable();
            $table->string('image_path')->nullable();
            $table->text('scene')->nullable();
            $table->text('hint')->nullable();
            $table->text('challenge')->nullable();
            $table->text('starter_code')->nullable();
            $table->text('sample_input')->nullable();
            $table->text('expected_output');
            $table->text('solution')->nullable();
            $table->text('success_text')->nullable();
            $table->string('unlocks', 500)->nullable();
            $table->text('image_prompt')->nullable();
            $table->timestamps();

            $table->unique(['node_id', 'code']);
        });

        Schema::create('node_step_completions', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->foreignId('node_step_id')->constrained()->cascadeOnDelete();
            $table->timestamp('completed_at');
            $table->timestamps();

            $table->unique(['user_id', 'node_step_id']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('node_step_completions');
        Schema::dropIfExists('node_steps');
    }
};
