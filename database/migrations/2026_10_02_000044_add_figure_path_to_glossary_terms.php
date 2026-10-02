<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/** El personaje de cuerpo entero (Mis Crónicas, D80): una segunda imagen, además del retrato redondo. */
return new class extends Migration
{
    public function up(): void
    {
        Schema::table('glossary_terms', function (Blueprint $table) {
            $table->string('figure_path')->nullable()->after('icon_path');
        });
    }

    public function down(): void
    {
        Schema::table('glossary_terms', function (Blueprint $table) {
            $table->dropColumn('figure_path');
        });
    }
};
