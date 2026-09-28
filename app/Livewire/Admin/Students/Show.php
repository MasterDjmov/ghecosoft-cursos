<?php

namespace App\Livewire\Admin\Students;

use App\Concerns\ProfileValidationRules;
use App\Enums\CoinReason;
use App\Enums\XpReason;
use App\Exceptions\InsufficientFunds;
use App\Models\CoinTransaction;
use App\Models\Currency;
use App\Models\Submission;
use App\Models\User;
use App\Models\XpTransaction;
use App\Services\Ledger;
use App\Services\Ranking;
use App\Services\StudentAccounts;
use App\Support\HeroName;
use Flux\Flux;
use Illuminate\Support\Str;
use InvalidArgumentException;
use Livewire\Attributes\Locked;
use Livewire\Attributes\Title;
use Livewire\Component;

/** Ficha del alumno: cursos, abonos, saldos, movimientos, entregas y ajuste manual. */
#[Title('Alumno')]
class Show extends Component
{
    use ProfileValidationRules;

    public User $user;

    /** Cuenta y contacto: el docente los cambia para reactivar a quien perdió el acceso (D36). */
    public string $username = '';

    public string $email = '';

    public string $phone = '';

    /** Datos de acceso después de resetear la clave (se muestran una vez). */
    #[Locked]
    public ?array $credentials = null;

    /** 'xp' o el id de una moneda. */
    public string $target = 'xp';

    public int $amount = 0;

    public string $reason = '';

    /** Moderación del héroe (D38). */
    public string $heroName = '';

    public function mount(User $user): void
    {
        abort_unless($user->isStudent(), 404);
        $this->heroName = (string) $user->hero_name;
        $this->username = $user->username;
        $this->email = (string) $user->email;
        $this->phone = (string) $user->phone;
    }

    public function saveAccount()
    {
        $this->username = Str::lower(trim($this->username));
        $this->email = Str::lower(trim($this->email));
        $this->phone = trim($this->phone);

        $validated = $this->validate([
            'username' => $this->usernameRules($this->user->id),
            'email' => $this->emailRules($this->user->id),
            'phone' => $this->phoneRules(),
        ], $this->profileMessages(), ['username' => 'usuario', 'phone' => 'teléfono']);

        $renamed = $validated['username'] !== $this->user->username;
        $this->user->update([
            'username' => $validated['username'],
            'email' => $validated['email'] ?: null,
            'phone' => $validated['phone'] ?: null,
        ]);
        Flux::toast(variant: 'success', text: 'Cuenta actualizada.');

        // El usuario va en la URL de la ficha.
        if ($renamed) {
            return $this->redirectRoute('admin.students.show', $this->user, navigate: true);
        }
    }

    public function resetPassword(StudentAccounts $accounts): void
    {
        $password = $accounts->resetPassword($this->user);
        $this->credentials = [
            'message' => StudentAccounts::accessMessage($this->user, $password, reset: true),
            'whatsapp' => $this->user->whatsappUrl(),
        ];
        Flux::modal('credentials')->show();
    }

    public function saveHero(): void
    {
        $this->heroName = (string) HeroName::normalize($this->heroName);
        $this->validate(HeroName::rules('heroName', $this->user), HeroName::messages('heroName'), ['heroName' => 'nombre del héroe']);

        $this->user->update(['hero_name' => $this->heroName ?: null]);
        Ranking::forget();
        Flux::toast(variant: 'success', text: 'Héroe actualizado.');
    }

    /** Dar o quitar monedas o XP. El motivo es obligatorio y queda en el libro. */
    public function adjust(Ledger $ledger): void
    {
        $this->validate([
            'target' => ['required', 'string'],
            'amount' => ['required', 'integer', 'not_in:0', 'between:-10000,10000'],
            'reason' => ['required', 'string', 'min:3', 'max:255'],
        ], ['amount.not_in' => 'Poné un monto distinto de 0 (negativo para quitar).'], ['amount' => 'monto', 'reason' => 'motivo']);

        try {
            if ($this->target === 'xp') {
                $ledger->addXp($this->user, $this->amount, XpReason::ManualAdjustment, note: $this->reason, by: auth()->user());
            } else {
                $currency = Currency::findOrFail((int) $this->target);
                $this->amount > 0
                    ? $ledger->credit($this->user, $currency, $this->amount, CoinReason::ManualAdjustment, note: $this->reason, by: auth()->user())
                    : $ledger->debit($this->user, $currency, -$this->amount, CoinReason::ManualAdjustment, note: $this->reason, by: auth()->user());
            }
        } catch (InsufficientFunds|InvalidArgumentException) {
            $this->addError('amount', 'No alcanza el saldo para quitar esa cantidad.');

            return;
        }

        $this->reset('amount', 'reason');
        Flux::toast(variant: 'success', text: 'Ajuste registrado.');
    }

    public function render(Ledger $ledger)
    {
        $balances = $ledger->balances($this->user);

        return view('livewire.admin.students.show', [
            'subscriptions' => $this->user->subscriptions()->with(['course', 'cohort'])->orderByDesc('ends_at')->get(),
            'balances' => $balances,
            'currencies' => Currency::with('course')->get()->sortBy(fn ($c) => $c->is_wildcard ? 'zzz' : $c->course?->title),
            'coinMovements' => CoinTransaction::with(['currency.course', 'creator:id,name'])->where('user_id', $this->user->id)->latest('id')->limit(30)->get(),
            'xpMovements' => XpTransaction::with('creator:id,name')->where('user_id', $this->user->id)->latest('id')->limit(30)->get(),
            'submissions' => Submission::with('practice.node')->where('user_id', $this->user->id)->latest('submitted_at')->limit(15)->get(),
            'badges' => $this->user->badges()->get(),
        ])->title($this->user->fullName());
    }
}
