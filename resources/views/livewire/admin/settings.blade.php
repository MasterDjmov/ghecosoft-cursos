<div class="mx-auto flex w-full max-w-3xl flex-col gap-6 p-4 sm:p-8">
    <x-admin.page-header title="Configuración" />

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
</div>
