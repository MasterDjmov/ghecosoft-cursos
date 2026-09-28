<flux:dropdown position="bottom" align="end">
    <button type="button" class="flex items-center gap-2 rounded-lg p-1 hover:bg-surface-high" data-test="sidebar-menu-button">
        <flux:avatar :name="auth()->user()->fullName()" :initials="auth()->user()->initials()" class="!bg-secondary !text-white" />
        <flux:icon.chevron-down variant="micro" class="text-ink-muted" />
    </button>

    <flux:menu class="min-w-64">
        <div class="flex items-center gap-3 px-2 py-2 text-start text-sm">
            <flux:avatar :name="auth()->user()->fullName()" :initials="auth()->user()->initials()" class="!bg-secondary !text-white" />
            <div class="grid flex-1 leading-tight">
                <span class="truncate font-semibold text-white">{{ auth()->user()->fullName() }}</span>
                <span class="truncate text-xs text-ink-muted">{{ auth()->user()->email ?? '@'.auth()->user()->username }}</span>
            </div>
        </div>
        <flux:menu.separator />
        <flux:menu.item :href="route('profile.edit')" icon="cog-6-tooth" wire:navigate>
            Mi cuenta
        </flux:menu.item>
        <flux:menu.separator />
        <form method="POST" action="{{ route('logout') }}" class="w-full">
            @csrf
            <flux:menu.item as="button" type="submit" icon="arrow-right-start-on-rectangle" variant="danger" class="w-full cursor-pointer" data-test="logout-button">
                {{ __('Log out') }}
            </flux:menu.item>
        </form>
    </flux:menu>
</flux:dropdown>
