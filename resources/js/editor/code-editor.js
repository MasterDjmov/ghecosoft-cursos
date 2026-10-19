// Editor de código (CodeMirror 6) con el tema "DevLevel Obsidian".
// Se carga con import dinámico solo donde hay un editor.

import { EditorView, basicSetup } from 'codemirror';
import { EditorState, StateEffect, StateField } from '@codemirror/state';
import { keymap, Decoration } from '@codemirror/view';
import { indentWithTab } from '@codemirror/commands';
import { HighlightStyle, syntaxHighlighting, indentUnit, StreamLanguage } from '@codemirror/language';
import { python } from '@codemirror/lang-python';
import { cpp } from '@codemirror/lang-cpp';
import { java } from '@codemirror/lang-java';
import { php } from '@codemirror/lang-php';
import { html } from '@codemirror/lang-html';
import { sql } from '@codemirror/lang-sql';
import { tags as t } from '@lezer/highlight';

const theme = EditorView.theme(
    {
        '&': { backgroundColor: '#060e20', color: '#e2e8f0', fontSize: '14px', borderRadius: '0.5rem', border: '1px solid #334155' },
        '&.cm-focused': { outline: '2px solid #22d3ee', outlineOffset: '2px' },
        '.cm-scroller': { fontFamily: '"JetBrains Mono", ui-monospace, monospace', lineHeight: '1.6' },
        '.cm-content': { caretColor: '#22d3ee', padding: '10px 0' },
        '.cm-cursor': { borderLeftColor: '#22d3ee' },
        '.cm-gutters': { backgroundColor: '#060e20', color: '#475569', border: 'none', borderRadius: '0.5rem 0 0 0.5rem' },
        '.cm-activeLine': { backgroundColor: 'rgba(34,211,238,0.05)' },
        '.cm-activeLineGutter': { backgroundColor: 'transparent', color: '#94a3b8' },
        '&.cm-focused .cm-selectionBackground, .cm-selectionBackground, ::selection': { backgroundColor: 'rgba(139,92,246,0.35) !important' },
        '.cm-matchingBracket': { backgroundColor: 'rgba(34,211,238,0.2)', outline: 'none' },
        '.cm-tooltip': { backgroundColor: '#131b2e', border: '1px solid #334155' },
        '.cm-run-line': { backgroundColor: 'rgba(250,204,21,0.18)', boxShadow: 'inset 3px 0 0 #facc15' },
        '.cm-tooltip-autocomplete > ul > li[aria-selected]': { backgroundColor: '#1d263d', color: '#22d3ee' },
    },
    { dark: true },
);

const highlight = HighlightStyle.define([
    { tag: [t.keyword, t.controlKeyword, t.definitionKeyword, t.operatorKeyword], color: '#a855f7' },
    { tag: [t.string, t.special(t.string)], color: '#34d399' },
    { tag: [t.number, t.bool, t.null], color: '#f59e0b' },
    { tag: t.comment, color: '#64748b', fontStyle: 'italic' },
    { tag: [t.function(t.variableName), t.function(t.propertyName)], color: '#22d3ee' },
    { tag: [t.definition(t.variableName), t.className], color: '#60a5fa' },
    { tag: [t.standard(t.variableName), t.self], color: '#f472b6' },
    { tag: t.operator, color: '#94a3b8' },
]);

// Ensamblador 8086 (D110): órdenes, registros, directivas, números, textos y comentarios.
const ASM_REGISTERS = /^(ax|bx|cx|dx|si|di|bp|sp|al|ah|bl|bh|cl|ch|dl|dh|cs|ds|ss|es|ip)\b/i;
const ASM_KEYWORDS = /^(proc|endp|macro|endm|local|end|equ|db|dw|dup|offset|ptr|byte|word|near|short)\b/i;
const asm8086 = StreamLanguage.define({
    name: 'asm8086',
    startState: () => ({ start: true }),
    token(stream, state) {
        if (stream.sol()) state.start = true;
        if (stream.eatSpace()) return null;
        if (stream.match(/^;.*/)) return 'comment';
        if (stream.match(/^'(?:[^']|'')*'?/) || stream.match(/^"(?:[^"]|"")*"?/)) return 'string';
        if (stream.match(/^\.[a-z0-9]+/i)) return 'keyword';
        if (stream.match(/^[0-9][0-9a-f]*[hbqod]?\b/i)) return 'number';
        if (stream.match(ASM_REGISTERS)) return 'variableName.standard';
        if (stream.match(ASM_KEYWORDS)) return 'keyword';
        if (stream.match(/^[a-z_@?][a-z0-9_@?]*:/i)) { state.start = false; return 'variableName.definition'; }
        if (stream.match(/^[a-z_@?][a-z0-9_@?]*/i)) {
            const first = state.start;
            state.start = false;
            return first ? 'function' : 'variableName';
        }
        stream.next();
        return 'operator';
    },
    languageData: { commentTokens: { line: ';' } },
});

// C, C++ y Arduino comparten resaltado; los demás lenguajes se ven sin colores por ahora.
const LANGUAGES = { python: () => python(), c: () => cpp(), cpp: () => cpp(), arduino: () => cpp(), java: () => java(), php: () => php(), html: () => html(), sql: () => sql(), asm: () => asm8086 };

// La línea que se ejecuta ahora (el paso a paso del tablero del Gólem, D110).
const setActiveLine = StateEffect.define();
const activeLineMark = Decoration.line({ class: 'cm-run-line' });
const activeLineField = StateField.define({
    create: () => Decoration.none,
    update(deco, tr) {
        for (const e of tr.effects) {
            if (e.is(setActiveLine)) {
                if (e.value === null || e.value < 1 || e.value > tr.state.doc.lines) return Decoration.none;
                return Decoration.set([activeLineMark.range(tr.state.doc.line(e.value).from)]);
            }
        }
        return deco.map(tr.changes);
    },
    provide: (f) => EditorView.decorations.from(f),
});

/**
 * @param {HTMLElement} parent
 * @param {{doc: string, language?: string, readOnly?: boolean, onChange?: (code: string) => void, onRun?: () => void}} options
 */
export function createEditor(parent, { doc, language = 'python', readOnly = false, onChange, onRun }) {
    const extensions = [
        basicSetup,
        theme,
        syntaxHighlighting(highlight),
        indentUnit.of('    '),
        EditorState.tabSize.of(4),
        keymap.of([indentWithTab, { key: 'Mod-Enter', run: () => (onRun?.(), true) }]),
        EditorView.updateListener.of((update) => update.docChanged && onChange?.(update.state.doc.toString())),
        EditorView.contentAttributes.of({ 'aria-label': 'Editor de código', spellcheck: 'false' }),
        activeLineField,
    ];
    if (LANGUAGES[language]) extensions.push(LANGUAGES[language]());
    if (readOnly) extensions.push(EditorState.readOnly.of(true), EditorView.editable.of(false));

    const view = new EditorView({ doc, extensions, parent });

    return {
        view,
        setDoc(text) {
            view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: text } });
        },
        /** Marca la línea que se ejecuta (null la saca) y la trae a la vista. */
        markLine(line) {
            const effects = [setActiveLine.of(line)];
            if (line && line <= view.state.doc.lines) effects.push(EditorView.scrollIntoView(view.state.doc.line(line).from, { y: 'nearest' }));
            view.dispatch({ effects });
        },
        destroy() {
            view.destroy();
        },
    };
}
