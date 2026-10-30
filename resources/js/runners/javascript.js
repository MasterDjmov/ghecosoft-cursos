// JavaScript en el navegador de quien ejecuta (D115): el alumno con su código y el docente al corregir. Corre en la
// caja de js-caja.js (sandbox sin mismo origen, sin red) con el mundo virtual de js-sandbox/world.js. Nada corre
// en el servidor.
import WORLD from './js-sandbox/world.js?raw';
import { execute, stopCaja } from './js-caja.js';

/**
 * @param {string} code
 * @param {object} options ver execute() en js-caja.js
 */
export function runJavaScript(code, options = {}) {
    return execute(WORLD, code, options);
}

export { stopCaja };
