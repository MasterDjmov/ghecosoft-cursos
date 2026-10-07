<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/** Lo que escribió el alumno al superar la micro-misión y lo que obtuvo, para volver a mirarlo (D88). */
return new class extends Migration
{
    public function up(): void
    {
        Schema::table('node_step_completions', function (Blueprint $table) {
            $table->text('code')->nullable()->after('node_step_id');
            $table->text('output')->nullable()->after('code');
        });
    }

    public function down(): void
    {
        Schema::table('node_step_completions', function (Blueprint $table) {
            $table->dropColumn(['code', 'output']);
        });
    }
};
