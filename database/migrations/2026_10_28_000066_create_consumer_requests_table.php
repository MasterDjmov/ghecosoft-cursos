<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * D112: botón de arrepentimiento (Res. 424/2020) y botón de baja (Res. 316/2018), sin necesidad de entrar
 * a la cuenta, con un código de trámite; y qué versión de los Términos y la Privacidad aceptó cada cuenta.
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::create('consumer_requests', function (Blueprint $table) {
            $table->id();
            $table->string('kind', 20);
            $table->string('code', 16)->unique();
            $table->foreignId('user_id')->nullable()->constrained()->nullOnDelete();
            $table->string('name');
            $table->string('contact');
            $table->string('course')->nullable();
            $table->text('details')->nullable();
            $table->string('status', 20)->default('pending');
            $table->text('admin_note')->nullable();
            $table->timestamp('handled_at')->nullable();
            $table->foreignId('handled_by')->nullable()->constrained('users')->nullOnDelete();
            $table->timestamps();
            $table->index(['status', 'created_at']);
        });

        Schema::table('users', function (Blueprint $table) {
            $table->timestamp('terms_accepted_at')->nullable();
            $table->string('terms_version', 20)->nullable();
        });
    }

    public function down(): void
    {
        Schema::table('users', function (Blueprint $table) {
            $table->dropColumn(['terms_accepted_at', 'terms_version']);
        });
        Schema::dropIfExists('consumer_requests');
    }
};
