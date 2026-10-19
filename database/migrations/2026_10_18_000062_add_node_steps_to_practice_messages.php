<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/*
 * D110: las consultas también se mandan desde una micro-misión (en todos los cursos). Cada mensaje del alumno
 * guarda una foto del código que tenía en el editor y de lo que le dio al ejecutar, para que el docente lo
 * vea junto a la solución sin salir del chat.
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::table('practice_messages', function (Blueprint $table) {
            $table->foreignId('practice_id')->nullable()->change();
            $table->foreignId('node_step_id')->nullable()->after('practice_id')->constrained()->cascadeOnDelete();
            $table->text('code')->nullable()->after('body');
            $table->text('output')->nullable()->after('code');
            $table->index(['student_id', 'node_step_id']);
        });
    }

    public function down(): void
    {
        Schema::table('practice_messages', function (Blueprint $table) {
            $table->dropIndex(['student_id', 'node_step_id']);
            $table->dropConstrainedForeignId('node_step_id');
            $table->dropColumn(['code', 'output']);
        });
    }
};
