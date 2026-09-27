<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('nodes', function (Blueprint $table) {
            $table->id();
            $table->foreignId('course_id')->constrained()->cascadeOnDelete();
            $table->foreignId('branch_id')->nullable()->constrained()->nullOnDelete();
            $table->foreignId('parent_id')->nullable()->constrained('nodes')->nullOnDelete();
            $table->string('type')->default('topic');
            $table->string('title');
            $table->unsignedInteger('position')->default(0);
            $table->unsignedInteger('price')->default(0);
            $table->foreignId('price_currency_id')->nullable()->constrained('currencies')->nullOnDelete();
            $table->string('video_url')->nullable();
            $table->longText('content')->nullable();
            $table->text('example_code')->nullable();
            $table->string('example_language')->nullable();
            $table->text('expected_output')->nullable();
            $table->text('sample_input')->nullable();
            $table->decimal('pos_x', 8, 2)->nullable();
            $table->decimal('pos_y', 8, 2)->nullable();
            $table->boolean('is_published')->default(true);
            $table->timestamps();
            $table->index(['course_id', 'type']);
            $table->index(['branch_id', 'position']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('nodes');
    }
};
