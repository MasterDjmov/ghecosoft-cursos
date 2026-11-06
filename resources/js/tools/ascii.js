// La pantalla de la tabla de caracteres (D120): clic para copiar. Los datos están en ascii-data.js.
import { forms, FORM_LABELS, search, sectionsOf, TABLE_LABELS, TABLES, uPlus } from './ascii-data.js';
import { copyText, instanceStore } from './copy.js';

export function asciiTool(user) {
    const store = instanceStore(user, 'tabla-ascii');

    return {
        tab: 'ascii',
        copyAs: 'symbol',
        query: '',
        selected: null,
        copied: '',
        copiedKey: '',
        formLabels: FORM_LABELS,
        tableLabels: TABLE_LABELS,

        init() {
            const saved = store.load();
            if (TABLES[saved.tab]) this.tab = saved.tab;
            if (FORM_LABELS[saved.copyAs]) this.copyAs = saved.copyAs;
            ['tab', 'copyAs'].forEach((field) => this.$watch(field, () => store.save({ tab: this.tab, copyAs: this.copyAs })));
            this.$watch('tab', () => (this.selected = null));
        },

        get searching() {
            return this.query !== '';
        },

        get sections() {
            return this.searching
                ? sectionsOf(search(this.query).map((entry) => ({ ...entry, group: `${TABLE_LABELS[entry.table]} · ${entry.group}` })))
                : sectionsOf(TABLES[this.tab]);
        },

        /** Lo de abajo de cada casilla: Unicode va por su código; las demás, decimal y hexa. */
        lineOf(entry) {
            return entry.table === 'unicode' ? uPlus(entry.cp) : `0x${entry.code.toString(16).toUpperCase().padStart(2, '0')}`;
        },

        titleOf(entry) {
            const all = forms(entry);
            return [entry.name, `DEC ${all.dec}`, `HEX ${all.hex}`, `OCT ${all.oct}`, `BIN ${all.bin}`].filter(Boolean).join(' · ');
        },

        formsOf(entry) {
            const all = forms(entry);
            return Object.keys(FORM_LABELS).map((key) => ({ key, label: FORM_LABELS[key], value: all[key] }));
        },

        uPlus,

        async pick(entry) {
            this.selected = entry;
            await this.copy(forms(entry)[this.copyAs], entry.key);
        },

        async copy(text, key = '') {
            if (await copyText(text)) {
                this.copied = text;
                this.copiedKey = key;
                clearTimeout(this._copiedTimer);
                this._copiedTimer = setTimeout(() => {
                    this.copied = '';
                    this.copiedKey = '';
                }, 1500);
            }
        },
    };
}
