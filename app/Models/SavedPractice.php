<?php

namespace App\Models;

use App\Enums\Language;
use App\Support\PracticeTools;
use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Support\Str;

/** D124: una práctica guardada en Mis prácticas (lo escrito en Herramientas → Practicar, con un nombre). */
#[Fillable(['user_id', 'language', 'title', 'code', 'stdin'])]
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

    /** «Python», «C#»… (el nombre de la herramienta). */
    public function languageLabel(): string
    {
        return PracticeTools::TOOLS[$this->language]['label'] ?? $this->language;
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
        return route('student.practice-tool', ['language' => $this->language, 'practica' => $this->id]);
    }
}
