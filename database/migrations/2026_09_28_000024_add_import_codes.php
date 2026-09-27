<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * IDs estables del importador (Fase 7): "R01" para una rama, "R01-N02" para un nodo,
 * "R01-N02-M1" para una práctica. Reimportar actualiza por código sin perder el progreso.
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::table('branches', function (Blueprint $table) {
            $table->string('code', 40)->nullable()->after('course_id');
            $table->unique(['course_id', 'code']);
        });

        Schema::table('nodes', function (Blueprint $table) {
            $table->string('code', 40)->nullable()->after('course_id');
            $table->unique(['course_id', 'code']);
        });

        Schema::table('practices', function (Blueprint $table) {
            $table->string('code', 60)->nullable()->after('node_id');
            $table->unique(['node_id', 'code']);
        });
    }

    public function down(): void
    {
        Schema::table('practices', fn (Blueprint $table) => $table->dropUnique(['node_id', 'code']));
        Schema::table('practices', fn (Blueprint $table) => $table->dropColumn('code'));
        Schema::table('nodes', fn (Blueprint $table) => $table->dropUnique(['course_id', 'code']));
        Schema::table('nodes', fn (Blueprint $table) => $table->dropColumn('code'));
        Schema::table('branches', fn (Blueprint $table) => $table->dropUnique(['course_id', 'code']));
        Schema::table('branches', fn (Blueprint $table) => $table->dropColumn('code'));
    }
};
