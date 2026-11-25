/* SDL3_ttf de la plataforma (D126): texto con fuentes TrueType (con tildes y ñ). La fuente sale del archivo .ttf
 * del juego y la dibuja el navegador. Mismos nombres que SDL3_ttf 3.x (el tamaño en puntos = píxeles, como SDL_ttf). */
#ifndef SDL_TTF_PLATAFORMA_H
#define SDL_TTF_PLATAFORMA_H
#include <SDL3/SDL.h>

#define SDL_TTF_MAJOR_VERSION 3
#define SDL_TTF_MINOR_VERSION 2
#define SDL_TTF_MICRO_VERSION 2

#define TTF_STYLE_NORMAL 0x00
#define TTF_STYLE_BOLD 0x01
#define TTF_STYLE_ITALIC 0x02
typedef Uint32 TTF_FontStyleFlags;

typedef struct TTF_Font { int id; float size; TTF_FontStyleFlags style; } TTF_Font;

SDLW_IMPORT(font_open) int sdlw_font_open(const void *data, int length);
SDLW_IMPORT(font_render) int sdlw_font_render(int font, float size, int style, const char *text, int length, Uint32 fg, Uint32 bg, int mode, int *w, int *h);
SDLW_IMPORT(font_measure) bool sdlw_font_measure(int font, float size, int style, const char *text, int length, int *w, int *h);

static inline int TTF_Version(void) { return SDL_VERSIONNUM(SDL_TTF_MAJOR_VERSION, SDL_TTF_MINOR_VERSION, SDL_TTF_MICRO_VERSION); }
static inline bool TTF_Init(void) { return true; }
static inline void TTF_Quit(void) {}
static inline TTF_Font *TTF_OpenFont(const char *file, float ptsize)
{
    size_t size = 0;
    void *data = SDL_LoadFile(file, &size);
    if (!data) return NULL;
    int id = sdlw_font_open(data, (int)size);
    free(data);
    if (!id) return NULL;
    TTF_Font *font = (TTF_Font *)calloc(1, sizeof(TTF_Font));
    if (font) { font->id = id; font->size = ptsize; }
    return font;
}
static inline void TTF_CloseFont(TTF_Font *font) { free(font); }
static inline bool TTF_SetFontSize(TTF_Font *font, float ptsize) { if (font) font->size = ptsize; return font != NULL; }
static inline float TTF_GetFontSize(TTF_Font *font) { return font ? font->size : 0.0f; }
static inline void TTF_SetFontStyle(TTF_Font *font, TTF_FontStyleFlags style) { if (font) font->style = style; }
static inline TTF_FontStyleFlags TTF_GetFontStyle(const TTF_Font *font) { return font ? font->style : 0; }
static inline bool TTF_GetStringSize(TTF_Font *font, const char *text, size_t length, int *w, int *h)
{
    return font && sdlw_font_measure(font->id, font->size, (int)font->style, text, length ? (int)length : (int)strlen(text), w, h);
}
static inline int TTF_GetFontHeight(const TTF_Font *font)
{
    int w = 0, h = 0;
    if (font) sdlw_font_measure(font->id, font->size, (int)font->style, "Ag", 2, &w, &h);
    return h;
}
static inline Uint32 sdlw_color(SDL_Color c) { return (Uint32)c.r << 24 | (Uint32)c.g << 16 | (Uint32)c.b << 8 | c.a; }
static inline SDL_Surface *sdlw_ttf_render(TTF_Font *font, const char *text, size_t length, SDL_Color fg, SDL_Color bg, int mode)
{
    if (!font || !text) return NULL;
    int w = 0, h = 0;
    int blob = sdlw_font_render(font->id, font->size, (int)font->style, text, length ? (int)length : (int)strlen(text), sdlw_color(fg), sdlw_color(bg), mode, &w, &h);
    if (!blob) return NULL;
    SDL_Surface *s = SDL_CreateSurface(w, h, SDL_PIXELFORMAT_RGBA32);
    if (s) sdlw_blob_copy(blob, s->pixels);
    return s;
}
/* Blended: bordes suaves y fondo transparente. Solid: sin suavizar. Shaded: sobre un color de fondo. */
static inline SDL_Surface *TTF_RenderText_Blended(TTF_Font *font, const char *text, size_t length, SDL_Color fg) { return sdlw_ttf_render(font, text, length, fg, fg, 0); }
static inline SDL_Surface *TTF_RenderText_Solid(TTF_Font *font, const char *text, size_t length, SDL_Color fg) { return sdlw_ttf_render(font, text, length, fg, fg, 1); }
static inline SDL_Surface *TTF_RenderText_Shaded(TTF_Font *font, const char *text, size_t length, SDL_Color fg, SDL_Color bg) { return sdlw_ttf_render(font, text, length, fg, bg, 2); }

#endif
