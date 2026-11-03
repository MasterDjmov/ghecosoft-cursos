{{-- Solapas del visor (D116): index.html, estilos.css y app.js en HTML y CSS (resources/js/editor/html-files.js), o los
     archivos de un ejemplo de varios (App\Support\CodeFiles: dado.h, dado.c, main.c…). Vive dentro de un
     x-data="codeRunner(...)": usa files, fileTab y selectFile. Solo aparece si hay más de un archivo. --}}
<div x-show="files.length > 1" x-cloak>
<div {{ $attributes->class('flex items-end gap-1 overflow-x-auto border-b border-outline bg-surface-low/60 px-2 pt-1.5') }}
     role="tablist" aria-label="Archivos" data-test="code-file-tabs">
    <template x-for="(file, i) in files" :key="file">
        <button type="button" role="tab" x-on:click="selectFile(i)" x-bind:aria-selected="fileTab === i" x-bind:title="file"
            class="flex shrink-0 items-center gap-1.5 rounded-t-md border border-b-0 px-3 py-1.5 font-mono text-xs transition"
            x-bind:class="fileTab === i ? 'border-outline bg-surface-lowest text-white' : 'border-transparent text-ink-muted hover:bg-surface-high hover:text-ink'">
            <span class="size-2 rounded-full"
                x-bind:class="{ css: 'bg-[#a855f7]', js: 'bg-[#fbbf24]', json: 'bg-[#fbbf24]', html: 'bg-[#f97316]', java: 'bg-[#ef4444]', php: 'bg-[#818cf8]', c: 'bg-[#22d3ee]', h: 'bg-[#67e8f9]', cpp: 'bg-[#22d3ee]', sql: 'bg-[#34d399]', py: 'bg-[#facc15]' }[file.includes('.') ? file.split('.').pop() : ''] ?? 'bg-[#64748b]'"></span>
            <span x-text="file.split('/').pop()"></span>
        </button>
    </template>
</div>
{{-- La carpeta del archivo abierto (src/imperio/modelo/…), si tiene. --}}
<p x-show="files[fileTab]?.includes('/')" class="border-b border-outline bg-surface-low/30 px-3 py-1 font-mono text-[11px] text-ink-muted" x-text="files[fileTab]"></p>
</div>
