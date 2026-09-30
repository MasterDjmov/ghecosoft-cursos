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
                onNodeClick: (node) => (node.url ? window.Livewire.navigate(node.url) : this.$wire.selectNode?.(node.key)),
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

// Editor + ejecutor: el ejemplo de un nodo, las hojas y la bandeja del docente.
// config: { code, stdin, expected, language, readOnly, runnable, tab, pyodideUrl, timeout }
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

            const { runPython, isPythonLoaded } = await import('./runners/python.js');
            this.status = isPythonLoaded() ? 'Ejecutando…' : 'Cargando Python (la primera vez tarda unos segundos)…';

            const result = await runPython(this.code, {
                stdin: this.stdin,
                url: config.pyodideUrl,
                timeout: config.timeout,
                onReady: () => (this.status = 'Ejecutando…'),
            });

            const separator = result.output && !result.output.endsWith('\n') ? '\n' : '';
            this.output = (result.output + (result.error ? separator + result.error : '')).replace(/\n+$/, '') || '(sin salida)';
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
