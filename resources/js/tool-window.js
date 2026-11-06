// Las ventanas flotantes de las Herramientas (D120): se mueven, se achican y siguen abiertas mientras se navega por la
// plataforma, para practicar con la clase al lado. Puede haber una por herramienta y varias de las que dicen
// data-tool-limit (la calculadora y la tabla), que además solo se cierran con la cruz. Cada una es un iframe de la
// misma plataforma; viven fuera del <body> porque wire:navigate reemplaza el <body> y un iframe que se mueve o se vuelve
// a crear pierde lo que estaba corriendo. Solo se abren en páginas con menú, que dicen quién las usa en
// <body data-tool-windows="id">.

const MIN = { width: 320, height: 240 };
const SMALL_SCREEN = 640;
const BAR_HEIGHT = 44;
const Z_BASE = 1000;
const STEP = 28;

/** Las ventanas abiertas; la última es la que está adelante. */
let windows = null;
let loadedFor = null;
const boxes = new Map();

const owner = () => document.body?.dataset.toolWindows ?? null;
const storageKey = () => `tool-windows:${owner()}`;

function save() {
    try {
        localStorage.setItem(storageKey(), JSON.stringify(windows));
    } catch (e) {
        // Sin almacenamiento, las ventanas igual funcionan: solo no se recuerdan.
    }
}

/** Solo herramientas de esta misma plataforma, aunque alguien toque lo guardado. */
function isSafe(saved) {
    return saved && typeof saved.url === 'string' && saved.url.startsWith('/herramientas/') && !saved.url.startsWith('//')
        && /^[a-z0-9]+$/i.test(saved.id ?? '') && typeof saved.title === 'string'
        && ['width', 'height', 'x', 'y'].every((field) => Number.isFinite(saved[field]));
}

function load() {
    try {
        const saved = JSON.parse(localStorage.getItem(storageKey()) ?? 'null');
        if (Array.isArray(saved)) return saved.filter(isSafe);

        // Lo que quedó de cuando había una sola ventana.
        const legacyKey = `tool-window:${owner()}`;
        const legacy = JSON.parse(localStorage.getItem(legacyKey) ?? 'null');
        localStorage.removeItem(legacyKey);
        const single = legacy ? { ...legacy, id: newId() } : null;
        return isSafe(single) ? [single] : [];
    } catch (e) {
        return [];
    }
}

function newId() {
    return Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
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

function applyOne(win) {
    const box = boxes.get(win.id);
    if (!box) return;
    const small = window.innerWidth < SMALL_SCREEN;
    const height = win.minimized ? BAR_HEIGHT : small ? window.innerHeight - 16 : win.height;
    const width = small ? window.innerWidth - 16 : win.minimized ? Math.min(win.width, 280) : win.width;
    win.x = Math.max(8, Math.min(win.x, window.innerWidth - Math.min(width, 120)));
    win.y = Math.max(8, Math.min(win.y, window.innerHeight - BAR_HEIGHT));
    // En el celular no se arrastran: las achicadas se apilan abajo.
    const stacked = windows.filter((other) => other.minimized).indexOf(win);
    const top = !small ? win.y : win.minimized ? window.innerHeight - (BAR_HEIGHT + 6) * (stacked + 1) : 8;
    Object.assign(box.style, { width: `${width}px`, height: `${height}px`, left: `${small ? 8 : win.x}px`, top: `${top}px`, zIndex: String(Z_BASE + windows.indexOf(win)) });
    box.querySelector('[data-part=frame]').style.display = win.minimized ? 'none' : '';
    box.querySelector('[data-part=resize]').style.display = win.minimized || small ? 'none' : '';
    const minimize = box.querySelector('[data-part=minimize]');
    minimize.title = win.minimized ? 'Agrandar' : 'Achicar';
    minimize.setAttribute('aria-label', minimize.title);
}

function applyAll() {
    windows?.forEach(applyOne);
}

/** Traerla adelante cambia solo el orden, no el lugar en la página: mover un iframe lo recargaría. */
function front(win) {
    if (windows[windows.length - 1] === win) return;
    windows = [...windows.filter((other) => other !== win), win];
    applyAll();
    save();
}

/** Mover o cambiar el tamaño: el puntero queda capturado, así no se pierde al pasar sobre un iframe. */
function dragging(handle, win, onMove) {
    handle.addEventListener('pointerdown', (event) => {
        if (event.button !== 0 || event.target.closest('button') || window.innerWidth < SMALL_SCREEN) return;
        event.preventDefault();
        handle.setPointerCapture(event.pointerId);
        const start = { x: event.clientX, y: event.clientY, state: { ...win } };
        const frames = [...boxes.values()].map((box) => box.querySelector('[data-part=frame]'));
        frames.forEach((frame) => (frame.style.pointerEvents = 'none'));
        const move = (e) => {
            onMove(e.clientX - start.x, e.clientY - start.y, start.state);
            applyOne(win);
        };
        const stop = () => {
            handle.removeEventListener('pointermove', move);
            handle.removeEventListener('pointerup', stop);
            handle.removeEventListener('pointercancel', stop);
            frames.forEach((frame) => (frame.style.pointerEvents = ''));
            save();
        };
        handle.addEventListener('pointermove', move);
        handle.addEventListener('pointerup', stop);
        handle.addEventListener('pointercancel', stop);
    });
}

function build(win) {
    const box = document.createElement('div');
    box.dataset.test = 'tool-window';
    box.dataset.toolUrl = win.url;
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-label', win.title);
    box.className = 'fixed flex flex-col overflow-hidden rounded-lg border border-primary-bright/50 bg-surface-lowest shadow-2xl';
    box.addEventListener('pointerdown', () => front(win), true);

    const bar = document.createElement('div');
    bar.className = 'flex h-11 shrink-0 cursor-move touch-none items-center gap-1 border-b border-outline bg-surface-low ps-3 pe-1 select-none';
    const title = document.createElement('span');
    title.className = 'min-w-0 flex-1 truncate font-mono text-xs text-ink';
    title.textContent = win.title;
    const minimize = iconButton('Achicar', 'M4 10h12', () => {
        win.minimized = !win.minimized;
        front(win);
        applyAll();
        save();
    });
    minimize.dataset.part = 'minimize';
    bar.append(title, minimize);
    // La calculadora y la tabla solo se cierran con la cruz: pasar a página la cerraría.
    if (!win.utility) {
        bar.append(iconButton('Abrir como página', 'M8 4H4v12h12v-4M11 4h5v5M16 4l-7 7', () => {
            const url = win.url;
            close(win);
            window.location.assign(url);
        }));
    }
    const closeButton = iconButton('Cerrar', 'M5 5l10 10M15 5L5 15', () => close(win));
    closeButton.dataset.part = 'close';
    bar.append(closeButton);

    const frame = document.createElement('iframe');
    frame.dataset.part = 'frame';
    frame.title = win.title;
    frame.className = 'min-h-0 w-full flex-1 bg-surface';
    // Tocar adentro también la trae adelante; los clics del iframe no llegan a esta página.
    frame.addEventListener('load', () => {
        try {
            frame.contentWindow.addEventListener('pointerdown', () => front(win), true);
        } catch (e) {
            // Es de la misma plataforma: no debería pasar, y solo se pierde traerla adelante.
        }
    });

    const resize = document.createElement('div');
    resize.dataset.part = 'resize';
    resize.title = 'Cambiar el tamaño';
    resize.className = 'absolute end-0 bottom-0 size-4 cursor-nwse-resize touch-none border-e-2 border-b-2 border-primary-bright/70';

    box.append(bar, frame, resize);
    // Afuera del <body>: wire:navigate lo reemplaza entero y esta ventana tiene que seguir corriendo.
    document.documentElement.append(box);
    boxes.set(win.id, box);

    dragging(bar, win, (dx, dy, from) => {
        win.x = from.x + dx;
        win.y = from.y + dy;
    });
    dragging(resize, win, (dx, dy, from) => {
        win.width = Math.max(MIN.width, Math.min(from.width + dx, window.innerWidth - win.x - 8));
        win.height = Math.max(MIN.height, Math.min(from.height + dy, window.innerHeight - win.y - 8));
    });
    frame.setAttribute('src', `${win.url}?ventana=1&w=${win.id}`);
}

function showAll() {
    windows.forEach((win) => {
        if (!boxes.has(win.id)) build(win);
        boxes.get(win.id).style.display = '';
    });
    applyAll();
}

function close(win) {
    boxes.get(win.id)?.remove();
    boxes.delete(win.id);
    windows = windows.filter((other) => other !== win);
    applyAll();
    save();
    try {
        localStorage.removeItem(`tool-instance:${owner()}:${win.id}`);
    } catch (e) {
        // Nada que recordar.
    }
}

function restore(win) {
    win.minimized = false;
    front(win);
    applyAll();
    save();
}

function create(url, title, limit, size) {
    const same = windows.filter((win) => win.url === url);
    const [wanted, wantedHeight] = (size ?? '760x620').split('x').map(Number);
    const width = Math.min(wanted, window.innerWidth - 32);
    const height = Math.min(wantedHeight, window.innerHeight - 96);
    const above = windows[windows.length - 1];
    // Cada una un poco corrida de la anterior, para que no queden una exactamente arriba de la otra.
    const x = above ? above.x - STEP : window.innerWidth - width - 16;
    const y = above ? above.y - STEP : window.innerHeight - height - 16;
    const used = new Set(same.map((win) => win.number ?? 1));
    let number = 1;
    while (used.has(number)) number++;
    const win = {
        id: newId(), url, number, utility: limit > 1,
        title: number > 1 ? `${title} ${number}` : title,
        minimized: false, width, height,
        x: x < 8 ? window.innerWidth - width - 16 : x,
        y: y < 8 ? window.innerHeight - height - 16 : y,
    };
    windows = [...windows, win];
    showAll();
    save();
}

function open(trigger) {
    const url = new URL(trigger.dataset.toolWindow, window.location.origin).pathname;
    const limit = Number(trigger.dataset.toolLimit ?? 1);
    const same = windows.filter((win) => win.url === url);
    const wantsAnother = trigger.dataset.toolNew !== undefined;
    if (same.length && (!wantsAnother || same.length >= limit)) {
        restore(same[same.length - 1]);
        return;
    }
    create(url, trigger.dataset.toolTitle, limit, trigger.dataset.toolSize);
}

function sync() {
    if (!owner()) {
        boxes.forEach((box) => (box.style.display = 'none'));
        return;
    }
    // Las ventanas son de quien las abrió: si entró otra persona en este navegador, no las ve.
    if (loadedFor !== owner()) {
        boxes.forEach((box) => box.remove());
        boxes.clear();
        loadedFor = owner();
        windows = load();
    }
    showAll();
}

// Adentro de una ventana no se abre otra.
if (window.self === window.top) {
    document.addEventListener('click', (event) => {
        const trigger = event.target.closest?.('[data-tool-window]');
        // Ctrl + clic en el menú abre la página en otra pestaña, como cualquier link.
        if (!trigger || !owner() || (trigger.tagName === 'A' && (event.ctrlKey || event.metaKey || event.shiftKey))) return;
        event.preventDefault();
        event.stopPropagation();
        sync();
        open(trigger);
    }, true);

    document.addEventListener('livewire:navigated', sync);
    window.addEventListener('resize', applyAll);
}
