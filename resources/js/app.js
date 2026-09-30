import './live-alerts.js';

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
    window.Alpine.data('universeMap', (data) => ({
        map: null,
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
            this.map = mountUniverse(this.$refs.canvas, data, { onSelect: (detail) => (this.selected = detail) });
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

// Editor + ejecutor: el ejemplo de un nodo, las hojas y la bandeja del docente.
// config: { code, stdin, expected, language, readOnly, runnable, tab, pyodideUrl, javaRunnerUrl, timeout }
document.addEventListener('alpine:init', () => {
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
        editor: null,

        async init() {
            if (!this.$refs.editor) return;
            const { createEditor } = await import('./editor/code-editor.js');
            this.$refs.editor.replaceChildren();
            this.editor = createEditor(this.$refs.editor, {
                doc: this.code,
                language: config.language ?? 'python',
                readOnly: Boolean(config.readOnly),
                onChange: (code) => (this.code = code),
                onRun: () => this.run(),
            });
        },

        destroy() {
            this.editor?.destroy();
        },

        async run() {
            if (this.running || config.runnable === false) return;
            this.running = true;
            this.tab = 'output';
            this.error = false;
            this.matches = null;
            this.output = '';

            let result;
            if (config.language === 'cpp' || config.language === 'c') {
                // C y C++: solo en la bandeja del docente (D66), compilando en el navegador.
                const { runCpp } = await import('./runners/cpp.js');
                result = await runCpp(this.code, {
                    stdin: this.stdin,
                    language: config.language,
                    timeout: config.timeout,
                    onStatus: (status) => (this.status = status),
                });
            } else if (config.language === 'java') {
                // Java: en la compu del docente, con scripts/JavaRunner.java abierto (D69).
                const { runJava } = await import('./runners/java.js');
                result = await runJava(this.code, { stdin: this.stdin, url: config.javaRunnerUrl, timeout: config.timeout, onStatus: (status) => (this.status = status) });
            } else if (config.language === 'php') {
                // PHP: solo en la bandeja del docente (D68), con PHP en WebAssembly.
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
                this.matches = result.output.trim() === config.expected.trim();
            }
            this.running = false;
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
