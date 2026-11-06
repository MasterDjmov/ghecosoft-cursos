@php($tab = 'inline-flex items-center gap-1.5 rounded px-2.5 py-1.5 text-xs font-semibold transition')
<div @class(['mx-auto flex w-full max-w-5xl flex-col gap-3', 'p-4 sm:p-8' => ! $inWindow, 'p-3' => $inWindow])>
    <x-tool-header title="Tabla ASCII" :in-window="$inWindow" :data-tool-limit="3" data-tool-size="600x640">
        Tocá un carácter y se copia. Del 0 al 127 es igual en todos lados; la parte extendida depende de dónde corra tu programa.
    </x-tool-header>

    <div wire:ignore x-data="asciiTool({{ auth()->id() }})" data-test="ascii-tool" class="flex flex-col gap-3">
        <div class="flex flex-wrap gap-1 rounded-md border border-outline p-0.5" role="tablist" aria-label="Tabla">
            <button type="button" role="tab" class="{{ $tab }}" :class="tab === 'ascii' ? 'bg-primary text-white' : 'text-ink-muted hover:text-ink'" :aria-selected="tab === 'ascii'" @click="tab = 'ascii'; query = ''" data-test="ascii-tab-ascii">ASCII</button>
            <button type="button" role="tab" class="{{ $tab }}" :class="tab === 'windows' ? 'bg-primary text-white' : 'text-ink-muted hover:text-ink'" :aria-selected="tab === 'windows'" @click="tab = 'windows'; query = ''" data-test="ascii-tab-windows"><x-os-icon name="windows" /> Windows 850</button>
            <button type="button" role="tab" class="{{ $tab }}" :class="tab === 'unicode' ? 'bg-primary text-white' : 'text-ink-muted hover:text-ink'" :aria-selected="tab === 'unicode'" @click="tab = 'unicode'; query = ''" data-test="ascii-tab-unicode"><x-os-icon name="linux" /> Linux y Unicode</button>
            <button type="button" role="tab" class="{{ $tab }}" :class="tab === 'dos' ? 'bg-primary text-white' : 'text-ink-muted hover:text-ink'" :aria-selected="tab === 'dos'" @click="tab = 'dos'; query = ''" data-test="ascii-tab-dos"><x-os-icon name="dos" /> DOS 437</button>
        </div>

        <div class="flex flex-wrap items-center gap-2">
            <input type="search" x-model="query" placeholder="Buscar: ñ, 65, 0x41, ESC, flecha…" aria-label="Buscar un carácter" data-test="ascii-search"
                class="min-w-40 flex-1 rounded-md border border-outline bg-surface-lowest px-3 py-1.5 text-sm text-ink placeholder:text-ink-muted focus:border-primary-bright focus:outline-none">
            <label class="flex items-center gap-1.5 text-xs text-ink-muted">Al tocar, copiar
                <select x-model="copyAs" data-test="ascii-copy-as" class="rounded-md border border-outline bg-surface-lowest px-2 py-1.5 text-xs text-ink focus:border-primary-bright focus:outline-none">
                    <template x-for="(label, key) in formLabels" :key="key"><option :value="key" x-text="label" :selected="copyAs === key"></option></template>
                </select>
            </label>
        </div>

        {{-- Cuál usar: el ícono solo no alcanza, porque depende también del lenguaje. --}}
        <details x-show="!searching && tab !== 'ascii'" class="rounded-md border border-outline bg-surface-low px-3 py-2 text-xs text-ink-muted" data-test="ascii-help">
            <summary class="cursor-pointer font-semibold text-ink">¿Cuándo uso esta tabla?</summary>
            <div class="mt-2 flex flex-col gap-1.5 leading-relaxed">
                <div x-show="tab === 'windows'" class="flex flex-col gap-1.5">
                    <p>Para <strong class="text-ink">C y C++ en la consola de Windows</strong>, que en español suele venir en la página 850: <code>printf("%c", 164);</code> muestra <code>ñ</code>. Para ver cuál tiene la tuya, escribí <code>chcp</code> en la consola.</p>
                    <p>En Python, Java, JavaScript y C#, aunque estés en Windows, usá la pestaña de Unicode.</p>
                    <p>Ojo: las Herramientas de esta plataforma no son una consola de Windows. Ahí, C y C++ funcionan como en Linux: usá los bytes de UTF-8 de la otra pestaña.</p>
                </div>
                <div x-show="tab === 'unicode'" class="flex flex-col gap-1.5">
                    <p>Para <strong class="text-ink">la terminal de Linux, las páginas web y las bases de datos en UTF-8</strong>, y para estos lenguajes en cualquier sistema:</p>
                    <ul class="list-disc space-y-0.5 ps-4">
                        <li><strong class="text-ink">Python:</strong> <code>chr(241)</code> da <code>ñ</code>, y <code>ord('ñ')</code> da 241.</li>
                        <li><strong class="text-ink">Java y C#:</strong> <code>(char) 241</code> da <code>ñ</code>.</li>
                        <li><strong class="text-ink">JavaScript:</strong> <code>String.fromCodePoint(241)</code> da <code>ñ</code>.</li>
                        <li><strong class="text-ink">PHP:</strong> <code>mb_chr(241)</code> da <code>ñ</code>; <code>chr(241)</code> da un byte suelto, que no es una <code>ñ</code>.</li>
                        <li><strong class="text-ink">HTML:</strong> <code>&amp;#241;</code> o <code>&amp;ntilde;</code>.</li>
                        <li><strong class="text-ink">C y C++ en Linux y en las Herramientas de esta plataforma:</strong> hay que mandar los bytes de UTF-8: <code>printf("\xC3\xB1");</code>.</li>
                    </ul>
                    <p>Acá está lo más usado; cualquier otro carácter se busca por su código, como <code>U+2603</code>.</p>
                </div>
                <div x-show="tab === 'dos'" class="flex flex-col gap-1.5">
                    <p>Para <strong class="text-ink">Ensamblador 8086</strong>: es la tabla del Gólem de esta plataforma y de los programas de DOS. Se parece mucho a la 850, pero algunos símbolos cambian.</p>
                </div>
            </div>
        </details>

        <p x-show="searching && !sections.length" class="rounded-md border border-outline p-4 text-center text-sm text-ink-muted">No encontré nada. Probá con el carácter, su número o un código como U+00F1.</p>

        <div class="flex flex-col gap-4">
            <template x-for="section in sections" :key="section.title">
                <section class="flex flex-col gap-1.5">
                    <h2 class="tech-label" x-text="section.title"></h2>
                    <div class="grid grid-cols-[repeat(auto-fill,minmax(4.25rem,1fr))] gap-1">
                        <template x-for="entry in section.items" :key="entry.key">
                            <button type="button" class="flex min-w-0 flex-col items-center rounded border px-1 py-1.5 transition hover:border-primary-bright hover:bg-surface-high"
                                :class="copiedKey === entry.key ? 'border-primary-bright bg-primary/30' : (selected?.key === entry.key ? 'border-primary-bright bg-surface-low' : 'border-outline bg-surface-low')"
                                :title="titleOf(entry)" :aria-label="(entry.name || entry.char) + ', decimal ' + entry.code" @click="pick(entry)" @mouseenter="selected = entry" :data-test="'ascii-' + entry.key">
                                <span class="flex h-7 items-center font-mono text-white" :class="entry.wide ? 'text-xs font-semibold' : 'text-xl'" x-text="entry.label"></span>
                                <span class="font-mono text-[11px] text-ink" x-text="entry.code"></span>
                                <span class="max-w-full truncate font-mono text-[10px] text-ink-muted" x-text="lineOf(entry)"></span>
                            </button>
                        </template>
                    </div>
                </section>
            </template>
        </div>

        {{-- Lo elegido, con todas sus formas para copiar. --}}
        <div class="sticky bottom-2 flex flex-col gap-1.5 rounded-md border border-primary-bright/50 bg-surface-lowest p-2 shadow-xl" x-show="selected || copied" data-test="ascii-detail">
            <template x-if="selected">
                <div class="flex flex-col gap-1.5">
                    <p class="truncate text-xs text-ink"><span class="me-1 font-mono text-base text-white" x-text="selected.label"></span> <span class="text-ink-muted" x-text="selected.name"></span></p>
                    <div class="flex flex-wrap gap-1">
                        <template x-for="form in formsOf(selected)" :key="form.key">
                            <button type="button" class="rounded border border-outline px-1.5 py-0.5 font-mono text-[11px] text-ink hover:border-primary-bright" :title="'Copiar ' + form.label" @click="copy(form.value)"><span class="text-ink-muted" x-text="form.label + ' '"></span><span x-text="form.value"></span></button>
                        </template>
                    </div>
                </div>
            </template>
            <p x-show="copied" class="truncate text-xs font-semibold text-primary-bright" aria-live="polite" data-test="ascii-copied">Copiado: <span class="font-mono" x-text="copied === ' ' ? 'espacio' : copied"></span></p>
        </div>
    </div>
</div>
