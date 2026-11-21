<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * Mensajes que el docente le manda a un alumno desde *Alumnos* (por ejemplo, a uno nuevo que está probando la
 * Clase 0, para ofrecerle ayuda). Le llegan a la campanita y por mail; queda anotado para no escribirle dos veces.
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::create('student_contacts', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->foreignId('sent_by')->nullable()->constrained('users')->nullOnDelete();
            $table->text('body');
            $table->timestamp('created_at')->useCurrent();

            $table->index(['user_id', 'created_at']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('student_contacts');
    }
};
