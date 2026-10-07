<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * Los ítems del juego (D84 § 7, D90): el catálogo, el libro de movimientos de la mochila (como el de las
 * monedas: la cantidad es la suma) y lo que cada héroe tiene puesto (arma, ropa y accesorio).
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::create('items', function (Blueprint $table) {
            $table->id();
            $table->string('code', 80)->unique();
            $table->string('name');
            $table->text('description')->nullable();
            $table->string('kind', 20);
            $table->string('rarity', 12)->default('common');
            // null = común: sirve en todos los mundos.
            $table->foreignId('course_id')->nullable()->constrained()->nullOnDelete();
            $table->smallInteger('attack')->default(0);
            $table->smallInteger('defense')->default(0);
            $table->smallInteger('strength')->default(0);
            $table->smallInteger('dexterity')->default(0);
            $table->smallInteger('intelligence')->default(0);
            $table->smallInteger('luck')->default(0);
            $table->unsignedSmallInteger('heal')->default(0);
            $table->unsignedInteger('price')->nullable();
            $table->unsignedSmallInteger('min_level')->default(1);
            $table->boolean('in_shop')->default(false);
            $table->boolean('droppable')->default(false);
            $table->string('image_path')->nullable();
            $table->timestamps();
        });

        Schema::create('item_movements', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->foreignId('item_id')->constrained()->cascadeOnDelete();
            $table->integer('quantity');
            $table->string('reason', 30);
            $table->nullableMorphs('source');
            $table->string('note')->nullable();
            $table->foreignId('created_by')->nullable()->constrained('users')->nullOnDelete();
            $table->timestamps();

            $table->index(['user_id', 'item_id']);
        });

        Schema::table('heroes', function (Blueprint $table) {
            $table->foreignId('weapon_item_id')->nullable()->after('luck')->constrained('items')->nullOnDelete();
            $table->foreignId('armor_item_id')->nullable()->after('weapon_item_id')->constrained('items')->nullOnDelete();
            $table->foreignId('accessory_item_id')->nullable()->after('armor_item_id')->constrained('items')->nullOnDelete();
            // Un Pergamino del Reinicio usado: puede reacomodar los puntos una vez.
            $table->boolean('respec_available')->default(false)->after('accessory_item_id');
        });
    }

    public function down(): void
    {
        Schema::table('heroes', function (Blueprint $table) {
            $table->dropConstrainedForeignId('weapon_item_id');
            $table->dropConstrainedForeignId('armor_item_id');
            $table->dropConstrainedForeignId('accessory_item_id');
            $table->dropColumn('respec_available');
        });
        Schema::dropIfExists('item_movements');
        Schema::dropIfExists('items');
    }
};
