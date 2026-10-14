<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * Micro-misiones de inglés (D106): la historia en inglés va en `scene`, el ejercicio armado en `checks`; acá, la
 * traducción al español y las palabras nuevas («window = ventana», una por renglón).
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::table('node_steps', function (Blueprint $table) {
            $table->text('translation')->nullable()->after('scene');
            $table->text('words')->nullable()->after('translation');
        });
    }

    public function down(): void
    {
        Schema::table('node_steps', function (Blueprint $table) {
            $table->dropColumn(['translation', 'words']);
        });
    }
};
