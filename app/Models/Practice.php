<?php

namespace App\Models;

use App\Enums\PracticeEnvironment;
use App\Enums\SubmissionMode;
use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Support\Facades\Storage;

#[Fillable(['node_id', 'code', 'title', 'instructions', 'approval_criteria', 'is_required', 'submission_mode', 'environment', 'allowed_extensions', 'starter_code', 'sample_input', 'expected_output', 'reference_mobile', 'reference_desktop', 'reference_solution', 'coin_reward', 'xp_reward', 'position'])]
class Practice extends Model
{
    /** Mismos valores por defecto que la base. */
    protected $attributes = ['is_required' => true, 'submission_mode' => 'code', 'environment' => 'browser', 'coin_reward' => 0, 'xp_reward' => 0, 'position' => 0];

    /** Solo del docente: nunca sale en un array o JSON (D37). */
    protected $hidden = ['reference_solution'];

    protected function casts(): array
    {
        return [
            'is_required' => 'boolean',
            'submission_mode' => SubmissionMode::class,
            'environment' => PracticeEnvironment::class,
            'coin_reward' => 'integer',
            'xp_reward' => 'integer',
        ];
    }

    public function node(): BelongsTo
    {
        return $this->belongsTo(Node::class);
    }

    public function hasStudentActivity(): bool
    {
        return $this->submissions()->exists() || PracticeMark::where('practice_id', $this->id)->exists();
    }

    /** Pruebas extra (D73), solo del docente: no se cargan en las vistas del alumno. */
    public function tests(): HasMany
    {
        return $this->hasMany(PracticeTest::class)->orderBy('position');
    }

    public function submissions(): HasMany
    {
        return $this->hasMany(Submission::class);
    }

    /**
     * «Así tiene que quedar» (D77): las capturas de la página resuelta, para comparar.
     *
     * @return array{mobile: ?string, desktop: ?string}
     */
    public function referenceUrls(): array
    {
        return [
            'mobile' => $this->reference_mobile ? Storage::disk('public')->url($this->reference_mobile) : null,
            'desktop' => $this->reference_desktop ? Storage::disk('public')->url($this->reference_desktop) : null,
        ];
    }
}
