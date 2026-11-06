// Copiar al portapapeles, también adentro de la ventana flotante, y lo que recuerda cada ventana de herramienta.

export async function copyText(text) {
    try {
        await navigator.clipboard.writeText(text);
        return true;
    } catch (e) {
        // Sin permiso o sin https: el camino viejo.
        const area = document.createElement('textarea');
        area.value = text;
        area.style.position = 'fixed';
        area.style.opacity = '0';
        document.body.append(area);
        area.select();
        const done = document.execCommand('copy');
        area.remove();
        return done;
    }
}

/** Cada ventana recuerda lo suyo (`?w=` lo pone tool-window.js, que lo borra al cerrarla); la página, aparte. */
export function instanceStore(user, tool) {
    const id = new URLSearchParams(window.location.search).get('w');
    const key = `tool-instance:${user}:${/^[a-z0-9]+$/i.test(id ?? '') ? id : `pagina-${tool}`}`;

    return {
        load() {
            try {
                return JSON.parse(localStorage.getItem(key) ?? '{}') ?? {};
            } catch (e) {
                return {};
            }
        },
        save(data) {
            try {
                localStorage.setItem(key, JSON.stringify(data));
            } catch (e) {
                // Sin almacenamiento, la herramienta igual funciona: solo no se recuerda.
            }
        },
    };
}
