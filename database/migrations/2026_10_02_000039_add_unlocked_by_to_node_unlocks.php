<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/** Quién abrió el nodo cuando no fue el alumno: el docente o el administrador que lo ayudó (con sus monedas). */
return new class extends Migration
{
    public function up(): void
    {
        Schema::table('node_unlocks', function (Blueprint $table) {
            $table->foreignId('unlocked_by')->nullable()->after('price_paid')->constrained('users')->nullOnDelete();
        });
    }

    public function down(): void
    {
        Schema::table('node_unlocks', function (Blueprint $table) {
            $table->dropConstrainedForeignId('unlocked_by');
        });
    }
};
