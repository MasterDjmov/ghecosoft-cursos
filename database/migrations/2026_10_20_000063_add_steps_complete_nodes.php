<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * D111: un curso donde las micro-misiones completan el nodo (con monedas del curso), micro-misiones que pagan
 * monedas del curso y prácticas retiradas (sacadas del .md pero con entregas, que no se borran).
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::table('courses', function (Blueprint $table) {
            $table->boolean('steps_complete_nodes')->default(false)->after('subscription_days');
        });
        Schema::table('node_steps', function (Blueprint $table) {
            $table->unsignedSmallInteger('coin_reward')->default(0)->after('gold_reward');
        });
        Schema::table('practices', function (Blueprint $table) {
            $table->timestamp('retired_at')->nullable()->after('position');
        });
    }

    public function down(): void
    {
        Schema::table('practices', fn (Blueprint $table) => $table->dropColumn('retired_at'));
        Schema::table('node_steps', fn (Blueprint $table) => $table->dropColumn('coin_reward'));
        Schema::table('courses', fn (Blueprint $table) => $table->dropColumn('steps_complete_nodes'));
    }
};
