<?php

namespace App\Livewire\Settings;

use App\Concerns\ProfileValidationRules;
use App\Models\User;
use App\Services\Ranking;
use App\Support\HeroName;
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

    /** D38: nombre del héroe, público y único. */
    public string $hero_name = '';

    public function mount(): void
    {
        $user = Auth::user();

        $this->name = $user->name;
        $this->last_name = $user->last_name;
        $this->username = $user->username;
        $this->email = (string) $user->email;
        $this->phone = (string) $user->phone;
        $this->dni = (string) $user->dni;
        $this->birth_date = (string) $user->birth_date?->format('Y-m-d');
        $this->hero_name = (string) $user->hero_name;
    }

    public function saveHero(): void
    {
        $user = Auth::user();
        $this->hero_name = (string) HeroName::normalize($this->hero_name);
        $this->validate(HeroName::rules('hero_name', $user), HeroName::messages('hero_name'), ['hero_name' => 'nombre del héroe']);

        $user->update(['hero_name' => $this->hero_name ?: null]);
        Ranking::forget();
        Flux::toast(variant: 'success', text: $this->hero_name ? "¡Que empiece la aventura, {$this->hero_name}!" : 'Tu héroe vuelve a llamarse '.term('hero.name').'.');
    }

    public function updateProfileInformation(): void
    {
        $user = Auth::user();

        $this->username = Str::lower(trim($this->username));
        $this->email = Str::lower(trim($this->email));

        $validated = $this->validate([
            ...$this->profileRules($user->id),
            'dni' => ['nullable', 'regex:/^\d{7,8}$/', Rule::unique(User::class)->ignore($user->id)],
            'birth_date' => ['nullable', 'date', 'before:today'],
        ], [
            ...$this->profileMessages(),
            'dni.regex' => 'El DNI tiene que tener 7 u 8 números, sin puntos.',
        ]);

        $user->fill([
            ...$validated,
            'email' => $validated['email'] ?: null,
            'phone' => $validated['phone'] ?: null,
            'dni' => $validated['dni'] ?: null,
            'birth_date' => $validated['birth_date'] ?: null,
        ]);

        $user->save();

        Flux::toast(variant: 'success', text: __('Profile updated.'));
    }
}
