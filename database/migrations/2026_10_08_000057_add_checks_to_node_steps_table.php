<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/** Qué revisa el inspector en una micro-misión de HTML y CSS (D102): un pedido por renglón. */
return new class extends Migration
{
    public function up(): void
    {
        Schema::table('node_steps', function (Blueprint $table) {
            $table->text('checks')->nullable()->after('sample_input');
        });
    }

    public function down(): void
    {
        Schema::table('node_steps', function (Blueprint $table) {
            $table->dropColumn('checks');
        });
    }
};
