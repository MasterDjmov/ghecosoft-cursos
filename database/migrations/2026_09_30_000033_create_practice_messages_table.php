<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * Consultas por práctica (D63): un hilo por alumno y práctica, sin necesidad de entregar.
 * read_at = cuándo lo leyó el otro lado (el docente si escribió el alumno, y al revés).
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::create('practice_messages', function (Blueprint $table) {
            $table->id();
            $table->foreignId('practice_id')->constrained()->cascadeOnDelete();
            $table->foreignId('student_id')->constrained('users')->cascadeOnDelete();
            $table->foreignId('author_id')->constrained('users')->cascadeOnDelete();
            $table->text('body');
            $table->timestamp('read_at')->nullable();
            $table->timestamps();

            $table->index(['student_id', 'practice_id']);
            $table->index(['read_at', 'author_id']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('practice_messages');
    }
};
