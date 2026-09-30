// Versión del ejecutor de PHP del docente (D68). Tiene que coincidir con @php-wasm/web-8-3 de package.json:
// scripts/build-php-toolchain.sh copia su .wasm (comprimido) a public/toolchains/php.
export const PHP_VERSION = '8.3.33';
export const PHP_WASM_URL = `/toolchains/php/php-${PHP_VERSION}.wasm.gz`;
