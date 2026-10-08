<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/** Una micro-misión en otro lenguaje que su curso (las de SQL de Java corren con SQLite en el navegador). */
return new class extends Migration
{
    public function up(): void
    {
        Schema::table('node_steps', function (Blueprint $table) {
            $table->string('language', 20)->nullable()->after('code');
        });
    }

    public function down(): void
    {
        Schema::table('node_steps', function (Blueprint $table) {
            $table->dropColumn('language');
        });
    }
};
