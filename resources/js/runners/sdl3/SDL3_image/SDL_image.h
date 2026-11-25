/* SDL3_image de la plataforma (D126): cargar PNG, JPG, BMP, GIF o WebP como superficies o texturas (los decodifica
 * el navegador) y guardar PNG. Mismos nombres que SDL3_image 3.x. */
#ifndef SDL_IMAGE_PLATAFORMA_H
#define SDL_IMAGE_PLATAFORMA_H
#include <SDL3/SDL.h>

#define SDL_IMAGE_MAJOR_VERSION 3
#define SDL_IMAGE_MINOR_VERSION 2
#define SDL_IMAGE_MICRO_VERSION 0

static inline int IMG_Version(void) { return SDL_VERSIONNUM(SDL_IMAGE_MAJOR_VERSION, SDL_IMAGE_MINOR_VERSION, SDL_IMAGE_MICRO_VERSION); }
static inline SDL_Surface *IMG_Load(const char *file) { return sdlw_load_image(file); }
static inline SDL_Texture *IMG_LoadTexture(SDL_Renderer *renderer, const char *file)
{
    SDL_Surface *s = IMG_Load(file);
    if (!s) return NULL;
    SDL_Texture *t = SDL_CreateTextureFromSurface(renderer, s);
    SDL_DestroySurface(s);
    return t;
}
static inline bool IMG_SavePNG(SDL_Surface *s, const char *file)
{
    if (!s) return false;
    int size = 0;
    int blob = sdlw_image_encode(s->pixels, s->w, s->h, s->pitch, s->format, &size);
    if (!blob) return false;
    void *data = malloc((size_t)size);
    if (!data) return false;
    sdlw_blob_copy(blob, data);
    bool ok = SDL_SaveFile(file, data, (size_t)size);
    free(data);
    return ok;
}

#endif
