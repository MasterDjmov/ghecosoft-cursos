<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * Sesión única (D65): una cuenta de alumno solo está abierta en un lugar a la vez.
 * session_token = el de la última sesión que entró; blocked_at = el docente la pausó.
 * session_evictions = cada vez que una sesión se cerró porque la cuenta entró en otro lado.
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::table('users', function (Blueprint $table) {
            $table->string('session_token', 64)->nullable()->after('remember_token');
            $table->timestamp('blocked_at')->nullable()->after('session_token');
        });

        Schema::create('session_evictions', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->string('ip', 45)->nullable();
            $table->string('user_agent', 255)->nullable();
            $table->timestamp('created_at')->useCurrent();

            $table->index(['user_id', 'created_at']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('session_evictions');
        Schema::table('users', function (Blueprint $table) {
            $table->dropColumn(['session_token', 'blocked_at']);
        });
    }
};
