{{-- Hilo de consultas de una práctica (D63) o de una micro-misión (D110): burbujas a la derecha las propias, a la izquierda
     las del otro lado. Adentro de un editor, el mensaje del alumno lleva la foto de su código y de su salida (code y output). --}}
<div wire:poll.20s.visible class="flex flex-col gap-3" data-test="practice-chat"
    x-data x-init="$nextTick(() => $refs.list && ($refs.list.scrollTop = $refs.list.scrollHeight))"
    x-on:practice-chat-sent.window="$nextTick(() => $refs.list && ($refs.list.scrollTop = $refs.list.scrollHeight))">
    @if ($messages->isEmpty())
        <p class="rounded-lg border border-dashed border-outline p-3 text-sm text-ink-muted">
            @if ($viewer->isStaff())
                Todavía no hay mensajes con {{ $student->name }} sobre {{ $isStep ? 'esta micro-misión' : 'esta práctica' }}.
            @elseif ($isStep)
                ¿Te trabaste? Escribile al profe: junto con tu mensaje le llega el código que tenés en el editor y lo que te dio al ejecutarlo.
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
                        {{ $mine ? 'Vos' : ($message->author->isStaff() ? 'El profe' : $message->author->name) }} · {{ $message->created_at->format('d/m H:i') }}
                    </span>
                    <p @class([
                        'whitespace-pre-line break-words rounded-lg border px-3 py-2 text-sm',
                        'border-primary-bright/50 bg-primary/10 text-ink' => $mine,
                        'border-outline bg-surface-high text-ink' => ! $mine,
                    ])>{{ $message->body }}</p>
                    @if ($message->code)
                        <details class="w-full max-w-full rounded-md border border-outline/70 bg-surface-lowest text-xs" data-test="message-code">
                            <summary class="cursor-pointer px-2 py-1 text-ink-muted">Código que tenía en el editor</summary>
                            <pre class="max-h-60 overflow-auto px-2 pb-2 font-mono text-[11px] whitespace-pre text-ink">{{ $message->code }}</pre>
                            @if ($message->output)
                                <p class="px-2 text-[11px] text-ink-muted">Lo que le dio:</p>
                                <pre class="max-h-32 overflow-auto px-2 pb-2 font-mono text-[11px] whitespace-pre-wrap text-success">{{ $message->output }}</pre>
                            @endif
                        </details>
                    @endif
                </li>
            @endforeach
        </ol>
    @endif

    @if ($canSend)
        <form x-on:submit.prevent="$wire.send(typeof code === 'string' ? code : null, typeof output === 'string' ? output : null)" class="flex items-end gap-2">
            <x-emoji-field class="flex-1">
                <flux:textarea class="pe-10" wire:model="body" rows="2" :placeholder="$viewer->isStaff() ? 'Respondele…' : 'Escribile al profe…'" aria-label="Mensaje" />
            </x-emoji-field>
            <flux:button type="submit" icon="paper-airplane" aria-label="Enviar mensaje" />
        </form>
        <flux:error name="body" />
    @else
        <p class="flex items-start gap-2 text-xs text-ink-muted"><flux:icon name="lock-closed" variant="micro" class="mt-px shrink-0" /> Con el abono vencido podés leer la conversación, pero para escribir tenés que renovarlo.</p>
    @endif
</div>
