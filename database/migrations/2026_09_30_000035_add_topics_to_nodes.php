<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * Universo de cursos (D70): los temas del catálogo (cursos/temas.md) que cada nodo enseña (topics)
 * y los que da por sabidos (uses). Salen del Markdown del curso ("temas:" y "usa:"); el alumno no los ve.
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::table('nodes', function (Blueprint $table) {
            $table->json('topics')->nullable()->after('beast_key');
            $table->json('uses')->nullable()->after('topics');
        });
    }

    public function down(): void
    {
        Schema::table('nodes', function (Blueprint $table) {
            $table->dropColumn(['topics', 'uses']);
        });
    }
};
