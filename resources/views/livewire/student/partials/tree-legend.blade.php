{{-- Referencias del árbol del alumno. --}}
<div class="panel absolute top-3 right-3 hidden w-56 flex-col gap-3 p-3 text-xs sm:flex" x-data="{ open: true }">
    <button type="button" class="flex items-center justify-between font-display text-sm font-semibold text-white" x-on:click="open = ! open">
        Referencias
        <flux:icon name="chevron-down" variant="micro" class="transition" x-bind:class="open || '-rotate-90'" />
    </button>
    <div x-show="open" class="flex flex-col gap-3">
        <div class="flex flex-col gap-1.5">
            <span class="tech-label">{{ ucfirst(term('node', $course, 2)) }}</span>
            <span class="flex items-center gap-2"><span class="size-3 rounded-full bg-[#334155]"></span> {{ term('state.locked', $course) }}</span>
            <span class="flex items-center gap-2"><span class="size-3 rounded-full border border-dashed border-[#3b82f6]"></span> {{ term('state.available', $course) }}</span>
            <span class="flex items-center gap-2"><span class="size-3 rounded-full bg-[#3b82f6]"></span> {{ term('state.unlocked', $course) }}</span>
            <span class="flex items-center gap-2"><span class="size-3 rounded-full bg-[#3b82f6] ring-2 ring-[#10b981]"></span> {{ term('state.completed', $course) }}</span>
            <span class="flex items-center gap-2"><span class="size-3 rounded-full bg-[#ef4444]"></span> {{ ucfirst(term('node.boss', $course)) }}</span>
            <span class="flex items-center gap-2"><span class="size-3 rounded-full bg-[#a855f7]"></span> Extra ({{ term('coin.wildcard', null, 2) }})</span>
        </div>
        <div class="flex flex-col gap-1.5">
            <span class="tech-label">{{ ucfirst(term('practice', $course, 2)) }}</span>
            <span class="flex items-center gap-2"><span class="size-3 rounded-full bg-[#10b981]"></span> Aprobada</span>
            <span class="flex items-center gap-2"><span class="size-3 rounded-full bg-[#f59e0b]"></span> Entregada, sin corregir</span>
            <span class="flex items-center gap-2"><span class="size-3 rounded-full bg-[#f87171]"></span> Rehacer</span>
            <span class="flex items-center gap-2"><span class="size-3 rounded-full bg-[#475569]"></span> Sin hacer</span>
        </div>
    </div>
</div>
