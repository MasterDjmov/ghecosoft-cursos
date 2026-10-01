// Avisos en vivo (D62): la campanita (Livewire) manda cuántos avisos hay sin leer y cuál es el último:
// cada 20 s con la pestaña a la vista y cada 60 s en segundo plano, para no cargar el hosting compartido. Acá: la cantidad en el título de la pestaña, un punto rojo en el ícono y, si el aviso es
// nuevo, un tono corto y la notificación del sistema (según las preferencias de Mi cuenta → Avisos).

const TITLE_COUNT = /^\(\d+\+?\) /;
let prefs = { sound: true, desktop: false };
let originalIcon = null;
let audio = null;

function setTitle(unread) {
    const base = document.title.replace(TITLE_COUNT, '');
    document.title = unread > 0 ? `(${unread > 99 ? '99+' : unread}) ${base}` : base;
}

function setIconDot(show) {
    const link = document.querySelector('link[rel~="icon"]');
    if (!link) return;
    originalIcon ??= link.href;
    if (!show) {
        link.href = originalIcon;
        return;
    }
    const img = new Image();
    img.onload = () => {
        const size = 64;
        const canvas = Object.assign(document.createElement('canvas'), { width: size, height: size });
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0, size, size);
        ctx.beginPath();
        ctx.arc(size - 14, 14, 13, 0, 2 * Math.PI);
        ctx.fillStyle = '#ef4444';
        ctx.fill();
        ctx.lineWidth = 4;
        ctx.strokeStyle = '#060e20';
        ctx.stroke();
        link.href = canvas.toDataURL('image/png');
    };
    img.src = originalIcon;
}

// Dos notas cortas con Web Audio (sin archivos). El navegador lo permite después del primer clic en la página.
function beep() {
    try {
        audio ??= new (window.AudioContext || window.webkitAudioContext)();
        const now = audio.currentTime;
        [[880, 0], [1320, 0.12]].forEach(([frequency, start]) => {
            const osc = audio.createOscillator();
            const gain = audio.createGain();
            osc.type = 'sine';
            osc.frequency.value = frequency;
            gain.gain.setValueAtTime(0.0001, now + start);
            gain.gain.exponentialRampToValueAtTime(0.18, now + start + 0.02);
            gain.gain.exponentialRampToValueAtTime(0.0001, now + start + 0.22);
            osc.connect(gain).connect(audio.destination);
            osc.start(now + start);
            osc.stop(now + start + 0.25);
        });
    } catch (e) {
        // Sin audio disponible: no pasa nada.
    }
}

function desktopNotification(newest) {
    if (!('Notification' in window) || Notification.permission !== 'granted') return;
    const notification = new Notification(newest.title, { body: newest.body, icon: originalIcon ?? '/favicon.png', tag: newest.id });
    notification.onclick = () => {
        window.focus();
        window.Livewire?.navigate(newest.url) ?? (window.location.href = newest.url);
        notification.close();
    };
}

function read(key) {
    try {
        return localStorage.getItem(key);
    } catch (e) {
        return null;
    }
}

function write(key, value) {
    try {
        localStorage.setItem(key, value);
    } catch (e) {
        // Navegación privada o almacenamiento bloqueado: solo se pierde recordar el último aviso.
    }
}

function handle({ user, unread, newest, sound, desktop }) {
    prefs = { sound, desktop };
    setTitle(unread);
    setIconDot(unread > 0);

    // Solo avisa lo que llegó después de la última vez que se miró (entre pestañas y recargas).
    const key = `live-alerts:${user}`;
    const last = read(key);
    if (!newest || newest.id === last) return;
    write(key, newest.id);
    if (last === null) return; // primera vez en este navegador: no suena por avisos viejos

    if (prefs.sound) beep();
    // La notificación del sistema, solo si no está mirando la plataforma (otra pestaña u otro programa).
    if (prefs.desktop && !document.hasFocus()) desktopNotification(newest);
}

const VISIBLE_MS = 20000;
const HIDDEN_MS = 60000;

// La campanita consulta sola: más seguido si se está mirando la pestaña y, al volver a ella, enseguida.
document.addEventListener('alpine:init', () => {
    window.Alpine.data('liveBell', () => ({
        open: false,
        timer: null,
        init() {
            this.onVisibility = () => {
                if (!document.hidden) this.schedule(0);
            };
            document.addEventListener('visibilitychange', this.onVisibility);
            this.schedule();
        },
        schedule(delay = document.hidden ? HIDDEN_MS : VISIBLE_MS) {
            clearTimeout(this.timer);
            this.timer = setTimeout(async () => {
                try {
                    await this.$wire.$refresh();
                } finally {
                    this.schedule();
                }
            }, delay);
        },
        destroy() {
            clearTimeout(this.timer);
            document.removeEventListener('visibilitychange', this.onVisibility);
        },
    }));
});

document.addEventListener('livewire:init', () => {
    // Sesión cerrada (la cuenta entró en otro lado, D65, o se pausó): en vez del cartel de Livewire en
    // inglés, directo al login, que explica qué pasó.
    window.Livewire.hook('request', ({ fail }) => {
        fail(({ status, preventDefault }) => {
            if (status === 419) {
                preventDefault();
                window.location.href = '/login';
            }
        });
    });
    window.Livewire.on('live-alerts', (payload) => handle(Array.isArray(payload) ? payload[0] : payload));
    window.Livewire.on('alert-preferences', (payload) => {
        const p = Array.isArray(payload) ? payload[0] : payload;
        prefs = { sound: p.sound, desktop: p.desktop };
    });
});

// Al navegar con wire:navigate el título se reemplaza: se vuelve a poner la cantidad.
document.addEventListener('livewire:navigated', () => {
    const count = Number(document.querySelector('[data-unread]')?.dataset.unread ?? 0);
    setTitle(count);
    originalIcon = null;
    setIconDot(count > 0);
});

window.liveAlerts = { beep };
