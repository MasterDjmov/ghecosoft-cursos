<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;

/**
 * Fase 8: ramas con tipo (tronco, extra o senda) y requisitos extra de un nodo, además de su padre.
 * `branches.is_extra` se mantiene (es "no es tronco") para no romper consultas existentes.
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::table('branches', function (Blueprint $table) {
            $table->string('kind', 20)->default('trunk')->after('title');
        });
        DB::table('branches')->where('is_extra', true)->update(['kind' => 'extra']);

        Schema::create('node_requirements', function (Blueprint $table) {
            $table->id();
            $table->foreignId('node_id')->constrained()->cascadeOnDelete();
            $table->foreignId('required_node_id')->constrained('nodes')->cascadeOnDelete();
            $table->timestamps();
            $table->unique(['node_id', 'required_node_id']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('node_requirements');
        Schema::table('branches', fn (Blueprint $table) => $table->dropColumn('kind'));
    }
};
