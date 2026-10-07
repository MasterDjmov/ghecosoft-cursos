<?php

namespace App\Livewire\Admin\Students;

use App\Concerns\ProfileValidationRules;
use App\Enums\CoinReason;
use App\Enums\Role;
use App\Enums\XpReason;
use App\Exceptions\InsufficientFunds;
use App\Models\Currency;
use App\Models\Hero;
use App\Models\PracticeMessage;
use App\Models\Submission;
use App\Models\User;
use App\Services\Heroes;
use App\Services\Ledger;
use App\Services\Ranking;
use App\Services\SingleSession;
use App\Services\StudentAccounts;
use App\Services\TeacherScope;
use App\Support\HeroName;
use Flux\Flux;
use Illuminate\Support\Facades\DB;
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
        // El docente (D72) solo abre la ficha de los alumnos de sus comisiones.
        $this->authorize('viewStudent', $user);
        $this->heroName = (string) $user->hero_name;
        $this->username = $user->username;
        $this->email = (string) $user->email;
        $this->phone = (string) $user->phone;
    }

    public function saveAccount()
    {
        $this->onlyAdmin();
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

    /** Rol docente (D72): la cuenta pasa a docente; sus abonos y progreso quedan guardados. */
    public function promote()
    {
        $this->onlyAdmin();
        $this->user->forceFill(['role' => Role::Teacher])->save();
        Flux::toast(variant: 'success', text: $this->user->fullName().' ahora es docente.');

        return $this->redirectRoute('admin.students.index', ['ver' => 'docentes'], navigate: true);
    }

    /** Lo que no hace un docente: cuenta, monedas, héroe, seguridad, comisiones desde la ficha. */
    private function onlyAdmin(): void
    {
        abort_unless(auth()->user()->isAdmin(), 403);
    }

    /** Para eliminar la cuenta (D87) hay que escribir su usuario. */
    public string $deleteConfirm = '';

    /** Eliminar la cuenta del alumno con todo lo suyo (D87). Solo el administrador. */
    public function deleteAccount(StudentAccounts $accounts)
    {
        $this->onlyAdmin();
        if (trim($this->deleteConfirm) !== $this->user->username) {
            $this->addError('deleteConfirm', 'Escribí exactamente «'.$this->user->username.'» para confirmar.');

            return null;
        }

        $name = $this->user->fullName();
        $accounts->delete($this->user);
        Flux::toast(variant: 'success', text: 'Se eliminó la cuenta de '.$name.'.');

        return $this->redirectRoute('admin.students.index', navigate: true);
    }

    /** Para reiniciar la cuenta hay que escribir su usuario. */
    public string $resetConfirm = '';

    /** Reiniciar la cuenta: queda sin cursos ni progreso, pero conserva el usuario y la clave. Solo el administrador. */
    public function resetAccount(StudentAccounts $accounts): void
    {
        $this->onlyAdmin();
        if (trim($this->resetConfirm) !== $this->user->username) {
            $this->addError('resetConfirm', 'Escribí exactamente «'.$this->user->username.'» para confirmar.');

            return;
        }

        $accounts->reset($this->user);
        $this->resetConfirm = '';
        $this->user->refresh();
        Flux::modal('reset-account')->close();
        Flux::toast(variant: 'success', text: 'Cuenta de '.$this->user->fullName().' reiniciada: ya no está en ningún curso. Habilitalo cuando quieras para que empiece de cero.');
    }

    /** Pausar la cuenta (D65): se cortan todas sus sesiones y no puede entrar hasta reactivarla. */
    public function block(SingleSession $sessions): void
    {
        $this->onlyAdmin();
        $sessions->block($this->user);
        Flux::toast(variant: 'success', text: 'Cuenta pausada: se cerraron sus sesiones.');
    }

    public function unblock(SingleSession $sessions): void
    {
        $this->onlyAdmin();
        $sessions->unblock($this->user);
        Flux::toast(variant: 'success', text: 'Cuenta reactivada.');
    }

    public function resetPassword(StudentAccounts $accounts): void
    {
        $this->authorize('resetPassword', $this->user);
        $password = $accounts->resetPassword($this->user);
        $this->credentials = [
            'message' => StudentAccounts::accessMessage($this->user, $password, reset: true),
            'whatsapp' => $this->user->whatsappUrl(),
        ];
        Flux::modal('credentials')->show();
    }

    public function saveHero(): void
    {
        $this->onlyAdmin();
        $this->heroName = (string) HeroName::normalize($this->heroName);
        $this->validate(HeroName::rules('heroName', $this->user), HeroName::messages('heroName'), ['heroName' => 'nombre del héroe']);

        $this->user->update(['hero_name' => $this->heroName ?: null]);
        Ranking::forget();
        Flux::toast(variant: 'success', text: 'Héroe actualizado.');
    }

    /** Comisión del alumno en un curso ('' = sin comisión). Es solo una etiqueta de sus abonos. */
    public function changeCohort(StudentAccounts $accounts, int $courseId, string $cohortId): void
    {
        $this->onlyAdmin();
        $course = $this->user->subscriptions()->where('course_id', $courseId)->firstOrFail()->course;

        try {
            $accounts->changeCohort($this->user, $course, $cohortId === '' ? null : (int) $cohortId);
        } catch (InvalidArgumentException) {
            Flux::toast(variant: 'danger', text: 'Esa comisión no es de este curso.');

            return;
        }

        Flux::toast(variant: 'success', text: 'Comisión actualizada.');
    }

    /** Reiniciar un héroe (D89): se devuelve el oro de los atributos y vuelve a «Tomá el control». */
    public function resetHero(int $heroId, Heroes $heroes): void
    {
        $hero = Hero::where('user_id', $this->user->id)->findOrFail($heroId);
        $this->authorize('resetHero', [$this->user, $hero->course]);

        $refund = $heroes->reset($hero, auth()->user());
        $this->dispatch('ledger-updated');
        Flux::toast(variant: 'success', text: 'Héroe reiniciado'.($refund > 0 ? ': se le devolvieron '.$refund.' de oro.' : '.'));
    }

    /** Dar o quitar monedas o XP. El motivo es obligatorio y queda en el libro. */
    public function adjust(Ledger $ledger): void
    {
        $this->onlyAdmin();
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
        $this->dispatch('ledger-updated');
        Flux::toast(variant: 'success', text: 'Ajuste registrado.');
    }

    public function render(Ledger $ledger)
    {
        $balances = $ledger->balances($this->user);

        $subscriptions = $this->user->subscriptions()->with(['course.cohorts', 'cohort'])->orderByDesc('ends_at')->get();

        return view('livewire.admin.students.show', [
            'subscriptions' => $subscriptions,
            // Un curso por fila (el abono más reciente manda) para elegir la comisión.
            'courseCohorts' => $subscriptions->unique('course_id')->filter(fn ($s) => $s->course->cohorts->isNotEmpty())->values(),
            'balances' => $balances,
            // Sus héroes (D89), solo los de cursos que este usuario puede corregir.
            'heroes' => Hero::with('course')->where('user_id', $this->user->id)->get()
                ->filter(fn (Hero $hero) => auth()->user()->can('resetHero', [$this->user, $hero->course]))
                ->map(fn (Hero $hero) => ['hero' => $hero, 'name' => app(Heroes::class)->protagonist($hero->course)['name'] ?? 'Héroe', 'spent' => app(Heroes::class)->spentOnStats($hero)]),
            'currencies' => Currency::with('course')->get()->sortBy(fn ($c) => $c->is_wildcard ? 'zzz' : $c->course?->title),
            'messageThreads' => app(TeacherScope::class)->messages(PracticeMessage::query(), auth()->user())->where('student_id', $this->user->id)
                ->selectRaw('practice_id, count(*) as total, sum(case when read_at is null and author_id = student_id then 1 else 0 end) as unread, max(created_at) as last_at')
                ->groupBy('practice_id')->orderByDesc('last_at')->with('practice.node')->get(),
            'evictions' => DB::table('session_evictions')->where('user_id', $this->user->id)
                ->where('created_at', '>=', now()->subDays(30))->latest('created_at')->limit(20)->get(),
            'submissions' => app(TeacherScope::class)->submissions(Submission::query(), auth()->user())->with('practice.node')->where('user_id', $this->user->id)->latest('submitted_at')->limit(15)->get(),
            'badges' => $this->user->badges()->get(),
        ])->title($this->user->fullName());
    }
}
