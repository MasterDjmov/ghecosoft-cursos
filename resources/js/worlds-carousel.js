// Carrusel 3D de «Seguí donde dejaste» (Mundos): la tarjeta del medio al frente y las de los costados giradas.
// Se cambia arrastrando (dedo o mouse), tocando una de los costados, con las flechas, los puntos o el teclado.
// En la compu se ven dos por lado; en el celular, una.
export function worldsCarousel(count, start = 0) {
    const desktop = window.matchMedia('(min-width: 1024px)');

    return {
        count,
        active: Math.min(Math.max(start, 0), count - 1),
        drag: 0,
        startX: null,
        moved: false,
        wide: desktop.matches,

        init() {
            const update = () => (this.wide = desktop.matches);
            desktop.addEventListener('change', update);
            this.stopWatching = () => desktop.removeEventListener('change', update);
        },

        destroy() {
            this.stopWatching?.();
        },

        go(index) {
            this.active = Math.min(Math.max(index, 0), this.count - 1);
        },

        prev() {
            this.go(this.active - 1);
        },

        next() {
            this.go(this.active + 1);
        },

        // Cuánto se corre una tarjeta por cada lugar que la separa del medio.
        step() {
            return this.$refs.stage ? this.$refs.stage.firstElementChild.offsetWidth * (this.wide ? 0.62 : 0.5) : 160;
        },

        cardStyle(index) {
            const offset = index - this.active + this.drag / this.step();
            const distance = Math.abs(offset);
            const visible = this.wide ? 2 : 1;
            const side = Math.sign(offset);
            // Más allá de la primera, se corren menos para que se apilen.
            const x = side * (Math.min(distance, 1) + Math.max(distance - 1, 0) * 0.55) * this.step();

            return {
                transform: `translateX(${x}px) translateZ(${-110 * distance}px) rotateY(${-side * Math.min(distance, 1.4) * 28}deg)`,
                opacity: distance > visible + 0.5 ? 0 : 1 - Math.min(distance, visible) * 0.3,
                zIndex: 30 - Math.round(distance * 10),
                transition: this.startX === null ? '' : 'none',
                pointerEvents: distance > visible + 0.5 ? 'none' : '',
            };
        },

        pointerDown(event) {
            if (this.count < 2 || (event.pointerType === 'mouse' && event.button !== 0)) return;
            this.startX = event.clientX;
            this.moved = false;
        },

        pointerMove(event) {
            if (this.startX === null) return;
            const dx = event.clientX - this.startX;
            if (!this.moved && Math.abs(dx) < 8) return;
            if (!this.moved) {
                this.moved = true;
                this.$refs.stage.setPointerCapture?.(event.pointerId);
            }
            // En los extremos cuesta más tirar (no hay más tarjetas).
            const edge = (dx > 0 && this.active === 0) || (dx < 0 && this.active === this.count - 1);
            this.drag = edge ? dx * 0.3 : dx;
        },

        pointerUp() {
            if (this.startX === null) return;
            const jump = Math.round(-this.drag / this.step());
            const flick = Math.abs(this.drag) > 40 && jump === 0 ? -Math.sign(this.drag) : jump;
            this.startX = null;
            this.drag = 0;
            if (this.moved) this.go(this.active + flick);
        },

        // Después de arrastrar no vale el clic que suelta el mouse encima de un enlace.
        swallowClick(event) {
            if (this.moved) {
                event.preventDefault();
                event.stopPropagation();
                this.moved = false;
            }
        },
    };
}
