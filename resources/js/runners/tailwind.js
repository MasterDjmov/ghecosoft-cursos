// Tailwind CSS v4 compilado en el navegador de quien mira (lo mismo que hace @tailwindcss/browser, pero acá
// afuera de la caja de la vista previa: adentro no corre JavaScript). Se carga solo en los cursos de HTML.
import { compile } from 'tailwindcss';
import indexCss from 'tailwindcss/index.css?raw';
import themeCss from 'tailwindcss/theme.css?raw';
import preflightCss from 'tailwindcss/preflight.css?raw';
import utilitiesCss from 'tailwindcss/utilities.css?raw';

const SHEETS = {
    tailwindcss: indexCss,
    'tailwindcss/index': indexCss,
    'tailwindcss/index.css': indexCss,
    'tailwindcss/theme': themeCss,
    'tailwindcss/theme.css': themeCss,
    'tailwindcss/preflight': preflightCss,
    'tailwindcss/preflight.css': preflightCss,
    'tailwindcss/utilities': utilitiesCss,
    'tailwindcss/utilities.css': utilitiesCss,
};

// La misma hoja con las mismas clases da el mismo CSS: mientras el alumno escribe se reusa la compilación.
let last = { css: null, compiler: null };

/**
 * @param {string} css lo que escribió el alumno (por ejemplo: @import "tailwindcss"; @theme { … })
 * @param {string[]} candidates las clases que usa la página
 */
export async function compileTailwind(css, candidates) {
    if (last.css !== css) {
        const compiler = await compile(css, {
            base: '/',
            loadStylesheet: async (id) => {
                const content = SHEETS[id];
                if (content === undefined) {
                    throw new Error(`no se puede importar «${id}»: en la vista previa solo se puede importar "tailwindcss"`);
                }
                return { path: id, base: '/', content };
            },
            loadModule: async (id) => {
                throw new Error(`los plugins («${id}») no se pueden usar en la vista previa`);
            },
        });
        last = { css, compiler };
    }

    return last.compiler.build(candidates);
}
