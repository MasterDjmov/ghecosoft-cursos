<?php

namespace App\Livewire\Admin\Courses;

use App\Enums\CourseLevel;
use App\Enums\Language;
use App\Exceptions\TreeEditRefused;
use App\Models\Course;
use App\Services\CourseDeleter;
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

    /** Para borrar un curso con alumnos (D87) hay que escribir su nombre corto. */
    public string $deleteConfirm = '';

    public string $title = '';

    public string $slug = '';

    public string $short_description = '';

    public string $description = '';

    public string $language = 'python';

    public string $level = 'beginner';

    public bool $is_published = false;

    public bool $is_featured = false;

    public bool $is_upcoming = false;

    /** Temario corto para "Próximamente" y las tarjetas: un tema por línea. */
    public string $syllabus = '';

    public int $root_price = 10;

    public int $subscription_days = 30;

    /** @var TemporaryUploadedFile|null */
    public $logo = null;

    /** @var TemporaryUploadedFile|null */
    public $cover = null;

    public function mount(?Course $course = null): void
    {
        if ($course?->exists) {
            $this->course = $course;
            $this->fill($course->only(['title', 'slug', 'is_published', 'is_featured', 'is_upcoming', 'root_price', 'subscription_days']));
            $this->level = $course->level->value;
            $this->syllabus = (string) $course->syllabus;
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
            'level' => ['required', Rule::enum(CourseLevel::class)],
            'is_published' => ['boolean'],
            'is_featured' => ['boolean'],
            'is_upcoming' => ['boolean'],
            'syllabus' => ['nullable', 'string', 'max:2000'],
            'root_price' => ['required', 'integer', 'min:1', 'max:1000'],
            'subscription_days' => ['required', 'integer', 'min:1', 'max:3650'],
            'logo' => ['nullable', 'image', 'mimes:'.implode(',', config('uploads.image.mimes')), 'max:'.config('uploads.image.max_kb')],
            'cover' => ['nullable', 'image', 'mimes:'.implode(',', config('uploads.image.mimes')), 'max:'.config('uploads.image.max_kb')],
        ], [], ['cover' => 'portada', 'syllabus' => 'temario', 'slug' => 'dirección', 'root_price' => 'precio del raíz', 'subscription_days' => 'días de abono', 'short_description' => 'descripción corta']);

        unset($data['logo'], $data['cover']);
        foreach (['logo', 'cover'] as $image) {
            if ($this->{$image}) {
                $data[$image] = $this->{$image}->storeAs('courses', Str::uuid().'.'.$this->{$image}->extension(), 'public');
                if ($this->course?->{$image}) {
                    Storage::disk('public')->delete($this->course->{$image});
                }
            }
        }
        $data['syllabus'] = trim($data['syllabus'] ?? '') ?: null;

        if ($this->course) {
            $editor->updateCourse($this->course, $data);
            $this->logo = $this->cover = null;
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

    public function removeCover(): void
    {
        if ($this->course?->cover) {
            Storage::disk('public')->delete($this->course->cover);
            $this->course->update(['cover' => null]);
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

    /** Borra el curso aunque tenga alumnos (D87): todo lo de adentro se pierde. Solo el administrador. */
    public function deleteWithStudents(CourseDeleter $deleter)
    {
        abort_unless(auth()->user()->isAdmin() && $this->course, 403);
        if (trim($this->deleteConfirm) !== $this->course->slug) {
            $this->addError('deleteConfirm', 'Escribí exactamente «'.$this->course->slug.'» para confirmar.');

            return null;
        }

        $title = $this->course->title;
        $deleter->delete($this->course);
        Flux::toast(variant: 'success', text: '«'.$title.'» borrado, con todo lo de adentro.');

        return $this->redirectRoute('admin.courses.index', navigate: true);
    }

    public function render()
    {
        return view('livewire.admin.courses.form', [
            'languages' => Language::cases(), 'levels' => CourseLevel::cases(),
            'impact' => $this->course ? app(CourseDeleter::class)->impact($this->course) : null,
        ])
            ->title($this->course ? 'Editar '.$this->course->title : 'Nuevo curso');
    }
}
