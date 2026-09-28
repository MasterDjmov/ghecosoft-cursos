<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/** Catálogo: nivel, destacado, "Próximamente" con temario, y quién pidió que le avisen. */
return new class extends Migration
{
    public function up(): void
    {
        Schema::table('courses', function (Blueprint $table) {
            $table->string('level')->default('beginner')->after('language');
            $table->boolean('is_featured')->default(false)->after('is_published');
            $table->boolean('is_upcoming')->default(false)->after('is_featured');
            $table->text('syllabus')->nullable()->after('description');
        });

        Schema::create('course_interests', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->foreignId('course_id')->constrained()->cascadeOnDelete();
            $table->timestamp('notified_at')->nullable();
            $table->timestamps();
            $table->unique(['user_id', 'course_id']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('course_interests');
        Schema::table('courses', function (Blueprint $table) {
            $table->dropColumn(['level', 'is_featured', 'is_upcoming', 'syllabus']);
        });
    }
};
