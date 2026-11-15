// D123: el botón «Necesito ayuda» de una micro-misión (docs/AYUDA.md). Vive adentro del editor (codeRunner), así
// que ve `code`, `running`, `matches`, `error`, `programOutput` y `editor` del que lo contiene.
import { sideBySide } from './runners/compare.js';

// Gheco ofrece ayuda solo después de estos fallos seguidos, o de este tiempo sin ejecutar.
const OFFER_FAILS = 2;
const OFFER_IDLE_MS = 3 * 60 * 1000;

// Las frases que se están leyendo (si nadie las guarda, Chrome puede descartarlas antes de que suenen).
let queued = [];

/** Las voces del navegador: en Chrome llegan un rato después de cargar la página. */
function availableVoices() {
    const now = speechSynthesis.getVoices();
    if (now.length) return Promise.resolve(now);
    return new Promise((resolve) => {
        const done = () => resolve(speechSynthesis.getVoices());
        speechSynthesis.addEventListener('voiceschanged', done, { once: true });
        setTimeout(done, 1500);
    });
}

document.addEventListener('alpine:init', () => {
    // config: { stepId, where: bool, compare: bool, line: bool, expected: string, state: { lines, solution } }
    window.Alpine.data('stepHelp', (config) => ({
        helpOpen: false,
        helpBusy: false,
        helpError: null,
        whereLines: null,
        compareOpen: false,
        shownLines: config.state?.lines ?? [],
        fullSolution: config.state?.solution ?? null,
        lineWait: false,
        newLine: null,
        fails: 0,
        offer: false,
        offerDone: false,
        idleTimer: null,
        wasRunning: false,
        logged: {},
        reading: false,
        readError: null,

        init() {
            this.restartIdle();
        },

        destroy() {
            clearTimeout(this.idleTimer);
        },

        /** Se llama con cada cambio del ejecutor (x-effect): cuenta los fallos al terminar de ejecutar. */
        watchRun() {
            const running = this.running;
            if (running && !this.wasRunning) this.restartIdle();
            if (!running && this.wasRunning) {
                if (this.matches === false || this.error) {
                    this.fails++;
                    this.lineWait = false;
                    if (this.fails >= OFFER_FAILS) this.offerHelp();
                } else if (this.matches === true) {
                    this.offer = false;
                    clearTimeout(this.idleTimer);
                }
            }
            this.wasRunning = running;
        },

        restartIdle() {
            clearTimeout(this.idleTimer);
            if (this.offerDone) return;
            this.idleTimer = setTimeout(() => this.offerHelp(), OFFER_IDLE_MS);
        },

        offerHelp() {
            if (this.offerDone || this.helpOpen || this.matches === true) return;
            this.offer = true;
            this.offerDone = true;
            clearTimeout(this.idleTimer);
            this.logHelp('offer');
        },

        acceptOffer() {
            this.offer = false;
            this.helpOpen = true;
        },

        logHelp(kind) {
            if (this.logged[kind]) return;
            this.logged[kind] = true;
            this.$wire.helpLog(config.stepId, kind).catch(() => {});
        },

        // ---- ¿Dónde toco?

        async showWhere() {
            if (this.helpBusy) return;
            this.helpBusy = true;
            this.helpError = null;
            const r = await this.$wire.helpWhere(config.stepId);
            this.helpBusy = false;
            if (!r.ok) return (this.helpError = r.error);
            this.whereLines = r.lines;
            this.editor?.markLines(r.lines);
        },

        whereText() {
            const lines = this.whereLines ?? [];
            if (!lines.length) return 'No encontré renglones para marcar: compará tu código con la consigna.';
            const list = lines.length === 1 ? `el renglón ${lines[0]}` : `los renglones ${lines.slice(0, -1).join(', ')} y ${lines.at(-1)}`;

            return `Marqué en ámbar ${list}: ahí hay que cambiar algo o agregar algo justo debajo. El resto ya está bien.`;
        },

        // ---- Comparemos

        canCompare() {
            return config.compare && this.programOutput !== null && this.matches === false;
        },

        rows() {
            return this.canCompare() ? sideBySide(config.expected, this.programOutput) : [];
        },

        toggleCompare() {
            this.compareOpen = !this.compareOpen;
            if (this.compareOpen) this.logHelp('compare');
        },

        // ---- Mostrame una línea

        async showLine() {
            if (this.helpBusy) return;
            this.helpBusy = true;
            this.helpError = null;
            const r = await this.$wire.helpLine(config.stepId, this.code ?? '');
            this.helpBusy = false;
            if (!r.ok) return (this.helpError = r.error);
            this.shownLines = r.lines;
            this.fullSolution = r.solution;
            this.lineWait = r.wait;
            this.newLine = r.new;
        },

        // ---- Escuchar el desafío (la voz del navegador)

        canRead() {
            return 'speechSynthesis' in window;
        },

        /**
         * Lee el desafío en voz alta. Chrome en Linux viene sin voces (hay que abrirlo con --enable-speech-dispatcher)
         * y entonces speak() no suena ni avisa: si no hay ninguna voz, se dice. Va por oraciones porque Chrome corta
         * las lecturas largas, y se guardan las frases para que no se pierdan antes de sonar.
         */
        async readAloud(element) {
            if (!this.canRead() || !element) return;
            if (this.reading) {
                speechSynthesis.cancel();
                this.reading = false;
                return;
            }
            this.readError = null;
            const voices = await availableVoices();
            if (!voices.length) {
                this.helpOpen = true;
                this.readError = 'Este navegador no tiene voces instaladas. Probá con otro (en Windows, Edge o Chrome ya traen voces en español).';
                return;
            }
            const spanish = voices.find((v) => v.lang?.toLowerCase() === 'es-ar')
                ?? voices.find((v) => v.lang?.toLowerCase().startsWith('es'));
            const parts = element.innerText.replace(/[`*_#>]/g, ' ')
                .split(/\n+|(?<=[.!?:;])\s+/).map((part) => part.trim()).filter(Boolean);
            speechSynthesis.cancel();
            queued = parts.map((part, i) => {
                const utterance = new SpeechSynthesisUtterance(part);
                utterance.lang = spanish?.lang ?? 'es-AR';
                if (spanish) utterance.voice = spanish;
                utterance.rate = 0.95;
                if (i === parts.length - 1) utterance.onend = () => { this.reading = false; };
                utterance.onerror = (e) => {
                    this.reading = false;
                    if (e.error !== 'canceled' && e.error !== 'interrupted') this.readError = `No se pudo leer en voz alta en este navegador (${e.error}).`;
                };
                return utterance;
            });
            this.reading = true;
            // Chrome a veces se traga lo que se pide justo después de cancel(): un respiro antes de hablar.
            setTimeout(() => {
                if (speechSynthesis.paused) speechSynthesis.resume();
                queued.forEach((utterance) => speechSynthesis.speak(utterance));
            }, 80);
            this.logHelp('read');
        },
    }));
});
