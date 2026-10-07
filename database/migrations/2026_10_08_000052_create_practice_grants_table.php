<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/** D95: el docente le abre a un alumno las prácticas de un nodo sin que termine las micro-misiones (si se traba). */
return new class extends Migration
{
    public function up(): void
    {
        Schema::create('practice_grants', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->foreignId('node_id')->constrained()->cascadeOnDelete();
            $table->foreignId('granted_by')->nullable()->constrained('users')->nullOnDelete();
            $table->timestamps();
            $table->unique(['user_id', 'node_id']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('practice_grants');
    }
};
