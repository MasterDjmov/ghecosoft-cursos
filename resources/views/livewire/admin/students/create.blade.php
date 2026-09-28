<div class="mx-auto flex w-full max-w-3xl flex-col gap-6 p-4 sm:p-8">
    <x-admin.page-header label="Alumnos" title="Nuevo alumno" subtitle="Para quien necesita una mano: le creás la cuenta y le pasás los datos por WhatsApp.">
        <x-slot:actions>
            <flux:button variant="ghost" icon="arrow-left" :href="route('admin.students.index')" wire:navigate>Alumnos</flux:button>
        </x-slot:actions>
    </x-admin.page-header>

    @if ($created)
        <section class="panel flex flex-col gap-4 p-5" data-test="student-created">
            <div class="flex items-center gap-3">
                <flux:icon name="check-circle" class="size-6 text-success" />
                <h2 class="font-display text-lg font-semibold text-white">Cuenta creada: {{ $created['name'] }}</h2>
            </div>
            @if ($created['course'])
                <p class="text-sm text-ink-muted">Quedó inscripto en «{{ $created['course'] }}», con sus monedas y el abono.</p>
            @endif
            @if ($created['minor'])
                <flux:callout icon="exclamation-triangle" color="amber">
                    <flux:callout.text>Es menor de 18: para tener CV público y ranking global, falta la autorización firmada del adulto responsable (la sube desde su cuenta).</flux:callout.text>
                </flux:callout>
            @endif

            @include('livewire.admin.students.partials.credentials', ['credentials' => $created])

            <div class="flex flex-wrap justify-end gap-2 border-t border-outline pt-4">
                <flux:button variant="ghost" icon="plus" wire:click="createAnother">Crear otro</flux:button>
                <flux:button variant="primary" icon="user" :href="route('admin.students.show', $created['username'])" wire:navigate>Ver ficha</flux:button>
            </div>
        </section>
    @else
        <form wire:submit="save" class="panel flex flex-col gap-5 p-5">
            <div class="grid gap-5 sm:grid-cols-2">
                <flux:input wire:model="name" wire:blur="suggestUsername" label="Nombre" required />
                <flux:input wire:model="last_name" wire:blur="suggestUsername" label="Apellido" required />
            </div>
            <flux:input wire:model="username" label="Usuario" required description="Con esto entra. Minúsculas, números, - y _." />
            <div class="grid gap-5 sm:grid-cols-2">
                <flux:input wire:model="email" type="email" label="Email (opcional)" description="Sin email, si olvida la clave se la reseteás vos." />
                <flux:input wire:model="phone" type="tel" label="Teléfono (opcional)" placeholder="+54 9 380 412-3456" description="Con código de país, para el botón de WhatsApp." />
            </div>
            <flux:input wire:model="birth_date" type="date" label="Fecha de nacimiento (opcional)" description="Para saber si es menor." />

            <div class="flex items-end gap-2">
                <div class="flex-1">
                    <flux:input wire:model="password" label="Clave provisoria" required class:input="font-mono" description="Al entrar, la tiene que cambiar." />
                </div>
                <flux:button icon="arrow-path" wire:click="newPassword" aria-label="Generar otra" />
            </div>

            <fieldset class="flex flex-col gap-4 rounded-lg border border-outline p-4">
                <legend class="tech-label px-2">Inscribirlo ya (opcional)</legend>
                <div class="grid gap-4 sm:grid-cols-2">
                    <flux:select wire:model.live="courseId" label="Curso">
                        <flux:select.option value="">Sin inscribir</flux:select.option>
                        @foreach ($courses as $course)
                            <flux:select.option :value="(string) $course->id">{{ $course->title }}{{ $course->is_published ? '' : ' (sin publicar)' }}</flux:select.option>
                        @endforeach
                    </flux:select>
                    <flux:select wire:model="cohortId" label="Comisión" :disabled="$cohorts->isEmpty()">
                        <flux:select.option value="">{{ $cohorts->isEmpty() ? 'Sin comisiones' : 'Sin comisión' }}</flux:select.option>
                        @foreach ($cohorts as $cohort)
                            <flux:select.option :value="(string) $cohort->id">{{ $cohort->name }}</flux:select.option>
                        @endforeach
                    </flux:select>
                </div>
                <p class="text-xs text-ink-muted">Es como aprobarle una solicitud: recibe las monedas del curso, arranca el abono y queda en el libro de movimientos.</p>
            </fieldset>

            <div class="flex justify-end">
                <flux:button type="submit" variant="primary" icon="user-plus" data-test="create-student-button">Crear cuenta</flux:button>
            </div>
        </form>
    @endif
</div>
