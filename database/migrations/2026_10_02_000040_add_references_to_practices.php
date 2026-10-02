<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/** «Así tiene que quedar» (D77): la captura de la página resuelta, en celular y en compu (disco público). */
return new class extends Migration
{
    public function up(): void
    {
        Schema::table('practices', function (Blueprint $table) {
            $table->string('reference_mobile')->nullable()->after('expected_output');
            $table->string('reference_desktop')->nullable()->after('reference_mobile');
        });
    }

    public function down(): void
    {
        Schema::table('practices', function (Blueprint $table) {
            $table->dropColumn(['reference_mobile', 'reference_desktop']);
        });
    }
};
