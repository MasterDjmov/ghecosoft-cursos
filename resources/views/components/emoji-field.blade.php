@props(['emojis' => ['🙂', '😀', '😄', '😅', '😂', '😉', '😊', '😍', '🤔', '😮', '😢', '😭', '😤', '😎', '🥳', '🙏', '👍', '👎', '👏', '💪', '🙌', '👀', '✅', '❌', '⚠️', '❓', '❗', '💡', '🔥', '⭐', '🎉', '🚀', '🐛', '🧠', '📚', '✍️', '⏰', '🤝', '❤️', '💯']])

{{-- Envuelve un cuadro de texto y le suma un botón de emojis: el elegido se inserta donde está el cursor
     (y el evento input avisa a wire:model). Uso: <x-emoji-field><flux:textarea … /></x-emoji-field> --}}
<div {{ $attributes->class('relative') }}
    x-data="{
        open: false,
        pick(emoji) {
            const field = $root.querySelector('textarea, input[type=text]');
            const start = field.selectionStart ?? field.value.length;
            const end = field.selectionEnd ?? start;
            field.setRangeText(emoji, start, end, 'end');
            field.dispatchEvent(new Event('input', { bubbles: true }));
            field.focus();
            this.open = false;
        },
    }"
    x-on:keydown.escape="open = false">
    {{ $slot }}
    <button type="button" class="absolute end-1.5 bottom-1.5 grid size-7 place-items-center rounded-md text-base opacity-70 transition hover:bg-surface-high hover:opacity-100"
        x-on:click="open = ! open" x-bind:aria-expanded="open" aria-label="Agregar un emoji" title="Emojis" data-test="emoji-button">🙂</button>
    <div x-show="open" x-cloak x-transition.opacity x-on:click.outside="open = false"
        class="absolute end-0 bottom-10 z-30 grid w-72 grid-cols-8 gap-0.5 rounded-lg border border-outline bg-surface-container p-2 shadow-lg"
        role="listbox" aria-label="Emojis">
        @foreach ($emojis as $emoji)
            <button type="button" class="grid size-8 place-items-center rounded-md text-lg transition hover:bg-surface-high"
                x-on:click="pick(@js($emoji))" role="option" aria-label="{{ $emoji }}">{{ $emoji }}</button>
        @endforeach
    </div>
</div>
