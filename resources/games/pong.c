/*
 * La Cancha de las Paletas: un Pong completo con SDL3.
 *
 * Jugador 1 (izquierda): W y S, o el primer joystick.
 * Jugador 2 (derecha):   flechas arriba y abajo, o el segundo joystick.
 * Con un solo jugador, la paleta de la derecha la mueve la compu.
 * Gana el primero que llega a 5 puntos.
 */
#include <SDL3/SDL.h>
#include <SDL3/SDL_main.h>

#define ANCHO 640
#define ALTO 480
#define PALETA_ANCHO 12
#define PALETA_ALTO 80
#define PELOTA 10
#define VELOCIDAD_PALETA 360.0f  /* píxeles por segundo */
#define VELOCIDAD_PELOTA 300.0f
#define PUNTOS_PARA_GANAR 5

/* En qué parte del juego estamos. */
typedef enum { MENU, JUGANDO, FIN } Estado;

typedef struct {
    float x, y;
    int puntos;
} Paleta;

typedef struct {
    float x, y;
    float vx, vy;  /* velocidad: cuánto se mueve por segundo en x y en y */
} Pelota;

/* Las paletas no se salen de la cancha. */
static float limitar(float y)
{
    return SDL_clamp(y, 0.0f, (float)(ALTO - PALETA_ALTO));
}

/* La pelota vuelve al medio y sale hacia el que perdió el punto (dir = -1 izquierda, 1 derecha). */
static void sacar(Pelota *p, int dir)
{
    p->x = ANCHO / 2.0f - PELOTA / 2.0f;
    p->y = ALTO / 2.0f - PELOTA / 2.0f;
    p->vx = VELOCIDAD_PELOTA * dir;
    p->vy = (SDL_randf() * 2.0f - 1.0f) * 180.0f;  /* un poco hacia arriba o hacia abajo, al azar */
}

/* ¿Se tocan la pelota y la paleta? Dos rectángulos se tocan si se pisan en x y en y. */
static bool toca(const Pelota *p, const Paleta *pal)
{
    return p->x < pal->x + PALETA_ANCHO && p->x + PELOTA > pal->x &&
           p->y < pal->y + PALETA_ALTO && p->y + PELOTA > pal->y;
}

/* Rebote: cuanto más lejos del centro de la paleta pega, más sale torcida. Y cada golpe la acelera un poco. */
static void rebotar(Pelota *p, const Paleta *pal, int dir)
{
    float centro = pal->y + PALETA_ALTO / 2.0f;
    float donde = (p->y + PELOTA / 2.0f - centro) / (PALETA_ALTO / 2.0f);  /* de -1 (arriba) a 1 (abajo) */
    float rapidez = SDL_fabsf(p->vx) * 1.06f;
    p->vx = rapidez * dir;
    p->vy = donde * 300.0f;
    p->x = dir > 0 ? pal->x + PALETA_ANCHO : pal->x - PELOTA;  /* que no quede adentro de la paleta */
}

/* Texto centrado, con letras más grandes (escala). */
static void texto_centrado(SDL_Renderer *r, float y, float escala, const char *texto)
{
    float ancho = (float)SDL_strlen(texto) * SDL_DEBUG_TEXT_FONT_CHARACTER_SIZE * escala;
    SDL_SetRenderScale(r, escala, escala);
    SDL_RenderDebugText(r, (ANCHO - ancho) / 2.0f / escala, y / escala, texto);
    SDL_SetRenderScale(r, 1.0f, 1.0f);
}

/* Cuánto pide mover el joystick: -1 arriba, 0 quieto, 1 abajo (con la cruz o la palanca). */
static float joystick(SDL_Gamepad *pad)
{
    if (!pad) return 0.0f;
    if (SDL_GetGamepadButton(pad, SDL_GAMEPAD_BUTTON_DPAD_UP)) return -1.0f;
    if (SDL_GetGamepadButton(pad, SDL_GAMEPAD_BUTTON_DPAD_DOWN)) return 1.0f;
    Sint16 palanca = SDL_GetGamepadAxis(pad, SDL_GAMEPAD_AXIS_LEFTY);
    if (palanca < -8000) return -1.0f;
    if (palanca > 8000) return 1.0f;
    return 0.0f;
}

int main(int argc, char *argv[])
{
    (void)argc;
    (void)argv;

    if (!SDL_Init(SDL_INIT_VIDEO | SDL_INIT_GAMEPAD)) {
        SDL_Log("No pude iniciar SDL: %s", SDL_GetError());
        return 1;
    }
    SDL_Window *ventana = NULL;
    SDL_Renderer *pincel = NULL;
    if (!SDL_CreateWindowAndRenderer("La Cancha de las Paletas", ANCHO, ALTO, 0, &ventana, &pincel)) {
        SDL_Log("No pude abrir la ventana: %s", SDL_GetError());
        SDL_Quit();
        return 1;
    }

    SDL_Gamepad *pads[2] = { NULL, NULL };
    Paleta izq = { 24, ALTO / 2.0f - PALETA_ALTO / 2.0f, 0 };
    Paleta der = { ANCHO - 24 - PALETA_ANCHO, ALTO / 2.0f - PALETA_ALTO / 2.0f, 0 };
    Pelota pelota;
    sacar(&pelota, 1);
    Estado estado = MENU;
    int jugadores = 1;
    const char *ganador = "";

    bool abierto = true;
    Uint64 antes = SDL_GetTicks();

    /* El bucle del juego: 1) leer eventos, 2) actualizar, 3) dibujar. Una vuelta por cuadro. */
    while (abierto) {
        /* 1) Eventos: cerrar la ventana, teclas que se apretan una vez, joysticks que se conectan. */
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_EVENT_QUIT) {
                abierto = false;
            } else if (e.type == SDL_EVENT_GAMEPAD_ADDED) {
                for (int i = 0; i < 2; i++) {
                    if (!pads[i]) { pads[i] = SDL_OpenGamepad(e.gdevice.which); break; }
                }
            } else if (e.type == SDL_EVENT_GAMEPAD_REMOVED) {
                for (int i = 0; i < 2; i++) {
                    if (pads[i] && SDL_GetGamepadID(pads[i]) == e.gdevice.which) { SDL_CloseGamepad(pads[i]); pads[i] = NULL; }
                }
            } else if (e.type == SDL_EVENT_KEY_DOWN && !e.key.repeat) {
                if (e.key.key == SDLK_ESCAPE) {
                    estado = MENU;
                } else if (estado != JUGANDO && (e.key.key == SDLK_1 || e.key.key == SDLK_2)) {
                    jugadores = e.key.key == SDLK_1 ? 1 : 2;
                    izq.puntos = der.puntos = 0;
                    sacar(&pelota, 1);
                    estado = JUGANDO;
                }
            } else if (e.type == SDL_EVENT_GAMEPAD_BUTTON_DOWN && e.gbutton.button == SDL_GAMEPAD_BUTTON_START && estado != JUGANDO) {
                jugadores = pads[1] ? 2 : 1;
                izq.puntos = der.puntos = 0;
                sacar(&pelota, 1);
                estado = JUGANDO;
            }
        }

        /* Delta time: cuántos segundos pasaron desde el cuadro anterior. Así el juego va igual de rápido en cualquier compu. */
        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;
        if (dt > 0.05f) dt = 0.05f;  /* si la compu se trabó, no saltar de golpe */

        /* 2) Actualizar: solo mientras se juega. */
        if (estado == JUGANDO) {
            /* Las teclas que se mantienen apretadas se leen del estado del teclado. */
            const bool *teclas = SDL_GetKeyboardState(NULL);
            float mover_izq = joystick(pads[0]);
            if (teclas[SDL_SCANCODE_W]) mover_izq = -1.0f;
            if (teclas[SDL_SCANCODE_S]) mover_izq = 1.0f;
            izq.y = limitar(izq.y + mover_izq * VELOCIDAD_PALETA * dt);

            if (jugadores == 2) {
                float mover_der = joystick(pads[1]);
                if (teclas[SDL_SCANCODE_UP]) mover_der = -1.0f;
                if (teclas[SDL_SCANCODE_DOWN]) mover_der = 1.0f;
                der.y = limitar(der.y + mover_der * VELOCIDAD_PALETA * dt);
            } else {
                /* La compu sigue a la pelota, pero un poco más lenta que vos: así se le puede ganar. */
                float objetivo = pelota.y + PELOTA / 2.0f - PALETA_ALTO / 2.0f;
                float paso = VELOCIDAD_PALETA * 0.7f * dt;
                if (der.y < objetivo - paso) der.y += paso;
                else if (der.y > objetivo + paso) der.y -= paso;
                der.y = limitar(der.y);
            }

            pelota.x += pelota.vx * dt;
            pelota.y += pelota.vy * dt;

            /* Rebote arriba y abajo. */
            if (pelota.y < 0) { pelota.y = 0; pelota.vy = -pelota.vy; }
            if (pelota.y > ALTO - PELOTA) { pelota.y = ALTO - PELOTA; pelota.vy = -pelota.vy; }

            /* Rebote en las paletas. */
            if (pelota.vx < 0 && toca(&pelota, &izq)) rebotar(&pelota, &izq, 1);
            if (pelota.vx > 0 && toca(&pelota, &der)) rebotar(&pelota, &der, -1);

            /* Punto: la pelota salió por un costado. */
            if (pelota.x + PELOTA < 0) { der.puntos++; sacar(&pelota, -1); }
            if (pelota.x > ANCHO) { izq.puntos++; sacar(&pelota, 1); }

            if (izq.puntos == PUNTOS_PARA_GANAR || der.puntos == PUNTOS_PARA_GANAR) {
                ganador = izq.puntos == PUNTOS_PARA_GANAR ? "GANA EL JUGADOR 1" : (jugadores == 2 ? "GANA EL JUGADOR 2" : "GANA LA COMPU");
                estado = FIN;
            }
        }

        /* 3) Dibujar: limpiar, dibujar todo y presentar. */
        SDL_SetRenderDrawColor(pincel, 16, 20, 36, 255);
        SDL_RenderClear(pincel);

        SDL_SetRenderDrawColor(pincel, 70, 80, 120, 255);
        for (int y = 0; y < ALTO; y += 24) {  /* la red del medio */
            SDL_FRect raya = { ANCHO / 2.0f - 2, (float)y + 4, 4, 14 };
            SDL_RenderFillRect(pincel, &raya);
        }

        SDL_SetRenderDrawColor(pincel, 255, 255, 255, 255);
        SDL_FRect p1 = { izq.x, izq.y, PALETA_ANCHO, PALETA_ALTO };
        SDL_FRect p2 = { der.x, der.y, PALETA_ANCHO, PALETA_ALTO };
        SDL_RenderFillRect(pincel, &p1);
        SDL_RenderFillRect(pincel, &p2);

        SDL_SetRenderScale(pincel, 4.0f, 4.0f);
        SDL_RenderDebugTextFormat(pincel, (ANCHO / 2.0f - 80) / 4, 6, "%d", izq.puntos);
        SDL_RenderDebugTextFormat(pincel, (ANCHO / 2.0f + 56) / 4, 6, "%d", der.puntos);
        SDL_SetRenderScale(pincel, 1.0f, 1.0f);

        if (estado == JUGANDO) {
            SDL_SetRenderDrawColor(pincel, 255, 210, 80, 255);
            SDL_FRect bola = { pelota.x, pelota.y, PELOTA, PELOTA };
            SDL_RenderFillRect(pincel, &bola);
        } else {
            SDL_SetRenderDrawColor(pincel, 255, 210, 80, 255);
            texto_centrado(pincel, 150, 3.0f, estado == FIN ? ganador : "PONG");
            SDL_SetRenderDrawColor(pincel, 220, 225, 240, 255);
            texto_centrado(pincel, 240, 2.0f, "1: un jugador   2: dos jugadores");
            texto_centrado(pincel, 280, 1.0f, "Jugador 1: W y S    Jugador 2: flechas    Joystick: START");
            texto_centrado(pincel, 300, 1.0f, "ESC: volver al menu");
        }

        SDL_RenderPresent(pincel);
        SDL_Delay(16);  /* unos 60 cuadros por segundo */
    }

    for (int i = 0; i < 2; i++) if (pads[i]) SDL_CloseGamepad(pads[i]);
    SDL_DestroyRenderer(pincel);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
