import './live-alerts.js';
import { describeDifference } from './runners/compare.js';
import { englishStep, speak } from './runners/english.js';

// Componente Alpine del árbol de habilidades. force-graph se descarga solo
// en las páginas que muestran el árbol (import dinámico).
document.addEventListener('alpine:init', () => {
    // Categorías de nombres que se pueden ocultar desde el panel de referencias (se recuerdan por navegador).
    const LABEL_GROUPS = ['trunk', 'boss', 'window', 'path', 'extra'];
    const readHidden = () => {
        try {
            return JSON.parse(localStorage.getItem('tree-hidden-labels') ?? '[]').filter((g) => LABEL_GROUPS.includes(g));
        } catch (e) {
            return [];
        }
    };

    // Crónicas en Inglés (D106): una micro-misión de inglés, y la voz para leer el episodio entero.
    window.Alpine.data('englishStep', englishStep);
    window.speakEnglish = speak;

    window.Alpine.data('skillTree', (data, options = {}) => ({
        tree: null,
        hiddenLabels: readHidden(),

        async init() {
            const { mountSkillTree } = await import('./tree/skill-tree.js');

            this.tree = mountSkillTree(this.$refs.canvas, data, {
                editable: Boolean(options.editable),
                hiddenLabels: this.hiddenLabels,
                // Nodo abierto: se entra. Cerrado: el componente muestra precio y motivos.
                onNodeClick: (node) => {
                    if (node.url) window.Livewire.navigate(node.url);
                    else if (!options.readOnly) this.$wire.selectNode?.(node.key);
                },
                onPracticeClick: (practice) => practice.url && window.Livewire.navigate(practice.url),
                onNodeMoved: (id, x, y) => this.$wire.moveNode(id, x, y),
            });
        },

        fit() {
            this.tree?.fit();
        },

        labelVisible(group) {
            return !this.hiddenLabels.includes(group);
        },

        toggleLabel(group) {
            this.hiddenLabels = this.labelVisible(group) ? [...this.hiddenLabels, group] : this.hiddenLabels.filter((g) => g !== group);
            this.tree?.setHiddenLabels(this.hiddenLabels);
            try {
                localStorage.setItem('tree-hidden-labels', JSON.stringify(this.hiddenLabels));
            } catch (e) {
                // Sin almacenamiento: vale solo para esta visita.
            }
        },

        destroy() {
            this.tree?.destroy();
        },
    }));
});

// Universo de cursos (D70, Admin → Universo): el mapa 3D se descarga solo en esa página.
document.addEventListener('alpine:init', () => {
    window.Alpine.data('universeMap', (data, options = {}) => ({
        map: null,
        // D81: el alumno mira y vota «Quiero aprender esto» (un voto por tema o curso que viene).
        votes: { ...(data.votes ?? {}) },
        myVotes: [...(data.myVotes ?? [])],
        voting: false,
        selected: null,
        query: '',
        notFound: false,
        dimensions: 3,
        courses: data.courses.filter((c) => c.nodes > 0 || c.upcoming).map((c) => c.id),
        // De entrada, solo las familias compartidas (las de cada lenguaje llenan el centro de temas comunes).
        families: data.families.filter((f) => f.scope === 'compartido').map((f) => f.key),
        missing: true,
        uses: true,
        colors: {},
        statusLabels: {},

        async init() {
            const { mountUniverse, familyColors, STATUS_LABELS } = await import('./universe/universe-map.js');
            this.colors = familyColors(data.families);
            this.statusLabels = STATUS_LABELS;
            this.map = mountUniverse(this.$refs.canvas, data, { onSelect: (detail) => (this.selected = detail), student: Boolean(options.student) });
            this.apply();
            setTimeout(() => this.map?.fit(), 2500);
            this.$watch('courses', () => this.apply());
            this.$watch('families', () => this.apply());
            this.$watch('missing', () => this.apply());
            this.$watch('uses', () => this.apply());
        },

        apply() {
            this.map?.setFilters({ courses: this.courses, families: this.families, missing: this.missing, uses: this.uses });
        },

        toggleScope(scope, on) {
            const keys = data.families.filter((f) => f.scope === scope).map((f) => f.key);
            this.families = on ? [...new Set([...this.families, ...keys])] : this.families.filter((k) => !keys.includes(k));
        },

        search() {
            this.notFound = this.query.trim() !== '' && !this.map?.search(this.query);
        },

        async vote(target) {
            if (this.voting) return;
            this.voting = true;
            try {
                const { voted, count } = await this.$wire.toggleVote(target);
                this.votes = { ...this.votes, [target]: count };
                this.myVotes = voted ? [...this.myVotes, target] : this.myVotes.filter((t) => t !== target);
                this.map?.setVotes(this.votes);
            } finally {
                this.voting = false;
            }
        },

        go(id) {
            this.map?.select(id);
        },

        toggleDimensions() {
            this.dimensions = this.dimensions === 3 ? 2 : 3;
            this.map?.dimensions(this.dimensions);
        },

        fit() {
            this.map?.fit();
        },

        destroy() {
            this.map?.destroy();
        },
    }));
});

// Corrección asistida (D73): las pruebas de una entrega, al abrirla, y «Probar pendientes» en la bandeja.
// config: { language, code, cases, pyodideUrl, javaRunnerUrl, timeout }
document.addEventListener('alpine:init', () => {
    window.Alpine.data('submissionCases', (config) => ({
        running: false,
        status: '',
        results: [],
        passed: 0,
        total: config.cases.length,
        unavailable: null,

        init() {
            this.run();
        },

        async run() {
            if (this.running) return;
            this.running = true;
            this.unavailable = null;
            const { runCases, diffLines } = await import('./runners/cases.js');
            const outcome = await runCases({ ...config, onStatus: (status) => (this.status = status) });
            this.results = outcome.results.map((r) => ({ ...r, lines: r.passed ? [] : diffLines(r.expected, r.output) }));
            this.passed = outcome.passed;
            this.unavailable = outcome.unavailable;
            this.status = '';
            this.running = false;
            // Si el ejecutor no estaba, no se guarda nada: no es que el alumno falló.
            if (!outcome.unavailable) this.$wire.saveCheck(outcome.passed, outcome.total);
        },
    }));

    // config: { ids, pyodideUrl, javaRunnerUrl, timeout }
    window.Alpine.data('inboxChecks', (config) => ({
        running: false,
        progress: '',
        problem: null,

        async run() {
            if (this.running) return;
            this.running = true;
            this.problem = null;
            const { runCases } = await import('./runners/cases.js');
            for (const [i, id] of config.ids.entries()) {
                this.progress = `Probando ${i + 1} de ${config.ids.length}…`;
                const data = await this.$wire.casesFor(id);
                if (!data.cases.length) continue;
                const outcome = await runCases({ ...config, language: data.language, code: data.code, cases: data.cases });
                if (outcome.unavailable) {
                    this.problem = outcome.unavailable;
                    continue;
                }
                await this.$wire.saveCheck(id, outcome.passed, outcome.total);
            }
            this.progress = '';
            this.running = false;
            this.$wire.$refresh();
        },
    }));
});

// Editor + ejecutor: el ejemplo de un nodo, las hojas y la bandeja del docente.
// config: { code, stdin, expected, language, readOnly, runnable, tab, pyodideUrl, javaRunnerUrl, javaHelpUrl, timeout }
document.addEventListener('alpine:init', () => {
    // Las sesiones del tablero del Gólem (D110) viven fuera de Alpine: una máquina de 1 MB no puede ser reactiva.
    const asmSessions = new Map();
    let asmCounter = 0;

    window.Alpine.data('codeRunner', (config) => ({
        code: config.code ?? '',
        original: config.code ?? '',
        stdin: config.stdin ?? '',
        tab: config.tab ?? 'output',
        output: null,
        status: '',
        error: false,
        running: false,
        copied: false,
        matches: null,
        mismatch: null,
        editor: null,
        // HTML y CSS (D76): la página dibujada en la caja aislada, el tamaño de pantalla y la pantalla completa.
        preview: '',
        device: 'mobile',
        fullscreen: false,
        renderTimer: null,
        // «Así tiene que quedar» (D77): las capturas de la página resuelta, para comparar en el mismo tamaño.
        references: config.references ?? {},
        showReference: false,
        // Ensamblador 8086 (D110): lo que dibuja el tablero, el error del ensamblador y el modo del paso a paso.
        asmId: ++asmCounter,
        asm: null,
        asmError: null,
        asmMode: 'idle',
        asmWaiting: null,
        asmKey: '',
        asmEnd: null,
        asmPanel: 'registers',
        asmContinuous: false,

        async init() {
            const isHtml = config.language === 'html' && config.runnable !== false;
            if (isHtml) this.run();
            if (!this.$refs.editor) return;
            const { createEditor } = await import('./editor/code-editor.js');
            this.$refs.editor.replaceChildren();
            this.editor = createEditor(this.$refs.editor, {
                doc: this.code,
                language: config.language ?? 'python',
                readOnly: Boolean(config.readOnly),
                onChange: (code) => {
                    this.code = code;
                    // La página se vuelve a dibujar sola mientras se escribe (con una pausa corta).
                    if (isHtml) {
                        clearTimeout(this.renderTimer);
                        this.renderTimer = setTimeout(() => this.run(), 400);
                    }
                },
                onRun: () => this.run(),
            });
        },

        destroy() {
            clearTimeout(this.renderTimer);
            this.editor?.destroy();
        },

        async run() {
            if (config.language === 'html') return this.renderHtml();
            if (config.language === 'asm') return this.asmRun();
            if (this.running || config.runnable === false) return;
            this.running = true;
            this.tab = 'output';
            this.error = false;
            this.matches = null;
            this.mismatch = null;
            this.output = '';

            let result;
            if (config.language === 'cpp' || config.language === 'c') {
                // C y C++, compilando en el navegador: también para el alumno (D98 C, D100 C++).
                const { runCpp } = await import('./runners/cpp.js');
                result = await runCpp(this.code, {
                    stdin: this.stdin,
                    language: config.language,
                    timeout: config.timeout,
                    onStatus: (status) => (this.status = status),
                });
            } else if (config.language === 'java') {
                // Java: en la compu de quien lo usa, con scripts/JavaRunner.java abierto (D69 docente, D85 alumno).
                const { runJava } = await import('./runners/java.js');
                result = await runJava(this.code, { stdin: this.stdin, url: config.javaRunnerUrl, helpUrl: config.javaHelpUrl, timeout: config.timeout, onStatus: (status) => (this.status = status) });
            } else if (config.language === 'sql') {
                // SQL: SQLite en WebAssembly, en el navegador (las micro-misiones de SQL de Java).
                const { runSql } = await import('./runners/sql.js');
                result = await runSql(this.code, { timeout: config.timeout, onStatus: (status) => (this.status = status) });
            } else if (config.language === 'php') {
                // PHP: PHP 8.3 en WebAssembly, en el navegador del docente (D68) y del alumno (D105).
                const { runPhp } = await import('./runners/php.js');
                result = await runPhp(this.code, { stdin: this.stdin, timeout: config.timeout, onStatus: (status) => (this.status = status) });
            } else {
                const { runPython, isPythonLoaded } = await import('./runners/python.js');
                this.status = isPythonLoaded() ? 'Ejecutando…' : 'Cargando Python (la primera vez tarda unos segundos)…';
                result = await runPython(this.code, {
                    stdin: this.stdin,
                    url: config.pyodideUrl,
                    timeout: config.timeout,
                    onReady: () => (this.status = 'Ejecutando…'),
                });
            }

            const separator = result.output && !result.output.endsWith('\n') ? '\n' : '';
            const compiler = result.diagnostics ? `── Compilador ──\n${result.diagnostics.trimEnd()}\n── Programa ──\n` : '';
            // Lo que el programa escribió en STDERR sin fallar (avisos de PHP, std::cerr) va al final.
            const notices = result.stderr?.trim() ? `${result.output && !result.output.endsWith('\n') ? '\n' : ''}── STDERR ──\n${result.stderr.trim()}` : '';
            this.output = (compiler + result.output + (result.error ? separator + result.error : notices)).replace(/\n+$/, '') || '(sin salida)';
            this.error = Boolean(result.error);
            this.status = result.error ? (result.timedOut ? 'Tiempo agotado' : 'Error') : `Listo en ${result.ms} ms`;
            if (!result.error && config.expected) {
                // Como el servidor (LocalCodeRunner::normalize); si no coincide, se dice dónde (sobre todo lo invisible).
                this.mismatch = describeDifference(config.expected, result.output);
                this.matches = this.mismatch === null;
            }
            this.running = false;
        },

        async renderHtml() {
            if (config.runnable === false) return;
            const { buildPreview } = await import('./runners/html.js');
            const result = await buildPreview(this.code);
            this.preview = result.html;
            this.error = Boolean(result.error);
            this.status = result.error ?? `Dibujada en ${result.ms} ms`;
            // Micro-misión de HTML (D102): el inspector lee el código sin ejecutarlo y su informe es «la salida».
            // Recién se compara cuando el alumno cambió algo, para no recibirlo con un «Todavía no».
            if (config.checks) {
                const { inspect } = await import('./runners/inspector.js');
                this.output = inspect(this.code, config.checks);
                if (config.expected && this.code !== this.original) {
                    this.mismatch = describeDifference(config.expected, this.output);
                    this.matches = this.mismatch === null;
                }
            }
        },

        // ---------------- Ensamblador 8086: el tablero del Gólem (D110)

        async asmBegin() {
            const { AsmSession } = await import('./runners/asm8086/session.js');
            const session = new AsmSession(this.code, { stdin: this.stdin, checks: config.checks ?? '' });
            asmSessions.set(this.asmId, session);
            this.matches = null;
            this.mismatch = null;
            this.error = false;
            this.output = null;
            this.asmEnd = null;
            this.asmWaiting = null;
            const problem = session.start();
            if (problem) {
                this.asmError = problem;
                this.asm = null;
                this.error = true;
                this.output = `Línea ${problem.line ?? '?'}: ${problem.message}\n(${problem.raw})`;
                this.status = 'El Gólem no entendió una orden';
                this.asmMode = 'idle';
                this.editor?.markLine(problem.line);
                return null;
            }
            this.asmError = null;
            this.asmRefresh();
            return session;
        },

        asmRefresh(mark = false) {
            const session = asmSessions.get(this.asmId);
            if (!session?.machine) return;
            this.asm = session.view();
            if (mark) this.editor?.markLine(this.asm.line);
        },

        async asmRun() {
            if (this.running) return;
            const session = this.asmMode === 'stepping' || this.asmMode === 'waiting' ? asmSessions.get(this.asmId) : await this.asmBegin();
            if (!session) return;
            this.running = true;
            this.asmContinuous = true;
            this.asmMode = 'running';
            this.status = 'El Gólem está trabajando…';
            this.editor?.markLine(null);
            const result = await session.runToEnd(() => this.asmRefresh());
            this.running = false;
            this.asmAfter(session, result, false);
        },

        async asmStep() {
            let session = asmSessions.get(this.asmId);
            if (!session || this.asmMode === 'idle' || this.asmMode === 'done') {
                session = await this.asmBegin();
                if (!session) return;
                this.asmMode = 'stepping';
                this.status = 'Paso a paso: mirá qué cambia con cada orden';
                this.editor?.markLine(session.currentLine());
                return;
            }
            if (this.asmMode === 'waiting') return;
            this.asmContinuous = false;
            const result = session.step();
            this.asmAfter(session, result, true);
        },

        asmAfter(session, result, stepping) {
            this.asmRefresh(stepping);
            if (result === 'input') {
                this.asmMode = 'waiting';
                this.asmWaiting = session.waiting;
                this.status = session.waiting === 'line' ? 'El Gólem espera que escribas una línea y Enter' : 'El Gólem espera una tecla';
                this.$nextTick(() => this.$refs.asmKey?.focus());
                return;
            }
            if (result === 'ok') {
                this.asmMode = 'stepping';
                return;
            }
            if (result === 'stopped') {
                this.asmMode = 'stepping';
                this.status = 'En pausa: seguí de a una orden o ejecutá hasta el final';
                this.editor?.markLine(session.currentLine());
                return;
            }
            this.asmFinish(session, result === 'loop');
        },

        async asmFinish(session, loop) {
            this.asmMode = 'done';
            this.editor?.markLine(null);
            const output = session.result();
            this.output = output || '(sin salida)';
            const end = loop ? 'El Gólem se quedó dando vueltas: el programa no terminó (¿un bucle sin salida?)' : session.endMessage();
            this.asmEnd = end;
            this.error = Boolean(end);
            this.status = end ? 'El Gólem se detuvo con un problema' : `Listo en ${session.machine.steps} órdenes`;
            if (!end && config.expected) {
                const { describeDifference } = await import('./runners/compare.js');
                this.mismatch = this.asmDifference(config.expected, output) ?? describeDifference(config.expected, output);
                this.matches = this.mismatch === null;
            }
        },

        /** Si lo que no coincide es el estado, se dice en criollo: «AX quedó en 0012h; tenía que ser 1234h». */
        asmDifference(expected, actual) {
            const header = '── Estado ──';
            if (!expected.includes(header) || !actual.includes(header)) return null;
            const want = expected.split(header)[1].trim().split('\n');
            const got = actual.split(header)[1].trim().split('\n');
            for (let i = 0; i < want.length; i++) {
                if (want[i] !== got[i]) {
                    const [name, value] = want[i].split(' = ');
                    const mine = (got[i] ?? '').split(' = ')[1] ?? '?';
                    return `${name} quedó en ${mine}; tenía que ser ${value}.`;
                }
            }
            return null;
        },

        asmSend() {
            const session = asmSessions.get(this.asmId);
            if (!session || this.asmMode !== 'waiting') return;
            const text = this.asmWaiting === 'line' ? `${this.asmKey}\n` : (this.asmKey || '\r').slice(0, 1);
            session.feed(text);
            this.asmKey = '';
            this.asmWaiting = null;
            // Si venía corriendo, sigue; si era paso a paso, la próxima orden ya tiene la tecla.
            if (this.asmContinuous) return this.asmRun();
            this.asmMode = 'stepping';
            this.asmStep();
        },

        asmStop() {
            const session = asmSessions.get(this.asmId);
            if (this.running) return session?.stop();
            asmSessions.delete(this.asmId);
            this.asm = null;
            this.asmMode = 'idle';
            this.asmWaiting = null;
            this.status = '';
            this.editor?.markLine(null);
        },

        asmGoto(address) {
            const session = asmSessions.get(this.asmId);
            if (!session) return;
            const n = parseInt(String(address).replace(/h$/i, ''), 16);
            session.memoryBase = Number.isNaN(n) ? null : n & 0xfff0;
            session.memoryManual = !Number.isNaN(n);
            this.asmRefresh();
        },

        async copy() {
            try {
                await navigator.clipboard.writeText(this.code);
                this.copied = true;
                setTimeout(() => (this.copied = false), 1500);
            } catch (e) {
                // Sin permiso de portapapeles: no pasa nada.
            }
        },

        restore() {
            this.code = this.original;
            this.editor?.setDoc(this.original);
        },
    }));
});
