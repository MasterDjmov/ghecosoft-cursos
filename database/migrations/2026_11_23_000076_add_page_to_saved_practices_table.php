<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * D124: la columna `page` (el HTML de la página de la caja de la Feria) se sumó a la migración que crea
 * saved_practices después de que esa migración ya había corrido en producción; ahí la tabla quedó sin la columna y
 * guardar daba error. Esta la agrega donde falta (en una base nueva ya viene de la migración anterior).
 */
return new class extends Migration
{
    public function up(): void
    {
        if (! Schema::hasColumn('saved_practices', 'page')) {
            Schema::table('saved_practices', function (Blueprint $table) {
                $table->text('page')->nullable()->after('stdin');
            });
        }
    }

    public function down(): void
    {
        // No se saca: la migración que crea la tabla también la trae.
    }
};
