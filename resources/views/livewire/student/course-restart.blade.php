<div class="flex justify-end" data-test="course-restart">
    <flux:modal.trigger name="course-restart">
        <flux:button size="sm" variant="ghost" icon="arrow-path">Reiniciar este curso</flux:button>
    </flux:modal.trigger>

    <flux:modal name="course-restart" class="w-full max-w-md">
        <form wire:submit="restart" class="flex flex-col gap-4">
            <flux:heading size="lg">¿Reiniciar {{ $course->title }}?</flux:heading>
            <div class="flex flex-col gap-3 text-sm text-ink-muted">
                <div>
                    <p class="font-medium text-ink">Se borra, y no se puede deshacer:</p>
                    <ul class="mt-1 list-disc ps-5">
                        <li>los nodos abiertos, las micro-misiones y tus entregas de este curso;</li>
                        <li>sus monedas, la XP que ganaste acá y sus insignias;</li>
                        <li>tu héroe de este curso (te devuelve el oro de sus atributos).</li>
                    </ul>
                </div>
                <div>
                    <p class="font-medium text-ink">Queda igual:</p>
                    <ul class="mt-1 list-disc ps-5">
                        <li>los otros cursos y tu abono;</li>
                        <li>tus consultas al profe;</li>
                        <li>tu oro y tu mochila. Lo que ya ganaste acá no se vuelve a pagar.</li>
                    </ul>
                </div>
            </div>
            <flux:input wire:model="confirmation" :label="'Escribí '.$word.' para confirmar'" autocomplete="off" data-test="course-restart-word" />
            <div class="flex justify-end gap-2">
                <flux:modal.close><flux:button variant="ghost">Cancelar</flux:button></flux:modal.close>
                <flux:button type="submit" variant="danger" data-test="course-restart-confirm">Reiniciar</flux:button>
            </div>
        </form>
    </flux:modal>
</div>
