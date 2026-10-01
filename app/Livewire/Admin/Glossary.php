<?php

namespace App\Livewire\Admin;

use App\Enums\Gender;
use App\Models\Course;
use App\Models\GlossaryTerm;
use App\Models\Level;
use App\Models\Setting;
use App\Support\Glossary as GlossaryResolver;
use App\Support\Portraits;
use Flux\Flux;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;
use Illuminate\Validation\Rule;
use Livewire\Attributes\Title;
use Livewire\Attributes\Url;
use Livewire\Component;
use Livewire\Features\SupportFileUploads\TemporaryUploadedFile;
use Livewire\WithFileUploads;

/** Diccionario narrativo: nombres, género, íconos e historia por clave, general o por curso. */
#[Title('Diccionario')]
class Glossary extends Component
{
    use WithFileUploads;

    public const GROUPS = [
        'world' => 'Mundo',
        'companions' => 'Compañía',
        'economy' => 'Economía',
        'progress' => 'Progreso',
        'levels' => 'Niveles',
        'states' => 'Estados',
        'story' => 'Historia',
        'bestiary' => 'Bestiario',
        'custom' => 'Propias',
    ];

    /** Tamaño de los retratos en píxeles (App\Support\Portraits): la compañía y la mentora, y las criaturas. */
    public int $companionSize = 48;

    public int $beastSize = 80;

    /** 'general' o el id de un curso. */
    #[Url(as: 'ambito')]
    public string $scope = 'general';

    #[Url(as: 'grupo', except: '')]
    public string $group = '';

    // Modal de edición.
    public string $key = '';

    public bool $isNewKey = false;

    public string $singular = '';

    public string $plural = '';

    public string $gender = 'f';

    public string $short_description = '';

    public string $lore = '';

    /** @var TemporaryUploadedFile|null */
    public $icon = null;

    public function edit(string $key): void
    {
        $this->resetValidation();
        $this->reset('icon');

        $resolved = app(GlossaryResolver::class)->resolve($key, $this->course());
        $this->key = $key;
        $this->isNewKey = false;
        $this->singular = $resolved['singular'];
        $this->plural = $resolved['plural'];
        $this->gender = $resolved['gender'];
        $this->short_description = (string) $resolved['short_description'];
        $this->lore = (string) $resolved['lore'];

        Flux::modal('term')->show();
    }

    /** Desde el General: editar un personaje propio de un curso (para subirle el retrato). */
    public function editIn(int $courseId, string $key): void
    {
        $this->scope = (string) Course::findOrFail($courseId)->id;
        $this->group = '';
        $this->edit($key);
    }

    public function newKey(): void
    {
        $this->resetValidation();
        $this->reset('key', 'singular', 'plural', 'short_description', 'lore', 'icon');
        $this->gender = 'f';
        $this->isNewKey = true;

        Flux::modal('term')->show();
    }

    public function save(): void
    {
        $courseId = $this->course()?->id;

        $this->validate([
            'key' => ['required', 'string', 'max:100', 'regex:/^[a-z0-9_]+(\.[a-z0-9_]+)*$/'],
            'singular' => ['required', 'string', 'max:255'],
            'plural' => ['nullable', 'string', 'max:255'],
            'gender' => ['required', Rule::enum(Gender::class)],
            'short_description' => ['nullable', 'string', 'max:255'],
            'lore' => ['nullable', 'string', 'max:20000'],
            'icon' => ['nullable', 'image', 'mimes:'.implode(',', config('uploads.image.mimes')), 'max:'.config('uploads.image.max_kb')],
        ], ['key.regex' => 'La clave va en minúsculas, con puntos: story.dragon_intro.'], [
            'key' => 'clave', 'short_description' => 'descripción corta', 'lore' => 'historia',
        ]);

        $term = GlossaryTerm::firstOrNew(['key' => $this->key, 'course_id' => $courseId]);
        $term->fill([
            'singular' => $this->singular,
            'plural' => $this->plural ?: null,
            'gender' => $this->gender,
            'short_description' => $this->short_description ?: null,
            'lore' => $this->lore ?: null,
        ]);

        if ($this->icon) {
            if ($term->icon_path) {
                Storage::disk('public')->delete($term->icon_path);
            }
            $term->icon_path = $this->icon->storeAs('glossary', Str::uuid().'.'.$this->icon->extension(), 'public');
        }

        $term->save();

        Flux::modal('term')->close();
        Flux::toast(variant: 'success', text: 'Término guardado.');
    }

    /** Borra el valor de este ámbito: vuelve a usar el general o el de fábrica. */
    public function revert(string $key): void
    {
        $term = GlossaryTerm::where('key', $key)->where('course_id', $this->course()?->id)->first();

        if ($term) {
            if ($term->icon_path) {
                Storage::disk('public')->delete($term->icon_path);
            }
            $term->delete();
            Flux::toast(text: 'Se volvió al valor heredado.');
        }
    }

    /** Copia al curso los términos generales que el curso todavía no redefinió. */
    public function copyFromGeneral(): void
    {
        $course = $this->course();
        abort_unless($course !== null, 404);

        $existing = GlossaryTerm::where('course_id', $course->id)->pluck('key');
        $copied = 0;

        foreach (GlossaryTerm::whereNull('course_id')->whereNotIn('key', $existing)->get() as $general) {
            $copy = $general->replicate();
            $copy->course_id = $course->id;
            $copy->icon_path = null;
            $copy->save();
            $copied++;
        }

        Flux::toast(text: $copied === 0 ? 'No había términos generales para copiar.' : "Se copiaron {$copied} términos.");
    }

    public function mount(): void
    {
        $this->companionSize = Portraits::companion();
        $this->beastSize = Portraits::beast();
    }

    public function savePortraitSizes(): void
    {
        $this->validate([
            'companionSize' => ['required', 'integer', 'between:24,200'],
            'beastSize' => ['required', 'integer', 'between:24,200'],
        ], [], ['companionSize' => 'tamaño de la compañía', 'beastSize' => 'tamaño de las criaturas']);
        Setting::put('portrait_companion_px', (string) $this->companionSize);
        Setting::put('portrait_beast_px', (string) $this->beastSize);
        Flux::toast(variant: 'success', text: 'Tamaños guardados: ya se ven así en los nodos.');
    }

    private function course(): ?Course
    {
        return $this->scope === 'general' ? null : Course::find((int) $this->scope);
    }

    /** @return Collection<int, array{key: string, label: string, group: string}> */
    private function catalog(): Collection
    {
        $catalog = collect(config('glossary'))
            ->map(fn (array $entry, string $key) => ['key' => $key, 'label' => $entry['label'] ?? $key, 'group' => $entry['group'] ?? 'custom']);

        foreach (Level::orderBy('number')->get() as $level) {
            $catalog['level.'.$level->number] = ['key' => 'level.'.$level->number, 'label' => "Nombre del nivel {$level->number} ({$level->xp_required} XP)", 'group' => 'levels'];
        }

        // Claves creadas por el docente, en cualquier ámbito.
        foreach (GlossaryTerm::distinct()->pluck('key') as $key) {
            $catalog[$key] ??= ['key' => $key, 'label' => 'Clave propia', 'group' => str_starts_with($key, 'level.') ? 'levels' : 'custom'];
        }

        return $catalog->values();
    }

    public function render(GlossaryResolver $resolver)
    {
        $course = $this->course();

        $rows = $this->catalog()
            ->when($this->group !== '', fn ($rows) => $rows->where('group', $this->group))
            ->map(fn (array $row) => [
                ...$row,
                'term' => $resolver->resolve($row['key'], $course),
                'source' => $resolver->source($row['key'], $course),
            ]);

        return view('livewire.admin.glossary', [
            'rows' => $rows,
            'courses' => Course::orderBy('position')->get(['id', 'title']),
            'course' => $course,
            'groups' => self::GROUPS,
            'genders' => Gender::cases(),
            'courseCharacters' => $course ? collect() : $resolver->courseCharacters(['hero.', 'mentor.', 'companion.', 'beast.']),
            'previewCompanion' => $resolver->resolve('companion.theory', $course)['icon_path'],
            'previewBeast' => $resolver->resolve('beast.slime', $course)['icon_path'],
            'currentIcon' => $this->key !== '' ? GlossaryTerm::where('key', $this->key)->where('course_id', $course?->id)->value('icon_path') : null,
        ]);
    }
}
