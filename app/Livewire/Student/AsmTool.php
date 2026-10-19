<?php

namespace App\Livewire\Student;

use App\Enums\Language;
use App\Models\Course;
use Livewire\Attributes\Title;
use Livewire\Component;

/**
 * Herramientas → Gólem 8086 (D110): el tablero del Gólem suelto, para practicar lo que se quiera fuera de las
 * micro-misiones. Corre en el navegador del alumno (como las micro-misiones); pide el abono vigente de un curso
 * de Ensamblador (CoursePolicy::useAsmTool).
 */
#[Title('Gólem 8086')]
class AsmTool extends Component
{
    public const STARTER = <<<'ASM'
        ; El tablero del Gólem: escribí tus órdenes y probá Ejecutar o Paso a paso.
        .model small
        .stack 100h
        .data
        saludo db 'Hola, Gólem', 13, 10, '$'
        .code
        main proc
            mov ax, @data
            mov ds, ax

            mov dx, offset saludo
            mov ah, 09h
            int 21h

        fin:
            mov ax, 4C00h
            int 21h
        main endp
        end main
        ASM;

    public function mount(): void
    {
        abort_unless($this->course() !== null, 403);
    }

    /** El primer curso de Ensamblador con el que puede usar el tablero. */
    private function course(): ?Course
    {
        return Course::where('language', Language::Asm)->get()
            ->first(fn (Course $course) => auth()->user()->can('useAsmTool', $course));
    }

    public function render()
    {
        return view('livewire.student.asm-tool', ['course' => $this->course(), 'starter' => str_replace('Gólem', 'Golem', self::STARTER)]);
    }
}
