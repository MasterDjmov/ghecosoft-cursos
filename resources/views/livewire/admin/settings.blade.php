<div class="mx-auto flex w-full max-w-3xl flex-col gap-6 p-4 sm:p-8">
    <x-admin.page-header title="Configuración" />

    {{-- Mantenimiento (D86): la plataforma entera (solo entra el administrador) o algunos cursos. --}}
    <form wire:submit="saveMaintenance" @class(['panel flex flex-col gap-5 p-5 sm:p-6', 'border-warning/60' => $maintenance_platform || $maintenance_courses]) data-test="maintenance-settings">
        <div class="flex flex-col gap-1">
            <h2 class="flex items-center gap-2 font-display font-semibold text-white">
                <flux:icon name="wrench-screwdriver" variant="mini" class="text-warning" /> Mantenimiento
            </h2>
            <p class="text-sm text-ink-muted">Para subir cambios tranquilo. Con la plataforma en mantenimiento <strong class="text-ink">solo entrás vos</strong>: a los demás (alumnos y docentes) se les cierra la sesión y el login les muestra el aviso; nadie puede crear una cuenta. Con un curso en mantenimiento, sus alumnos no entran a ese curso (vos y los docentes sí, para revisarlo). Los días de abono siguen corriendo.</p>
        </div>
        <flux:switch wire:model.live="maintenance_platform" label="Plataforma en mantenimiento" description="Solo el administrador puede entrar." />
        <flux:textarea wire:model="maintenance_message" label="Mensaje" rows="2" :placeholder="$defaultMaintenanceMessage"
            description:trailing="Lo ven en el login. Vacío, se usa el de ejemplo." />
        <flux:checkbox.group wire:model.live="maintenance_courses" label="Cursos en mantenimiento">
            @foreach ($courses as $course)
                <flux:checkbox :value="(string) $course->id" :label="$course->title.($course->is_published ? '' : ' (sin publicar)')" />
            @endforeach
        </flux:checkbox.group>
        <div class="flex justify-end">
            <flux:button variant="primary" type="submit">Guardar</flux:button>
        </div>
    </form>

    <form wire:submit="save" class="panel flex flex-col gap-6 p-5 sm:p-6">
        <flux:input wire:model="whatsapp_number" label="Tu WhatsApp" placeholder="+54 9 380 412-3456"
            description:trailing="Lo usa el botón «Contactar al profe». Si está vacío, el botón no aparece." />
        <flux:textarea wire:model="whatsapp_message" label="Mensaje prearmado" rows="3"
            description:trailing="Podés usar {nombre}, {usuario} y {curso}." />
        <flux:input wire:model="welcome_text" label="Frase de bienvenida" />
        <div class="flex justify-end">
            <flux:button variant="primary" type="submit">Guardar</flux:button>
        </div>
    </form>

    {{-- Correo: el Gmail del docente tiene un límite diario que comparte con su otra página. --}}
    <form wire:submit="saveMail" class="panel flex flex-col gap-5 p-5 sm:p-6" data-test="mail-settings">
        <div class="flex flex-col gap-1">
            <h2 class="font-display font-semibold text-white">Correo</h2>
            <p class="text-sm text-ink-muted">Avisos por mail, recuperar la clave y verificar el correo. Apagado o con el tope del día alcanzado, no sale ningún mail: los avisos quedan igual en la campanita.</p>
        </div>
        @unless ($mailConfigured)
            <flux:callout icon="information-circle" color="zinc">
                <flux:callout.text>En este servidor no hay un correo SMTP configurado (`.env`): por ahora no sale ningún mail.</flux:callout.text>
            </flux:callout>
        @endunless
        <flux:switch wire:model.live="mail_enabled" label="Enviar mails" description="Apagalo si Gmail está por llegar a su límite o mientras hacés pruebas." />
        <div class="flex flex-col gap-4 sm:flex-row sm:items-end">
            <flux:input type="number" min="0" max="2000" wire:model="mail_daily_limit" label="Tope por día" class="sm:w-48"
                description:trailing="Gmail permite unos 500 por día para toda la cuenta (también tu otra página): dejá margen." />
            <div class="flex flex-col gap-1 sm:ms-auto sm:items-end" data-test="mail-counter">
                <span class="tech-label">Hoy</span>
                <span class="font-display text-2xl font-semibold {{ $mailSentToday >= $mail_daily_limit ? 'text-danger' : 'text-white' }}">{{ $mailSentToday }} <span class="text-base text-ink-muted">de {{ $mail_daily_limit }}</span></span>
            </div>
        </div>
        <div class="flex justify-end">
            <flux:button variant="primary" type="submit">Guardar</flux:button>
        </div>
    </form>
</div>
