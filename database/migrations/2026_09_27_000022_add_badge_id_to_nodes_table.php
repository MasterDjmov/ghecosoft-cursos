<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /** La insignia que entrega un nodo jefe al completarse (G7). */
    public function up(): void
    {
        Schema::table('nodes', function (Blueprint $table) {
            $table->foreignId('badge_id')->nullable()->after('price_currency_id')->constrained()->nullOnDelete();
        });
    }

    public function down(): void
    {
        Schema::table('nodes', function (Blueprint $table) {
            $table->dropConstrainedForeignId('badge_id');
        });
    }
};
