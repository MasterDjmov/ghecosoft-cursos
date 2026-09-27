@php
    $coinCourse = fn (int $n) => term('coin.course', $course, $n);
    $coinWildcard = fn (int $n) => term('coin.wildcard', null, $n);
    $isRoot = $node->isRoot();
@endphp

<div class="mx-auto flex w-full max-w-5xl flex-col gap-6 p-4 sm:p-8" x-data="{ tab: '{{ $initialTab }}' }">
    <x-admin.page-header :label="'Cursos · '.$course->title.' · '.$node->type->label().($node->code ? ' · '.$node->code : '')" :title="$node->title">
        <x-slot:actions>
            <flux:button variant="ghost" icon="arrow-left" :href="route('admin.courses.tree', $course)" wire:navigate>Árbol</flux:button>
        </x-slot:actions>
    </x-admin.page-header>

    {{-- Resumen de economía del nodo --}}
    <div class="grid gap-3 sm:grid-cols-4">
        <div class="panel flex flex-col gap-1 p-4">
            <span class="tech-label">Cuesta</span>
            <span class="font-display text-xl font-semibold text-white">{{ $node->price }} {{ $paidWith === 'wildcard' ? $coinWildcard($node->price) : $coinCourse($node->price) }}</span>
        </div>
        <div class="panel flex flex-col gap-1 p-4">
            <span class="tech-label">Obligatorias pagan</span>
            <span class="font-display text-xl font-semibold text-white">{{ $requiredReward }} {{ $coinCourse($requiredReward) }}</span>
        </div>
        <div class="panel flex flex-col gap-1 p-4">
            <span class="tech-label">Optativas pagan</span>
            <span class="font-display text-xl font-semibold text-white">{{ $optionalReward }} {{ $coinWildcard($optionalReward) }}</span>
        </div>
        <div class="panel flex flex-col gap-1 p-4">
            <span class="tech-label">XP del nodo</span>
            <span class="font-display text-xl font-semibold text-white">{{ $xpTotal }} {{ term('xp.short') }}</span>
        </div>
    </div>

    {{-- Pestañas --}}
    <nav class="flex gap-1 overflow-x-auto border-b border-outline" role="tablist">
        @foreach (['data' => 'Datos', 'content' => 'Contenido', 'practices' => 'Hojas ('.$practices->count().')', 'resources' => 'Recursos ('.$resources->count().')', 'teacher' => 'Solo docente'] as $key => $label)
            <button type="button" role="tab" x-on:click="tab = '{{ $key }}'"
                class="-mb-px shrink-0 border-b-2 px-4 py-2 text-sm font-medium transition"
                x-bind:class="tab === '{{ $key }}' ? 'border-primary-bright text-primary-bright' : 'border-transparent text-ink-muted hover:text-ink'">
                {{ $label }}
            </button>
        @endforeach
    </nav>

    {{-- Datos y contenido (un solo formulario) --}}
    <form wire:submit="save" x-show="['data', 'content', 'teacher'].includes(tab)" class="flex flex-col gap-6">
        <div x-show="tab === 'data'" class="panel flex flex-col gap-6 p-5 sm:p-6">
            <flux:input wire:model="title" label="Título" required />

            @if ($isRoot)
                <flux:callout icon="information-circle" color="cyan">
                    <flux:callout.text>
                        Es el nodo raíz: no depende de otro, no va en una rama y cuesta lo mismo que el precio del raíz del curso
                        ({{ $course->root_price }} {{ $coinCourse($course->root_price) }}). Eso se cambia en
                        <flux:link :href="route('admin.courses.edit', $course)" wire:navigate>Datos del curso</flux:link>.
                    </flux:callout.text>
                </flux:callout>
            @else
                <flux:radio.group wire:model.live="type" label="Tipo" variant="segmented">
                    @foreach ($nodeTypes as $nodeType)
                        <flux:radio :value="$nodeType->value" :label="$nodeType->label()" />
                    @endforeach
                </flux:radio.group>

                <div class="grid gap-6 sm:grid-cols-2">
                    <flux:select wire:model="parent_id" label="Requisito">
                        @foreach ($parentOptions as $option)
                            <flux:select.option :value="$option->id">{{ $option->isRoot() ? '★ ' : '' }}{{ $option->title }}</flux:select.option>
                        @endforeach
                    </flux:select>
                    <flux:select wire:model="branch_id" label="Rama">
                        <flux:select.option value="">Sin rama</flux:select.option>
                        @foreach ($branches as $branch)
                            <flux:select.option :value="$branch->id">{{ $branch->title }}</flux:select.option>
                        @endforeach
                    </flux:select>
                </div>

                <flux:text class="-mt-3 text-sm">El alumno tiene que aprobar las obligatorias del requisito antes de abrir este nodo.</flux:text>

                <flux:checkbox.group wire:model="requirementIds" label="Requisitos extra (opcional)"
                    description="Nodos que también hay que completar, además del requisito principal. Por ejemplo: una parte de una Senda que necesita un tema avanzado del tronco.">
                    <div class="grid max-h-56 gap-2 overflow-y-auto rounded-lg border border-outline bg-surface-lowest/40 p-3 sm:grid-cols-2">
                        @foreach ($parentOptions as $option)
                            @continue($option->isRoot())
                            <flux:checkbox :value="(string) $option->id" :label="$option->title" />
                        @endforeach
                    </div>
                </flux:checkbox.group>

                <div class="grid gap-6 sm:grid-cols-2">
                    <flux:input wire:model="price" type="number" min="0" label="Precio" />
                    <flux:select wire:model.live="paidWith" label="Se paga con">
                        <flux:select.option value="course">{{ ucfirst($coinCourse(2)) }}</flux:select.option>
                        <flux:select.option value="wildcard">{{ ucfirst($coinWildcard(2)) }}</flux:select.option>
                    </flux:select>
                </div>
                <div class="grid gap-6 sm:grid-cols-2">
                    @if ($type === 'boss')
                        <flux:select wire:model="badge_id" label="Insignia al vencerlo" description:trailing="Se crean en Insignias.">
                            <flux:select.option value="">Sin insignia</flux:select.option>
                            @foreach ($badges as $badge)
                                <flux:select.option :value="$badge->id">{{ $badge->name }}</flux:select.option>
                            @endforeach
                        </flux:select>
                    @endif
                </div>
            @endif

            <flux:input wire:model="video_url" type="url" label="Video (opcional)" placeholder="https://www.youtube.com/watch?v=…" />
            <flux:switch wire:model="is_published" label="Publicado" description="Sin publicar, el alumno lo ve bloqueado y no lo puede abrir." />
        </div>

        {{-- Contenido por secciones (D37): cada una con su personaje. Todo admite markdown. --}}
        <div x-show="tab === 'content'" x-cloak class="flex flex-col gap-6">
            <flux:callout icon="information-circle" color="cyan">
                <flux:callout.text>
                    El alumno ve las secciones en este orden y solo las que tengan texto. Todas admiten markdown.
                    Los nombres de la compañía se cambian en <flux:link :href="route('admin.glossary')" wire:navigate>Diccionario</flux:link>.
                </flux:callout.text>
            </flux:callout>

            <div class="panel flex flex-col gap-5 p-5 sm:p-6">
                <flux:heading>Historia</flux:heading>
                <flux:textarea wire:model="chronicle" label="Crónica" rows="3"
                    description:trailing="2 a 4 líneas, en segunda persona: qué te pasa y por qué necesitás este tema." />
            </div>

            <div class="panel flex flex-col gap-5 p-5 sm:p-6">
                <flux:heading>Antes de la explicación</flux:heading>
                <flux:textarea wire:model="objectives" label="Objetivos" rows="3" placeholder="- Guardar un valor en una variable&#10;- Cambiarlo y mostrarlo"
                    description:trailing="Una lista: «Al terminar, vas a poder…»." />
                <flux:textarea wire:model="before_you_start" label="Antes de empezar" rows="2"
                    description:trailing="Qué tenés que saber ya (podés nombrar los nodos anteriores)." />
            </div>

            <div class="panel flex flex-col gap-2 p-5 sm:p-6" x-data="{ preview: false }">
                <div class="flex items-center justify-between">
                    <flux:heading>Explicación · {{ term('companion.theory', $course) }}</flux:heading>
                    <flux:button size="xs" variant="ghost" x-on:click="preview = ! preview" x-text="preview ? 'Editar' : 'Vista previa'" />
                </div>
                <div x-show="! preview">
                    <flux:textarea wire:model.blur="content" rows="14" class="font-mono text-sm" placeholder="## Variables&#10;&#10;Una variable es…" aria-label="Explicación" />
                </div>
                <div x-show="preview" x-cloak class="markdown min-h-40 rounded-lg border border-outline bg-surface-lowest/60 p-4">{!! $contentPreview !!}</div>
                <flux:description>Markdown: <code>## Título</code>, <code>**negrita**</code>, listas y bloques de código con <code>```python</code>.</flux:description>
            </div>

            <div class="panel flex flex-col gap-5 p-5 sm:p-6">
                <flux:heading>Código de ejemplo</flux:heading>
                <flux:textarea wire:model="example_code" rows="8" class="font-mono text-sm" aria-label="Código de ejemplo"
                    description:trailing="El alumno lo puede ejecutar en el navegador (si el lenguaje del curso tiene ejecutor)." />
                <div class="grid gap-6 sm:grid-cols-2">
                    <flux:textarea wire:model="sample_input" label="Entrada de ejemplo (opcional)" rows="3" class="font-mono text-sm"
                        description:trailing="Una línea por cada lectura de teclado." />
                    <flux:textarea wire:model="expected_output" label="Salida esperada (opcional)" rows="3" class="font-mono text-sm" />
                </div>
            </div>

            <div class="panel flex flex-col gap-5 p-5 sm:p-6">
                <flux:heading>¿Para qué sirve? · {{ term('companion.uses', $course) }}</flux:heading>
                <flux:textarea wire:model="use_cases" rows="3" aria-label="¿Para qué sirve?" description:trailing="Uno o dos usos reales, fuera del juego." />
            </div>

            <div class="panel flex flex-col gap-5 p-5 sm:p-6">
                <flux:heading>Errores habituales · {{ term('companion.errors', $course) }}</flux:heading>
                <flux:select wire:model="beast_key" label="Criatura del bestiario" description:trailing="Se muestra con su nombre, ícono y descripción del Diccionario.">
                    <flux:select.option value="">Sin criatura</flux:select.option>
                    @foreach ($beasts as $key => $name)
                        <flux:select.option :value="$key">{{ $name }}</flux:select.option>
                    @endforeach
                </flux:select>
                <flux:textarea wire:model="common_errors" rows="6" class="font-mono text-sm" aria-label="Errores habituales"
                    description:trailing="El error típico, cómo se ve el traceback y cómo leerlo." />
            </div>

            <div class="panel flex flex-col gap-4 p-5 sm:p-6">
                <div class="flex flex-wrap items-center justify-between gap-2">
                    <div>
                        <flux:heading>Prueba del sello</flux:heading>
                        <flux:text class="text-sm">Autoevaluación sin nota: el alumno lee la pregunta y despliega la respuesta.</flux:text>
                    </div>
                    <flux:button size="sm" icon="plus" wire:click="addSelfCheck">Pregunta</flux:button>
                </div>
                @forelse ($selfCheck as $index => $item)
                    <div class="flex flex-col gap-3 rounded-lg border border-outline bg-surface-lowest/40 p-4 sm:flex-row" wire:key="self-check-{{ $index }}">
                        <div class="flex flex-1 flex-col gap-3">
                            <flux:input wire:model="selfCheck.{{ $index }}.question" :label="'Pregunta '.($index + 1)" />
                            <flux:textarea wire:model="selfCheck.{{ $index }}.answer" label="Respuesta" rows="2" />
                        </div>
                        <flux:button size="xs" variant="ghost" icon="trash" wire:click="removeSelfCheck({{ $index }})" aria-label="Quitar pregunta" class="self-start" />
                    </div>
                @empty
                    <p class="text-sm text-ink-muted">Sin preguntas todavía.</p>
                @endforelse
            </div>
        </div>

        {{-- Solo docente --}}
        <div x-show="tab === 'teacher'" x-cloak class="panel flex flex-col gap-5 p-5 sm:p-6">
            <flux:callout icon="lock-closed" color="amber">
                <flux:callout.text>El alumno <strong>nunca</strong> ve esta pestaña: la plataforma no le manda estos textos.</flux:callout.text>
            </flux:callout>
            <flux:textarea wire:model="teacher_solutions" label="Soluciones y notas del nodo" rows="14" class="font-mono text-sm"
                description:trailing="Soluciones de referencia, tiempo estimado y dificultades frecuentes. La solución de cada hoja va en la hoja." />
        </div>

        <div class="flex justify-end">
            <flux:button variant="primary" type="submit" icon="check">Guardar nodo</flux:button>
        </div>
    </form>

    {{-- Hojas --}}
    <section x-show="tab === 'practices'" x-cloak class="flex flex-col gap-4">
        <div class="flex flex-wrap items-center justify-between gap-3">
            <flux:text>Las obligatorias pagan {{ $coinCourse(2) }} y habilitan el nodo siguiente; las optativas pagan {{ $coinWildcard(2) }}.</flux:text>
            <flux:button variant="primary" icon="plus" wire:click="newPractice">Nueva hoja</flux:button>
        </div>

        <ol class="flex flex-col gap-2" wire:sort="sortPractice">
            @forelse ($practices as $practice)
                <li class="panel flex flex-col gap-3 p-4 sm:flex-row sm:items-center" wire:key="practice-{{ $practice->id }}" wire:sort:item="{{ $practice->id }}">
                    <div class="flex min-w-0 flex-1 items-start gap-3">
                        <flux:icon name="bars-3" class="mt-0.5 size-4 shrink-0 cursor-grab text-ink-muted" wire:sort:handle />
                        <div class="flex min-w-0 flex-col gap-1">
                            <div class="flex flex-wrap items-center gap-2">
                                <span class="font-medium text-white">{{ $practice->title }}</span>
                                @if ($practice->is_required)
                                    <flux:badge size="sm" color="cyan">Obligatoria</flux:badge>
                                @else
                                    <flux:badge size="sm" color="violet">Optativa</flux:badge>
                                @endif
                                <flux:badge size="sm">{{ $practice->submission_mode->label() }}</flux:badge>
                            </div>
                            <p class="font-mono text-[11px] text-ink-muted">
                                +{{ $practice->coin_reward }} {{ $practice->is_required ? $coinCourse($practice->coin_reward) : $coinWildcard($practice->coin_reward) }}
                                · +{{ $practice->xp_reward }} {{ term('xp.short') }}
                                @if ($practice->allowed_extensions) · archivos: {{ $practice->allowed_extensions }} @endif
                            </p>
                            @if ($practice->instructions)
                                <p class="line-clamp-2 text-sm text-ink-muted">{{ $practice->instructions }}</p>
                            @endif
                        </div>
                    </div>
                    <div class="flex shrink-0 gap-1">
                        <flux:button size="xs" icon="pencil-square" wire:click="editPractice({{ $practice->id }})">Editar</flux:button>
                        <flux:button size="xs" variant="ghost" icon="trash" wire:click="deletePractice({{ $practice->id }})"
                            wire:confirm="¿Borrar la hoja «{{ $practice->title }}»?" aria-label="Borrar" />
                    </div>
                </li>
            @empty
                <li class="panel p-6 text-center text-ink-muted" wire:sort:ignore>Este nodo todavía no tiene hojas.</li>
            @endforelse
        </ol>
    </section>

    {{-- Recursos --}}
    <section x-show="tab === 'resources'" x-cloak class="flex flex-col gap-4">
        <form wire:submit="addResource" class="panel flex flex-col gap-4 p-5">
            <flux:heading>Agregar recurso</flux:heading>
            <flux:radio.group wire:model.live="resourceType" variant="segmented">
                <flux:radio value="link" label="Link" />
                <flux:radio value="file" label="Archivo" />
            </flux:radio.group>
            <div class="grid gap-4 sm:grid-cols-2">
                <flux:input wire:model="resourceTitle" label="Título" placeholder="Apunte de variables" />
                @if ($resourceType === 'file')
                    <div class="flex flex-col gap-2">
                        <flux:label>Archivo</flux:label>
                        <input type="file" wire:model="resourceFile"
                            class="text-sm text-ink-muted file:me-3 file:rounded-md file:border-0 file:bg-surface-highest file:px-3 file:py-2 file:text-ink hover:file:bg-surface-high">
                        <flux:error name="resourceFile" />
                    </div>
                @else
                    <flux:input wire:model="resourceUrl" type="url" label="Link" placeholder="https://…" />
                @endif
            </div>
            <div class="flex items-center justify-between gap-3">
                <flux:description>Los archivos quedan privados: solo los descargan quienes abrieron el nodo. Hasta 20 MB.</flux:description>
                <flux:button type="submit" icon="plus" wire:loading.attr="disabled" wire:target="resourceFile,addResource">Agregar</flux:button>
            </div>
        </form>

        <ol class="flex flex-col gap-2" wire:sort="sortResource">
            @forelse ($resources as $resource)
                <li class="panel flex items-center gap-3 p-3" wire:key="resource-{{ $resource->id }}" wire:sort:item="{{ $resource->id }}">
                    <flux:icon name="bars-3" class="size-4 shrink-0 cursor-grab text-ink-muted" wire:sort:handle />
                    <flux:icon :name="$resource->type === \App\Enums\ResourceType::File ? 'paper-clip' : 'link'" class="size-4 shrink-0 text-primary-bright" />
                    <div class="flex min-w-0 flex-1 flex-col">
                        @if ($resource->type === \App\Enums\ResourceType::File)
                            <a href="{{ route('files.resource', $resource) }}" class="truncate font-medium text-white hover:text-primary-bright">{{ $resource->title }}</a>
                            <span class="truncate font-mono text-[11px] text-ink-muted">{{ $resource->original_name }}</span>
                        @else
                            <a href="{{ $resource->url }}" target="_blank" rel="noopener noreferrer" class="truncate font-medium text-white hover:text-primary-bright">{{ $resource->title }}</a>
                            <span class="truncate font-mono text-[11px] text-ink-muted">{{ $resource->url }}</span>
                        @endif
                    </div>
                    <flux:button size="xs" variant="ghost" icon="trash" wire:click="deleteResource({{ $resource->id }})"
                        wire:confirm="¿Borrar el recurso «{{ $resource->title }}»?" aria-label="Borrar" />
                </li>
            @empty
                <li class="panel p-6 text-center text-ink-muted" wire:sort:ignore>Sin recursos todavía.</li>
            @endforelse
        </ol>
    </section>

    {{-- Modal: hoja --}}
    <flux:modal name="practice" class="w-full max-w-2xl">
        <form wire:submit="savePractice" class="flex flex-col gap-5">
            <flux:heading size="lg">{{ $practiceId ? 'Editar hoja' : 'Nueva hoja' }}</flux:heading>

            <flux:input wire:model="practiceTitle" label="Título" placeholder="Misión 1" />
            <flux:textarea wire:model="practiceInstructions" label="Consigna" rows="5" description:trailing="Admite markdown." />
            <flux:textarea wire:model="practiceCriteria" label="Criterio de aprobación" rows="3" placeholder="- Pide el nombre con input()&#10;- Muestra el saludo en una línea"
                description:trailing="Lo ve el alumno («Para aprobar») y lo tenés a mano al corregir." />

            <div class="grid gap-5 sm:grid-cols-2">
                <flux:switch wire:model.live="practiceRequired" label="Obligatoria"
                    description="Apagado = optativa (paga {{ $coinWildcard(2) }})." />
                <flux:select wire:model.live="practiceMode" label="Entrega">
                    @foreach ($modes as $mode)
                        <flux:select.option :value="$mode->value">{{ $mode->label() }}</flux:select.option>
                    @endforeach
                </flux:select>
            </div>

            <flux:radio.group wire:model.live="practiceEnvironment" label="Dónde se resuelve" variant="segmented">
                @foreach ($environments as $environment)
                    <flux:radio :value="$environment->value" :label="$environment->label()" />
                @endforeach
            </flux:radio.group>
            @if ($practiceEnvironment === 'local' && $practiceMode === 'code')
                <flux:text class="-mt-3 text-sm text-warning">Las prácticas locales suelen entregarse como archivo: revisá el tipo de entrega.</flux:text>
            @endif

            @if (in_array($practiceMode, ['file', 'both'], true))
                <flux:input wire:model="practiceExtensions" label="Extensiones permitidas" placeholder="py, txt, zip" />
            @endif
            @if ($practiceMode === 'none')
                <flux:callout icon="information-circle" color="cyan">
                    <flux:callout.text>Sin entrega: el alumno la marca como completada. Si ponés recompensa, se paga cuando la marca.</flux:callout.text>
                </flux:callout>
            @endif

            <div class="grid gap-5 sm:grid-cols-2">
                <flux:input wire:model="practiceCoins" type="number" min="0"
                    :label="'Recompensa en '.($practiceRequired ? $coinCourse(2) : $coinWildcard(2))" />
                <flux:input wire:model="practiceXp" type="number" min="0" :label="term('xp.short')" />
            </div>

            @if ($practiceMode !== 'none')
                <flux:textarea wire:model="practiceStarterCode" label="Código inicial (opcional)" rows="4" class="font-mono text-sm" />
                <div class="grid gap-5 sm:grid-cols-2">
                    <flux:textarea wire:model="practiceSampleInput" label="Entrada de prueba (opcional)" rows="2" class="font-mono text-sm" />
                    <flux:textarea wire:model="practiceExpectedOutput" label="Salida esperada (opcional)" rows="2" class="font-mono text-sm" />
                </div>
            @endif

            <flux:textarea wire:model="practiceSolution" label="Solución de referencia (solo docente)" rows="5" class="font-mono text-sm"
                description:trailing="El alumno nunca la ve. La tenés a mano al corregir." />

            <div class="flex justify-end gap-2">
                <flux:modal.close><flux:button variant="ghost">Cancelar</flux:button></flux:modal.close>
                <flux:button variant="primary" type="submit">Guardar hoja</flux:button>
            </div>
        </form>
    </flux:modal>
</div>
