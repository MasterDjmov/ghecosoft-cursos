<?php

namespace App\Livewire\Admin\Nodes;

use App\Enums\NodeType;
use App\Enums\PracticeEnvironment;
use App\Enums\ResourceType;
use App\Enums\SubmissionMode;
use App\Exceptions\TreeEditRefused;
use App\Models\Badge;
use App\Models\Course;
use App\Models\Currency;
use App\Models\GlossaryTerm;
use App\Models\Node;
use App\Models\Practice;
use App\Services\TreeEditor;
use App\Support\Markdown;
use App\Support\Reorder;
use Flux\Flux;
use Illuminate\Support\Str;
use Illuminate\Validation\Rule;
use Livewire\Attributes\Title;
use Livewire\Attributes\Url;
use Livewire\Component;
use Livewire\Features\SupportFileUploads\TemporaryUploadedFile;
use Livewire\WithFileUploads;

/** Editor de un nodo: datos, contenido por secciones (D37), hojas (prácticas), recursos y soluciones del docente. */
#[Title('Editar nodo')]
class Edit extends Component
{
    use WithFileUploads;

    public Course $course;

    public Node $node;

    /** Abre el modal de hoja nueva al llegar desde el botón "+ Nueva hoja" del árbol. */
    #[Url(as: 'hoja', except: '')]
    public string $openPractice = '';

    // Datos del nodo.
    public string $title = '';

    public string $type = 'topic';

    public ?int $branch_id = null;

    public ?int $parent_id = null;

    public int $price = 10;

    /** 'course' | 'wildcard' (cualquier nodo salvo el raíz). */
    public string $paidWith = 'course';

    /** Requisitos extra (además del padre). @var list<int> */
    public array $requirementIds = [];

    public string $initialTab = 'data';

    public ?int $badge_id = null;

    public bool $is_published = true;

    public string $video_url = '';

    // Secciones del nodo (D37). `content` es la explicación.
    public string $chronicle = '';

    public string $objectives = '';

    public string $before_you_start = '';

    public string $content = '';

    public string $use_cases = '';

    public string $common_errors = '';

    public string $beast_key = '';

    /** Prueba del sello: [['question' => '', 'answer' => '']]. */
    public array $selfCheck = [];

    /** Solo del docente. */
    public string $teacher_solutions = '';

    public string $example_code = '';

    public string $expected_output = '';

    public string $sample_input = '';

    // Hoja en edición (modal).
    public ?int $practiceId = null;

    public string $practiceTitle = '';

    public string $practiceInstructions = '';

    public string $practiceCriteria = '';

    public string $practiceEnvironment = 'browser';

    public string $practiceExpectedOutput = '';

    public string $practiceSolution = '';

    public bool $practiceRequired = true;

    public string $practiceMode = 'code';

    public string $practiceExtensions = '';

    public string $practiceStarterCode = '';

    public string $practiceSampleInput = '';

    public int $practiceCoins = 0;

    public int $practiceXp = 10;

    // Recurso nuevo.
    public string $resourceType = 'link';

    public string $resourceTitle = '';

    public string $resourceUrl = '';

    /** @var TemporaryUploadedFile|null */
    public $resourceFile = null;

    public function mount(Course $course, Node $node): void
    {
        abort_unless($node->course_id === $course->id, 404);

        $this->fillFromNode();

        // "+ Nueva hoja" (?hoja=nueva) o una hoja tocada en el árbol dibujado (?hoja=12).
        if ($this->openPractice !== '') {
            $this->initialTab = 'practices';
            ctype_digit($this->openPractice) && $this->node->practices()->whereKey((int) $this->openPractice)->exists()
                ? $this->editPractice((int) $this->openPractice)
                : $this->newPractice();
            $this->openPractice = '';
        }
    }

    private function fillFromNode(): void
    {
        $node = $this->node;

        $this->title = $node->title;
        $this->type = $node->type->value;
        $this->branch_id = $node->branch_id;
        $this->parent_id = $node->parent_id;
        $this->price = $node->price;
        $this->paidWith = $node->priceCurrency?->is_wildcard ? 'wildcard' : 'course';
        $this->badge_id = $node->badge_id;
        $this->requirementIds = $node->requirements()->pluck('nodes.id')->map(fn ($id) => (string) $id)->all();
        $this->is_published = $node->is_published;
        $this->video_url = (string) $node->video_url;
        $this->chronicle = (string) $node->chronicle;
        $this->objectives = (string) $node->objectives;
        $this->before_you_start = (string) $node->before_you_start;
        $this->content = (string) $node->content;
        $this->use_cases = (string) $node->use_cases;
        $this->common_errors = (string) $node->common_errors;
        $this->beast_key = (string) $node->beast_key;
        $this->selfCheck = $node->selfCheckItems();
        $this->teacher_solutions = (string) $node->teacher_solutions;
        $this->example_code = (string) $node->example_code;
        $this->expected_output = (string) $node->expected_output;
        $this->sample_input = (string) $node->sample_input;
    }

    public function save(TreeEditor $editor): void
    {
        $isRoot = $this->node->isRoot();

        $this->validate([
            'title' => ['required', 'string', 'max:255'],
            'type' => $isRoot ? [] : ['required', Rule::in(array_map(fn (NodeType $t) => $t->value, NodeType::editable()))],
            'requirementIds' => ['array', 'max:20'],
            'requirementIds.*' => ['integer'],
            'branch_id' => ['nullable', Rule::exists('branches', 'id')->where('course_id', $this->course->id)],
            'parent_id' => $isRoot ? [] : ['required', 'integer'],
            'price' => ['required', 'integer', 'min:0', 'max:1000'],
            'badge_id' => ['nullable', Rule::exists('badges', 'id')],
            'is_published' => ['boolean'],
            'video_url' => ['nullable', 'url:https', 'max:500'],
            'chronicle' => ['nullable', 'string', 'max:5000'],
            'objectives' => ['nullable', 'string', 'max:5000'],
            'before_you_start' => ['nullable', 'string', 'max:5000'],
            'content' => ['nullable', 'string', 'max:65000'],
            'use_cases' => ['nullable', 'string', 'max:10000'],
            'common_errors' => ['nullable', 'string', 'max:20000'],
            'beast_key' => ['nullable', 'string', 'max:60', 'regex:/^beast\.[a-z0-9_.]+$/'],
            'selfCheck' => ['array', 'max:20'],
            'selfCheck.*.question' => ['nullable', 'string', 'max:1000'],
            'selfCheck.*.answer' => ['nullable', 'string', 'max:5000'],
            'teacher_solutions' => ['nullable', 'string', 'max:100000'],
            'example_code' => ['nullable', 'string', 'max:20000'],
            'expected_output' => ['nullable', 'string', 'max:5000'],
            'sample_input' => ['nullable', 'string', 'max:5000'],
        ], [], [
            'parent_id' => 'requisito', 'video_url' => 'video', 'branch_id' => 'rama', 'badge_id' => 'insignia',
            'chronicle' => 'crónica', 'objectives' => 'objetivos', 'before_you_start' => 'antes de empezar',
            'use_cases' => '¿para qué sirve?', 'common_errors' => 'errores habituales', 'beast_key' => 'criatura',
            'selfCheck.*.question' => 'pregunta', 'selfCheck.*.answer' => 'respuesta', 'teacher_solutions' => 'soluciones',
        ]);

        try {
            if ($this->is_published) {
                $editor->assertPublishable($this->node);
            }
            $editor->updateNode($this->node, [
                'title' => $this->title,
                'type' => $this->type,
                'branch_id' => $this->branch_id,
                'parent_id' => $this->parent_id,
                'price' => $this->price,
                'price_currency_id' => ! $isRoot && $this->paidWith === 'wildcard' ? Currency::wildcard()->id : null,
                'badge_id' => $this->type === NodeType::Boss->value ? $this->badge_id : null,
                'is_published' => $this->is_published,
                'video_url' => $this->video_url ?: null,
                'chronicle' => $this->chronicle ?: null,
                'objectives' => $this->objectives ?: null,
                'before_you_start' => $this->before_you_start ?: null,
                'content' => $this->content ?: null,
                'use_cases' => $this->use_cases ?: null,
                'common_errors' => $this->common_errors ?: null,
                'beast_key' => $this->beast_key ?: null,
                'self_check' => $this->cleanSelfCheck() ?: null,
                'teacher_solutions' => $this->teacher_solutions ?: null,
                'example_code' => $this->example_code ?: null,
                'example_language' => $this->example_code ? $this->course->language->value : null,
                'expected_output' => $this->expected_output ?: null,
                'sample_input' => $this->sample_input ?: null,
            ]);
            $editor->setRequirements($this->node->refresh(), $isRoot ? [] : $this->requirementIds);
        } catch (TreeEditRefused $e) {
            Flux::toast(variant: 'danger', text: $e->getMessage());

            return;
        }

        $this->node->refresh();
        $this->fillFromNode();
        Flux::toast(variant: 'success', text: 'Nodo guardado.');
    }

    public function addSelfCheck(): void
    {
        $this->selfCheck[] = ['question' => '', 'answer' => ''];
    }

    public function removeSelfCheck(int $index): void
    {
        unset($this->selfCheck[$index]);
        $this->selfCheck = array_values($this->selfCheck);
    }

    /** @return list<array{question: string, answer: string}> */
    private function cleanSelfCheck(): array
    {
        return collect($this->selfCheck)
            ->map(fn ($item) => ['question' => trim((string) ($item['question'] ?? '')), 'answer' => trim((string) ($item['answer'] ?? ''))])
            ->filter(fn ($item) => $item['question'] !== '')
            ->values()
            ->all();
    }

    public function newPractice(): void
    {
        $this->practiceId = null;
        $this->practiceTitle = '';
        $this->practiceInstructions = '';
        $this->practiceCriteria = '';
        $this->practiceEnvironment = PracticeEnvironment::Browser->value;
        $this->practiceExpectedOutput = '';
        $this->practiceSolution = '';
        $this->practiceRequired = true;
        $this->practiceMode = SubmissionMode::Code->value;
        $this->practiceExtensions = '';
        $this->practiceStarterCode = '';
        $this->practiceSampleInput = '';
        $this->practiceCoins = 3;
        $this->practiceXp = 10;
        $this->resetValidation();

        Flux::modal('practice')->show();
    }

    public function editPractice(int $practiceId): void
    {
        $practice = $this->findPractice($practiceId);

        $this->practiceId = $practice->id;
        $this->practiceTitle = $practice->title;
        $this->practiceInstructions = (string) $practice->instructions;
        $this->practiceCriteria = (string) $practice->approval_criteria;
        $this->practiceEnvironment = $practice->environment->value;
        $this->practiceExpectedOutput = (string) $practice->expected_output;
        $this->practiceSolution = (string) $practice->reference_solution;
        $this->practiceRequired = $practice->is_required;
        $this->practiceMode = $practice->submission_mode->value;
        $this->practiceExtensions = (string) $practice->allowed_extensions;
        $this->practiceStarterCode = (string) $practice->starter_code;
        $this->practiceSampleInput = (string) $practice->sample_input;
        $this->practiceCoins = $practice->coin_reward;
        $this->practiceXp = $practice->xp_reward;
        $this->resetValidation();

        Flux::modal('practice')->show();
    }

    public function savePractice(TreeEditor $editor): void
    {
        $this->validate([
            'practiceTitle' => ['required', 'string', 'max:255'],
            'practiceInstructions' => ['nullable', 'string', 'max:20000'],
            'practiceCriteria' => ['nullable', 'string', 'max:5000'],
            'practiceEnvironment' => ['required', Rule::enum(PracticeEnvironment::class)],
            'practiceExpectedOutput' => ['nullable', 'string', 'max:5000'],
            'practiceSolution' => ['nullable', 'string', 'max:50000'],
            'practiceRequired' => ['boolean'],
            'practiceMode' => ['required', Rule::enum(SubmissionMode::class)],
            'practiceExtensions' => ['nullable', 'string', 'max:100', 'regex:/^[a-z0-9]+(\s*,\s*[a-z0-9]+)*$/i'],
            'practiceStarterCode' => ['nullable', 'string', 'max:20000'],
            'practiceSampleInput' => ['nullable', 'string', 'max:5000'],
            'practiceCoins' => ['required', 'integer', 'min:0', 'max:1000'],
            'practiceXp' => ['required', 'integer', 'min:0', 'max:10000'],
        ], ['practiceExtensions.regex' => 'Escribí las extensiones separadas por coma, sin punto: py, txt, zip.'], [
            'practiceTitle' => 'título', 'practiceInstructions' => 'consigna', 'practiceCoins' => 'recompensa',
            'practiceXp' => 'XP', 'practiceExtensions' => 'extensiones', 'practiceCriteria' => 'criterio de aprobación',
            'practiceExpectedOutput' => 'salida esperada', 'practiceSolution' => 'solución de referencia',
        ]);

        $usesFile = in_array($this->practiceMode, [SubmissionMode::File->value, SubmissionMode::Both->value], true);

        $data = [
            'title' => $this->practiceTitle,
            'instructions' => $this->practiceInstructions ?: null,
            'approval_criteria' => $this->practiceCriteria ?: null,
            'environment' => $this->practiceEnvironment,
            'expected_output' => $this->practiceMode !== SubmissionMode::None->value ? ($this->practiceExpectedOutput ?: null) : null,
            'reference_solution' => $this->practiceSolution ?: null,
            'is_required' => $this->practiceRequired,
            'submission_mode' => $this->practiceMode,
            'allowed_extensions' => $usesFile ? (Str::of($this->practiceExtensions)->lower()->replaceMatches('/\s+/', '')->toString() ?: null) : null,
            'starter_code' => $this->practiceStarterCode ?: null,
            'sample_input' => $this->practiceSampleInput ?: null,
            'coin_reward' => $this->practiceCoins,
            'xp_reward' => $this->practiceXp,
        ];

        try {
            if ($this->practiceId) {
                $practice = $this->findPractice($this->practiceId);
                if (! $this->practiceRequired) {
                    $editor->assertCanBeOptional($practice);
                }
                $practice->update($data);
            } else {
                $editor->createPractice($this->node, $data);
            }
        } catch (TreeEditRefused $e) {
            $this->addError('practiceRequired', $e->getMessage());

            return;
        }

        Flux::modal('practice')->close();
        Flux::toast(variant: 'success', text: 'Hoja guardada.');
    }

    public function deletePractice(int $practiceId, TreeEditor $editor): void
    {
        try {
            $editor->deletePractice($this->findPractice($practiceId));
        } catch (TreeEditRefused $e) {
            Flux::toast(variant: 'danger', text: $e->getMessage());

            return;
        }

        Flux::toast(variant: 'success', text: 'Hoja borrada.');
    }

    public function sortPractice(int $id, int $position): void
    {
        Reorder::move($this->node->practices(), $this->findPractice($id), $position);
    }

    public function addResource(): void
    {
        $isFile = $this->resourceType === ResourceType::File->value;

        $this->validate([
            'resourceType' => ['required', Rule::enum(ResourceType::class)],
            'resourceTitle' => ['required', 'string', 'max:255'],
            'resourceUrl' => $isFile ? [] : ['required', 'url:http,https', 'max:500'],
            'resourceFile' => $isFile ? ['required', 'file', 'extensions:'.implode(',', config('uploads.resource.mimes')), 'max:'.config('uploads.resource.max_kb')] : [],
        ], [], ['resourceTitle' => 'título', 'resourceUrl' => 'link', 'resourceFile' => 'archivo']);

        $data = ['type' => $this->resourceType, 'title' => $this->resourceTitle, 'position' => Reorder::next($this->node->resources())];

        if ($isFile) {
            $extension = Str::lower($this->resourceFile->getClientOriginalExtension());
            $data['file_path'] = $this->resourceFile->storeAs('resources', Str::uuid().'.'.$extension, 'local');
            $data['original_name'] = Str::limit($this->resourceFile->getClientOriginalName(), 250, '');
        } else {
            $data['url'] = $this->resourceUrl;
        }

        $this->node->resources()->create($data);
        $this->reset('resourceTitle', 'resourceUrl', 'resourceFile');
        Flux::toast(variant: 'success', text: 'Recurso agregado.');
    }

    public function deleteResource(int $resourceId, TreeEditor $editor): void
    {
        $editor->deleteResource($this->node->resources()->findOrFail($resourceId));
    }

    public function sortResource(int $id, int $position): void
    {
        Reorder::move($this->node->resources(), $this->node->resources()->findOrFail($id), $position);
    }

    /**
     * Criaturas del bestiario: las del catálogo más las que el docente creó (general o del curso).
     *
     * @return array<string, string> clave => nombre
     */
    private function beastOptions(): array
    {
        $keys = collect(array_keys(config('glossary')))
            ->merge(GlossaryTerm::where('key', 'like', 'beast.%')
                ->where(fn ($q) => $q->whereNull('course_id')->orWhere('course_id', $this->course->id))
                ->pluck('key'))
            ->filter(fn ($key) => str_starts_with($key, 'beast.'))
            ->unique();

        return $keys->mapWithKeys(fn ($key) => [$key => Str::ucfirst(term($key, $this->course))])->sort()->all();
    }

    private function findPractice(int $practiceId): Practice
    {
        return $this->node->practices()->findOrFail($practiceId);
    }

    public function render(TreeEditor $editor)
    {
        $practices = $this->node->practices()->get();

        return view('livewire.admin.nodes.edit', [
            'practices' => $practices,
            'resources' => $this->node->resources()->get(),
            'branches' => $this->course->branches()->get(),
            'parentOptions' => $editor->allowedParents($this->course, $this->node),
            'badges' => Badge::where(fn ($q) => $q->whereNull('course_id')->orWhere('course_id', $this->course->id))->orderBy('name')->get(),
            'nodeTypes' => NodeType::editable(),
            'modes' => SubmissionMode::cases(),
            'environments' => PracticeEnvironment::cases(),
            'beasts' => $this->beastOptions(),
            'requiredReward' => $practices->where('is_required', true)->sum('coin_reward'),
            'optionalReward' => $practices->where('is_required', false)->sum('coin_reward'),
            'xpTotal' => $practices->sum('xp_reward'),
            'contentPreview' => Markdown::render($this->content),
        ])->title($this->node->title.' · '.$this->course->title);
    }
}
