<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * Rol docente (D72): cada comisión puede tener su docente (el que la creó o el que asigna el
 * administrador). El docente ve y corrige lo de los alumnos de sus comisiones. users.role suma 'teacher'.
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::table('cohorts', function (Blueprint $table) {
            $table->foreignId('teacher_id')->nullable()->after('course_id')->constrained('users')->nullOnDelete();
        });
    }

    public function down(): void
    {
        Schema::table('cohorts', function (Blueprint $table) {
            $table->dropConstrainedForeignId('teacher_id');
        });
    }
};
