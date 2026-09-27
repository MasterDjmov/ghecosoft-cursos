<?php

namespace App\Livewire\Admin\Courses;

use App\Services\CourseImporter;
use Livewire\Attributes\Title;
use Livewire\Component;
use Livewire\Features\SupportFileUploads\TemporaryUploadedFile;
use Livewire\WithFileUploads;

/** Importar o actualizar un curso completo desde archivos .md (docs/FORMATO-CURSO.md). */
#[Title('Importar curso')]
class Import extends Component
{
    use WithFileUploads;

    /** @var list<TemporaryUploadedFile> */
    public array $files = [];

    /** Resultado de la última revisión o importación. */
    public ?array $report = null;

    /** Si el último informe fue una importación real (no una revisión). */
    public bool $applied = false;

    public function updatedFiles(): void
    {
        $this->reset('report', 'applied');
    }

    public function review(CourseImporter $importer): void
    {
        $this->run($importer, apply: false);
    }

    public function import(CourseImporter $importer): void
    {
        $this->run($importer, apply: true);
    }

    private function run(CourseImporter $importer, bool $apply): void
    {
        $this->validate([
            'files' => ['required', 'array', 'min:1', 'max:40'],
            'files.*' => ['file', 'extensions:md,txt', 'max:2048'],
        ], [], ['files' => 'archivos', 'files.*' => 'archivo']);

        // Se leen en orden por nombre: 00-curso.md, 01-rama.md…
        $contents = collect($this->files)
            ->map(fn (TemporaryUploadedFile $file) => ['name' => $file->getClientOriginalName(), 'content' => (string) file_get_contents($file->getRealPath())])
            ->sortBy('name')
            ->values()
            ->all();

        $this->report = $importer->import($contents, dryRun: ! $apply)->toArray();
        $this->applied = $apply && $this->report['errors'] === [];
    }

    public function render()
    {
        return view('livewire.admin.courses.import');
    }
}
