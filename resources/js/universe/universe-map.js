// Mapa 3D del universo de cursos (D70, Admin → Universo). Cada curso es una galaxia (su centro y sus nodos,
// unidos como en su árbol) y los temas del catálogo (cursos/temas.md) son octaedros que atan los nodos que
// los enseñan (línea) o los usan (línea con partículas). Solo para mirar: no cambia nada.
import ForceGraph3D from '3d-force-graph';
import SpriteText from 'three-spritetext';
import * as THREE from 'three';
import { forceX, forceY, forceZ } from 'd3-force-3d';

const MISSING = '#475569';
const NEEDED = '#ef4444';

const escape = (text) => String(text ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
const normalize = (text) => String(text ?? '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();

export const STATUS_LABELS = {
    ok: 'Enseñado',
    repeated: 'Repetido entre cursos',
    needed: 'Falta y se usa',
    missing: 'Falta',
};

/** Colores de las familias (vienen de UniverseGraph: los mismos en el mapa y en el tablero). */
export function familyColors(families) {
    return Object.fromEntries(families.map((family) => [family.key, family.color]));
}

export function mountUniverse(element, data, { onSelect } = {}) {
    const courses = new Map(data.courses.map((course) => [course.id, course]));
    const colors = familyColors(data.families);
    const families = new Map(data.families.map((family) => [family.key, family]));
    const rawNodes = new Map(data.nodes.map((node) => [node.id, node]));

    // Centros de las galaxias en un círculo.
    const radius = 220 + 45 * data.courses.length;
    const centers = new Map(data.courses.map((course, i) => {
        const angle = (i / data.courses.length) * Math.PI * 2;
        return [course.id, { x: Math.cos(angle) * radius, y: Math.sin(angle) * radius, z: 0 }];
    }));

    const topicStatus = (topic) => {
        const taughtIn = new Set(topic.taught.map((id) => rawNodes.get(id)?.course_id));
        if (taughtIn.size === 0) return topic.used.length ? 'needed' : 'missing';
        return taughtIn.size > 1 && families.get(topic.family)?.scope === 'compartido' ? 'repeated' : 'ok';
    };

    // Todas las piezas se arman una vez; los filtros eligen cuáles se muestran (así conservan su lugar).
    const all = {
        courses: data.courses.map((course) => ({ id: `c${course.id}`, kind: 'course', course, color: course.color })),
        nodes: data.nodes.map((node) => ({ id: `n${node.id}`, kind: 'node', node, courseId: node.course_id, color: courses.get(node.course_id)?.color })),
        topics: data.topics.map((topic) => {
            const status = topicStatus(topic);
            return { id: `t${topic.key}`, kind: 'topic', topic, family: topic.family, status,
                color: status === 'missing' ? MISSING : status === 'needed' ? NEEDED : (colors[topic.family] ?? '#94a3b8') };
        }),
    };
    const byId = new Map([...all.courses, ...all.nodes, ...all.topics].map((item) => [item.id, item]));
    const topicCenter = (topic) => {
        const points = topic.taught.map((id) => centers.get(rawNodes.get(id)?.course_id)).filter(Boolean);
        if (!points.length) return { x: 0, y: 0, z: 0 };
        return { x: points.reduce((s, p) => s + p.x, 0) / points.length, y: points.reduce((s, p) => s + p.y, 0) / points.length, z: 0 };
    };
    const center = (item) => item.kind === 'topic' ? topicCenter(item.topic) : centers.get(item.kind === 'course' ? item.course.id : item.courseId) ?? { x: 0, y: 0, z: 0 };

    const allLinks = [];
    for (const node of data.nodes) {
        const course = courses.get(node.course_id);
        const parent = node.parent_id && rawNodes.has(node.parent_id) ? `n${node.parent_id}` : `c${node.course_id}`;
        allLinks.push({ source: parent, target: `n${node.id}`, kind: 'tree', color: course?.color });
        for (const key of node.topics) allLinks.push({ source: `n${node.id}`, target: `t${key}`, kind: 'teaches', color: colors[key.split('.')[0]] ?? '#94a3b8' });
        for (const key of node.uses) allLinks.push({ source: `n${node.id}`, target: `t${key}`, kind: 'uses', color: '#e2e8f0' });
    }

    let filters = { courses: new Set(data.courses.map((c) => c.id)), families: new Set(), missing: true, uses: true };
    let selected = null;

    const graph = new ForceGraph3D(element, { controlType: 'orbit' })
        .backgroundColor('#05070d')
        .showNavInfo(false)
        .nodeId('id')
        .nodeLabel((item) => tooltip(item))
        .nodeVal((item) => item.kind === 'node' ? ({ root: 8, boss: 4, extra: 1.2 }[item.node.type] ?? 2) : 1)
        .nodeColor((item) => item.color)
        .nodeOpacity(0.95)
        .nodeThreeObject((item) => item.kind === 'course' ? courseObject(item) : item.kind === 'topic' ? topicObject(item) : null)
        .linkColor((link) => link.color)
        .linkOpacity(0.28)
        .linkWidth((link) => isFocused(link) ? 1.6 : link.kind === 'tree' ? 0.7 : link.kind === 'teaches' ? 0.5 : 0.25)
        .linkDirectionalParticles((link) => link.kind === 'uses' ? 2 : 0)
        .linkDirectionalParticleWidth(1.4)
        .linkDirectionalParticleSpeed(0.004)
        .onNodeClick((item) => select(item.id))
        .onBackgroundClick(() => select(null));

    graph.d3Force('charge').strength(-45);
    graph.d3Force('link').distance((link) => link.kind === 'tree' ? 16 : link.kind === 'teaches' ? 70 : 110).strength((link) => link.kind === 'tree' ? 0.9 : 0.08);
    graph.d3Force('x', forceX((item) => center(item).x).strength((item) => item.kind === 'topic' ? 0.03 : 0.1));
    graph.d3Force('y', forceY((item) => center(item).y).strength((item) => item.kind === 'topic' ? 0.03 : 0.1));
    graph.d3Force('z', forceZ(0).strength(0.02));

    const resize = () => graph.width(element.clientWidth).height(element.clientHeight);
    const observer = new ResizeObserver(resize);
    observer.observe(element);
    resize();

    function courseObject(item) {
        const group = new THREE.Group();
        const sphere = new THREE.Mesh(new THREE.SphereGeometry(10, 24, 24),
            new THREE.MeshLambertMaterial({ color: item.color, transparent: item.course.upcoming, opacity: item.course.upcoming ? 0.3 : 1 }));
        group.add(sphere);
        const label = new SpriteText(item.course.title + (item.course.upcoming ? ' (próximamente)' : ''), 7, item.color);
        label.fontWeight = '600';
        label.position.set(0, 20, 0);
        group.add(label);
        return group;
    }

    function topicObject(item) {
        const group = new THREE.Group();
        const size = item.status === 'repeated' ? 6 : 4;
        const faded = item.status === 'missing';
        group.add(new THREE.Mesh(new THREE.OctahedronGeometry(size),
            new THREE.MeshLambertMaterial({ color: item.color, transparent: true, opacity: faded ? 0.3 : 0.95,
                emissive: item.status === 'repeated' ? item.color : '#000000', emissiveIntensity: 0.6 })));
        const label = new SpriteText(item.topic.title, 3, faded ? '#64748b' : item.color);
        label.position.set(0, -size - 4, 0);
        group.add(label);
        return group;
    }

    function tooltip(item) {
        if (item.kind === 'course') return `<b>${escape(item.course.title)}</b><br>${item.course.nodes} nodos`;
        if (item.kind === 'node') {
            const course = courses.get(item.courseId);
            return `<b>${escape(item.node.title)}</b><br>${escape(course?.title)} · ${escape(item.node.code)}`;
        }
        return `<b>${escape(item.topic.title)}</b> <small>${escape(item.topic.key)}</small><br>${escape(STATUS_LABELS[item.status])}`;
    }

    const isFocused = (link) => selected && (endId(link.source) === selected || endId(link.target) === selected);
    const endId = (end) => typeof end === 'object' ? end.id : end;

    function visibleTopic(item) {
        // Los temas sueltos (fuera del catálogo) se muestran siempre, para que se vean y se corrijan.
        if (!filters.families.has(item.family) && !item.topic.loose) return false;
        if (item.status === 'missing' || item.status === 'needed') return filters.missing;
        return item.topic.taught.some((id) => filters.courses.has(rawNodes.get(id)?.course_id))
            || (filters.uses && item.topic.used.some((id) => filters.courses.has(rawNodes.get(id)?.course_id)));
    }

    function apply() {
        const nodes = [
            ...all.courses.filter((item) => filters.courses.has(item.course.id)),
            ...all.nodes.filter((item) => filters.courses.has(item.courseId)),
            ...all.topics.filter(visibleTopic),
        ];
        const shown = new Set(nodes.map((item) => item.id));
        const links = allLinks.filter((link) => shown.has(endId(link.source)) && shown.has(endId(link.target)) && (link.kind !== 'uses' || filters.uses));
        graph.graphData({ nodes, links });
    }

    function details(id) {
        const item = byId.get(id);
        if (!item) return null;
        const nodeInfo = (nodeId) => {
            const node = rawNodes.get(nodeId);
            const course = courses.get(node?.course_id);
            return node && { id: `n${node.id}`, title: node.title, code: node.code, course: course?.title, color: course?.color, url: node.url };
        };
        const topicInfo = (key) => {
            const topic = byId.get(`t${key}`);
            return { id: `t${key}`, key, title: topic?.topic.title ?? key, color: topic?.color ?? '#94a3b8', status: topic?.status };
        };
        if (item.kind === 'course') {
            return { kind: 'course', title: item.course.title, color: item.color, nodes: item.course.nodes, upcoming: item.course.upcoming, url: item.course.url };
        }
        if (item.kind === 'node') {
            const node = item.node;
            const course = courses.get(node.course_id);
            return {
                kind: 'node', title: node.title, code: node.code, course: course?.title, color: course?.color, branch: node.branch,
                published: node.published, url: node.url, practices: node.practices,
                teaches: node.topics.map((key) => ({ ...topicInfo(key),
                    others: (byId.get(`t${key}`)?.topic.taught ?? []).filter((other) => other !== node.id).map(nodeInfo).filter(Boolean) })),
                uses: node.uses.map((key) => ({ ...topicInfo(key),
                    taughtBy: (byId.get(`t${key}`)?.topic.taught ?? []).map(nodeInfo).filter(Boolean) })),
            };
        }
        const topic = item.topic;
        const family = families.get(topic.family);
        return {
            kind: 'topic', title: topic.title, key: topic.key, description: topic.description, color: item.color,
            family: family?.title ?? topic.family, scope: family?.scope, status: item.status, statusLabel: STATUS_LABELS[item.status],
            loose: topic.loose, taught: topic.taught.map(nodeInfo).filter(Boolean), used: topic.used.map(nodeInfo).filter(Boolean),
        };
    }

    function select(id, { fly = false } = {}) {
        selected = id;
        graph.linkWidth(graph.linkWidth());
        onSelect?.(id ? details(id) : null);
        if (id && fly) focus(id);
    }

    function focus(id) {
        const item = byId.get(id);
        if (!item || item.x === undefined) return;
        const distance = 240;
        const ratio = 1 + distance / Math.hypot(item.x, item.y, item.z || 1);
        graph.cameraPosition({ x: item.x * ratio, y: item.y * ratio, z: (item.z || 1) * ratio + 40 }, item, 1200);
    }

    return {
        setFilters(next) {
            filters = { ...filters, ...next, courses: new Set(next.courses ?? filters.courses), families: new Set(next.families ?? filters.families) };
            apply();
        },
        select: (id) => select(id, { fly: true }),
        search(query) {
            const q = normalize(query).trim();
            if (!q) return null;
            // Primero los temas, después los nodos y al final los cursos.
            const text = (item) => item.kind === 'node' ? item.node.title + ' ' + item.node.code : item.kind === 'topic' ? item.topic.title + ' ' + item.topic.key : item.course.title;
            const shown = graph.graphData().nodes;
            const match = ['topic', 'node', 'course'].map((kind) => shown.find((item) => item.kind === kind && normalize(text(item)).includes(q))).find(Boolean);
            if (match) select(match.id, { fly: true });
            return match?.id ?? null;
        },
        fit: () => graph.zoomToFit(800, 40),
        dimensions: (n) => graph.numDimensions(n),
        destroy() {
            observer.disconnect();
            graph._destructor?.();
        },
    };
}
