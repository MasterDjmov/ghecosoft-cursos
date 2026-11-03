{{-- Solapas del visor de HTML y CSS: index.html, estilos.css y app.js (resources/js/editor/html-files.js). Vive dentro de
     un x-data="codeRunner(...)": usa files, fileTab y selectFile. Solo aparece si la página se pudo separar en archivos. --}}
<div {{ $attributes->class('flex items-end gap-1 overflow-x-auto border-b border-outline bg-surface-low/60 px-2 pt-1.5') }}
     x-show="files.length > 1" x-cloak role="tablist" aria-label="Archivos" data-test="code-file-tabs">
    <template x-for="(file, i) in files" :key="file">
        <button type="button" role="tab" x-on:click="selectFile(i)" x-bind:aria-selected="fileTab === i"
            class="flex shrink-0 items-center gap-1.5 rounded-t-md border border-b-0 px-3 py-1.5 font-mono text-xs transition"
            x-bind:class="fileTab === i ? 'border-outline bg-surface-lowest text-white' : 'border-transparent text-ink-muted hover:bg-surface-high hover:text-ink'">
            <span class="size-2 rounded-full"
                x-bind:class="file.endsWith('.css') ? 'bg-[#a855f7]' : (file.endsWith('.js') ? 'bg-[#fbbf24]' : 'bg-[#f97316]')"></span>
            <span x-text="file"></span>
        </button>
    </template>
</div>
