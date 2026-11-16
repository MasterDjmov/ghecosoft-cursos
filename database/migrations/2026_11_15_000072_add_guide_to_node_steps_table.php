<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

// D123, fase 2: los «Pasos» de la micro-misión (el desafío en pasos cortos y literales, `#### Pasos` en el .md).
return new class extends Migration
{
    public function up(): void
    {
        Schema::table('node_steps', function (Blueprint $table) {
            $table->text('guide')->nullable()->after('challenge');
        });
    }

    public function down(): void
    {
        Schema::table('node_steps', function (Blueprint $table) {
            $table->dropColumn('guide');
        });
    }
};
