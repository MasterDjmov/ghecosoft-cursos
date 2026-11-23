<?php

namespace App\Models;

use App\Enums\Language;
use App\Support\PracticeTools;
use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Support\Str;

/**
 * D124: una práctica guardada en Mis prácticas: lo escrito en Herramientas (Practicar, el Gólem 8086 o la caja de la
 * Feria), con un nombre. `page` es el HTML de la página de la caja, si tiene.
 */
#[Fillable(['user_id', 'language', 'title', 'code', 'stdin', 'page'])]
class SavedPractice extends Model
{
    /** Cuántas puede guardar cada uno. */
    public const LIMIT = 200;

    /** Hasta cuántos caracteres de código. */
    public const MAX_CODE = 100_000;

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function messages(): HasMany
    {
        return $this->hasMany(PracticeMessage::class);
    }

    /** Los lenguajes de las herramientas que no son «Practicar»: el Gólem y la caja de la Feria. */
    public const OTHER_TOOLS = ['asm' => 'Ensamblador 8086', 'javascript' => 'JavaScript', 'typescript' => 'TypeScript'];

    /** «Python», «C#», «Ensamblador 8086»… */
    public function languageLabel(): string
    {
        return PracticeTools::TOOLS[$this->language]['label'] ?? self::OTHER_TOOLS[$this->language] ?? $this->language;
    }

    /** El nombre del archivo al bajarla: el título sin acentos ni espacios, con la extensión del lenguaje. */
    public function fileName(): string
    {
        $extension = Language::tryFrom($this->language)?->extension() ?? 'txt';

        return (Str::slug($this->title, '_') ?: 'practica').'.'.$extension;
    }

    /** Donde se abre: la herramienta de su lenguaje con la práctica cargada. */
    public function url(): string
    {
        return match ($this->language) {
            'asm' => route('student.asm-tool', ['practica' => $this->id]),
            'javascript', 'typescript' => route('student.js-tool', ['practica' => $this->id]),
            default => route('student.practice-tool', ['language' => $this->language, 'practica' => $this->id]),
        };
    }
}
