<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/** «Así se ve»: las capturas del ejemplo del nodo en celular y en compu (HTML y CSS), como las de las prácticas (D77). */
return new class extends Migration
{
    public function up(): void
    {
        Schema::table('nodes', function (Blueprint $table) {
            $table->string('example_reference_mobile')->nullable()->after('example_runnable');
            $table->string('example_reference_desktop')->nullable()->after('example_reference_mobile');
        });
    }

    public function down(): void
    {
        Schema::table('nodes', function (Blueprint $table) {
            $table->dropColumn(['example_reference_mobile', 'example_reference_desktop']);
        });
    }
};
