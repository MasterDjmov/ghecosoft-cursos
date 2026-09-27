{{-- Panel de referencias del árbol dibujado (como "Referencias de Red" del mapa escolar). --}}
<div class="panel absolute top-3 right-3 hidden w-60 flex-col gap-3 p-3 text-xs sm:flex" x-data="{ open: true }">
    <button type="button" class="flex items-center justify-between font-display text-sm font-semibold text-white" x-on:click="open = ! open">
        Referencias
        <flux:icon name="chevron-down" variant="micro" class="transition" x-bind:class="open || '-rotate-90'" />
    </button>
    <div x-show="open" class="flex max-h-[60vh] flex-col gap-3 overflow-y-auto pe-1">
        <div class="flex flex-col gap-1.5">
            <span class="tech-label">{{ ucfirst(term('node', $course, 2)) }}</span>
            <span class="flex items-center gap-2"><span class="size-3 rounded-full bg-[#22d3ee]"></span> {{ ucfirst(term('node.root', $course)) }} (clase 0)</span>
            <span class="flex items-center gap-2"><span class="size-3 rounded-full bg-[#3b82f6]"></span> Tema</span>
            <span class="flex items-center gap-2"><span class="size-3 rounded-full bg-[#ef4444]"></span> {{ ucfirst(term('node.boss', $course)) }}</span>
            <span class="flex items-center gap-2"><span class="size-3 rounded-full bg-[#a855f7]"></span> Extra</span>
            <span class="flex items-center gap-2"><span class="size-3 rounded-full bg-[#2dd4bf]"></span> {{ ucfirst(term('node.window', $course)) }}</span>
            <span class="flex items-center gap-2"><span class="size-3 rounded-full bg-[#f472b6]"></span> {{ ucfirst(term('branch.path', $course)) }}</span>
            <span class="flex items-center gap-2"><span class="w-3 border-t-2 border-dotted border-[#f472b6]"></span> Requisito extra</span>
            <span class="flex items-center gap-2"><span class="size-3 rounded-full border border-dashed border-[#3b82f6] bg-[#3b82f6]/40"></span> Sin publicar</span>
        </div>
        <x-tree-label-filter :course="$course" />
        <div class="flex flex-col gap-1.5">
            <span class="tech-label">{{ ucfirst(term('practice', $course, 2)) }}</span>
            <span class="flex items-center gap-2"><span class="size-3 rounded-full bg-[#10b981]"></span> Obligatoria ({{ term('coin.course', $course, 2) }})</span>
            <span class="flex items-center gap-2"><span class="size-3 rounded-full bg-[#8b5cf6]"></span> Optativa ({{ term('coin.wildcard', null, 2) }})</span>
            <span class="flex items-center gap-2"><flux:icon name="code-bracket" variant="micro" class="text-ink-muted" /> Código</span>
            <span class="flex items-center gap-2"><flux:icon name="document-arrow-up" variant="micro" class="text-ink-muted" /> Archivo</span>
            <span class="flex items-center gap-2"><flux:icon name="paper-clip" variant="micro" class="text-ink-muted" /> Código y archivo</span>
            <span class="flex items-center gap-2"><flux:icon name="check" variant="micro" class="text-ink-muted" /> Sin entrega</span>
        </div>
    </div>
</div>
