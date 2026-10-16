<?php

namespace App\Livewire\Student;

use App\Models\Course;
use App\Support\Encyclopedia as Book;
use App\Support\EncyclopediaItems as Items;
use App\Support\EncyclopediaWorlds as Worlds;
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
        Worlds::CLASSES => 'Clases / Lenguajes',
        Book::MASTERS => 'Maestros',
        Book::BESTIARY => 'Bestiario',
        Worlds::MOUNTS => 'Monturas',
        Items::COINS => 'Monedas',
        Items::ARTIFACTS => 'Artefactos',
        Worlds::REALMS => 'Reinos / Mapas',
        'hechizos' => 'Hechizos & Sintaxis',
    ];

    public const SECTIONS_READY = [Worlds::CLASSES, Book::MASTERS, Book::BESTIARY, Worlds::MOUNTS, Items::COINS, Items::ARTIFACTS, Worlds::REALMS, 'hechizos'];

    /** Las secciones con fichas (la de hechizos lleva al Grimorio). */
    public const BROWSABLE = [Worlds::CLASSES, Book::MASTERS, Book::BESTIARY, Worlds::MOUNTS, Items::COINS, Items::ARTIFACTS, Worlds::REALMS];

    #[Url(as: 'seccion', except: '')]
    public string $section = '';

    #[Url(as: 'curso', except: '')]
    public string $course = '';

    public string $search = '';

    public ?string $selected = null;

    public function mount(): void
    {
        if ($this->section !== '' && ! in_array($this->section, self::BROWSABLE, true)) {
            $this->section = '';
        }
    }

    public function show(string $section): void
    {
        if ($section === 'hechizos') {
            $this->redirectRoute('student.grimoire', navigate: true);

            return;
        }
        if (in_array($section, self::BROWSABLE, true)) {
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
        $user = auth()->user();
        $items = new Items($user);
        $worlds = new Worlds($user);
        // Solo se arma lo que hace falta: en la portada, todo (para los contadores); adentro, la sección abierta.
        $entries = collect()
            ->when(in_array($this->section, ['', Book::MASTERS, Book::BESTIARY], true), fn ($all) => $all->concat((new Book($user))->entries()))
            ->when(in_array($this->section, ['', Items::ARTIFACTS], true), fn ($all) => $all->concat($items->artifacts()))
            ->when(in_array($this->section, ['', Items::COINS], true), fn ($all) => $all->concat($items->coins()))
            ->when(in_array($this->section, ['', Worlds::CLASSES], true), fn ($all) => $all->concat($worlds->classes()))
            ->when(in_array($this->section, ['', Worlds::MOUNTS], true), fn ($all) => $all->concat($worlds->mounts()))
            ->when(in_array($this->section, ['', Worlds::REALMS], true), fn ($all) => $all->concat($worlds->realms()));
        $shown = $entries->where('section', $this->section)
            ->when($this->course !== '', fn ($all) => $all->filter(fn ($entry) => $entry['course']?->slug === $this->course))
            ->when(trim($this->search) !== '', fn ($all) => $all->filter(fn ($entry) => Str::contains(Str::ascii(Str::lower($entry['name'])), Str::ascii(Str::lower(trim($this->search))))));

        return view('livewire.student.encyclopedia', [
            'counts' => collect(self::BROWSABLE)->mapWithKeys(fn ($section) => [$section => Book::count($entries, $section)])->filter(fn ($count) => $count['total'] > 0),
            'groups' => $shown->groupBy('group'),
            'courses' => $this->section === '' ? collect() : Course::whereIn('id', $entries->where('section', $this->section)->pluck('course.id')->filter())->orderBy('id')->get(),
            'entry' => $this->selected ? $entries->firstWhere('key', $this->selected) : null,
        ]);
    }
}
