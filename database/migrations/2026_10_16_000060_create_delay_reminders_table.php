<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * Alumnos demorados: cada aviso que el docente o el administrador le manda a un alumno que no avanza en un
 * curso. Es la copia interna del mail (también le llega a la campanita).
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::create('delay_reminders', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->foreignId('course_id')->constrained()->cascadeOnDelete();
            $table->foreignId('sent_by')->nullable()->constrained('users')->nullOnDelete();
            $table->text('body');
            $table->timestamp('created_at')->useCurrent();

            $table->index(['user_id', 'course_id', 'created_at']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('delay_reminders');
    }
};
