<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * D38: el héroe del alumno. Público y único en toda la plataforma. La intercalación
 * utf8mb4_unicode_ci hace que el índice único no distinga mayúsculas ni tildes.
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::table('users', function (Blueprint $table) {
            $table->string('hero_name', 20)->nullable()->unique()->after('nickname');
        });
    }

    public function down(): void
    {
        Schema::table('users', function (Blueprint $table) {
            $table->dropUnique(['hero_name']);
            $table->dropColumn('hero_name');
        });
    }
};
