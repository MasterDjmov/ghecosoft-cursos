<?php

namespace App\Livewire\Admin\Nodes;

use App\Enums\NodeType;
use App\Enums\ResourceType;
use App\Enums\SubmissionMode;
use App\Exceptions\TreeEditRefused;
use App\Models\Badge;
use App\Models\Course;
use App\Models\Currency;
use App\Models\Node;
use App\Models\Practice;
use App\Services\TreeEditor;
use App\Support\Reorder;
use Flux\Flux;
use Illuminate\Support\Str;
use Illuminate\Validation\Rule;
use Livewire\Attributes\Title;
use Livewire\Attributes\Url;
use Livewire\Component;
use Livewire\Features\SupportFileUploads\TemporaryUploadedFile;
use Livewire\WithFileUploads;

/** Editor de un nodo: datos, contenido, hojas (prácticas) y recursos. */
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

    /** 'course' | 'wildcard' (solo extras). */
    public string $paidWith = 'course';

    public string $initialTab = 'data';

    public ?int $badge_id = null;

    public bool $is_published = true;

    public string $video_url = '';

    public string $content = '';

    public string $example_code = '';

    public string $expected_output = '';

    public string $sample_input = '';

    // Hoja en edición (modal).
    public ?int $practiceId = null;

    public string $practiceTitle = '';

    public string $practiceInstructions = '';

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

        if ($this->openPractice === 'nueva') {
            $this->initialTab = 'practices';
            $this->newPractice();
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
        $this->is_published = $node->is_published;
        $this->video_url = (string) $node->video_url;
        $this->content = (string) $node->content;
        $this->example_code = (string) $node->example_code;
        $this->expected_output = (string) $node->expected_output;
        $this->sample_input = (string) $node->sample_input;
    }

    public function save(TreeEditor $editor): void
    {
        $isRoot = $this->node->isRoot();

        $this->validate([
            'title' => ['required', 'string', 'max:255'],
            'type' => $isRoot ? [] : ['required', Rule::in([NodeType::Topic->value, NodeType::Boss->value, NodeType::Extra->value])],
            'branch_id' => ['nullable', Rule::exists('branches', 'id')->where('course_id', $this->course->id)],
            'parent_id' => $isRoot ? [] : ['required', 'integer'],
            'price' => ['required', 'integer', 'min:0', 'max:1000'],
            'badge_id' => ['nullable', Rule::exists('badges', 'id')],
            'is_published' => ['boolean'],
            'video_url' => ['nullable', 'url:https', 'max:500'],
            'content' => ['nullable', 'string', 'max:65000'],
            'example_code' => ['nullable', 'string', 'max:20000'],
            'expected_output' => ['nullable', 'string', 'max:5000'],
            'sample_input' => ['nullable', 'string', 'max:5000'],
        ], [], ['parent_id' => 'requisito', 'video_url' => 'video', 'branch_id' => 'rama', 'badge_id' => 'insignia']);

        try {
            $editor->updateNode($this->node, [
                'title' => $this->title,
                'type' => $this->type,
                'branch_id' => $this->branch_id,
                'parent_id' => $this->parent_id,
                'price' => $this->price,
                'price_currency_id' => $this->type === NodeType::Extra->value && $this->paidWith === 'wildcard' ? Currency::wildcard()->id : null,
                'badge_id' => $this->type === NodeType::Boss->value ? $this->badge_id : null,
                'is_published' => $this->is_published,
                'video_url' => $this->video_url ?: null,
                'content' => $this->content ?: null,
                'example_code' => $this->example_code ?: null,
                'example_language' => $this->example_code ? $this->course->language->value : null,
                'expected_output' => $this->expected_output ?: null,
                'sample_input' => $this->sample_input ?: null,
            ]);
        } catch (TreeEditRefused $e) {
            Flux::toast(variant: 'danger', text: $e->getMessage());

            return;
        }

        $this->node->refresh();
        $this->fillFromNode();
        Flux::toast(variant: 'success', text: 'Nodo guardado.');
    }

    public function newPractice(): void
    {
        $this->practiceId = null;
        $this->practiceTitle = '';
        $this->practiceInstructions = '';
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
            'practiceRequired' => ['boolean'],
            'practiceMode' => ['required', Rule::enum(SubmissionMode::class)],
            'practiceExtensions' => ['nullable', 'string', 'max:100', 'regex:/^[a-z0-9]+(\s*,\s*[a-z0-9]+)*$/i'],
            'practiceStarterCode' => ['nullable', 'string', 'max:20000'],
            'practiceSampleInput' => ['nullable', 'string', 'max:5000'],
            'practiceCoins' => ['required', 'integer', 'min:0', 'max:1000'],
            'practiceXp' => ['required', 'integer', 'min:0', 'max:10000'],
        ], ['practiceExtensions.regex' => 'Escribí las extensiones separadas por coma, sin punto: py, txt, zip.'], [
            'practiceTitle' => 'título', 'practiceInstructions' => 'consigna', 'practiceCoins' => 'recompensa',
            'practiceXp' => 'XP', 'practiceExtensions' => 'extensiones',
        ]);

        $usesFile = in_array($this->practiceMode, [SubmissionMode::File->value, SubmissionMode::Both->value], true);

        $data = [
            'title' => $this->practiceTitle,
            'instructions' => $this->practiceInstructions ?: null,
            'is_required' => $this->practiceRequired,
            'submission_mode' => $this->practiceMode,
            'allowed_extensions' => $usesFile ? (Str::of($this->practiceExtensions)->lower()->replaceMatches('/\s+/', '')->toString() ?: null) : null,
            'starter_code' => $this->practiceStarterCode ?: null,
            'sample_input' => $this->practiceSampleInput ?: null,
            'coin_reward' => $this->practiceCoins,
            'xp_reward' => $this->practiceXp,
        ];

        if ($this->practiceId) {
            $this->findPractice($this->practiceId)->update($data);
        } else {
            $editor->createPractice($this->node, $data);
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
            'nodeTypes' => [NodeType::Topic, NodeType::Boss, NodeType::Extra],
            'modes' => SubmissionMode::cases(),
            'requiredReward' => $practices->where('is_required', true)->sum('coin_reward'),
            'optionalReward' => $practices->where('is_required', false)->sum('coin_reward'),
            'xpTotal' => $practices->sum('xp_reward'),
            'contentPreview' => Str::markdown($this->content, ['html_input' => 'escape', 'allow_unsafe_links' => false]),
        ])->title($this->node->title.' · '.$this->course->title);
    }
}
