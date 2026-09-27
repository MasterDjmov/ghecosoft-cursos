<?php

namespace App\Livewire\Admin\Courses;

use App\Enums\Language;
use App\Exceptions\TreeEditRefused;
use App\Models\Course;
use App\Services\TreeEditor;
use App\Support\Reorder;
use Flux\Flux;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;
use Illuminate\Validation\Rule;
use Livewire\Attributes\Title;
use Livewire\Component;
use Livewire\Features\SupportFileUploads\TemporaryUploadedFile;
use Livewire\WithFileUploads;

/** Alta y edición de los datos de un curso (el árbol se edita aparte). */
#[Title('Datos del curso')]
class Form extends Component
{
    use WithFileUploads;

    public ?Course $course = null;

    public string $title = '';

    public string $slug = '';

    public string $short_description = '';

    public string $description = '';

    public string $language = 'python';

    public bool $is_published = false;

    public int $root_price = 10;

    public int $subscription_days = 30;

    /** @var TemporaryUploadedFile|null */
    public $logo = null;

    public function mount(?Course $course = null): void
    {
        if ($course?->exists) {
            $this->course = $course;
            $this->fill($course->only(['title', 'slug', 'is_published', 'root_price', 'subscription_days']));
            $this->description = (string) $course->description;
            $this->short_description = (string) $course->short_description;
            $this->language = $course->language->value;
        }
    }

    public function updatedTitle(string $value): void
    {
        if (! $this->course) {
            $this->slug = Str::slug($value);
        }
    }

    public function save(TreeEditor $editor)
    {
        $data = $this->validate([
            'title' => ['required', 'string', 'max:120'],
            'slug' => ['required', 'string', 'max:60', 'regex:/^[a-z0-9]+(-[a-z0-9]+)*$/', Rule::unique('courses', 'slug')->ignore($this->course)],
            'short_description' => ['nullable', 'string', 'max:255'],
            'description' => ['nullable', 'string', 'max:20000'],
            'language' => ['required', Rule::enum(Language::class)],
            'is_published' => ['boolean'],
            'root_price' => ['required', 'integer', 'min:1', 'max:1000'],
            'subscription_days' => ['required', 'integer', 'min:1', 'max:3650'],
            'logo' => ['nullable', 'image', 'mimes:'.implode(',', config('uploads.image.mimes')), 'max:'.config('uploads.image.max_kb')],
        ], [], ['slug' => 'dirección', 'root_price' => 'precio del raíz', 'subscription_days' => 'días de abono', 'short_description' => 'descripción corta']);

        unset($data['logo']);
        if ($this->logo) {
            $data['logo'] = $this->logo->storeAs('courses', Str::uuid().'.'.$this->logo->extension(), 'public');
            if ($this->course?->logo) {
                Storage::disk('public')->delete($this->course->logo);
            }
        }

        if ($this->course) {
            $editor->updateCourse($this->course, $data);
            $this->logo = null;
            Flux::toast(variant: 'success', text: 'Curso guardado.');

            return null;
        }

        $course = $editor->createCourse([...$data, 'position' => Reorder::next(Course::query())]);
        Flux::toast(variant: 'success', text: 'Curso creado con su nodo raíz. Ahora armá el árbol.');

        return $this->redirectRoute('admin.courses.tree', $course, navigate: true);
    }

    public function removeLogo(): void
    {
        if ($this->course?->logo) {
            Storage::disk('public')->delete($this->course->logo);
            $this->course->update(['logo' => null]);
        }
    }

    public function delete(TreeEditor $editor)
    {
        try {
            $editor->deleteCourse($this->course);
        } catch (TreeEditRefused $e) {
            Flux::modal('delete-course')->close();
            Flux::toast(variant: 'danger', text: $e->getMessage());

            return null;
        }

        Flux::toast(variant: 'success', text: 'Curso borrado.');

        return $this->redirectRoute('admin.courses.index', navigate: true);
    }

    public function render()
    {
        return view('livewire.admin.courses.form', ['languages' => Language::cases()])
            ->title($this->course ? 'Editar '.$this->course->title : 'Nuevo curso');
    }
}
