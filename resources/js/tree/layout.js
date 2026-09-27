// Posiciones del árbol "estilo Path of Exile": el raíz en el centro y cada rama
// sale en su propio sector, con sus nodos en orden hacia afuera. Las hojas
// (prácticas) se abren a los costados de su nodo. Es determinista: el árbol
// se ve siempre igual. Si el docente movió un nodo, se respeta su pos_x/pos_y.

const FIRST_RING = 120;
const STEP = 100;
const LEAF_DISTANCE = 34;

export function layoutTree(data) {
    const positions = new Map();
    const root = data.nodes.find((node) => node.type === 'root');
    if (root) {
        positions.set(root.id, { x: 0, y: 0, angle: -Math.PI / 2 });
    }

    // Grupos: ramas en orden (los extras al final) y los nodos sin rama.
    const groups = data.branches
        .slice()
        .sort((a, b) => Number(a.is_extra) - Number(b.is_extra) || a.position - b.position)
        .map((branch) => ({ key: branch.id, nodes: [] }));
    const loose = { key: 'none', nodes: [] };

    for (const node of data.nodes) {
        if (node.type === 'root') continue;
        (groups.find((group) => group.key === node.branch_id) ?? loose).nodes.push(node);
    }
    if (loose.nodes.length) groups.push(loose);

    // Profundidad = pasos desde el raíz siguiendo los requisitos. Una rama que
    // continúa a otra (Control después del jefe de Fundamentos) queda más afuera.
    const byId = new Map(data.nodes.map((node) => [node.id, node]));
    const depthOf = (node, seen = new Set()) => {
        if (!node || node.type === 'root' || seen.has(node.id)) return 0;
        seen.add(node.id);
        return 1 + depthOf(byId.get(node.parent_id), seen);
    };

    const active = groups.filter((group) => group.nodes.length);
    const sector = (2 * Math.PI) / Math.max(active.length, 1);

    active.forEach((group, index) => {
        const angle = -Math.PI / 2 + index * sector;
        const byDepth = new Map();

        group.nodes
            .sort((a, b) => depthOf(a) - depthOf(b) || a.position - b.position || a.id - b.id)
            .forEach((node) => {
                const depth = Math.max(depthOf(node), 1);
                const siblings = byDepth.get(depth) ?? [];
                siblings.push(node);
                byDepth.set(depth, siblings);
            });

        for (const [depth, siblings] of byDepth) {
            const radius = FIRST_RING + (depth - 1) * STEP;
            // Hermanos a la misma distancia: se abren en abanico dentro del sector.
            const spread = Math.min(sector * 0.6, (siblings.length - 1) * (70 / radius));
            siblings.forEach((node, k) => {
                const offset = siblings.length === 1 ? 0 : -spread / 2 + (spread * k) / (siblings.length - 1);
                const sway = Math.sin(depth * 1.7) * Math.min(0.1, sector / 8);
                const nodeAngle = angle + offset + sway;
                positions.set(node.id, { x: Math.cos(nodeAngle) * radius, y: Math.sin(nodeAngle) * radius, angle: nodeAngle });
            });
        }
    });

    // Posiciones retocadas a mano desde el admin.
    for (const node of data.nodes) {
        if (node.pos_x !== null && node.pos_y !== null) {
            const x = Number(node.pos_x);
            const y = Number(node.pos_y);
            positions.set(node.id, { x, y, angle: Math.atan2(y, x) });
        }
    }

    return positions;
}

/** Hojas a los costados del nodo (perpendiculares a su rama), alternando lados. */
export function leafPositions(nodePosition, count) {
    const { x, y, angle } = nodePosition;
    const result = [];

    for (let j = 0; j < count; j++) {
        const side = j % 2 === 0 ? 1 : -1;
        const row = Math.floor(j / 2);
        const spread = (Math.PI / 2) * side + (row - 0.5) * 0.55 * side;
        const leafAngle = angle + spread;
        const distance = LEAF_DISTANCE + row * 6;
        result.push({ x: x + Math.cos(leafAngle) * distance, y: y + Math.sin(leafAngle) * distance });
    }

    return result;
}
