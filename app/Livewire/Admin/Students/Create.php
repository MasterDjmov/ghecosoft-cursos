<?php

namespace App\Livewire\Admin\Students;

use App\Concerns\ProfileValidationRules;
use App\Models\Course;
use App\Services\StudentAccounts;
use Illuminate\Support\Str;
use Illuminate\Validation\Rule;
use Livewire\Attributes\Locked;
use Livewire\Attributes\Title;
use Livewire\Component;

/** El docente le crea la cuenta a un alumno (sin email si hace falta, D36). */
#[Title('Nuevo alumno')]
class Create extends Component
{
    use ProfileValidationRules;

    public string $name = '';

    public string $last_name = '';

    public string $username = '';

    public string $email = '';

    public string $phone = '';

    public string $birth_date = '';

    public string $password = '';

    /** Inscripción directa (opcional). */
    public string $courseId = '';

    public string $cohortId = '';

    /** Datos de acceso para copiar, después de crearla. */
    #[Locked]
    public ?array $created = null;

    public function mount(): void
    {
        $this->password = StudentAccounts::temporaryPassword();
    }

    /** Propone el usuario a partir del nombre, si todavía está vacío. */
    public function suggestUsername(): void
    {
        if ($this->username !== '' || trim($this->name) === '') {
            return;
        }
        $base = Str::of($this->name.' '.$this->last_name)->ascii()->lower()->replaceMatches('/[^a-z0-9]+/', '_')->trim('_')->limit(24, '')->toString();
        $this->username = strlen($base) >= 3 ? $base : '';
    }

    public function updatedCourseId(): void
    {
        $this->cohortId = '';
    }

    public function newPassword(): void
    {
        $this->password = StudentAccounts::temporaryPassword();
    }

    public function save(StudentAccounts $accounts): void
    {
        $this->username = Str::lower(trim($this->username));
        $this->email = Str::lower(trim($this->email));
        $this->phone = trim($this->phone);
        $this->password = trim($this->password);

        $validated = $this->validate([
            ...$this->profileRules(),
            'birth_date' => ['nullable', 'date', 'before:today'],
            'password' => ['required', 'string', 'min:6', 'max:64'],
            'courseId' => ['nullable', Rule::exists('courses', 'id')],
            'cohortId' => ['nullable', Rule::exists('cohorts', 'id')->where('course_id', (int) $this->courseId)],
        ], $this->profileMessages(), [
            'username' => 'usuario', 'phone' => 'teléfono', 'birth_date' => 'fecha de nacimiento', 'password' => 'clave provisoria',
            'courseId' => 'curso', 'cohortId' => 'comisión',
        ]);

        $course = $this->courseId !== '' ? Course::find((int) $this->courseId) : null;
        $student = $accounts->create([
            'name' => trim($validated['name']),
            'last_name' => trim($validated['last_name']),
            'username' => $validated['username'],
            'email' => $validated['email'] ?: null,
            'phone' => $validated['phone'] ?: null,
            'birth_date' => $validated['birth_date'] ?: null,
        ], $this->password, auth()->user(), $course, $this->cohortId !== '' ? (int) $this->cohortId : null);

        $this->created = [
            'name' => $student->fullName(),
            'username' => $student->username,
            'message' => StudentAccounts::accessMessage($student, $this->password),
            'whatsapp' => $student->whatsappUrl(),
            'course' => $course?->title,
            'minor' => $student->isMinor(),
        ];
        $this->reset('name', 'last_name', 'username', 'email', 'phone', 'birth_date', 'courseId', 'cohortId');
        $this->password = StudentAccounts::temporaryPassword();
    }

    public function createAnother(): void
    {
        $this->created = null;
    }

    public function render()
    {
        $courses = Course::orderBy('title')->get(['id', 'title', 'is_published']);

        return view('livewire.admin.students.create', [
            'courses' => $courses,
            'cohorts' => $this->courseId !== '' ? $courses->firstWhere('id', (int) $this->courseId)?->cohorts()->orderBy('name')->get() ?? collect() : collect(),
        ]);
    }
}
