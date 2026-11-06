@php
    $key = 'rounded-md border border-outline bg-surface-low py-2 font-mono text-sm text-ink transition hover:bg-surface-high active:bg-surface-high disabled:cursor-not-allowed disabled:opacity-25 disabled:hover:bg-surface-low';
    $op = 'rounded-md border border-outline bg-surface-high py-2 font-mono text-sm text-primary-bright transition hover:border-primary-bright active:bg-surface-high';
    $tab = 'rounded px-3 py-1 text-xs font-semibold transition';
@endphp
<div @class(['mx-auto flex w-full max-w-md flex-col gap-3', 'p-4 sm:p-8' => ! $inWindow, 'p-3' => $inWindow])>
    <x-tool-header title="Calculadora" :in-window="$inWindow" :data-tool-limit="3" data-tool-size="400x740">
        Simple o para programar, con hexadecimal, binario y bits. Se usa también con el teclado: Enter calcula y Esc borra.
    </x-tool-header>

    <div wire:ignore x-data="calculatorTool({{ auth()->id() }})" data-test="calculator-tool" class="flex flex-col gap-3">
        <div class="flex items-center justify-between gap-2">
            <div class="inline-flex rounded-md border border-outline p-0.5" role="group" aria-label="Tipo de calculadora">
                <button type="button" class="{{ $tab }}" :class="mode === 'simple' ? 'bg-primary text-white' : 'text-ink-muted hover:text-ink'" :aria-pressed="mode === 'simple'" @click="setMode('simple')" data-test="calc-simple">Simple</button>
                <button type="button" class="{{ $tab }}" :class="mode === 'programmer' ? 'bg-primary text-white' : 'text-ink-muted hover:text-ink'" :aria-pressed="mode === 'programmer'" @click="setMode('programmer')" data-test="calc-programmer">Programador</button>
            </div>
            <div x-show="mode === 'programmer'" class="inline-flex rounded-md border border-outline p-0.5" role="group" aria-label="Cantidad de bits">
                <template x-for="bits in widths" :key="bits">
                    <button type="button" class="rounded px-2 py-1 font-mono text-xs transition" :class="width === bits ? 'bg-surface-high text-white' : 'text-ink-muted hover:text-ink'" :aria-pressed="width === bits" :title="bits + ' bits'" @click="width = bits" x-text="bits" :data-test="'calc-width-' + bits"></button>
                </template>
            </div>
        </div>

        {{-- Lo hecho: un clic en un resultado lo vuelve a traer, para seguir con sumas parciales. --}}
        <div x-show="history.length" class="flex max-h-28 flex-col gap-0.5 overflow-y-auto rounded-md border border-outline bg-surface-lowest p-2 font-mono text-xs" data-test="calc-history">
            <template x-for="(row, i) in history" :key="i + row.expr">
                <button type="button" class="flex items-baseline justify-end gap-2 rounded px-1 py-0.5 text-end hover:bg-surface-high" title="Usar este resultado" @click="reuse(row)">
                    <span class="min-w-0 truncate text-ink-muted" x-text="row.expr"></span>
                    <span class="shrink-0 text-ink" x-text="'= ' + row.result"></span>
                </button>
            </template>
            <button type="button" class="mt-1 self-start text-[11px] text-ink-muted underline hover:text-ink" @click="clearHistory()">Borrar lo hecho</button>
        </div>

        <div class="relative">
            <input x-ref="input" x-model="input" @keydown="onKey($event)" @input="fresh = false" type="text" autocomplete="off" autocapitalize="off" spellcheck="false" :inputmode="window.matchMedia('(pointer: fine)').matches ? 'text' : 'none'"
                aria-label="Cuenta" data-test="calc-input" placeholder="0"
                class="w-full rounded-md border border-outline bg-surface-lowest py-3 ps-3 pe-11 text-end font-mono text-2xl text-white placeholder:text-ink-muted focus:border-primary-bright focus:outline-none">
            <button type="button" @click="copyInput()" title="Copiar" aria-label="Copiar lo que hay en la pantalla" class="absolute end-2 top-1/2 grid size-7 -translate-y-1/2 place-items-center rounded text-ink-muted hover:bg-surface-high hover:text-ink">
                <flux:icon name="clipboard" variant="micro" />
            </button>
        </div>
        <p x-show="error" x-text="error" role="alert" class="-mt-1 text-xs text-red-400" data-test="calc-error"></p>
        <p x-show="copied" class="-mt-1 truncate text-xs text-primary-bright" aria-live="polite">Copiado: <span class="font-mono" x-text="copied"></span></p>

        {{-- Programador: el valor en las cuatro bases y los bits. --}}
        <template x-if="mode === 'programmer'">
            <div class="flex flex-col gap-3">
                <div class="flex flex-col rounded-md border border-outline bg-surface-lowest p-1 font-mono text-xs">
                    <template x-for="row in rows()" :key="row.base">
                        <div class="flex items-center gap-1 rounded" :class="base === row.base ? 'bg-primary/20' : ''">
                            <button type="button" class="flex min-w-0 flex-1 items-baseline gap-2 rounded px-2 py-1 text-start hover:bg-surface-high" :aria-pressed="base === row.base" :title="'Escribir en ' + row.name" @click="setBase(row.base)" :data-test="'calc-base-' + row.base">
                                <span class="w-8 shrink-0 font-semibold" :class="base === row.base ? 'text-primary-bright' : 'text-ink-muted'" x-text="row.name"></span>
                                <span class="min-w-0 break-words text-ink" x-text="row.text" :data-test="'calc-value-' + row.base"></span>
                            </button>
                            <button type="button" class="grid size-6 shrink-0 place-items-center rounded text-ink-muted hover:bg-surface-high hover:text-ink" :aria-label="'Copiar ' + row.name" title="Copiar" @click="copy(row.copy)"><flux:icon name="clipboard" variant="micro" /></button>
                        </div>
                    </template>
                    <p class="flex flex-wrap gap-x-4 px-2 pt-1 pb-0.5 text-ink-muted">
                        <span x-show="isNegative">Con signo: <span class="text-ink" x-text="signedText" data-test="calc-signed"></span></span>
                        <span x-show="charText">Carácter: <span class="text-ink" x-text="charText" data-test="calc-char"></span></span>
                    </p>
                </div>
                <p x-show="live.overflow && !live.error" class="-mt-1 text-xs text-amber-400" data-test="calc-overflow">No entra en <span x-text="width"></span> bits: se recortó, como en un registro.</p>

                <div class="flex flex-col gap-1 rounded-md border border-outline bg-surface-lowest p-2" aria-label="Bits: tocá uno para cambiarlo">
                    <template x-for="row in bitRows()" :key="row.top">
                        <div class="flex items-center gap-1">
                            <span class="w-5 shrink-0 text-end font-mono text-[10px] text-ink-muted" x-text="row.top"></span>
                            <div class="flex min-w-0 flex-1 justify-center gap-1.5">
                                <template x-for="(nibble, n) in row.nibbles" :key="n">
                                    <div class="flex">
                                        <template x-for="bit in nibble" :key="bit.index">
                                            <button type="button" class="w-[1.05rem] rounded py-0.5 font-mono text-xs transition hover:bg-surface-high" :class="bit.on ? 'font-bold text-primary-bright' : 'text-ink-muted'" :aria-label="'Bit ' + bit.index" :aria-pressed="bit.on" :title="'Bit ' + bit.index" @click="flip(bit.index)" x-text="bit.on ? '1' : '0'" :data-test="'calc-bit-' + bit.index"></button>
                                        </template>
                                    </div>
                                </template>
                            </div>
                            <span class="w-5 shrink-0 font-mono text-[10px] text-ink-muted" x-text="row.low"></span>
                        </div>
                    </template>
                </div>
            </div>
        </template>

        {{-- Simple --}}
        <div x-show="mode === 'simple'" class="grid grid-cols-5 gap-1.5" data-test="calc-keys-simple">
            <button type="button" class="{{ $op }} text-red-400" @click="clear()">C</button>
            <button type="button" class="{{ $op }}" @click="backspace()" aria-label="Borrar lo último">⌫</button>
            <button type="button" class="{{ $op }}" @click="press('(', true)">(</button>
            <button type="button" class="{{ $op }}" @click="press(')')">)</button>
            <button type="button" class="{{ $op }}" @click="press(' mod ')">mod</button>
            @foreach ([7, 8, 9] as $digit)<button type="button" class="{{ $key }}" @click="press('{{ $digit }}', true)">{{ $digit }}</button>@endforeach
            <button type="button" class="{{ $op }}" @click="press('÷')">÷</button>
            <button type="button" class="{{ $op }}" @click="press('√', true)">√</button>
            @foreach ([4, 5, 6] as $digit)<button type="button" class="{{ $key }}" @click="press('{{ $digit }}', true)">{{ $digit }}</button>@endforeach
            <button type="button" class="{{ $op }}" @click="press('×')">×</button>
            <button type="button" class="{{ $op }}" @click="square()">x²</button>
            @foreach ([1, 2, 3] as $digit)<button type="button" class="{{ $key }}" @click="press('{{ $digit }}', true)">{{ $digit }}</button>@endforeach
            <button type="button" class="{{ $op }}" @click="press('−')">−</button>
            <button type="button" class="{{ $op }}" @click="press('%')">%</button>
            <button type="button" class="{{ $key }}" @click="press('0', true)">0</button>
            <button type="button" class="{{ $key }}" @click="press(',', true)">,</button>
            <button type="button" class="{{ $op }}" @click="press('π', true)">π</button>
            <button type="button" class="{{ $op }}" @click="press('+')">+</button>
            <button type="button" class="rounded-md bg-primary py-2.5 font-mono text-sm font-bold text-white transition hover:bg-primary-bright" @click="equals()" data-test="calc-equals">=</button>
        </div>

        {{-- Programador: AND, OR y los demás escriben su símbolo, el mismo de C, Java, Python y JavaScript. --}}
        <div x-show="mode === 'programmer'" class="grid grid-cols-6 gap-1.5" data-test="calc-keys-programmer">
            <button type="button" class="{{ $op }}" title="Y bit a bit: &" @click="press('&')">AND</button>
            <button type="button" class="{{ $op }}" title="O bit a bit: |" @click="press('|')">OR</button>
            <button type="button" class="{{ $op }}" title="O exclusivo: ^" @click="press('^')">XOR</button>
            <button type="button" class="{{ $op }}" title="Invertir todos los bits: ~" @click="press('~', true)">NOT</button>
            <button type="button" class="{{ $op }}" title="Correr a la izquierda" @click="press('<<')">&lt;&lt;</button>
            <button type="button" class="{{ $op }}" title="Correr a la derecha" @click="press('>>')">&gt;&gt;</button>

            @foreach (['A', 'B', 'C'] as $digit)<button type="button" class="{{ $key }}" :disabled="!digitEnabled('{{ $digit }}')" @click="press('{{ $digit }}', true)">{{ $digit }}</button>@endforeach
            <button type="button" class="{{ $op }}" @click="press('(', true)">(</button>
            <button type="button" class="{{ $op }}" @click="press(')')">)</button>
            <button type="button" class="{{ $op }}" @click="backspace()" aria-label="Borrar lo último">⌫</button>

            @foreach (['D', 'E', 'F'] as $digit)<button type="button" class="{{ $key }}" :disabled="!digitEnabled('{{ $digit }}')" @click="press('{{ $digit }}', true)">{{ $digit }}</button>@endforeach
            <button type="button" class="{{ $op }}" @click="press(' mod ')">mod</button>
            <button type="button" class="{{ $op }} col-span-2 text-red-400" @click="clear()">C</button>

            @foreach ([7, 8, 9] as $digit)<button type="button" class="{{ $key }}" :disabled="!digitEnabled('{{ $digit }}')" @click="press('{{ $digit }}', true)">{{ $digit }}</button>@endforeach
            <button type="button" class="{{ $op }}" @click="press('÷')">÷</button>
            <button type="button" class="{{ $op }} col-span-2 text-xs" title="Complemento a dos: cambia el signo" @click="setValue(-live.value)" data-test="calc-twos">Comp. a 2</button>

            @foreach ([4, 5, 6] as $digit)<button type="button" class="{{ $key }}" :disabled="!digitEnabled('{{ $digit }}')" @click="press('{{ $digit }}', true)">{{ $digit }}</button>@endforeach
            <button type="button" class="{{ $op }}" @click="press('×')">×</button>
            <button type="button" class="col-span-2 row-span-3 rounded-md bg-primary font-mono text-lg font-bold text-white transition hover:bg-primary-bright" @click="equals()" data-test="calc-equals-programmer">=</button>

            @foreach ([1, 2, 3] as $digit)<button type="button" class="{{ $key }}" :disabled="!digitEnabled('{{ $digit }}')" @click="press('{{ $digit }}', true)">{{ $digit }}</button>@endforeach
            <button type="button" class="{{ $op }}" @click="press('−')">−</button>

            <button type="button" class="{{ $key }} col-span-3" @click="press('0', true)">0</button>
            <button type="button" class="{{ $op }}" @click="press('+')">+</button>
        </div>
    </div>
</div>
