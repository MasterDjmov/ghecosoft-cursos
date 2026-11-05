// La ventana flotante de las Herramientas (D120): se mueve, se achica y sigue abierta mientras se navega por la
// plataforma, para practicar con la clase al lado. Es un iframe de la misma plataforma; vive fuera del <body> porque
// wire:navigate reemplaza el <body> y un iframe que se mueve o se vuelve a crear pierde lo que estaba corriendo.
// Solo se abre en páginas con menú, que dicen quién usa la ventana en <body data-tool-windows="id">.

const MIN = { width: 320, height: 240 };
const SMALL_SCREEN = 640;
let box = null;
let state = null;

const owner = () => document.body?.dataset.toolWindows ?? null;
const storageKey = () => `tool-window:${owner()}`;

function save() {
    try {
        localStorage.setItem(storageKey(), JSON.stringify(state));
    } catch (e) {
        // Sin almacenamiento, la ventana igual funciona: solo no se recuerda.
    }
}

function load() {
    try {
        const saved = JSON.parse(localStorage.getItem(storageKey()) ?? 'null');
        // Solo herramientas de esta misma plataforma, aunque alguien toque lo guardado.
        return saved && typeof saved.url === 'string' && saved.url.startsWith('/herramientas/') && !saved.url.startsWith('//') ? saved : null;
    } catch (e) {
        return null;
    }
}

function iconButton(label, path, onClick) {
    const button = document.createElement('button');
    button.type = 'button';
    button.title = label;
    button.setAttribute('aria-label', label);
    button.className = 'grid size-7 place-items-center rounded text-ink-muted transition hover:bg-surface-high hover:text-ink';
    button.innerHTML = `<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" class="size-4" aria-hidden="true"><path d="${path}"/></svg>`;
    button.addEventListener('click', onClick);
    return button;
}

function apply() {
    if (!box) return;
    const small = window.innerWidth < SMALL_SCREEN;
    const height = state.minimized ? 44 : small ? window.innerHeight - 16 : state.height;
    const width = small ? window.innerWidth - 16 : state.minimized ? Math.min(state.width, 320) : state.width;
    state.x = Math.max(8, Math.min(state.x, window.innerWidth - Math.min(width, 120)));
    state.y = Math.max(8, Math.min(state.y, window.innerHeight - 44));
    Object.assign(box.style, { width: `${width}px`, height: `${height}px`, left: `${small ? 8 : state.x}px`, top: `${small ? 8 : state.y}px` });
    box.querySelector('[data-part=frame]').style.display = state.minimized ? 'none' : '';
    box.querySelector('[data-part=resize]').style.display = state.minimized || small ? 'none' : '';
    box.querySelector('[data-part=minimize]').title = state.minimized ? 'Agrandar' : 'Achicar';
}

/** Mover o cambiar el tamaño: el puntero queda capturado, así no se pierde al pasar sobre el iframe. */
function dragging(handle, onMove) {
    handle.addEventListener('pointerdown', (event) => {
        if (event.button !== 0 || event.target.closest('button') || window.innerWidth < SMALL_SCREEN) return;
        event.preventDefault();
        handle.setPointerCapture(event.pointerId);
        const start = { x: event.clientX, y: event.clientY, state: { ...state } };
        const frame = box.querySelector('[data-part=frame]');
        frame.style.pointerEvents = 'none';
        const move = (e) => {
            onMove(e.clientX - start.x, e.clientY - start.y, start.state);
            apply();
        };
        const stop = () => {
            handle.removeEventListener('pointermove', move);
            handle.removeEventListener('pointerup', stop);
            handle.removeEventListener('pointercancel', stop);
            frame.style.pointerEvents = '';
            save();
        };
        handle.addEventListener('pointermove', move);
        handle.addEventListener('pointerup', stop);
        handle.addEventListener('pointercancel', stop);
    });
}

function build() {
    box = document.createElement('div');
    box.dataset.test = 'tool-window';
    box.setAttribute('role', 'dialog');
    box.className = 'fixed z-50 flex flex-col overflow-hidden rounded-lg border border-primary-bright/50 bg-surface-lowest shadow-2xl';

    const bar = document.createElement('div');
    bar.className = 'flex h-11 shrink-0 cursor-move touch-none items-center gap-1 border-b border-outline bg-surface-low ps-3 pe-1 select-none';
    const title = document.createElement('span');
    title.dataset.part = 'title';
    title.className = 'min-w-0 flex-1 truncate font-mono text-xs text-ink';
    const minimize = iconButton('Achicar', 'M4 10h12', () => {
        state.minimized = !state.minimized;
        apply();
        save();
    });
    minimize.dataset.part = 'minimize';
    const page = iconButton('Abrir como página', 'M8 4H4v12h12v-4M11 4h5v5M16 4l-7 7', () => {
        const url = state.url;
        close();
        window.location.assign(url);
    });
    bar.append(title, minimize, page, iconButton('Cerrar', 'M5 5l10 10M15 5L5 15', close));

    const frame = document.createElement('iframe');
    frame.dataset.part = 'frame';
    frame.className = 'min-h-0 w-full flex-1 bg-surface';

    const resize = document.createElement('div');
    resize.dataset.part = 'resize';
    resize.title = 'Cambiar el tamaño';
    resize.className = 'absolute end-0 bottom-0 size-4 cursor-nwse-resize touch-none border-e-2 border-b-2 border-primary-bright/70';

    box.append(bar, frame, resize);
    // Afuera del <body>: wire:navigate lo reemplaza entero y esta ventana tiene que seguir corriendo.
    document.documentElement.append(box);

    dragging(bar, (dx, dy, from) => {
        state.x = from.x + dx;
        state.y = from.y + dy;
    });
    dragging(resize, (dx, dy, from) => {
        state.width = Math.max(MIN.width, Math.min(from.width + dx, window.innerWidth - state.x - 8));
        state.height = Math.max(MIN.height, Math.min(from.height + dy, window.innerHeight - state.y - 8));
    });
}

function show() {
    if (!box) build();
    box.querySelector('[data-part=title]').textContent = state.title;
    box.setAttribute('aria-label', state.title);
    const frame = box.querySelector('[data-part=frame]');
    const src = `${state.url}?ventana=1`;
    if (frame.getAttribute('src') !== src) frame.setAttribute('src', src);
    box.style.display = '';
    apply();
}

function close() {
    state = null;
    box?.remove();
    box = null;
    try {
        localStorage.removeItem(storageKey());
    } catch (e) {
        // Nada que recordar.
    }
}

function open(url, title) {
    const width = Math.min(760, window.innerWidth - 32);
    const height = Math.min(620, window.innerHeight - 96);
    state = { url, title, minimized: false, width, height, x: window.innerWidth - width - 16, y: window.innerHeight - height - 16, ...(state ? { width: state.width, height: state.height, x: state.x, y: state.y } : {}) };
    show();
    save();
}

// Adentro de la propia ventana no se abre otra.
if (window.self === window.top) {
    document.addEventListener('click', (event) => {
        const button = event.target.closest?.('[data-tool-window]');
        if (!button) return;
        event.preventDefault();
        event.stopPropagation();
        open(new URL(button.dataset.toolWindow, window.location.origin).pathname, button.dataset.toolTitle);
    }, true);

    document.addEventListener('livewire:navigated', () => {
        if (!owner()) {
            if (box) box.style.display = 'none';
            return;
        }
        state ??= load();
        if (state) show();
    });

    window.addEventListener('resize', apply);
}
