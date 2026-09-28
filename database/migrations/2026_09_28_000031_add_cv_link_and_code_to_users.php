<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;
use Illuminate\Support\Str;

/**
 * El CV deja de usar el usuario de login: tiene su propio link (nombre + código al
 * azar) y, si el alumno quiere, un código de acceso de 6 cifras (guardado cifrado,
 * así se le puede volver a mostrar).
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::table('users', function (Blueprint $table) {
            $table->string('cv_slug', 80)->nullable()->unique()->after('cv_public');
            $table->text('cv_code')->nullable()->after('cv_slug');
        });

        DB::table('users')->orderBy('id')->each(function ($user) {
            $base = Str::limit(Str::slug(trim($user->name.' '.$user->last_name)) ?: 'alumno', 60, '');
            DB::table('users')->where('id', $user->id)->update(['cv_slug' => $base.'-'.Str::lower(Str::random(6))]);
        });
    }

    public function down(): void
    {
        Schema::table('users', function (Blueprint $table) {
            $table->dropUnique(['cv_slug']);
            $table->dropColumn(['cv_slug', 'cv_code']);
        });
    }
};
