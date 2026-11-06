<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * Alumnos demorados: a quién quitó a mano de la lista el docente o el administrador, en cada curso. Vale hasta
 * que el alumno vuelva a avanzar o renueve el abono: si después se vuelve a frenar, aparece de nuevo.
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::create('delay_dismissals', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->foreignId('course_id')->constrained()->cascadeOnDelete();
            $table->foreignId('dismissed_by')->nullable()->constrained('users')->nullOnDelete();
            $table->timestamp('created_at')->useCurrent();

            $table->unique(['user_id', 'course_id']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('delay_dismissals');
    }
};
