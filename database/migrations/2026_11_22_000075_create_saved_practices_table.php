<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * D124: Mis prácticas. Lo que cada uno escribe en Herramientas → Practicar se puede guardar con un nombre, retomar
 * después y consultarlo con el profe (el hilo va en practice_messages.saved_practice_id).
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::create('saved_practices', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->string('language', 20);
            $table->string('title', 120);
            $table->mediumText('code');
            $table->text('stdin')->nullable();
            $table->timestamps();

            $table->index(['user_id', 'updated_at']);
        });

        Schema::table('practice_messages', function (Blueprint $table) {
            $table->foreignId('saved_practice_id')->nullable()->after('node_step_id')->constrained()->cascadeOnDelete();
        });
    }

    public function down(): void
    {
        Schema::table('practice_messages', function (Blueprint $table) {
            $table->dropConstrainedForeignId('saved_practice_id');
        });
        Schema::dropIfExists('saved_practices');
    }
};
