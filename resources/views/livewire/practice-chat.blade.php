{{-- Hilo de consultas de una práctica (D63): burbujas a la derecha las propias, a la izquierda las del otro lado. --}}
<div wire:poll.20s.visible class="flex flex-col gap-3" data-test="practice-chat"
    x-data x-init="$nextTick(() => $refs.list && ($refs.list.scrollTop = $refs.list.scrollHeight))"
    x-on:practice-chat-sent.window="$nextTick(() => $refs.list && ($refs.list.scrollTop = $refs.list.scrollHeight))">
    @if ($messages->isEmpty())
        <p class="rounded-lg border border-dashed border-outline p-3 text-sm text-ink-muted">
            @if ($viewer->isAdmin())
                Todavía no hay mensajes con {{ $student->name }} sobre esta práctica.
            @else
                ¿Te trabaste o tenés una duda? Escribile al profe acá, sin necesidad de entregar. La conversación queda guardada en esta práctica.
            @endif
        </p>
    @else
        <ol x-ref="list" class="flex max-h-96 flex-col gap-2 overflow-y-auto pe-1">
            @foreach ($messages as $message)
                @php($mine = $message->author_id === $viewer->id)
                <li wire:key="message-{{ $message->id }}" @class(['flex flex-col max-w-[85%] gap-0.5', 'self-end items-end' => $mine, 'self-start items-start' => ! $mine])>
                    <span class="px-1 text-[11px] text-ink-muted">
                        {{ $mine ? 'Vos' : ($message->author->isAdmin() ? 'El profe' : $message->author->name) }} · {{ $message->created_at->format('d/m H:i') }}
                    </span>
                    <p @class([
                        'whitespace-pre-line break-words rounded-lg border px-3 py-2 text-sm',
                        'border-primary-bright/50 bg-primary/10 text-ink' => $mine,
                        'border-outline bg-surface-high text-ink' => ! $mine,
                    ])>{{ $message->body }}</p>
                </li>
            @endforeach
        </ol>
    @endif

    @if ($canSend)
        <form wire:submit="send" class="flex items-end gap-2">
            <x-emoji-field class="flex-1">
                <flux:textarea class="pe-10" wire:model="body" rows="2" :placeholder="$viewer->isAdmin() ? 'Respondele…' : 'Escribile al profe…'" aria-label="Mensaje" />
            </x-emoji-field>
            <flux:button type="submit" icon="paper-airplane" aria-label="Enviar mensaje" />
        </form>
        <flux:error name="body" />
    @else
        <p class="flex items-start gap-2 text-xs text-ink-muted"><flux:icon name="lock-closed" variant="micro" class="mt-px shrink-0" /> Con el abono vencido podés leer la conversación, pero para escribir tenés que renovarlo.</p>
    @endif
</div>
