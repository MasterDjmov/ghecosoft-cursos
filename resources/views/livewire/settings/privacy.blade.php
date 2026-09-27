<section class="w-full">
    @include('partials.settings-heading')

    <x-settings.layout heading="Privacidad" subheading="Qué ven los demás de vos">
        <form wire:submit="save" class="my-6 flex w-full flex-col gap-6">
            <div class="flex flex-col gap-2">
                <flux:switch wire:model="cv_public" label="Compartir mi CV públicamente" :disabled="(bool) $blocker"
                    description="Tu CV (cursos, {{ term('node', null, 2) }} completados, insignias y nivel) se ve en el link de abajo y aparecés en el ranking global. Nunca muestra tu código ni los comentarios." />
                <flux:error name="cv_public" />
                @if ($blocker)
                    <p class="flex items-start gap-2 text-sm text-warning"><flux:icon name="lock-closed" variant="micro" class="mt-0.5 shrink-0" /> {{ $blocker }}</p>
                @endif
                <p class="text-sm text-ink-muted">
                    Tu link: <a href="{{ $cvUrl }}" target="_blank" class="font-mono text-primary-bright hover:underline">{{ $cvUrl }}</a>
                    (mientras esté apagado, solo lo ves vos).
                </p>
            </div>

            <flux:separator variant="subtle" />

            <flux:radio.group wire:model.live="ranking_display" label="En el ranking de mis cursos aparezco con">
                <flux:radio value="name" :label="auth()->user()->name.' '.mb_substr((string) auth()->user()->last_name, 0, 1).'.'" description="Tu nombre y la inicial del apellido." />
                <flux:radio value="nickname" label="Un apodo" />
            </flux:radio.group>

            @if ($ranking_display === 'nickname')
                <flux:input wire:model="nickname" label="Apodo" placeholder="kira_dev" />
            @endif

            <div>
                <flux:button variant="primary" type="submit">Guardar</flux:button>
            </div>
        </form>

        @if ($isMinor || $authorizations->isNotEmpty())
            <section class="panel flex flex-col gap-4 p-5">
                <div class="flex flex-col gap-1">
                    <h3 class="font-display font-semibold text-white">Autorización de tu adulto responsable</h3>
                    <p class="text-sm text-ink-muted">
                        Como sos menor de 18, para tener CV público y aparecer en el ranking global hace falta una nota firmada por vos,
                        tu adulto responsable (madre, padre o tutor) y el profe. Pedile el modelo al profe, firmala y subí una foto o el PDF.
                    </p>
                </div>

                @foreach ($authorizations as $item)
                    <div class="flex flex-wrap items-center gap-2 text-sm">
                        <flux:badge size="sm" :color="['pending' => 'amber', 'approved' => 'green', 'rejected' => 'red'][$item->status->value]">{{ $item->status->label() }}</flux:badge>
                        <span class="text-ink">{{ $item->original_name }}</span>
                        <span class="text-ink-muted">{{ $item->created_at->format('d/m/Y') }}</span>
                        @if ($item->admin_note) <span class="text-ink-muted">· {{ $item->admin_note }}</span> @endif
                    </div>
                @endforeach

                @unless ($hasApproved)
                    <form wire:submit="uploadAuthorization" class="flex flex-col gap-3">
                        <input type="file" wire:model="authorization" accept="image/jpeg,image/png,application/pdf"
                            class="text-sm text-ink-muted file:me-3 file:rounded-md file:border-0 file:bg-surface-highest file:px-3 file:py-2 file:text-ink hover:file:bg-surface-high">
                        <flux:error name="authorization" />
                        <div>
                            <flux:button type="submit" icon="document-arrow-up" wire:loading.attr="disabled" wire:target="authorization,uploadAuthorization">Subir autorización</flux:button>
                        </div>
                    </form>
                @endunless
            </section>
        @endif
    </x-settings.layout>
</section>
