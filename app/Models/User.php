<?php

namespace App\Models;

use App\Enums\RankingDisplay;
use App\Enums\Role;
use Database\Factories\UserFactory;
use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Attributes\Hidden;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Support\Carbon;
use Illuminate\Support\Str;
use Laravel\Fortify\Contracts\PasskeyUser;
use Laravel\Fortify\PasskeyAuthenticatable;
use Laravel\Fortify\TwoFactorAuthenticatable;

/**
 * @property int $id
 * @property string $name
 * @property string $last_name
 * @property string $username
 * @property string $email
 * @property Role $role
 * @property string|null $phone
 * @property string|null $dni
 * @property Carbon|null $birth_date
 * @property string|null $avatar
 * @property int $xp_total
 * @property string|null $nickname
 * @property RankingDisplay $ranking_display
 * @property bool $cv_public
 */
#[Fillable(['name', 'last_name', 'username', 'email', 'password', 'phone', 'dni', 'birth_date', 'avatar', 'nickname', 'ranking_display', 'cv_public'])]
#[Hidden(['password', 'two_factor_secret', 'two_factor_recovery_codes', 'remember_token'])]
class User extends Authenticatable implements PasskeyUser
{
    /** @use HasFactory<UserFactory> */
    use HasFactory, Notifiable, PasskeyAuthenticatable, TwoFactorAuthenticatable;

    /** Mismos valores por defecto que la base, para que estén en memoria al crear. */
    protected $attributes = [
        'role' => 'student',
        'xp_total' => 0,
        'ranking_display' => 'name',
        'cv_public' => false,
    ];

    protected function casts(): array
    {
        return [
            'email_verified_at' => 'datetime',
            'password' => 'hashed',
            'role' => Role::class,
            'birth_date' => 'date',
            'ranking_display' => RankingDisplay::class,
            'cv_public' => 'boolean',
            'xp_total' => 'integer',
        ];
    }

    public function isAdmin(): bool
    {
        return $this->role === Role::Admin;
    }

    public function isStudent(): bool
    {
        return $this->role === Role::Student;
    }

    public function fullName(): string
    {
        return trim($this->name.' '.$this->last_name);
    }

    public function isMinor(): bool
    {
        return $this->birth_date !== null && $this->birth_date->age < 18;
    }

    public function initials(): string
    {
        return Str::upper(Str::substr($this->name, 0, 1).Str::substr($this->last_name ?: $this->name, 0, 1));
    }

    public function subscriptions(): HasMany
    {
        return $this->hasMany(CourseSubscription::class);
    }

    public function enrollmentRequests(): HasMany
    {
        return $this->hasMany(EnrollmentRequest::class);
    }

    public function nodeUnlocks(): HasMany
    {
        return $this->hasMany(NodeUnlock::class);
    }

    public function submissions(): HasMany
    {
        return $this->hasMany(Submission::class);
    }

    public function coinTransactions(): HasMany
    {
        return $this->hasMany(CoinTransaction::class);
    }

    public function xpTransactions(): HasMany
    {
        return $this->hasMany(XpTransaction::class);
    }

    public function badges(): BelongsToMany
    {
        return $this->belongsToMany(Badge::class, 'user_badges')->withPivot('awarded_at');
    }

    public function guardianAuthorizations(): HasMany
    {
        return $this->hasMany(GuardianAuthorization::class);
    }
}
