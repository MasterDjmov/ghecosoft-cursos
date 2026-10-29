<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * D113: el link «No quiero recibir más estos avisos» de los mails que no son de la cuenta («Avisame»):
 * desde esa fecha esos avisos quedan solo en la campanita.
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::table('users', function (Blueprint $table) {
            $table->timestamp('announcements_muted_at')->nullable();
        });
    }

    public function down(): void
    {
        Schema::table('users', function (Blueprint $table) {
            $table->dropColumn('announcements_muted_at');
        });
    }
};
