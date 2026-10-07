<?php

namespace App\Livewire\Admin;

use App\Models\Course;
use App\Models\Node;
use App\Models\NodeStep;
use App\Rules\SafeUpload;
use App\Support\Narrative;
use App\Support\PracticeReferences;
use Flux\Flux;
use Livewire\Attributes\Title;
use Livewire\Attributes\Url;
use Livewire\Component;
use Livewire\WithFileUploads;

/**
 * Historia → Escenas (D88): las imágenes de las micro-misiones de un curso, nodo por nodo con su crónica.
 * Cada una con su ID (el nombre del archivo), el pedido para generarla y si ya tiene imagen; se sube desde acá.
 * También se cargan solas desde «escenas/<ID>.webp» de la carpeta del curso al importarlo. Solo el administrador.
 */
#[Title('Escenas')]
class Scenes extends Component
{
    use WithFileUploads;

    /** Estilo común de todas las imágenes (docs/historias/python-r01.md § 1). */
    public const STYLE = 'Estilo: anime/cómic cyber-arcana, 16:9 (1376×768), de noche, con luz propia; los personajes con su aspecto fijo (docs/historias/PERSONAJES.md).';

    #[Url(as: 'curso', except: '')]
    public string $courseSlug = '';

    #[Url(as: 'faltan', except: false)]
    public bool $onlyMissing = false;

    /** @var array<int, mixed> una imagen por micro-misión (id → archivo) */
    public array $uploads = [];

    public function mount(): void
    {
        if ($this->courseSlug === '') {
            $this->courseSlug = (string) Course::whereHas('nodes.steps')->orderBy('position')->value('slug');
        }
    }

    public function updatedUploads(mixed $file, string $stepId): void
    {
        $step = $this->steps()->findOrFail((int) $stepId);
        $this->validate(
            ["uploads.{$stepId}" => ['image', 'mimes:png,jpg,jpeg,webp', 'max:'.PracticeReferences::MAX_KB, new SafeUpload]],
            [], ["uploads.{$stepId}" => 'imagen'],
        );
        $step->update(['image_path' => PracticeReferences::store($file->getRealPath(), $file->extension())]);
        unset($this->uploads[$stepId]);
        Flux::toast(variant: 'success', text: "Imagen de {$step->code} guardada.");
    }

    public function removeImage(int $stepId): void
    {
        $this->steps()->findOrFail($stepId)->update(['image_path' => null]);
        Flux::toast(text: 'Imagen quitada: se ve el fondo del mundo.');
    }

    private function course(): ?Course
    {
        return $this->courseSlug !== '' ? Course::where('slug', $this->courseSlug)->first() : null;
    }

    private function steps()
    {
        return NodeStep::whereHas('node', fn ($q) => $q->where('course_id', $this->course()?->id));
    }

    public function render()
    {
        $course = $this->course();
        $nodes = $course ? Node::where('course_id', $course->id)->whereHas('steps')
            ->with(['steps' => fn ($q) => $q->when($this->onlyMissing, fn ($q) => $q->whereNull('image_path'))])
            ->orderBy('code')->get()->filter(fn ($node) => $node->steps->isNotEmpty()) : collect();
        $all = $course ? $this->steps()->count() : 0;

        return view('livewire.admin.scenes', [
            'courses' => Course::whereHas('nodes.steps')->orderBy('position')->orderBy('title')->get(),
            'course' => $course,
            'nodes' => $nodes,
            'total' => $all,
            'withImage' => $course ? $this->steps()->whereNotNull('image_path')->count() : 0,
            'chronicle' => fn (Node $node) => Narrative::render($node->chronicle, $course, auth()->user()),
            'scene' => fn (NodeStep $step) => Narrative::render($step->scene, $course, auth()->user()),
        ]);
    }
}
