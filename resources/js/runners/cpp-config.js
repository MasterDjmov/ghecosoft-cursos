// Versiones y opciones del ejecutor de C++ del docente (D66). scripts/build-cpp-toolchain.sh usa las mismas:
// si se cambia una versión, hay que volver a correrlo (el PCH solo sirve para el mismo clang y las mismas opciones).
export const YOWASP_CLANG = '22.0.0-git20542-10';
export const WASI_SDK = '34';
export const CLANG_URL = `https://cdn.jsdelivr.net/npm/@yowasp/clang@${YOWASP_CLANG}/gen/bundle.js`;
export const SYSROOT_URL = `/toolchains/cpp/sysroot-${WASI_SDK}.tar.gz`;
export const PCH_URL = `/toolchains/cpp/comun-${YOWASP_CLANG}.pch.gz`;

// Como compila el alumno con g++ -std=c++20, pero hacia WebAssembly con excepciones.
export const COMPILE_FLAGS = [
    '--sysroot=/sysroot', '-nostdinc++', '-isystem', '/sysroot/include/wasm32-wasip1/eh/c++/v1',
    '-std=c++20', '-O0', '-fwasm-exceptions', '-mllvm', '-wasm-use-legacy-eh=false',
];
export const LINK_FLAGS = ['--sysroot=/sysroot', '-L/sysroot/lib/wasm32-wasip1/eh', '-fwasm-exceptions', '-lunwind'];

// C: como gcc -std=c11 -Wall -Wextra del curso de C.
export const C_FLAGS = ['--sysroot=/sysroot', '-std=c11', '-O0', '-Wall', '-Wextra'];
