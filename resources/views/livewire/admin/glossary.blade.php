<div class="mx-auto flex w-full max-w-6xl flex-col gap-6 p-4 sm:p-8">
    <x-admin.page-header title="Diccionario"
        subtitle="Los nombres del juego y partes de la historia. Un curso usa su propio término; si no lo tiene, el general; si tampoco, el de fábrica.">
        <x-slot:actions>
            @if ($course)
                <flux:button icon="document-duplicate" wire:click="copyFromGeneral">Copiar del general</flux:button>
            @endif
            <flux:button variant="primary" icon="plus" wire:click="newKey">Clave propia</flux:button>
        </x-slot:actions>
    </x-admin.page-header>

    <div class="grid gap-4 sm:grid-cols-2">
        <flux:select wire:model.live="scope" label="Ámbito">
            <flux:select.option value="general">General (toda la plataforma)</flux:select.option>
            @foreach ($courses as $option)
                <flux:select.option :value="(string) $option->id">Curso: {{ $option->title }}</flux:select.option>
            @endforeach
        </flux:select>
        <flux:select wire:model.live="group" label="Grupo">
            <flux:select.option value="">Todos</flux:select.option>
            @foreach ($groups as $value => $label)
                <flux:select.option :value="$value">{{ $label }}</flux:select.option>
            @endforeach
        </flux:select>
    </div>

    <div class="panel overflow-hidden">
        <ul class="divide-y divide-outline">
            @foreach ($rows as $row)
                @php
                    [$sourceLabel, $sourceColor] = match ($row['source']) {
                        'course' => ['Este curso', 'cyan'],
                        'general' => [$course ? 'Heredado del general' : 'General', $course ? 'zinc' : 'cyan'],
                        default => ['De fábrica', 'zinc'],
                    };
                    $isOwn = $row['source'] === ($course ? 'course' : 'general');
                @endphp
                <li class="flex flex-col gap-3 p-4 sm:flex-row sm:items-center" wire:key="term-{{ $row['key'] }}">
                    <div class="flex min-w-0 flex-1 items-center gap-3">
                        @if ($row['term']['icon_path'])
                            <img src="{{ Storage::disk('public')->url($row['term']['icon_path']) }}" alt="" class="size-9 shrink-0 rounded-md object-cover">
                        @else
                            <div class="grid size-9 shrink-0 place-items-center rounded-md bg-surface-highest font-mono text-xs text-ink-muted">{{ $row['term']['gender'] === 'f' ? 'la' : 'el' }}</div>
                        @endif
                        <div class="flex min-w-0 flex-col gap-0.5">
                            <div class="flex flex-wrap items-center gap-2">
                                <span class="font-medium text-white">{{ $row['term']['singular'] }}</span>
                                @if ($row['term']['plural'] !== $row['term']['singular'])
                                    <span class="text-sm text-ink-muted">/ {{ $row['term']['plural'] }}</span>
                                @endif
                                <flux:badge size="sm" :color="$sourceColor">{{ $sourceLabel }}</flux:badge>
                            </div>
                            <p class="text-xs text-ink-muted"><code class="font-mono text-primary-bright/80">{{ $row['key'] }}</code> · {{ $row['label'] }}</p>
                        </div>
                    </div>
                    <div class="flex shrink-0 gap-1">
                        <flux:button size="xs" icon="pencil-square" wire:click="edit('{{ $row['key'] }}')">Editar</flux:button>
                        @if ($isOwn)
                            <flux:button size="xs" variant="ghost" icon="arrow-uturn-left" wire:click="revert('{{ $row['key'] }}')"
                                wire:confirm="¿Borrar este valor y volver al heredado?">Restaurar</flux:button>
                        @endif
                    </div>
                </li>
            @endforeach
        </ul>
    </div>

    <flux:modal name="term" class="w-full max-w-xl">
        <form wire:submit="save" class="flex flex-col gap-5">
            <div class="flex flex-col gap-1">
                <flux:heading size="lg">{{ $isNewKey ? 'Clave propia' : 'Editar término' }}</flux:heading>
                <flux:text>Ámbito: {{ $course ? 'curso '.$course->title : 'general' }}</flux:text>
            </div>

            @if ($isNewKey)
                <flux:input wire:model="key" label="Clave" placeholder="story.dragon_intro" description:trailing="Fija, en minúsculas; la usa el código." />
            @else
                <flux:input :value="$key" label="Clave" disabled />
            @endif

            <div class="grid gap-5 sm:grid-cols-3">
                <flux:input wire:model.live.debounce.300ms="singular" label="Singular" />
                <flux:input wire:model.live.debounce.300ms="plural" label="Plural" />
                <flux:select wire:model.live="gender" label="Género">
                    @foreach ($genders as $option)
                        <flux:select.option :value="$option->value">{{ $option->label() }}</flux:select.option>
                    @endforeach
                </flux:select>
            </div>

            <div class="rounded-lg border border-outline bg-surface-lowest/60 p-3 text-sm">
                <span class="tech-label">Así lo ve el alumno</span>
                <p class="mt-1 text-ink">
                    {{ $gender === 'f' ? 'la' : 'el' }} {{ $singular ?: '…' }} · ganaste 1 {{ $singular ?: '…' }} · ganaste 3 {{ $plural ?: $singular ?: '…' }}
                </p>
            </div>

            <flux:input wire:model="short_description" label="Descripción corta" description:trailing="Aparece como leyenda o tooltip." />
            <flux:textarea wire:model="lore" label="Historia (opcional)" rows="5" description:trailing="Texto narrativo en markdown: la crónica del rango, la presentación del jefe…" />

            <div class="flex flex-col gap-2">
                <flux:label>Ícono o imagen (opcional)</flux:label>
                <div class="flex items-center gap-3">
                    @if ($icon && $icon->isPreviewable())
                        <img src="{{ $icon->temporaryUrl() }}" alt="" class="size-12 rounded-md object-cover">
                    @elseif ($currentIcon)
                        <img src="{{ Storage::disk('public')->url($currentIcon) }}" alt="" class="size-12 rounded-md object-cover">
                    @endif
                    <input type="file" wire:model="icon" accept="image/png,image/jpeg,image/webp"
                        class="text-sm text-ink-muted file:me-3 file:rounded-md file:border-0 file:bg-surface-highest file:px-3 file:py-2 file:text-ink hover:file:bg-surface-high">
                </div>
                <flux:error name="icon" />
            </div>

            <div class="flex justify-end gap-2">
                <flux:modal.close><flux:button variant="ghost">Cancelar</flux:button></flux:modal.close>
                <flux:button variant="primary" type="submit">Guardar</flux:button>
            </div>
        </form>
    </flux:modal>
</div>
