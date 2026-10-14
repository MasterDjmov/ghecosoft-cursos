// Crónicas en Inglés (D106, docs/INGLES.md): una micro-misión de inglés en el navegador del alumno. No ejecuta
// nada: muestra la historia (cada palabra se toca y se escucha), lee en inglés y en español con la voz del
// navegador y compara las respuestas del ejercicio (App\Support\EnglishExercise arma el JSON). Al resolverlo,
// avisa «superada» al servidor, que da los premios de juego (StepCompleter).

const PASSED = 'superada';

const NUMBERS = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve',
    'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty'];

// Qué dice cada criatura cuando aparece (INGLES.md § 2).
export const CREATURES = {
    slime: '¡Un slime se comió una letra! Revisá cómo se escribe.',
    orc: '¡Un orco se robó un artículo! Mirá el a, an o the.',
    ogre: '¡Un ogro mezcló el orden! Probá con otro orden.',
    goblin: '¡Un goblin cambió el verbo! Fijate si concuerda.',
    skeleton: '¡Un esqueleto dejó una palabra que no va! Probá con otra.',
    troll: '¡Un troll desarmó la pregunta! Revisá cómo empieza.',
};

/** Minúsculas, sin acentos, sin signos ni apóstrofos y con un espacio entre palabras. */
export function normalize(text) {
    return String(text ?? '')
        .toLowerCase()
        .normalize('NFD').replace(/[̀-ͯ]/g, '')
        .replace(/['’`´]/g, '')
        .replace(/[^a-z0-9]+/g, ' ')
        .trim();
}

/** Distancia de edición (con las transposiciones): sirve para letras y para listas de palabras. */
export function levenshtein(a, b) {
    const d = Array.from({ length: a.length + 1 }, (_, i) => [i]);
    for (let j = 1; j <= b.length; j++) d[0][j] = j;
    for (let i = 1; i <= a.length; i++) {
        for (let j = 1; j <= b.length; j++) {
            d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
            // Dos letras dadas vuelta («thrid») cuentan como un solo error.
            if (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) d[i][j] = Math.min(d[i][j], d[i - 2][j - 2] + 1);
        }
    }
    return d[a.length][b.length];
}

/** «Iris has {a|an} book» → partes (lo mismo que EnglishExercise::template). */
export function template(text) {
    return String(text).split(/(\{[^}]*\})/).filter((chunk) => chunk !== '').map((chunk) => {
        const free = chunk.match(/^\{\*(\w+)\}$/);
        if (free) return { free: free[1].toLowerCase().startsWith('num') ? 'number' : 'name' };
        const hole = chunk.match(/^\{(.*)\}$/);
        if (hole) return { hole: hole[1].split('|').map((s) => s.trim()) };
        return { t: chunk };
    });
}

const escapeRegex = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const FREE_REGEX = {
    name: '[a-z]{2,}(?: [a-z]+){0,2}',
    number: `(?:\\d{1,3}|${NUMBERS.join('|')})`,
};

/** Un patrón de respuesta («there are {twenty|20} links», «my name is {*nombre}») como expresión regular. */
export function patternRegex(pattern) {
    const pieces = template(pattern).map((part) => {
        if (part.free) return FREE_REGEX[part.free];
        if (part.hole) return `(?:${part.hole.map((alt) => escapeRegex(normalize(alt))).join('|')})`;
        return escapeRegex(normalize(part.t));
    }).filter((piece) => piece !== '');

    return new RegExp(`^${pieces.join(' ')}$`);
}

/** El patrón con su primera opción en cada hueco: lo que se compara para el «¡Casi!». */
function patternExample(pattern) {
    return normalize(template(pattern).map((part) => part.t ?? (part.hole ? part.hole[0] : '')).join(' '));
}

/** Una respuesta escrita contra sus opciones: 'ok', 'almost' (a una letra) o 'bad'. */
export function judge(value, accepted) {
    const v = normalize(value);
    if (v === '') return 'bad';
    if (accepted.some((a) => normalize(a) === v)) return 'ok';
    return accepted.some((a) => levenshtein(normalize(a), v) <= 1) ? 'almost' : 'bad';
}

/** Una respuesta libre contra sus patrones. */
export function judgePattern(value, patterns) {
    const v = normalize(value);
    if (v === '') return 'bad';
    if (patterns.some((p) => patternRegex(p).test(v))) return 'ok';
    return patterns.some((p) => !p.includes('{*') && levenshtein(patternExample(p), v) <= 2) ? 'almost' : 'bad';
}

/** El dictado, palabra por palabra: cuáles ya están bien. */
export function compareWords(expected, written) {
    const want = normalize(expected).split(' ');
    const got = normalize(written).split(' ').filter(Boolean);
    return want.map((word, i) => ({ word, ok: got[i] === word }));
}

/** El peor resultado de varios: un 'bad' manda sobre un 'almost'. */
const worstOf = (verdicts) => (verdicts.includes('bad') ? 'bad' : verdicts.includes('almost') ? 'almost' : 'ok');

const shuffle = (list) => {
    const copy = [...list];
    for (let i = copy.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [copy[i], copy[j]] = [copy[j], copy[i]];
    }
    return copy;
};

/** Mezcla sin dejarlo igual (si se puede). */
const scramble = (list) => {
    if (list.length < 2) return [...list];
    for (let tries = 0; tries < 10; tries++) {
        const mixed = shuffle(list);
        if (mixed.some((x, i) => x !== list[i])) return mixed;
    }
    return [...list].reverse();
};

// ---------- Voz ----------

const browser = typeof window !== 'undefined';
let voices = [];
const loadVoices = () => { voices = window.speechSynthesis?.getVoices() ?? []; };
if (browser && 'speechSynthesis' in window) {
    loadVoices();
    window.speechSynthesis.addEventListener?.('voiceschanged', loadVoices);
}

function pickVoice(lang) {
    const base = lang.slice(0, 2);
    const preferred = lang === 'es' ? ['es-AR', 'es-US', 'es-MX', 'es-ES'] : ['en-US', 'en-GB'];
    for (const code of preferred) {
        const voice = voices.find((v) => v.lang === code && /google|natural|microsoft/i.test(v.name)) ?? voices.find((v) => v.lang === code);
        if (voice) return voice;
    }
    return voices.find((v) => v.lang?.startsWith(base)) ?? null;
}

export function speak(text, { lang = 'en', rate = 0.9 } = {}) {
    if (!browser || !('speechSynthesis' in window) || !text) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(String(text).replace(/[{}*]/g, ''));
    utterance.lang = lang === 'es' ? 'es-AR' : 'en-US';
    utterance.rate = rate;
    const voice = pickVoice(lang);
    if (voice) utterance.voice = voice;
    window.speechSynthesis.speak(utterance);
}

// ---------- «Decilo en voz alta» (INGLES.md § 4 bis) ----------

const SAME_SOUND = [['red', 'read'], ['two', 'too', 'to', '2'], ['blue', 'blew'], ['four', 'for', '4'], ['eight', 'ate', '8'],
    ['one', 'won', '1'], ['hi', 'high'], ['i', 'eye'], ['see', 'sea'], ['write', 'right'], ['no', 'know'], ['three', '3'],
    ['five', '5'], ['six', '6'], ['seven', '7'], ['nine', '9'], ['ten', '10'], ['iris', 'irish'], ['teo', 'theo'], ['lead', 'led']];
const CANON = Object.fromEntries(SAME_SOUND.flatMap((group) => group.map((w) => [w, group[0]])));
const spokenWords = (s) => normalize(s).split(' ').filter(Boolean).map((w) => CANON[w] ?? w);

/** Lo que entendió el reconocedor (con sus alternativas) contra la frase: 'ok', 'almost' o 'bad'. */
export function judgeSpoken(target, alternatives) {
    const hasFree = target.includes('{*');
    let best = 'bad';
    for (const alt of alternatives) {
        if (hasFree) {
            if (patternRegex(target).test(spokenWords(alt).join(' '))) return 'ok';
            continue;
        }
        const want = spokenWords(target);
        const heard = spokenWords(alt);
        if (want.length === 1 ? heard.includes(want[0]) : levenshtein(want, heard) === 0) return 'ok';
        if (want.length > 1 && levenshtein(want, heard) <= Math.max(1, Math.floor(want.length / 4))) best = 'almost';
    }
    return best;
}

const Recognition = browser ? (window.SpeechRecognition || window.webkitSpeechRecognition) : null;
// El reconocimiento en curso queda referenciado acá: si nadie lo guarda, Chrome puede descartarlo mientras escucha
// y no llega ningún resultado.
let activeRecognition = null;
export const canListen = () => Boolean(Recognition) && window.isSecureContext;

// ---------- El componente ----------

export function englishStep(config) {
    const exercise = config.exercise;

    return {
        exercise,
        type: exercise.type,
        tokens: String(config.story ?? '').split(/(\s+)/).filter((t) => t !== '').map((t) => ({ text: t, word: /[A-Za-z]/.test(t) })),
        showSpanish: false,
        slow: false,
        feedback: null,
        passed: config.done,
        sending: false,
        result: null,
        tries: 0,

        // escuchar
        round: 0,
        // completar / escribir / responder / transformar: un valor por hueco o por ítem
        answers: [],
        marks: [],
        selectedHole: null,
        usedBank: [],
        // ordenar y letras
        pool: [],
        built: [],
        // dictado
        dictationText: '',
        dictationMarks: [],
        // hablar
        listening: false,
        spoken: null,
        star: false,
        spokenXp: 0,

        init() {
            this.reset();
        },

        reset() {
            this.feedback = null;
            this.round = 0;
            this.selectedHole = null;
            this.usedBank = [];
            this.dictationText = '';
            this.dictationMarks = [];
            if (['fill', 'write'].includes(this.type)) {
                this.answers = exercise.items.map((item) => item.parts.map(() => ''));
                this.marks = exercise.items.map((item) => item.parts.map(() => null));
            } else if (['answer', 'transform'].includes(this.type)) {
                this.answers = exercise.items.map(() => '');
                this.marks = exercise.items.map(() => null);
            } else if (this.type === 'order') {
                this.loadOrder();
            } else if (this.type === 'letters') {
                this.loadLetters();
            }
        },

        // ----- lectura y voz -----
        say(text, lang = 'en') {
            speak(text, { lang, rate: this.slow ? 0.6 : 0.9 });
        },
        sayStory() {
            this.say(config.story);
        },
        saySpanish() {
            this.say(config.translation, 'es');
        },
        sayWord(token) {
            if (token.word) this.say(token.text.replace(/[^A-Za-z'’-]/g, ''));
        },

        // ----- escuchar -----
        get currentListen() {
            return exercise.items[this.round] ?? null;
        },
        playRound() {
            if (this.currentListen) this.say(this.currentListen.say);
        },
        pickOption(option) {
            const item = this.currentListen;
            if (!item) return;
            if (normalize(option) === normalize(item.answer)) {
                this.feedback = { kind: 'ok', text: '¡Bien!' };
                this.round++;
                if (this.round >= exercise.items.length) this.pass();
                else setTimeout(() => { this.feedback = null; this.playRound(); }, 700);
            } else {
                this.fail('bad');
            }
        },

        // ----- completar (con banco) -----
        get bankChips() {
            return exercise.bank.map((word, index) => ({ word, index, used: !exercise.reuse && this.usedBank.includes(index) }));
        },
        selectHole(item, part) {
            if (this.answers[item][part] !== '') {
                // Tocar un hueco lleno lo vacía y devuelve la ficha.
                const index = this.usedBank.find((i) => exercise.bank[i] === this.answers[item][part]);
                if (index !== undefined) this.usedBank = this.usedBank.filter((i) => i !== index);
                this.answers[item][part] = '';
                this.marks[item][part] = null;
            }
            this.selectedHole = [item, part];
        },
        nextEmptyHole() {
            for (let i = 0; i < exercise.items.length; i++) {
                for (let p = 0; p < exercise.items[i].parts.length; p++) {
                    if (exercise.items[i].parts[p].hole && this.answers[i][p] === '') return [i, p];
                }
            }
            return null;
        },
        placeChip(chip, target = null) {
            if (chip.used) return;
            const hole = target ?? (this.selectedHole && this.answers[this.selectedHole[0]][this.selectedHole[1]] === '' ? this.selectedHole : this.nextEmptyHole());
            if (!hole) return;
            const [item, part] = hole;
            if (this.answers[item][part] !== '') this.selectHole(item, part);
            this.answers[item][part] = chip.word;
            this.marks[item][part] = null;
            if (!exercise.reuse) this.usedBank.push(chip.index);
            this.selectedHole = this.nextEmptyHole();
        },
        dragChip(event, chip) {
            event.dataTransfer.setData('text/plain', String(chip.index));
        },
        dropChip(event, item, part) {
            const chip = this.bankChips[Number(event.dataTransfer.getData('text/plain'))];
            if (chip) this.placeChip(chip, [item, part]);
        },

        // ----- completar y escribir: comprobar -----
        checkHoles() {
            const verdicts = [];
            exercise.items.forEach((item, i) => item.parts.forEach((part, p) => {
                if (!part.hole && !part.free) return;
                const verdict = part.free
                    ? (new RegExp(`^${FREE_REGEX[part.free]}$`).test(normalize(this.answers[i][p])) ? 'ok' : 'bad')
                    : judge(this.answers[i][p], part.hole);
                this.marks[i][p] = verdict;
                verdicts.push(verdict);
            }));
            const worst = worstOf(verdicts);
            worst === 'ok' ? this.pass() : this.fail(worst);
        },

        // ----- ordenar -----
        loadOrder() {
            const words = exercise.items[0].answer.split(/\s+/);
            this.pool = scramble(words.map((word, index) => ({ word, index })));
            this.built = [];
        },
        // ----- letras: una palabra por vez -----
        loadLetters() {
            const item = exercise.items[this.round];
            if (!item) return;
            const letters = [...item.word, ...item.extra].map((letter, index) => ({ word: letter, index }));
            this.pool = scramble(letters);
            this.built = [];
        },
        take(tile) {
            this.pool = this.pool.filter((t) => t !== tile);
            this.built.push(tile);
            this.feedback = null;
        },
        giveBack(tile) {
            this.built = this.built.filter((t) => t !== tile);
            this.pool.push(tile);
        },
        get builtText() {
            return this.type === 'letters' ? this.built.map((t) => t.word).join('') : this.built.map((t) => t.word).join(' ');
        },
        checkOrder() {
            normalize(this.builtText) === normalize(exercise.items[0].answer) ? this.pass() : this.fail('bad', 'ogre');
        },
        checkLetters() {
            const item = exercise.items[this.round];
            const verdict = judge(this.builtText, [item.word]);
            if (verdict !== 'ok') return this.fail(verdict);
            this.say(item.word);
            this.round++;
            if (this.round >= exercise.items.length) return this.pass();
            this.feedback = { kind: 'ok', text: '¡Bien! Ahora la siguiente.' };
            this.loadLetters();
        },

        // ----- dictado -----
        checkDictation() {
            this.dictationMarks = compareWords(exercise.items[0].say, this.dictationText);
            const wrong = this.dictationMarks.filter((m) => !m.ok).length;
            if (wrong === 0) return this.pass();
            this.fail(wrong === 1 ? 'almost' : 'bad');
        },

        // ----- responder y transformar -----
        checkFree() {
            this.marks = exercise.items.map((item, i) => judgePattern(this.answers[i], item.answers));
            const worst = worstOf(this.marks);
            worst === 'ok' ? this.pass() : this.fail(worst);
        },

        // ----- resultado -----
        fail(kind, creature = null) {
            this.tries++;
            const who = kind === 'almost' ? 'slime' : (creature ?? config.creature ?? 'skeleton');
            this.feedback = {
                kind,
                creature: who,
                text: kind === 'almost' ? '¡Casi! Te falta o te sobra una letra.' : (CREATURES[who] ?? 'Todavía no. Probá de nuevo.'),
            };
        },

        async pass() {
            this.feedback = { kind: 'ok', text: '¡Muy bien!' };
            if (this.passed || this.sending) return;
            this.sending = true;
            const result = await this.$wire.completeStep(config.stepId, PASSED, '');
            this.sending = false;
            this.result = result;
            if (result.ok) this.passed = true;
            else this.feedback = { kind: 'bad', text: result.error };
        },

        // ----- hablar (opcional, nunca traba) -----
        canListen: canListen(),
        listen() {
            if (!Recognition || this.listening || !exercise.speak) return;
            window.speechSynthesis?.cancel();
            const recognition = new Recognition();
            activeRecognition = recognition;
            recognition.lang = 'en-US';
            recognition.interimResults = false;
            recognition.maxAlternatives = 5;
            this.listening = true;
            this.spoken = null;
            let echo = null;
            // Siempre hay un resultado al terminar: bien, casi, mal o «no te escuché» (nunca queda en blanco).
            recognition.onresult = (event) => {
                const alternatives = Array.from(event.results?.[0] ?? []).map((a) => String(a.transcript ?? '').trim()).filter(Boolean);
                if (alternatives.length === 0) return;
                const verdict = judgeSpoken(exercise.speak, alternatives);
                this.spoken = { verdict, heard: alternatives[0] };
                if (verdict === 'ok') {
                    this.star = true;
                    // La XP de «hablar» se da una sola vez por micro-misión (StepCompleter::speak).
                    this.$wire?.speakStep(config.stepId).then((result) => {
                        if (result?.ok && result.xp > 0) this.spokenXp = result.xp;
                    }).catch(() => {});
                    echo = exercise.speak.includes('{*') ? alternatives[0] : exercise.speak;
                }
            };
            recognition.onnomatch = () => {
                this.spoken = { verdict: 'bad', heard: '' };
            };
            recognition.onerror = (event) => {
                const messages = {
                    'not-allowed': 'El navegador no dio permiso para el micrófono.',
                    'audio-capture': 'No encuentro el micrófono. ¿Está conectado?',
                    network: 'El reconocimiento de voz necesita internet.',
                };
                this.spoken = { verdict: 'error', heard: messages[event.error] ?? 'No te escuché. Tocá «Decilo» y hablá enseguida.' };
            };
            recognition.onend = () => {
                activeRecognition = null;
                this.listening = false;
                this.spoken ??= { verdict: 'error', heard: 'No te escuché. Tocá «Decilo» y hablá enseguida.' };
                // Eco repite la frase recién con el micrófono cerrado, para que no se escuche a sí mismo.
                if (echo) this.say(echo);
            };
            try {
                recognition.start();
            } catch (e) {
                this.listening = false;
                this.spoken = { verdict: 'error', heard: 'No se pudo abrir el micrófono. Probá de nuevo.' };
            }
        },
    };
}
