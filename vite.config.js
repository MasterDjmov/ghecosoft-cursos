import tailwindcss from '@tailwindcss/vite';
import laravel from 'laravel-vite-plugin';
import { bunny } from 'laravel-vite-plugin/fonts';
import { fileURLToPath } from 'node:url';
import { defineConfig, lazyPlugins } from 'vite-plus';

// Ejecutor de PHP del docente (D68): el cargador de PHP 8.3 importa su .wasm (18 MB); no va al build,
// el worker lo baja comprimido de public/toolchains/php (scripts/build-php-toolchain.sh).
const phpWasmOutsideBuild = () => ({
    name: 'php-wasm-outside-build',
    enforce: 'pre',
    resolveId: (source, importer) => (source.endsWith('.wasm') && importer?.includes('@php-wasm') ? '\0php-wasm-stub' : null),
    load: (id) => (id === '\0php-wasm-stub' ? 'export default "";' : null),
});

export default defineConfig({
    plugins: lazyPlugins(() => [
        laravel({
            input: [
                'resources/css/app.css',
                'resources/js/app.js',
                'resources/js/passkeys.js',
            ],
            refresh: true,
            fonts: [
                bunny('Inter', { weights: [400, 500, 600, 700] }),
                bunny('Space Grotesk', { weights: [500, 600, 700] }),
                bunny('JetBrains Mono', { weights: [400, 500] }),
            ],
        }),
        tailwindcss(),
        phpWasmOutsideBuild(),
    ]),
    resolve: {
        alias: {
            'php-wasm-8-3-loader': fileURLToPath(new URL('./node_modules/@php-wasm/web-8-3/asyncify/php_8_3.js', import.meta.url)),
        },
    },
    worker: {
        format: 'es',
        plugins: () => [phpWasmOutsideBuild()],
    },
    server: {
        cors: true,
        watch: {
            ignored: [
                '**/.agents/**',
                '**/.claude/**',
                '**/.cursor/**',
                '**/.junie/**',
                '**/storage/framework/views/**',
                '**/vendor/**',
            ],
        },
    },
});
