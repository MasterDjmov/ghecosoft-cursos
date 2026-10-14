{{-- Ver una imagen en grande, entera: cualquier imagen con x-on:click="$dispatch('zoom-image', { src: '…' })". Va una sola vez por página. --}}
<div wire:ignore x-data="{ src: null }" x-on:zoom-image.window="src = $event.detail.src" x-on:keydown.escape.window="src = null"
    x-show="src" style="display: none" x-transition.opacity x-on:click="src = null" role="dialog" aria-modal="true" aria-label="Imagen en grande"
    class="fixed inset-0 z-50 flex cursor-zoom-out items-center justify-center bg-[#05070d]/90 p-4 sm:p-8" data-test="image-lightbox">
    <img :src="src" alt="" class="max-h-full max-w-full rounded-xl border border-outline object-contain shadow-2xl">
    <button type="button" class="absolute right-4 top-4 rounded-full bg-surface/80 p-2 text-white hover:bg-surface" aria-label="Cerrar">
        <flux:icon name="x-mark" />
    </button>
</div>
