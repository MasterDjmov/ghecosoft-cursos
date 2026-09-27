<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * D37: el nodo se escribe por secciones (cada una con su personaje) y la práctica
 * suma criterio, solución de referencia, salida esperada y entorno.
 * `nodes.content` sigue siendo la explicación (Mia).
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::table('nodes', function (Blueprint $table) {
            $table->text('chronicle')->nullable()->after('video_url');
            $table->text('objectives')->nullable()->after('chronicle');
            $table->text('before_you_start')->nullable()->after('objectives');
            $table->text('use_cases')->nullable()->after('sample_input');
            $table->text('common_errors')->nullable()->after('use_cases');
            $table->string('beast_key', 60)->nullable()->after('common_errors');
            $table->json('self_check')->nullable()->after('beast_key');
            // Solo del docente: nunca se manda al alumno.
            $table->longText('teacher_solutions')->nullable()->after('self_check');
        });

        Schema::table('practices', function (Blueprint $table) {
            $table->string('environment', 20)->default('browser')->after('submission_mode');
            $table->text('approval_criteria')->nullable()->after('instructions');
            $table->text('expected_output')->nullable()->after('sample_input');
            // Solo del docente: nunca se manda al alumno.
            $table->longText('reference_solution')->nullable()->after('expected_output');
        });
    }

    public function down(): void
    {
        Schema::table('nodes', function (Blueprint $table) {
            $table->dropColumn(['chronicle', 'objectives', 'before_you_start', 'use_cases', 'common_errors', 'beast_key', 'self_check', 'teacher_solutions']);
        });

        Schema::table('practices', function (Blueprint $table) {
            $table->dropColumn(['environment', 'approval_criteria', 'expected_output', 'reference_solution']);
        });
    }
};
