<?php

namespace App\Livewire\Admin\Students;

use App\Enums\Role;
use App\Models\CourseSubscription;
use App\Models\User;
use Livewire\Attributes\Title;
use Livewire\Attributes\Url;
use Livewire\Component;
use Livewire\WithPagination;

#[Title('Alumnos')]
class Index extends Component
{
    use WithPagination;

    #[Url(as: 'buscar', except: '')]
    public string $search = '';

    public function updatedSearch(): void
    {
        $this->resetPage();
    }

    public function render()
    {
        $students = User::where('role', Role::Student)
            ->when(trim($this->search) !== '', function ($q) {
                $term = '%'.trim($this->search).'%';
                $q->where(fn ($w) => $w->where('name', 'like', $term)->orWhere('last_name', 'like', $term)
                    ->orWhere('username', 'like', $term)->orWhere('email', 'like', $term)->orWhere('dni', 'like', $term));
            })
            ->orderBy('last_name')->orderBy('name')
            ->paginate(30);

        return view('livewire.admin.students.index', [
            'students' => $students,
            'active' => CourseSubscription::active()->whereIn('user_id', $students->pluck('id'))->pluck('user_id')->flip(),
        ]);
    }
}
