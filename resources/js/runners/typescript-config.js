// Versión del compilador de TypeScript del navegador (D115, fase 5). Tiene que coincidir con `typescript` de
// package.json: scripts/build-typescript-toolchain.mjs copia el compilador, sus .d.ts y los mensajes en español a
// public/toolchains/typescript. Es la 6.x porque TypeScript 7 es nativo (Go) y no corre en el navegador; los códigos
// de error (TS2322…) son los mismos.
export const TS_VERSION = '6.0.3';
export const TS_BASE = '/toolchains/typescript';
