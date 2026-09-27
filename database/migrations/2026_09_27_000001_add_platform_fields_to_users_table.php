<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('users', function (Blueprint $table) {
            $table->string('last_name')->after('name');
            $table->string('username')->unique()->after('last_name');
            $table->string('role')->default('student')->index()->after('password');
            $table->string('phone')->nullable();
            $table->string('dni')->nullable()->unique();
            $table->date('birth_date')->nullable();
            $table->string('avatar')->nullable();
            $table->unsignedInteger('xp_total')->default(0);
            $table->string('nickname')->nullable();
            $table->string('ranking_display')->default('name');
            $table->boolean('cv_public')->default(false);
        });
    }

    public function down(): void
    {

        Schema::table('users', function (Blueprint $table) {
            $table->dropUnique(['username']);
            $table->dropUnique(['dni']);
            $table->dropIndex(['role']);
            $table->dropColumn(['last_name', 'username', 'role', 'phone', 'dni', 'birth_date', 'avatar', 'xp_total', 'nickname', 'ranking_display', 'cv_public']);
        });
    }
};
