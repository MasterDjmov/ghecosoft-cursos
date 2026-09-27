<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('practices', function (Blueprint $table) {
            $table->id();
            $table->foreignId('node_id')->constrained()->cascadeOnDelete();
            $table->string('title');
            $table->longText('instructions')->nullable();
            $table->boolean('is_required')->default(true);
            $table->string('submission_mode')->default('code');
            $table->string('allowed_extensions')->nullable();
            $table->text('starter_code')->nullable();
            $table->text('sample_input')->nullable();
            $table->unsignedInteger('coin_reward')->default(0);
            $table->unsignedInteger('xp_reward')->default(0);
            $table->unsignedInteger('position')->default(0);
            $table->timestamps();
            $table->index(['node_id', 'position']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('practices');
    }
};
