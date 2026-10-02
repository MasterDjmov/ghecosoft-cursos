<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/** Mis Crónicas (D80): cuántas páginas desbloqueadas ya vio el alumno; si hoy tiene más, el menú late. */
return new class extends Migration
{
    public function up(): void
    {
        Schema::table('users', function (Blueprint $table) {
            $table->unsignedInteger('chronicles_seen')->default(0);
        });
    }

    public function down(): void
    {
        Schema::table('users', function (Blueprint $table) {
            $table->dropColumn('chronicles_seen');
        });
    }
};
