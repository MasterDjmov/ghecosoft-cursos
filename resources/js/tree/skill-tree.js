// Árbol de habilidades en canvas con force-graph (ARBOL-HABILIDADES.md § 6–8).
// Lo usan el editor del docente y (en la Fase 3) el árbol del alumno: los datos
// traen el estado de cada nodo y hoja; el dibujo es el mismo.

import ForceGraph from 'force-graph';
import { ICONS } from './icons.js';
import { layoutTree, leafPositions } from './layout.js';

const COLORS = {
    root: '#22d3ee',
    topic: '#3b82f6',
    boss: '#ef4444',
    extra: '#a855f7',
    locked: '#334155',
    required: '#10b981',
    optional: '#8b5cf6',
    approved: '#10b981',
    submitted: '#f59e0b',
    redo: '#f87171',
    pending: '#475569',
};

const RADIUS = { root: 20, topic: 10, boss: 13, extra: 9, practice: 6 };

// Desde qué zoom se ven los nombres de las hojas (como en el mapa escolar).
const LEAF_LABEL_ZOOM = 2.2;

const pathCache = new Map();

function drawIcon(ctx, name, x, y, size, color = '#ffffff') {
    const icon = ICONS[name];
    if (!icon) return;
    if (!pathCache.has(name)) pathCache.set(name, icon.map((part) => new Path2D(part.d)));

    ctx.save();
    ctx.translate(x - size / 2, y - size / 2);
    ctx.scale(size / 24, size / 24);
    ctx.fillStyle = color;
    pathCache.get(name).forEach((path, i) => ctx.fill(path, icon[i].rule));
    ctx.restore();
}

function escapeHtml(text) {
    return String(text).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
}

function drawLabel(ctx, text, x, y, scale, { small = false, dim = false } = {}) {
    const fontSize = (small ? 10 : 12) / scale;
    ctx.font = `${small ? '500' : '600'} ${fontSize}px Inter, sans-serif`;
    const width = ctx.measureText(text).width + fontSize * 0.9;
    const height = fontSize * 1.65;

    ctx.fillStyle = 'rgba(5,7,13,0.85)';
    ctx.fillRect(x - width / 2, y - height / 2, width, height);
    ctx.strokeStyle = 'rgba(148,163,184,0.35)';
    ctx.lineWidth = 1 / scale;
    ctx.strokeRect(x - width / 2, y - height / 2, width, height);

    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillStyle = dim ? '#94a3b8' : '#e2e8f0';
    ctx.fillText(text, x, y);
}

/** Color y estilo de un nodo del árbol según su tipo y su estado. */
function nodeStyle(node) {
    const base = COLORS[node.type] ?? COLORS.topic;

    switch (node.state) {
        case 'locked':
            return { fill: COLORS.locked, alpha: 0.75, dashed: false, icon: 'lock' };
        case 'available':
            return { fill: '#0b1326', stroke: base, alpha: 1, dashed: true, icon: null };
        case 'draft':
            return { fill: base, alpha: 0.4, dashed: true, icon: null };
        default: // unlocked, completed, admin
            return { fill: base, alpha: 1, dashed: false, icon: null };
    }
}

function buildGraph(data) {
    const positions = layoutTree(data);
    const nodes = [];
    const links = [];

    for (const node of data.nodes) {
        const position = positions.get(node.id) ?? { x: 0, y: 0, angle: 0 };
        nodes.push({ ...node, kind: 'node', id: `n${node.id}`, key: node.id, fx: position.x, fy: position.y, angle: position.angle });

        if (node.parent_id) {
            links.push({ source: `n${node.parent_id}`, target: `n${node.id}`, kind: 'trunk', state: node.state });
        }

        const practices = data.practices.filter((practice) => practice.node_id === node.id);
        leafPositions(position, practices.length).forEach((leaf, j) => {
            const practice = practices[j];
            nodes.push({ ...practice, kind: 'practice', id: `p${practice.id}`, key: practice.id, fx: leaf.x, fy: leaf.y, parentKey: `n${node.id}` });
            links.push({ source: `n${node.id}`, target: `p${practice.id}`, kind: 'leaf', status: practice.status, required: practice.required });
        });
    }

    return { nodes, links };
}

function practiceColor(practice) {
    if (practice.status && practice.status !== 'admin') return COLORS[practice.status] ?? COLORS.pending;
    return practice.required ? COLORS.required : COLORS.optional;
}

/**
 * Monta el árbol en `element`.
 * options: { editable, onNodeClick(node), onPracticeClick(practice), onNodeMoved(id, x, y) }
 */
export function mountSkillTree(element, data, options = {}) {
    const logo = new Image();
    let logoReady = false;
    if (data.course.logo) {
        logo.onload = () => (logoReady = true);
        logo.src = data.course.logo;
    }

    const graphData = buildGraph(data);

    const graph = new ForceGraph(element)
        .width(element.clientWidth)
        .height(element.clientHeight)
        .backgroundColor('rgba(0,0,0,0)')
        .graphData(graphData)
        .d3Force('charge', null)
        .d3Force('link', null)
        .d3Force('center', null)
        .cooldownTicks(0)
        .autoPauseRedraw(false)
        .enableNodeDrag(Boolean(options.editable))
        .nodeLabel((node) => escapeHtml(node.tooltip ?? node.title))
        .linkColor((link) => {
            if (link.kind === 'trunk') {
                return ['locked', 'available', 'draft'].includes(link.state) ? 'rgba(100,116,139,0.28)' : 'rgba(100,116,139,0.6)';
            }
            const color = link.status && link.status !== 'admin' ? COLORS[link.status] : link.required ? COLORS.required : COLORS.optional;
            return `${color}b3`;
        })
        .linkWidth((link) => (link.kind === 'trunk' ? 1.6 : 1))
        .linkLineDash((link) => {
            if (link.kind === 'trunk') return link.state === 'available' ? [4, 3] : null;
            return link.status === 'approved' ? null : [2, 2];
        })
        // "Flujo activo": el camino por el que ya avanzó el alumno (en el admin, todo lo publicado).
        .linkDirectionalParticles((link) => (link.kind === 'trunk' && ['unlocked', 'completed', 'admin'].includes(link.state) ? 2 : 0))
        .linkDirectionalParticleWidth(2.4)
        .linkDirectionalParticleSpeed(0.006)
        .linkDirectionalParticleColor(() => '#a5f3fc')
        .nodeCanvasObjectMode(() => 'replace')
        .nodeCanvasObject((node, ctx, scale) => {
            if (node.kind === 'practice') {
                const color = practiceColor(node);
                ctx.beginPath();
                ctx.arc(node.x, node.y, RADIUS.practice, 0, 2 * Math.PI);
                ctx.fillStyle = color;
                ctx.fill();
                drawIcon(ctx, node.mode, node.x, node.y, RADIUS.practice * 1.25);
                if (scale >= LEAF_LABEL_ZOOM) drawLabel(ctx, node.title, node.x, node.y + RADIUS.practice + 12 / scale, scale, { small: true });
                return;
            }

            const radius = RADIUS[node.type] ?? RADIUS.topic;
            const style = nodeStyle(node);

            // Pulso del centro, como el nodo de la provincia en el mapa escolar.
            if (node.type === 'root') {
                const t = (Date.now() % 2200) / 2200;
                ctx.beginPath();
                ctx.arc(node.x, node.y, radius + 3 + t * 14, 0, 2 * Math.PI);
                ctx.strokeStyle = `rgba(34,211,238,${(1 - t) * 0.55})`;
                ctx.lineWidth = 1.5;
                ctx.stroke();
            }

            // Anillo verde de "completado".
            if (node.state === 'completed') {
                ctx.beginPath();
                ctx.arc(node.x, node.y, radius + 3, 0, 2 * Math.PI);
                ctx.strokeStyle = COLORS.approved;
                ctx.lineWidth = 2;
                ctx.stroke();
            }

            ctx.save();
            ctx.globalAlpha = style.alpha;
            ctx.beginPath();
            ctx.arc(node.x, node.y, radius, 0, 2 * Math.PI);
            ctx.fillStyle = style.fill;
            ctx.fill();
            if (style.dashed || style.stroke) {
                ctx.setLineDash(style.dashed ? [3, 2] : []);
                ctx.strokeStyle = style.stroke ?? style.fill;
                ctx.lineWidth = 1.6;
                ctx.stroke();
                ctx.setLineDash([]);
            }

            if (node.type === 'root') {
                if (logoReady) {
                    ctx.save();
                    ctx.beginPath();
                    ctx.arc(node.x, node.y, radius - 1.5, 0, 2 * Math.PI);
                    ctx.clip();
                    ctx.drawImage(logo, node.x - radius, node.y - radius, radius * 2, radius * 2);
                    ctx.restore();
                } else {
                    ctx.fillStyle = '#0b1326';
                    ctx.font = `700 ${radius * 0.8}px "Space Grotesk", sans-serif`;
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.fillText(data.course.short, node.x, node.y + 1);
                }
            } else if (style.icon) {
                drawIcon(ctx, style.icon, node.x, node.y, radius, '#94a3b8');
            } else if (node.type === 'boss') {
                drawIcon(ctx, 'boss', node.x, node.y, radius * 1.2, node.state === 'available' ? COLORS.boss : '#ffffff');
            } else if (node.type === 'extra') {
                drawIcon(ctx, 'extra', node.x, node.y, radius * 1.2, node.state === 'available' ? COLORS.extra : '#ffffff');
            }
            ctx.restore();

            const label = node.state === 'available' && node.price_label ? `${node.title} · ${node.price_label}` : node.title;
            drawLabel(ctx, label, node.x, node.y + radius + 12 / scale + 4, scale, { dim: node.state === 'locked' });
        })
        .nodePointerAreaPaint((node, color, ctx) => {
            const radius = node.kind === 'practice' ? RADIUS.practice + 2 : (RADIUS[node.type] ?? RADIUS.topic) + 3;
            ctx.beginPath();
            ctx.arc(node.x, node.y, radius, 0, 2 * Math.PI);
            ctx.fillStyle = color;
            ctx.fill();
        })
        .onNodeClick((node) => {
            if (node.kind === 'practice') options.onPracticeClick?.(node);
            else options.onNodeClick?.(node);
        })
        .onNodeDrag((node, translate) => {
            if (node.kind === 'practice') return;
            // Las hojas acompañan a su nodo.
            for (const leaf of graphData.nodes) {
                if (leaf.parentKey === node.id) {
                    leaf.fx += translate.x;
                    leaf.fy += translate.y;
                }
            }
        })
        .onNodeDragEnd((node) => {
            node.fx = node.x;
            node.fy = node.y;
            if (node.kind === 'node') options.onNodeMoved?.(node.key, Math.round(node.x), Math.round(node.y));
        });

    const fit = () => graph.zoomToFit(500, 50);
    setTimeout(fit, 150);

    const observer = new ResizeObserver(() => graph.width(element.clientWidth).height(element.clientHeight));
    observer.observe(element);

    return {
        fit,
        focus(nodeKey) {
            const ids = new Set([`n${nodeKey}`]);
            graphData.nodes.forEach((n) => n.parentKey === `n${nodeKey}` && ids.add(n.id));
            graph.zoomToFit(500, 80, (n) => ids.has(n.id));
        },
        destroy() {
            observer.disconnect();
            graph._destructor?.();
            element.replaceChildren();
        },
    };
}
