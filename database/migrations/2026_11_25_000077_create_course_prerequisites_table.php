<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * D126: requisitos entre cursos. Un curso puede pedir haber completado un nodo de otro curso (Videojuegos pide C hasta
 * el jefe de R02; Ensamblador 32/64, el de 8086). Sin cumplirlo no se pide la inscripción ni se abre el primer nodo;
 * la Clase 0 se prueba igual.
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::create('course_prerequisites', function (Blueprint $table) {
            $table->id();
            $table->foreignId('course_id')->constrained()->cascadeOnDelete();
            $table->foreignId('required_node_id')->constrained('nodes')->cascadeOnDelete();
            $table->timestamps();
            $table->unique(['course_id', 'required_node_id']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('course_prerequisites');
    }
};
