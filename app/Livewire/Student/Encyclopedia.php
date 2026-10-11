<?php

namespace App\Livewire\Student;

use App\Models\Course;
use App\Support\Encyclopedia as Book;
use Flux\Flux;
use Illuminate\Support\Str;
use Livewire\Attributes\Title;
use Livewire\Attributes\Url;
use Livewire\Component;

/**
 * La Gran Enciclopedia del Código (D104): la portada con las 8 secciones y, adentro, las fichas en tarjetas.
 * Cada ficha se abre en un modal; lo no descubierto, en silueta y con su pista (el texto no sale del servidor).
 * La ven todos los alumnos, también los que solo prueban la Clase 0: es para que se motiven.
 */
#[Title('Enciclopedia')]
class Encyclopedia extends Component
{
    /** Las secciones de la portada: clave → [título, lo que tiene adentro]. Las que todavía no están, sin clave en SECTIONS_READY. */
    public const SECTIONS = [
        'clases' => 'Clases / Lenguajes',
        Book::MASTERS => 'Maestros',
        Book::BESTIARY => 'Bestiario',
        'monturas' => 'Monturas',
        'monedas' => 'Monedas',
        'artefactos' => 'Artefactos',
        'reinos' => 'Reinos / Mapas',
        'hechizos' => 'Hechizos & Sintaxis',
    ];

    public const SECTIONS_READY = [Book::MASTERS, Book::BESTIARY, 'hechizos'];

    #[Url(as: 'seccion', except: '')]
    public string $section = '';

    #[Url(as: 'curso', except: '')]
    public string $course = '';

    public string $search = '';

    public ?string $selected = null;

    public function mount(): void
    {
        if ($this->section !== '' && ! in_array($this->section, [Book::MASTERS, Book::BESTIARY], true)) {
            $this->section = '';
        }
    }

    public function show(string $section): void
    {
        if ($section === 'hechizos') {
            $this->redirectRoute('student.grimoire', navigate: true);

            return;
        }
        if (in_array($section, [Book::MASTERS, Book::BESTIARY], true)) {
            $this->section = $section;
            $this->reset('search', 'course', 'selected');
        }
    }

    public function back(): void
    {
        $this->reset('section', 'search', 'course', 'selected');
    }

    public function open(string $key): void
    {
        $this->selected = $key;
        Flux::modal('encyclopedia-entry')->show();
    }

    public function render()
    {
        $entries = (new Book(auth()->user()))->entries();
        $shown = $entries->where('section', $this->section)
            ->when($this->course !== '', fn ($all) => $all->filter(fn ($entry) => $entry['course']?->slug === $this->course))
            ->when(trim($this->search) !== '', fn ($all) => $all->filter(fn ($entry) => Str::contains(Str::ascii(Str::lower($entry['name'])), Str::ascii(Str::lower(trim($this->search))))));

        return view('livewire.student.encyclopedia', [
            'counts' => collect([Book::MASTERS, Book::BESTIARY])->mapWithKeys(fn ($section) => [$section => Book::count($entries, $section)]),
            'groups' => $shown->groupBy('group'),
            'courses' => $this->section === '' ? collect() : Course::whereIn('id', $entries->where('section', $this->section)->pluck('course.id')->filter())->orderBy('id')->get(),
            'entry' => $this->selected ? $entries->firstWhere('key', $this->selected) : null,
        ]);
    }
}
