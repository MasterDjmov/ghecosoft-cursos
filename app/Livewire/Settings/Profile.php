<?php

namespace App\Livewire\Settings;

use App\Concerns\ProfileValidationRules;
use App\Models\User;
use Flux\Flux;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Str;
use Illuminate\Validation\Rule;
use Livewire\Attributes\Title;
use Livewire\Component;

#[Title('Mi cuenta')]
class Profile extends Component
{
    use ProfileValidationRules;

    public string $name = '';

    public string $last_name = '';

    public string $username = '';

    public string $email = '';

    public string $phone = '';

    public string $dni = '';

    public string $birth_date = '';

    public function mount(): void
    {
        $user = Auth::user();

        $this->name = $user->name;
        $this->last_name = $user->last_name;
        $this->username = $user->username;
        $this->email = $user->email;
        $this->phone = (string) $user->phone;
        $this->dni = (string) $user->dni;
        $this->birth_date = (string) $user->birth_date?->format('Y-m-d');
    }

    public function updateProfileInformation(): void
    {
        $user = Auth::user();

        $this->username = Str::lower(trim($this->username));
        $this->email = Str::lower(trim($this->email));

        $validated = $this->validate([
            ...$this->profileRules($user->id),
            'phone' => ['nullable', 'string', 'max:30'],
            'dni' => ['nullable', 'regex:/^\d{7,8}$/', Rule::unique(User::class)->ignore($user->id)],
            'birth_date' => ['nullable', 'date', 'before:today'],
        ], [
            'dni.regex' => 'El DNI tiene que tener 7 u 8 números, sin puntos.',
        ]);

        $user->fill([
            ...$validated,
            'phone' => $validated['phone'] ?: null,
            'dni' => $validated['dni'] ?: null,
            'birth_date' => $validated['birth_date'] ?: null,
        ]);

        $user->save();

        Flux::toast(variant: 'success', text: __('Profile updated.'));
    }
}
