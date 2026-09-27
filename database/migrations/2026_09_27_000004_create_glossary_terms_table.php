<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('glossary_terms', function (Blueprint $table) {
            $table->id();
            $table->string('key');
            $table->foreignId('course_id')->nullable()->constrained()->cascadeOnDelete();
            $table->string('singular');
            $table->string('plural')->nullable();
            $table->string('gender', 1)->default('f');
            $table->string('icon_path')->nullable();
            $table->string('short_description')->nullable();
            $table->text('lore')->nullable();
            $table->timestamps();
            $table->unique(['key', 'course_id']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('glossary_terms');
    }
};
