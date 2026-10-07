<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/** El taller (D93): lo que el jugador está fabricando. Uno a la vez; se recoge al terminar (sin cron). */
return new class extends Migration
{
    public function up(): void
    {
        Schema::create('crafts', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->string('recipe', 80);
            $table->foreignId('item_id')->constrained()->restrictOnDelete();
            $table->unsignedInteger('quantity');
            $table->timestamp('started_at');
            $table->timestamp('ends_at');
            $table->timestamp('collected_at')->nullable();
            $table->timestamps();
            $table->index(['user_id', 'collected_at']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('crafts');
    }
};
