<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/** Foto diaria de las posiciones del ranking global, para la tendencia ▲▼ (sin cron). */
return new class extends Migration
{
    public function up(): void
    {
        Schema::create('ranking_snapshots', function (Blueprint $table) {
            $table->id();
            $table->date('taken_on');
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->unsignedInteger('position');
            $table->unique(['taken_on', 'user_id']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('ranking_snapshots');
    }
};
