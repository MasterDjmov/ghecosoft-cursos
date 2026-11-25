/*
 * SDL3 de la plataforma (D126): lo de SDL3 que usa el curso de Videojuegos, con los mismos nombres, tipos y
 * constantes que SDL3 real, para que el mismo archivo compile igual en la web y en la compu (con SDL3 de verdad).
 * Lo que dibuja, el teclado y el joystick los resuelve el navegador (resources/js/workers/sdl-run.worker.js).
 * Lo que no está acá, el curso no lo usa.
 */
#ifndef SDL_PLATAFORMA_H
#define SDL_PLATAFORMA_H

#include <stdbool.h>
#include <stdint.h>
#include <stddef.h>
#include <stdarg.h>
#include <string.h>

#define SDL_PLATAFORMA 1
#define SDL_MAJOR_VERSION 3
#define SDL_MINOR_VERSION 4
#define SDL_MICRO_VERSION 0

#define SDLW_IMPORT(name) __attribute__((import_module("sdl"), import_name(#name)))

typedef uint8_t Uint8;
typedef int8_t Sint8;
typedef uint16_t Uint16;
typedef int16_t Sint16;
typedef uint32_t Uint32;
typedef int32_t Sint32;
typedef uint64_t Uint64;
typedef int64_t Sint64;

typedef Uint32 SDL_InitFlags;
typedef Uint64 SDL_WindowFlags;
typedef Uint32 SDL_WindowID;
typedef Uint32 SDL_KeyboardID;
typedef Uint32 SDL_MouseID;
typedef Uint32 SDL_JoystickID;
typedef Uint32 SDL_Keycode;
typedef Uint16 SDL_Keymod;
typedef Uint32 SDL_MouseButtonFlags;

#define SDL_INIT_AUDIO 0x00000010u
#define SDL_INIT_VIDEO 0x00000020u
#define SDL_INIT_JOYSTICK 0x00000200u
#define SDL_INIT_HAPTIC 0x00001000u
#define SDL_INIT_GAMEPAD 0x00002000u
#define SDL_INIT_EVENTS 0x00004000u

#define SDL_WINDOW_FULLSCREEN 0x0000000000000001ull
#define SDL_WINDOW_RESIZABLE 0x0000000000000020ull

typedef struct SDL_Window SDL_Window;
typedef struct SDL_Renderer SDL_Renderer;
typedef struct SDL_Gamepad SDL_Gamepad;

typedef struct SDL_Point { int x, y; } SDL_Point;
typedef struct SDL_FPoint { float x, y; } SDL_FPoint;
typedef struct SDL_Rect { int x, y, w, h; } SDL_Rect;
typedef struct SDL_FRect { float x, y, w, h; } SDL_FRect;
typedef struct SDL_Color { Uint8 r, g, b, a; } SDL_Color;

#define SDL_min(x, y) (((x) < (y)) ? (x) : (y))
#define SDL_max(x, y) (((x) > (y)) ? (x) : (y))
#define SDL_clamp(x, a, b) (((x) < (a)) ? (a) : (((x) > (b)) ? (b) : (x)))

typedef enum SDL_BlendMode {
    SDL_BLENDMODE_NONE = 0x00000000u,
    SDL_BLENDMODE_BLEND = 0x00000001u,
    SDL_BLENDMODE_ADD = 0x00000002u,
} SDL_BlendMode;

/* ---------- Teclado: las teclas por su lugar (scancode) y por lo que escriben (keycode) ---------- */

typedef enum SDL_Scancode {
    SDL_SCANCODE_UNKNOWN = 0,
    SDL_SCANCODE_A = 4, SDL_SCANCODE_B = 5, SDL_SCANCODE_C = 6, SDL_SCANCODE_D = 7, SDL_SCANCODE_E = 8,
    SDL_SCANCODE_F = 9, SDL_SCANCODE_G = 10, SDL_SCANCODE_H = 11, SDL_SCANCODE_I = 12, SDL_SCANCODE_J = 13,
    SDL_SCANCODE_K = 14, SDL_SCANCODE_L = 15, SDL_SCANCODE_M = 16, SDL_SCANCODE_N = 17, SDL_SCANCODE_O = 18,
    SDL_SCANCODE_P = 19, SDL_SCANCODE_Q = 20, SDL_SCANCODE_R = 21, SDL_SCANCODE_S = 22, SDL_SCANCODE_T = 23,
    SDL_SCANCODE_U = 24, SDL_SCANCODE_V = 25, SDL_SCANCODE_W = 26, SDL_SCANCODE_X = 27, SDL_SCANCODE_Y = 28,
    SDL_SCANCODE_Z = 29,
    SDL_SCANCODE_1 = 30, SDL_SCANCODE_2 = 31, SDL_SCANCODE_3 = 32, SDL_SCANCODE_4 = 33, SDL_SCANCODE_5 = 34,
    SDL_SCANCODE_6 = 35, SDL_SCANCODE_7 = 36, SDL_SCANCODE_8 = 37, SDL_SCANCODE_9 = 38, SDL_SCANCODE_0 = 39,
    SDL_SCANCODE_RETURN = 40, SDL_SCANCODE_ESCAPE = 41, SDL_SCANCODE_BACKSPACE = 42, SDL_SCANCODE_TAB = 43,
    SDL_SCANCODE_SPACE = 44,
    SDL_SCANCODE_F1 = 58, SDL_SCANCODE_F2 = 59, SDL_SCANCODE_F3 = 60, SDL_SCANCODE_F4 = 61, SDL_SCANCODE_F5 = 62,
    SDL_SCANCODE_F6 = 63, SDL_SCANCODE_F7 = 64, SDL_SCANCODE_F8 = 65, SDL_SCANCODE_F9 = 66, SDL_SCANCODE_F10 = 67,
    SDL_SCANCODE_F11 = 68, SDL_SCANCODE_F12 = 69,
    SDL_SCANCODE_PAUSE = 72,
    SDL_SCANCODE_RIGHT = 79, SDL_SCANCODE_LEFT = 80, SDL_SCANCODE_DOWN = 81, SDL_SCANCODE_UP = 82,
    SDL_SCANCODE_KP_DIVIDE = 84, SDL_SCANCODE_KP_MULTIPLY = 85, SDL_SCANCODE_KP_MINUS = 86, SDL_SCANCODE_KP_PLUS = 87,
    SDL_SCANCODE_KP_ENTER = 88, SDL_SCANCODE_KP_1 = 89, SDL_SCANCODE_KP_2 = 90, SDL_SCANCODE_KP_3 = 91,
    SDL_SCANCODE_KP_4 = 92, SDL_SCANCODE_KP_5 = 93, SDL_SCANCODE_KP_6 = 94, SDL_SCANCODE_KP_7 = 95,
    SDL_SCANCODE_KP_8 = 96, SDL_SCANCODE_KP_9 = 97, SDL_SCANCODE_KP_0 = 98, SDL_SCANCODE_KP_PERIOD = 99,
    SDL_SCANCODE_LCTRL = 224, SDL_SCANCODE_LSHIFT = 225, SDL_SCANCODE_LALT = 226,
    SDL_SCANCODE_RCTRL = 228, SDL_SCANCODE_RSHIFT = 229, SDL_SCANCODE_RALT = 230,
    SDL_SCANCODE_COUNT = 512
} SDL_Scancode;

#define SDLK_SCANCODE_MASK (1u << 30)
#define SDL_SCANCODE_TO_KEYCODE(X) ((SDL_Keycode)(X) | SDLK_SCANCODE_MASK)
#define SDLK_UNKNOWN 0x00000000u
#define SDLK_RETURN 0x0000000du
#define SDLK_ESCAPE 0x0000001bu
#define SDLK_BACKSPACE 0x00000008u
#define SDLK_TAB 0x00000009u
#define SDLK_SPACE 0x00000020u
#define SDLK_0 0x00000030u
#define SDLK_1 0x00000031u
#define SDLK_2 0x00000032u
#define SDLK_3 0x00000033u
#define SDLK_4 0x00000034u
#define SDLK_5 0x00000035u
#define SDLK_6 0x00000036u
#define SDLK_7 0x00000037u
#define SDLK_8 0x00000038u
#define SDLK_9 0x00000039u
#define SDLK_A 0x00000061u
#define SDLK_B 0x00000062u
#define SDLK_C 0x00000063u
#define SDLK_D 0x00000064u
#define SDLK_E 0x00000065u
#define SDLK_F 0x00000066u
#define SDLK_G 0x00000067u
#define SDLK_H 0x00000068u
#define SDLK_I 0x00000069u
#define SDLK_J 0x0000006au
#define SDLK_K 0x0000006bu
#define SDLK_L 0x0000006cu
#define SDLK_M 0x0000006du
#define SDLK_N 0x0000006eu
#define SDLK_O 0x0000006fu
#define SDLK_P 0x00000070u
#define SDLK_Q 0x00000071u
#define SDLK_R 0x00000072u
#define SDLK_S 0x00000073u
#define SDLK_T 0x00000074u
#define SDLK_U 0x00000075u
#define SDLK_V 0x00000076u
#define SDLK_W 0x00000077u
#define SDLK_X 0x00000078u
#define SDLK_Y 0x00000079u
#define SDLK_Z 0x0000007au
#define SDLK_F1 0x4000003au
#define SDLK_F2 0x4000003bu
#define SDLK_F3 0x4000003cu
#define SDLK_F4 0x4000003du
#define SDLK_F5 0x4000003eu
#define SDLK_F6 0x4000003fu
#define SDLK_F7 0x40000040u
#define SDLK_F8 0x40000041u
#define SDLK_F9 0x40000042u
#define SDLK_F10 0x40000043u
#define SDLK_F11 0x40000044u
#define SDLK_F12 0x40000045u
#define SDLK_PAUSE 0x40000048u
#define SDLK_RIGHT 0x4000004fu
#define SDLK_LEFT 0x40000050u
#define SDLK_DOWN 0x40000051u
#define SDLK_UP 0x40000052u
#define SDLK_KP_DIVIDE 0x40000054u
#define SDLK_KP_MULTIPLY 0x40000055u
#define SDLK_KP_MINUS 0x40000056u
#define SDLK_KP_PLUS 0x40000057u
#define SDLK_KP_ENTER 0x40000058u
#define SDLK_KP_1 0x40000059u
#define SDLK_KP_2 0x4000005au
#define SDLK_KP_3 0x4000005bu
#define SDLK_KP_4 0x4000005cu
#define SDLK_KP_5 0x4000005du
#define SDLK_KP_6 0x4000005eu
#define SDLK_KP_7 0x4000005fu
#define SDLK_KP_8 0x40000060u
#define SDLK_KP_9 0x40000061u
#define SDLK_KP_0 0x40000062u
#define SDLK_KP_PERIOD 0x40000063u
#define SDLK_LCTRL 0x400000e0u
#define SDLK_LSHIFT 0x400000e1u
#define SDLK_LALT 0x400000e2u
#define SDLK_RCTRL 0x400000e4u
#define SDLK_RSHIFT 0x400000e5u
#define SDLK_RALT 0x400000e6u

#define SDL_KMOD_NONE 0x0000u
#define SDL_KMOD_LSHIFT 0x0001u
#define SDL_KMOD_RSHIFT 0x0002u
#define SDL_KMOD_LCTRL 0x0040u
#define SDL_KMOD_RCTRL 0x0080u
#define SDL_KMOD_LALT 0x0100u
#define SDL_KMOD_RALT 0x0200u
#define SDL_KMOD_SHIFT (SDL_KMOD_LSHIFT | SDL_KMOD_RSHIFT)
#define SDL_KMOD_CTRL (SDL_KMOD_LCTRL | SDL_KMOD_RCTRL)
#define SDL_KMOD_ALT (SDL_KMOD_LALT | SDL_KMOD_RALT)

/* ---------- Mouse ---------- */

#define SDL_BUTTON_LEFT 1
#define SDL_BUTTON_MIDDLE 2
#define SDL_BUTTON_RIGHT 3
#define SDL_BUTTON_MASK(X) (1u << ((X) - 1))
#define SDL_BUTTON_LMASK SDL_BUTTON_MASK(SDL_BUTTON_LEFT)
#define SDL_BUTTON_MMASK SDL_BUTTON_MASK(SDL_BUTTON_MIDDLE)
#define SDL_BUTTON_RMASK SDL_BUTTON_MASK(SDL_BUTTON_RIGHT)

/* ---------- Gamepad (joystick con la forma de un control de consola) ---------- */

typedef enum SDL_GamepadButton {
    SDL_GAMEPAD_BUTTON_INVALID = -1,
    SDL_GAMEPAD_BUTTON_SOUTH, SDL_GAMEPAD_BUTTON_EAST, SDL_GAMEPAD_BUTTON_WEST, SDL_GAMEPAD_BUTTON_NORTH,
    SDL_GAMEPAD_BUTTON_BACK, SDL_GAMEPAD_BUTTON_GUIDE, SDL_GAMEPAD_BUTTON_START,
    SDL_GAMEPAD_BUTTON_LEFT_STICK, SDL_GAMEPAD_BUTTON_RIGHT_STICK,
    SDL_GAMEPAD_BUTTON_LEFT_SHOULDER, SDL_GAMEPAD_BUTTON_RIGHT_SHOULDER,
    SDL_GAMEPAD_BUTTON_DPAD_UP, SDL_GAMEPAD_BUTTON_DPAD_DOWN, SDL_GAMEPAD_BUTTON_DPAD_LEFT, SDL_GAMEPAD_BUTTON_DPAD_RIGHT,
    SDL_GAMEPAD_BUTTON_COUNT = 26
} SDL_GamepadButton;

typedef enum SDL_GamepadAxis {
    SDL_GAMEPAD_AXIS_INVALID = -1,
    SDL_GAMEPAD_AXIS_LEFTX, SDL_GAMEPAD_AXIS_LEFTY, SDL_GAMEPAD_AXIS_RIGHTX, SDL_GAMEPAD_AXIS_RIGHTY,
    SDL_GAMEPAD_AXIS_LEFT_TRIGGER, SDL_GAMEPAD_AXIS_RIGHT_TRIGGER,
    SDL_GAMEPAD_AXIS_COUNT
} SDL_GamepadAxis;

#define SDL_JOYSTICK_AXIS_MAX 32767
#define SDL_JOYSTICK_AXIS_MIN -32768

/* ---------- Eventos ---------- */

typedef enum SDL_EventType {
    SDL_EVENT_FIRST = 0,
    SDL_EVENT_QUIT = 0x100,
    SDL_EVENT_KEY_DOWN = 0x300,
    SDL_EVENT_KEY_UP,
    SDL_EVENT_MOUSE_MOTION = 0x400,
    SDL_EVENT_MOUSE_BUTTON_DOWN,
    SDL_EVENT_MOUSE_BUTTON_UP,
    SDL_EVENT_MOUSE_WHEEL,
    SDL_EVENT_GAMEPAD_AXIS_MOTION = 0x650,
    SDL_EVENT_GAMEPAD_BUTTON_DOWN,
    SDL_EVENT_GAMEPAD_BUTTON_UP,
    SDL_EVENT_GAMEPAD_ADDED,
    SDL_EVENT_GAMEPAD_REMOVED,
    SDL_EVENT_USER = 0x8000,
    SDL_EVENT_LAST = 0xFFFF,
    SDL_EVENT_ENUM_PADDING = 0x7FFFFFFF
} SDL_EventType;

typedef struct SDL_CommonEvent { Uint32 type; Uint32 reserved; Uint64 timestamp; } SDL_CommonEvent;
typedef struct SDL_QuitEvent { SDL_EventType type; Uint32 reserved; Uint64 timestamp; } SDL_QuitEvent;

typedef struct SDL_KeyboardEvent {
    SDL_EventType type; Uint32 reserved; Uint64 timestamp;
    SDL_WindowID windowID; SDL_KeyboardID which;
    SDL_Scancode scancode; SDL_Keycode key; SDL_Keymod mod; Uint16 raw;
    bool down; bool repeat;
} SDL_KeyboardEvent;

typedef struct SDL_MouseMotionEvent {
    SDL_EventType type; Uint32 reserved; Uint64 timestamp;
    SDL_WindowID windowID; SDL_MouseID which; SDL_MouseButtonFlags state;
    float x, y, xrel, yrel;
} SDL_MouseMotionEvent;

typedef struct SDL_MouseButtonEvent {
    SDL_EventType type; Uint32 reserved; Uint64 timestamp;
    SDL_WindowID windowID; SDL_MouseID which;
    Uint8 button; bool down; Uint8 clicks; Uint8 padding;
    float x, y;
} SDL_MouseButtonEvent;

typedef enum SDL_MouseWheelDirection { SDL_MOUSEWHEEL_NORMAL, SDL_MOUSEWHEEL_FLIPPED } SDL_MouseWheelDirection;

typedef struct SDL_MouseWheelEvent {
    SDL_EventType type; Uint32 reserved; Uint64 timestamp;
    SDL_WindowID windowID; SDL_MouseID which;
    float x, y; SDL_MouseWheelDirection direction; float mouse_x, mouse_y; Sint32 integer_x, integer_y;
} SDL_MouseWheelEvent;

/* Los eventos propios (SDL_RegisterEvents + SDL_PushEvent): por ejemplo, el «tic» de un temporizador. */
typedef struct SDL_UserEvent {
    Uint32 type; Uint32 reserved; Uint64 timestamp;
    SDL_WindowID windowID; Sint32 code; void *data1; void *data2;
} SDL_UserEvent;

typedef struct SDL_GamepadDeviceEvent { SDL_EventType type; Uint32 reserved; Uint64 timestamp; SDL_JoystickID which; } SDL_GamepadDeviceEvent;

typedef struct SDL_GamepadAxisEvent {
    SDL_EventType type; Uint32 reserved; Uint64 timestamp; SDL_JoystickID which;
    Uint8 axis; Uint8 padding1, padding2, padding3; Sint16 value; Uint16 padding4;
} SDL_GamepadAxisEvent;

typedef struct SDL_GamepadButtonEvent {
    SDL_EventType type; Uint32 reserved; Uint64 timestamp; SDL_JoystickID which;
    Uint8 button; bool down; Uint8 padding1, padding2;
} SDL_GamepadButtonEvent;

typedef union SDL_Event {
    Uint32 type;
    SDL_CommonEvent common;
    SDL_QuitEvent quit;
    SDL_KeyboardEvent key;
    SDL_MouseMotionEvent motion;
    SDL_MouseButtonEvent button;
    SDL_MouseWheelEvent wheel;
    SDL_UserEvent user;
    SDL_GamepadDeviceEvent gdevice;
    SDL_GamepadAxisEvent gaxis;
    SDL_GamepadButtonEvent gbutton;
    Uint8 padding[128];
} SDL_Event;

/* ---------- Lo que resuelve el navegador ---------- */

SDLW_IMPORT(init) bool sdlw_init(Uint32 flags, bool *keys, int count);
SDLW_IMPORT(quit) void sdlw_quit(void);
SDLW_IMPORT(create_window) int sdlw_create_window(const char *title, int w, int h);
SDLW_IMPORT(set_title) bool sdlw_set_title(const char *title);
SDLW_IMPORT(create_renderer) int sdlw_create_renderer(void);
SDLW_IMPORT(set_color) bool sdlw_set_color(int r, int g, int b, int a);
SDLW_IMPORT(get_color) void sdlw_get_color(Uint8 *rgba);
SDLW_IMPORT(set_blend) bool sdlw_set_blend(int mode);
SDLW_IMPORT(set_scale) bool sdlw_set_scale(float x, float y);
SDLW_IMPORT(clear) bool sdlw_clear(void);
SDLW_IMPORT(rect) bool sdlw_rect(const SDL_FRect *rect, int fill);
SDLW_IMPORT(line) bool sdlw_line(float x1, float y1, float x2, float y2);
SDLW_IMPORT(point) bool sdlw_point(float x, float y);
SDLW_IMPORT(text) bool sdlw_text(float x, float y, const char *text);
SDLW_IMPORT(present) bool sdlw_present(void);
SDLW_IMPORT(delay) void sdlw_delay(Uint32 ms);
SDLW_IMPORT(ticks) double sdlw_ticks(void);
SDLW_IMPORT(poll) int sdlw_poll(Sint32 *out, void *raw);
SDLW_IMPORT(push_event) bool sdlw_push_event(const void *event);
SDLW_IMPORT(mouse) Uint32 sdlw_mouse(float *x, float *y);
SDLW_IMPORT(gamepads) int sdlw_gamepads(SDL_JoystickID *ids, int max);
SDLW_IMPORT(gamepad_axis) int sdlw_gamepad_axis(SDL_JoystickID id, int axis);
SDLW_IMPORT(gamepad_button) int sdlw_gamepad_button(SDL_JoystickID id, int button);
SDLW_IMPORT(gamepad_name) bool sdlw_gamepad_name(SDL_JoystickID id, char *out, int size);
SDLW_IMPORT(random) double sdlw_random(void);
SDLW_IMPORT(log) void sdlw_log(const char *text);

/* Lo que es solo C se resuelve acá mismo. */
extern void *malloc(size_t size);
extern void *calloc(size_t count, size_t size);
extern void free(void *pointer);
extern int vsnprintf(char *buffer, size_t size, const char *format, va_list args);

__attribute__((weak)) bool sdlw_keys[SDL_SCANCODE_COUNT];
__attribute__((weak)) char sdlw_text_buffer[1024];
__attribute__((weak)) char sdlw_name_buffer[8][64];

static inline size_t SDL_strlen(const char *text) { return strlen(text); }
static inline int SDL_abs(int x) { return x < 0 ? -x : x; }
static inline float SDL_fabsf(float x) { return __builtin_fabsf(x); }
static inline float SDL_sqrtf(float x) { return __builtin_sqrtf(x); }
static inline float SDL_floorf(float x) { return __builtin_floorf(x); }
static inline float SDL_roundf(float x) { return __builtin_roundf(x); }
static inline float SDL_sinf(float x) { extern float sinf(float); return sinf(x); }
static inline float SDL_cosf(float x) { extern float cosf(float); return cosf(x); }

static inline void *SDL_malloc(size_t size) { return malloc(size); }
static inline void *SDL_calloc(size_t count, size_t size) { return calloc(count, size); }
static inline void SDL_free(void *pointer) { free(pointer); }

static inline int SDL_vsnprintf(char *text, size_t size, const char *format, va_list args) { return vsnprintf(text, size, format, args); }
static inline int SDL_snprintf(char *text, size_t size, const char *format, ...)
{
    va_list args;
    va_start(args, format);
    int n = vsnprintf(text, size, format, args);
    va_end(args);
    return n;
}

static inline bool SDL_Init(SDL_InitFlags flags) { return sdlw_init(flags, sdlw_keys, SDL_SCANCODE_COUNT); }
static inline bool SDL_InitSubSystem(SDL_InitFlags flags) { return SDL_Init(flags); }
static inline void SDL_Quit(void) { sdlw_quit(); }
static inline const char *SDL_GetError(void) { return "(sin detalle en la plataforma)"; }
static inline bool SDL_SetHint(const char *name, const char *value) { (void)name; (void)value; return true; }
static inline bool SDL_SetAppMetadata(const char *name, const char *version, const char *id) { (void)name; (void)version; (void)id; return true; }

static inline SDL_Window *SDL_CreateWindow(const char *title, int w, int h, SDL_WindowFlags flags)
{
    (void)flags;
    return (SDL_Window *)(uintptr_t)sdlw_create_window(title, w, h);
}
static inline SDL_Renderer *SDL_CreateRenderer(SDL_Window *window, const char *name)
{
    (void)name;
    return window ? (SDL_Renderer *)(uintptr_t)sdlw_create_renderer() : NULL;
}
static inline bool SDL_CreateWindowAndRenderer(const char *title, int w, int h, SDL_WindowFlags flags, SDL_Window **window, SDL_Renderer **renderer)
{
    *window = SDL_CreateWindow(title, w, h, flags);
    *renderer = SDL_CreateRenderer(*window, NULL);
    return *window && *renderer;
}
static inline bool SDL_SetWindowTitle(SDL_Window *window, const char *title) { (void)window; return sdlw_set_title(title); }
static inline void SDL_DestroyRenderer(SDL_Renderer *renderer) { (void)renderer; }
static inline void SDL_DestroyWindow(SDL_Window *window) { (void)window; }
static inline bool SDL_SetRenderVSync(SDL_Renderer *renderer, int vsync) { (void)renderer; (void)vsync; return true; }

static inline bool SDL_SetRenderDrawColor(SDL_Renderer *renderer, Uint8 r, Uint8 g, Uint8 b, Uint8 a) { (void)renderer; return sdlw_set_color(r, g, b, a); }
static inline bool SDL_GetRenderDrawColor(SDL_Renderer *renderer, Uint8 *r, Uint8 *g, Uint8 *b, Uint8 *a)
{
    Uint8 rgba[4];
    (void)renderer;
    sdlw_get_color(rgba);
    if (r) *r = rgba[0];
    if (g) *g = rgba[1];
    if (b) *b = rgba[2];
    if (a) *a = rgba[3];
    return true;
}
static inline bool SDL_SetRenderDrawBlendMode(SDL_Renderer *renderer, SDL_BlendMode mode) { (void)renderer; return sdlw_set_blend((int)mode); }
static inline bool SDL_SetRenderScale(SDL_Renderer *renderer, float x, float y) { (void)renderer; return sdlw_set_scale(x, y); }
static inline bool SDL_RenderClear(SDL_Renderer *renderer) { (void)renderer; return sdlw_clear(); }
static inline bool SDL_RenderFillRect(SDL_Renderer *renderer, const SDL_FRect *rect) { (void)renderer; return sdlw_rect(rect, 1); }
static inline bool SDL_RenderRect(SDL_Renderer *renderer, const SDL_FRect *rect) { (void)renderer; return sdlw_rect(rect, 0); }
static inline bool SDL_RenderLine(SDL_Renderer *renderer, float x1, float y1, float x2, float y2) { (void)renderer; return sdlw_line(x1, y1, x2, y2); }
static inline bool SDL_RenderPoint(SDL_Renderer *renderer, float x, float y) { (void)renderer; return sdlw_point(x, y); }
static inline bool SDL_RenderPresent(SDL_Renderer *renderer) { (void)renderer; return sdlw_present(); }

/* El texto de depuración de SDL3: letras de 8 x 8 píxeles (solo ASCII, sin tildes). */
#define SDL_DEBUG_TEXT_FONT_CHARACTER_SIZE 8
static inline bool SDL_RenderDebugText(SDL_Renderer *renderer, float x, float y, const char *text) { (void)renderer; return sdlw_text(x, y, text); }
static inline bool SDL_RenderDebugTextFormat(SDL_Renderer *renderer, float x, float y, const char *format, ...)
{
    va_list args;
    va_start(args, format);
    vsnprintf(sdlw_text_buffer, sizeof sdlw_text_buffer, format, args);
    va_end(args);
    (void)renderer;
    return sdlw_text(x, y, sdlw_text_buffer);
}

static inline void SDL_Log(const char *format, ...)
{
    va_list args;
    va_start(args, format);
    vsnprintf(sdlw_text_buffer, sizeof sdlw_text_buffer, format, args);
    va_end(args);
    sdlw_log(sdlw_text_buffer);
}

static inline Uint64 SDL_GetTicks(void) { return (Uint64)sdlw_ticks(); }
static inline Uint64 SDL_GetTicksNS(void) { return (Uint64)(sdlw_ticks() * 1000000.0); }
static inline Uint64 SDL_GetPerformanceCounter(void) { return (Uint64)(sdlw_ticks() * 1000.0); }
static inline Uint64 SDL_GetPerformanceFrequency(void) { return 1000000u; }
static inline void SDL_Delay(Uint32 ms) { sdlw_delay(ms); }
static inline void SDL_DelayNS(Uint64 ns) { sdlw_delay((Uint32)(ns / 1000000u)); }

static inline Sint32 SDL_rand(Sint32 n) { return n <= 0 ? 0 : (Sint32)(sdlw_random() * n); }
static inline float SDL_randf(void) { return (float)sdlw_random(); }

static inline bool SDL_PollEvent(SDL_Event *event)
{
    Sint32 out[6] = { 0 };
    SDL_Event raw;
    int type = sdlw_poll(out, &raw);
    if (!type) return false;
    if (!event) return true;
    if (out[5] == 1) { *event = raw; return true; }  /* un evento propio (SDL_PushEvent), tal cual */
    memset(event, 0, sizeof *event);
    event->type = (Uint32)type;
    event->common.timestamp = SDL_GetTicksNS();
    switch (type) {
    case SDL_EVENT_KEY_DOWN:
    case SDL_EVENT_KEY_UP:
        event->key.scancode = (SDL_Scancode)out[0];
        event->key.key = (SDL_Keycode)out[1];
        event->key.mod = (SDL_Keymod)out[2];
        event->key.down = type == SDL_EVENT_KEY_DOWN;
        event->key.repeat = out[3] != 0;
        event->key.windowID = 1;
        break;
    case SDL_EVENT_MOUSE_MOTION:
        event->motion.x = (float)out[0];
        event->motion.y = (float)out[1];
        event->motion.xrel = (float)out[2];
        event->motion.yrel = (float)out[3];
        event->motion.state = (SDL_MouseButtonFlags)out[4];
        event->motion.windowID = 1;
        break;
    case SDL_EVENT_MOUSE_BUTTON_DOWN:
    case SDL_EVENT_MOUSE_BUTTON_UP:
        event->button.x = (float)out[0];
        event->button.y = (float)out[1];
        event->button.button = (Uint8)out[2];
        event->button.clicks = (Uint8)out[3];
        event->button.down = type == SDL_EVENT_MOUSE_BUTTON_DOWN;
        event->button.windowID = 1;
        break;
    case SDL_EVENT_MOUSE_WHEEL:
        event->wheel.x = (float)out[0];
        event->wheel.y = (float)out[1];
        event->wheel.integer_x = out[0];
        event->wheel.integer_y = out[1];
        event->wheel.mouse_x = (float)out[2];
        event->wheel.mouse_y = (float)out[3];
        event->wheel.windowID = 1;
        break;
    case SDL_EVENT_GAMEPAD_ADDED:
    case SDL_EVENT_GAMEPAD_REMOVED:
        event->gdevice.which = (SDL_JoystickID)out[0];
        break;
    case SDL_EVENT_GAMEPAD_AXIS_MOTION:
        event->gaxis.which = (SDL_JoystickID)out[0];
        event->gaxis.axis = (Uint8)out[1];
        event->gaxis.value = (Sint16)out[2];
        break;
    case SDL_EVENT_GAMEPAD_BUTTON_DOWN:
    case SDL_EVENT_GAMEPAD_BUTTON_UP:
        event->gbutton.which = (SDL_JoystickID)out[0];
        event->gbutton.button = (Uint8)out[1];
        event->gbutton.down = type == SDL_EVENT_GAMEPAD_BUTTON_DOWN;
        break;
    }
    return true;
}

static inline const bool *SDL_GetKeyboardState(int *numkeys)
{
    if (numkeys) *numkeys = SDL_SCANCODE_COUNT;
    return sdlw_keys;
}

static inline SDL_MouseButtonFlags SDL_GetMouseState(float *x, float *y) { return sdlw_mouse(x, y); }

static inline bool SDL_HasGamepad(void) { return sdlw_gamepads(NULL, 0) > 0; }
static inline SDL_JoystickID *SDL_GetGamepads(int *count)
{
    SDL_JoystickID *ids = (SDL_JoystickID *)calloc(9, sizeof(SDL_JoystickID));
    int n = sdlw_gamepads(ids, 8);
    if (count) *count = n;
    return ids;
}
static inline SDL_Gamepad *SDL_OpenGamepad(SDL_JoystickID id) { return id && sdlw_gamepad_axis(id, -1) ? (SDL_Gamepad *)(uintptr_t)id : NULL; }
static inline void SDL_CloseGamepad(SDL_Gamepad *gamepad) { (void)gamepad; }
static inline SDL_JoystickID SDL_GetGamepadID(SDL_Gamepad *gamepad) { return (SDL_JoystickID)(uintptr_t)gamepad; }
static inline bool SDL_GamepadConnected(SDL_Gamepad *gamepad) { return gamepad && sdlw_gamepad_axis(SDL_GetGamepadID(gamepad), -1); }
static inline const char *SDL_GetGamepadName(SDL_Gamepad *gamepad)
{
    SDL_JoystickID id = SDL_GetGamepadID(gamepad);
    char *out = sdlw_name_buffer[id % 8];
    return sdlw_gamepad_name(id, out, (int)sizeof sdlw_name_buffer[0]) ? out : NULL;
}
static inline Sint16 SDL_GetGamepadAxis(SDL_Gamepad *gamepad, SDL_GamepadAxis axis) { return gamepad ? (Sint16)sdlw_gamepad_axis(SDL_GetGamepadID(gamepad), (int)axis) : 0; }
static inline bool SDL_GetGamepadButton(SDL_Gamepad *gamepad, SDL_GamepadButton button) { return gamepad && sdlw_gamepad_button(SDL_GetGamepadID(gamepad), (int)button); }

/* ---------- Utilidades de C con nombre de SDL (SDL_stdinc) ---------- */

#define SDL_PI_D 3.141592653589793238462643383279502884
#define SDL_PI_F 3.141592653589793238462643383279502884F
#define SDL_arraysize(array) (sizeof(array) / sizeof(array[0]))
#define SDL_zero(x) memset(&(x), 0, sizeof((x)))
#define SDL_zerop(x) memset((x), 0, sizeof(*(x)))
#define SDL_zeroa(x) memset((x), 0, sizeof((x)))

extern void *realloc(void *pointer, size_t size);
extern double atof(const char *text);
extern int atoi(const char *text);
extern int vsscanf(const char *text, const char *format, va_list args);

static inline void *SDL_realloc(void *pointer, size_t size) { return realloc(pointer, size); }
static inline void *SDL_memset(void *d, int c, size_t n) { return memset(d, c, n); }
static inline void *SDL_memcpy(void *d, const void *s, size_t n) { return memcpy(d, s, n); }
static inline void *SDL_memmove(void *d, const void *s, size_t n) { return memmove(d, s, n); }
static inline int SDL_memcmp(const void *a, const void *b, size_t n) { return memcmp(a, b, n); }
static inline int SDL_strcmp(const char *a, const char *b) { return strcmp(a, b); }
static inline int SDL_strncmp(const char *a, const char *b, size_t n) { return strncmp(a, b, n); }
static inline char *SDL_strchr(const char *s, int c) { return strchr(s, c); }
static inline char *SDL_strstr(const char *s, const char *t) { return strstr(s, t); }
static inline int SDL_tolower(int c) { return c >= 'A' && c <= 'Z' ? c + 32 : c; }
static inline int SDL_toupper(int c) { return c >= 'a' && c <= 'z' ? c - 32 : c; }
static inline int SDL_strcasecmp(const char *a, const char *b)
{
    while (*a && SDL_tolower((unsigned char)*a) == SDL_tolower((unsigned char)*b)) { a++; b++; }
    return SDL_tolower((unsigned char)*a) - SDL_tolower((unsigned char)*b);
}
static inline size_t SDL_strlcpy(char *dst, const char *src, size_t size)
{
    size_t n = strlen(src);
    if (size) { size_t c = n < size - 1 ? n : size - 1; memcpy(dst, src, c); dst[c] = 0; }
    return n;
}
static inline size_t SDL_strlcat(char *dst, const char *src, size_t size)
{
    size_t d = strlen(dst);
    return d + SDL_strlcpy(dst + d, src, d < size ? size - d : 0);
}
static inline char *SDL_strdup(const char *s)
{
    size_t n = strlen(s) + 1;
    char *copy = (char *)malloc(n);
    if (copy) memcpy(copy, s, n);
    return copy;
}
static inline double SDL_atof(const char *s) { return atof(s); }
static inline int SDL_atoi(const char *s) { return atoi(s); }
static inline int SDL_sscanf(const char *text, const char *format, ...)
{
    va_list args;
    va_start(args, format);
    int n = vsscanf(text, format, args);
    va_end(args);
    return n;
}
static inline double SDL_sin(double x) { return __builtin_sin(x); }
static inline double SDL_cos(double x) { return __builtin_cos(x); }
static inline double SDL_sqrt(double x) { return __builtin_sqrt(x); }
static inline double SDL_fabs(double x) { return __builtin_fabs(x); }
static inline double SDL_floor(double x) { return __builtin_floor(x); }
static inline double SDL_ceil(double x) { return __builtin_ceil(x); }
static inline double SDL_pow(double x, double y) { return __builtin_pow(x, y); }
static inline double SDL_atan2(double y, double x) { return __builtin_atan2(y, x); }
static inline float SDL_ceilf(float x) { return __builtin_ceilf(x); }
static inline float SDL_powf(float x, float y) { return __builtin_powf(x, y); }
static inline float SDL_atan2f(float y, float x) { return __builtin_atan2f(y, x); }
static inline float SDL_fmodf(float x, float y) { return __builtin_fmodf(x, y); }
static inline int SDL_abs_int(int x) { return x < 0 ? -x : x; }

/* ---------- Versión, plataforma y pantalla ---------- */

#define SDL_VERSIONNUM(major, minor, patch) ((major) * 1000000 + (minor) * 1000 + (patch))
#define SDL_VERSIONNUM_MAJOR(version) ((version) / 1000000)
#define SDL_VERSIONNUM_MINOR(version) (((version) / 1000) % 1000)
#define SDL_VERSIONNUM_MICRO(version) ((version) % 1000)
#define SDL_VERSION SDL_VERSIONNUM(SDL_MAJOR_VERSION, SDL_MINOR_VERSION, SDL_MICRO_VERSION)
#define SDL_VERSION_ATLEAST(X, Y, Z) (SDL_VERSION >= SDL_VERSIONNUM(X, Y, Z))

typedef Uint32 SDL_DisplayID;
typedef Uint32 SDL_PixelFormat;
typedef struct SDL_DisplayModeData SDL_DisplayModeData;
typedef struct SDL_DisplayMode {
    SDL_DisplayID displayID; SDL_PixelFormat format; int w; int h; float pixel_density; float refresh_rate;
    int refresh_rate_numerator; int refresh_rate_denominator; SDL_DisplayModeData *internal;
} SDL_DisplayMode;

SDLW_IMPORT(display) void sdlw_display(int *w, int *h, float *density);

__attribute__((weak)) SDL_DisplayMode sdlw_mode;

static inline int SDL_GetVersion(void) { return SDL_VERSION; }
static inline const char *SDL_GetRevision(void) { return "SDL3 de la plataforma (web)"; }
static inline const char *SDL_GetPlatform(void) { return "Web"; }
static inline const char *SDL_GetCurrentVideoDriver(void) { return "web"; }
static inline SDL_DisplayID SDL_GetPrimaryDisplay(void) { return 1; }
static inline SDL_DisplayID *SDL_GetDisplays(int *count)
{
    SDL_DisplayID *ids = (SDL_DisplayID *)calloc(2, sizeof(SDL_DisplayID));
    if (ids) ids[0] = 1;
    if (count) *count = 1;
    return ids;
}
static inline const char *SDL_GetDisplayName(SDL_DisplayID id) { (void)id; return "Pantalla del navegador"; }
static inline const SDL_DisplayMode *SDL_GetDesktopDisplayMode(SDL_DisplayID id)
{
    if (id != 1) return NULL;
    sdlw_display(&sdlw_mode.w, &sdlw_mode.h, &sdlw_mode.pixel_density);
    sdlw_mode.displayID = 1;
    sdlw_mode.refresh_rate = 60.0f;
    sdlw_mode.refresh_rate_numerator = 60;
    sdlw_mode.refresh_rate_denominator = 1;
    return &sdlw_mode;
}
static inline const SDL_DisplayMode *SDL_GetCurrentDisplayMode(SDL_DisplayID id) { return SDL_GetDesktopDisplayMode(id); }

/* ---------- Eventos propios ---------- */

__attribute__((weak)) Uint32 sdlw_next_user_event = SDL_EVENT_USER;

static inline Uint32 SDL_RegisterEvents(int count)
{
    if (count <= 0 || sdlw_next_user_event + (Uint32)count > SDL_EVENT_LAST) return 0;
    Uint32 first = sdlw_next_user_event;
    sdlw_next_user_event += (Uint32)count;
    return first;
}
static inline bool SDL_PushEvent(SDL_Event *event)
{
    event->common.timestamp = SDL_GetTicksNS();
    return sdlw_push_event(event);
}

/* ---------- Audio (SDL_AudioStream): lo reproduce el audio del navegador ---------- */

typedef Uint32 SDL_AudioDeviceID;
typedef enum SDL_AudioFormat {
    SDL_AUDIO_UNKNOWN = 0x0000u,
    SDL_AUDIO_U8 = 0x0008u, SDL_AUDIO_S8 = 0x8008u,
    SDL_AUDIO_S16LE = 0x8010u, SDL_AUDIO_S16BE = 0x9010u,
    SDL_AUDIO_S32LE = 0x8020u, SDL_AUDIO_S32BE = 0x9020u,
    SDL_AUDIO_F32LE = 0x8120u, SDL_AUDIO_F32BE = 0x9120u,
    SDL_AUDIO_S16 = SDL_AUDIO_S16LE, SDL_AUDIO_S32 = SDL_AUDIO_S32LE, SDL_AUDIO_F32 = SDL_AUDIO_F32LE
} SDL_AudioFormat;
#define SDL_AUDIO_BITSIZE(x) ((x) & 0xFFu)
#define SDL_AUDIO_BYTESIZE(x) (SDL_AUDIO_BITSIZE(x) / 8)
#define SDL_AUDIO_FRAMESIZE(x) (SDL_AUDIO_BYTESIZE((x).format) * (x).channels)
#define SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK ((SDL_AudioDeviceID)0xFFFFFFFFu)

typedef struct SDL_AudioSpec { SDL_AudioFormat format; int channels; int freq; } SDL_AudioSpec;
typedef struct SDL_AudioStream SDL_AudioStream;
typedef void (*SDL_AudioStreamCallback)(void *userdata, SDL_AudioStream *stream, int additional_amount, int total_amount);

SDLW_IMPORT(audio_open) int sdlw_audio_open(int format, int channels, int freq, SDL_AudioStreamCallback callback, void *userdata);
SDLW_IMPORT(audio_put) bool sdlw_audio_put(int stream, const void *data, int length);
SDLW_IMPORT(audio_queued) int sdlw_audio_queued(int stream);
SDLW_IMPORT(audio_control) bool sdlw_audio_control(int stream, int action, float value);

#define SDLW_AUDIO_RESUME 1
#define SDLW_AUDIO_PAUSE 2
#define SDLW_AUDIO_CLEAR 3
#define SDLW_AUDIO_DESTROY 4
#define SDLW_AUDIO_GAIN 5

static inline int sdlw_stream_id(SDL_AudioStream *stream) { return (int)(uintptr_t)stream; }
static inline const char *SDL_GetCurrentAudioDriver(void) { return "web"; }
static inline SDL_AudioStream *SDL_OpenAudioDeviceStream(SDL_AudioDeviceID device, const SDL_AudioSpec *spec, SDL_AudioStreamCallback callback, void *userdata)
{
    (void)device;
    if (!spec) return NULL;
    int id = sdlw_audio_open((int)spec->format, spec->channels, spec->freq, callback, userdata);
    return id ? (SDL_AudioStream *)(uintptr_t)id : NULL;
}
static inline bool SDL_PutAudioStreamData(SDL_AudioStream *stream, const void *buf, int len) { return stream && sdlw_audio_put(sdlw_stream_id(stream), buf, len); }
static inline int SDL_GetAudioStreamQueued(SDL_AudioStream *stream) { return stream ? sdlw_audio_queued(sdlw_stream_id(stream)) : -1; }
static inline int SDL_GetAudioStreamAvailable(SDL_AudioStream *stream) { return SDL_GetAudioStreamQueued(stream); }
static inline bool SDL_FlushAudioStream(SDL_AudioStream *stream) { return stream != NULL; }
static inline bool SDL_ResumeAudioStreamDevice(SDL_AudioStream *stream) { return stream && sdlw_audio_control(sdlw_stream_id(stream), SDLW_AUDIO_RESUME, 0); }
static inline bool SDL_PauseAudioStreamDevice(SDL_AudioStream *stream) { return stream && sdlw_audio_control(sdlw_stream_id(stream), SDLW_AUDIO_PAUSE, 0); }
static inline bool SDL_ClearAudioStream(SDL_AudioStream *stream) { return stream && sdlw_audio_control(sdlw_stream_id(stream), SDLW_AUDIO_CLEAR, 0); }
static inline bool SDL_SetAudioStreamGain(SDL_AudioStream *stream, float gain) { return stream && sdlw_audio_control(sdlw_stream_id(stream), SDLW_AUDIO_GAIN, gain); }
static inline void SDL_DestroyAudioStream(SDL_AudioStream *stream) { if (stream) sdlw_audio_control(sdlw_stream_id(stream), SDLW_AUDIO_DESTROY, 0); }

/* ---------- Archivos (SDL_IOStream): la carpeta del juego, que queda guardada en el navegador ---------- */

typedef struct _IO_FILE FILE;
extern FILE *fopen(const char *path, const char *mode);
extern size_t fread(void *ptr, size_t size, size_t count, FILE *file);
extern size_t fwrite(const void *ptr, size_t size, size_t count, FILE *file);
extern int fclose(FILE *file);
extern int fseek(FILE *file, long offset, int whence);
extern long ftell(FILE *file);
extern int fflush(FILE *file);
extern int mkdir(const char *path, unsigned int mode);

SDLW_IMPORT(files_changed) void sdlw_files_changed(void);

typedef enum SDL_IOWhence { SDL_IO_SEEK_SET, SDL_IO_SEEK_CUR, SDL_IO_SEEK_END } SDL_IOWhence;
typedef struct SDL_IOStream { FILE *file; bool wrote; } SDL_IOStream;

static inline SDL_IOStream *SDL_IOFromFile(const char *file, const char *mode)
{
    FILE *f = fopen(file, mode);
    if (!f) return NULL;
    SDL_IOStream *io = (SDL_IOStream *)calloc(1, sizeof(SDL_IOStream));
    if (!io) { fclose(f); return NULL; }
    io->file = f;
    io->wrote = strpbrk(mode, "wa+") != NULL;
    return io;
}
static inline size_t SDL_ReadIO(SDL_IOStream *io, void *ptr, size_t size) { return io ? fread(ptr, 1, size, io->file) : 0; }
static inline size_t SDL_WriteIO(SDL_IOStream *io, const void *ptr, size_t size) { return io ? fwrite(ptr, 1, size, io->file) : 0; }
static inline Sint64 SDL_SeekIO(SDL_IOStream *io, Sint64 offset, SDL_IOWhence whence)
{
    if (!io || fseek(io->file, (long)offset, (int)whence) != 0) return -1;
    return ftell(io->file);
}
static inline Sint64 SDL_TellIO(SDL_IOStream *io) { return io ? ftell(io->file) : -1; }
static inline Sint64 SDL_GetIOSize(SDL_IOStream *io)
{
    if (!io) return -1;
    long here = ftell(io->file);
    fseek(io->file, 0, 2);
    long size = ftell(io->file);
    fseek(io->file, here, 0);
    return size;
}
static inline bool SDL_FlushIO(SDL_IOStream *io) { return io && fflush(io->file) == 0; }
static inline bool SDL_CloseIO(SDL_IOStream *io)
{
    if (!io) return false;
    bool ok = fclose(io->file) == 0;
    if (io->wrote) sdlw_files_changed();
    free(io);
    return ok;
}
static inline void *SDL_LoadFile(const char *file, size_t *datasize)
{
    SDL_IOStream *io = SDL_IOFromFile(file, "rb");
    if (!io) return NULL;
    Sint64 size = SDL_GetIOSize(io);
    char *data = (char *)malloc((size_t)size + 1);
    size_t n = data ? SDL_ReadIO(io, data, (size_t)size) : 0;
    if (data) data[n] = 0;
    SDL_CloseIO(io);
    if (datasize) *datasize = n;
    return data;
}
static inline bool SDL_SaveFile(const char *file, const void *data, size_t datasize)
{
    SDL_IOStream *io = SDL_IOFromFile(file, "wb");
    if (!io) return false;
    bool ok = SDL_WriteIO(io, data, datasize) == datasize;
    return SDL_CloseIO(io) && ok;
}
/* Donde el juego guarda lo suyo (récords, opciones): prefs/org/app/, una carpeta por juego. */
static inline char *SDL_GetPrefPath(const char *org, const char *app)
{
    char *path = (char *)malloc(512);
    if (!path) return NULL;
    mkdir("prefs", 0755);
    SDL_snprintf(path, 512, "prefs/%s", org ? org : "");
    mkdir(path, 0755);
    SDL_snprintf(path, 512, "prefs/%s/%s", org ? org : "", app ? app : "");
    mkdir(path, 0755);
    SDL_strlcat(path, "/", 512);
    return path;
}
static inline const char *SDL_GetBasePath(void) { return "./"; }

/* Un .wav a memoria (SDL_LoadWAV): PCM de 8, 16 o 32 bits, o decimales de 32. */
static inline Uint32 sdlw_le32(const Uint8 *p) { return (Uint32)p[0] | (Uint32)p[1] << 8 | (Uint32)p[2] << 16 | (Uint32)p[3] << 24; }
static inline Uint16 sdlw_le16(const Uint8 *p) { return (Uint16)(p[0] | p[1] << 8); }
static inline bool SDL_LoadWAV(const char *path, SDL_AudioSpec *spec, Uint8 **audio_buf, Uint32 *audio_len)
{
    size_t size = 0;
    Uint8 *data = (Uint8 *)SDL_LoadFile(path, &size);
    if (!data) return false;
    bool ok = false, fmt = false;
    if (size >= 12 && memcmp(data, "RIFF", 4) == 0 && memcmp(data + 8, "WAVE", 4) == 0) {
        size_t at = 12;
        while (at + 8 <= size) {
            Uint32 len = sdlw_le32(data + at + 4);
            const Uint8 *chunk = data + at + 8;
            if (at + 8 + len > size) len = (Uint32)(size - at - 8);
            if (memcmp(data + at, "fmt ", 4) == 0 && len >= 16) {
                Uint16 kind = sdlw_le16(chunk), bits = sdlw_le16(chunk + 14);
                spec->channels = sdlw_le16(chunk + 2);
                spec->freq = (int)sdlw_le32(chunk + 4);
                spec->format = kind == 3 ? SDL_AUDIO_F32 : bits == 8 ? SDL_AUDIO_U8 : bits == 32 ? SDL_AUDIO_S32 : SDL_AUDIO_S16;
                fmt = true;
            } else if (memcmp(data + at, "data", 4) == 0 && fmt) {
                *audio_buf = (Uint8 *)malloc(len ? len : 1);
                if (*audio_buf) { memcpy(*audio_buf, chunk, len); *audio_len = len; ok = true; }
                break;
            }
            at += 8 + len + (len & 1);
        }
    }
    free(data);
    return ok;
}

/* ---------- Hilos y temporizadores (en la web se turnan con el juego en cada pausa) ---------- */

typedef struct SDL_Thread SDL_Thread;
typedef Uint64 SDL_ThreadID;
typedef int (*SDL_ThreadFunction)(void *data);
typedef Uint32 SDL_TimerID;
typedef Uint32 (*SDL_TimerCallback)(void *userdata, SDL_TimerID timerID, Uint32 interval);
typedef struct SDL_AtomicInt { int value; } SDL_AtomicInt;
typedef struct SDL_Mutex SDL_Mutex;

SDLW_IMPORT(thread_create) int sdlw_thread_create(SDL_ThreadFunction fn, void *data, void *stack_top);
SDLW_IMPORT(thread_wait) int sdlw_thread_wait(int thread);
SDLW_IMPORT(thread_current) Uint64 sdlw_thread_current(void);
SDLW_IMPORT(timer_add) Uint32 sdlw_timer_add(Uint32 interval, SDL_TimerCallback callback, void *userdata);
SDLW_IMPORT(timer_remove) bool sdlw_timer_remove(Uint32 id);
SDLW_IMPORT(mutex_lock) void sdlw_mutex_lock(void *mutex);
SDLW_IMPORT(mutex_unlock) void sdlw_mutex_unlock(void *mutex);

#define SDLW_THREAD_STACK (256 * 1024)

static inline SDL_Thread *SDL_CreateThread(SDL_ThreadFunction fn, const char *name, void *data)
{
    (void)name;
    Uint8 *stack = (Uint8 *)malloc(SDLW_THREAD_STACK);
    if (!stack) return NULL;
    /* la pila crece hacia abajo: el hilo arranca desde el final de su pedazo de memoria (alineado a 16) */
    int id = sdlw_thread_create(fn, data, (void *)(((uintptr_t)(stack + SDLW_THREAD_STACK)) & ~(uintptr_t)15));
    return id ? (SDL_Thread *)(uintptr_t)id : NULL;
}
static inline void SDL_WaitThread(SDL_Thread *thread, int *status)
{
    if (!thread) return;
    int result = sdlw_thread_wait((int)(uintptr_t)thread);
    if (status) *status = result;
}
static inline void SDL_DetachThread(SDL_Thread *thread) { (void)thread; }
static inline SDL_ThreadID SDL_GetCurrentThreadID(void) { return sdlw_thread_current(); }
static inline SDL_TimerID SDL_AddTimer(Uint32 interval, SDL_TimerCallback callback, void *userdata) { return sdlw_timer_add(interval, callback, userdata); }
static inline bool SDL_RemoveTimer(SDL_TimerID id) { return sdlw_timer_remove(id); }

static inline int SDL_SetAtomicInt(SDL_AtomicInt *a, int v) { int old = a->value; a->value = v; return old; }
static inline int SDL_GetAtomicInt(SDL_AtomicInt *a) { return a->value; }
static inline int SDL_AddAtomicInt(SDL_AtomicInt *a, int v) { int old = a->value; a->value += v; return old; }
static inline bool SDL_CompareAndSwapAtomicInt(SDL_AtomicInt *a, int oldval, int newval)
{
    if (a->value != oldval) return false;
    a->value = newval;
    return true;
}
#define SDL_AtomicIncRef(a) (SDL_AddAtomicInt(a, 1))
#define SDL_AtomicDecRef(a) (SDL_AddAtomicInt(a, -1) == 1)

static inline SDL_Mutex *SDL_CreateMutex(void) { return (SDL_Mutex *)calloc(1, 16); }
static inline void SDL_LockMutex(SDL_Mutex *m) { if (m) sdlw_mutex_lock(m); }
static inline void SDL_UnlockMutex(SDL_Mutex *m) { if (m) sdlw_mutex_unlock(m); }
static inline void SDL_DestroyMutex(SDL_Mutex *m) { free(m); }

/* ---------- Varios a la vez y los nombres de las teclas ---------- */

static inline bool SDL_RenderFillRects(SDL_Renderer *renderer, const SDL_FRect *rects, int count)
{
    for (int i = 0; i < count; i++) SDL_RenderFillRect(renderer, &rects[i]);
    return count >= 0;
}
static inline bool SDL_RenderRects(SDL_Renderer *renderer, const SDL_FRect *rects, int count)
{
    for (int i = 0; i < count; i++) SDL_RenderRect(renderer, &rects[i]);
    return count >= 0;
}
static inline bool SDL_RenderPoints(SDL_Renderer *renderer, const SDL_FPoint *points, int count)
{
    for (int i = 0; i < count; i++) SDL_RenderPoint(renderer, points[i].x, points[i].y);
    return count >= 0;
}
static inline bool SDL_RenderLines(SDL_Renderer *renderer, const SDL_FPoint *points, int count)
{
    for (int i = 0; i + 1 < count; i++) SDL_RenderLine(renderer, points[i].x, points[i].y, points[i + 1].x, points[i + 1].y);
    return count >= 0;
}

static inline SDL_Keycode SDL_GetKeyFromScancode(SDL_Scancode scancode, SDL_Keymod modstate, bool key_event)
{
    (void)modstate; (void)key_event;
    if (scancode >= SDL_SCANCODE_A && scancode <= SDL_SCANCODE_Z) return 'a' + (scancode - SDL_SCANCODE_A);
    if (scancode >= SDL_SCANCODE_1 && scancode <= SDL_SCANCODE_9) return '1' + (scancode - SDL_SCANCODE_1);
    switch (scancode) {
    case SDL_SCANCODE_0: return '0';
    case SDL_SCANCODE_RETURN: return SDLK_RETURN;
    case SDL_SCANCODE_ESCAPE: return SDLK_ESCAPE;
    case SDL_SCANCODE_BACKSPACE: return SDLK_BACKSPACE;
    case SDL_SCANCODE_TAB: return SDLK_TAB;
    case SDL_SCANCODE_SPACE: return SDLK_SPACE;
    default: return SDL_SCANCODE_TO_KEYCODE(scancode);
    }
}
static inline SDL_Scancode SDL_GetScancodeFromKey(SDL_Keycode key, SDL_Keymod *modstate)
{
    if (modstate) *modstate = 0;
    if (key & SDLK_SCANCODE_MASK) return (SDL_Scancode)(key & ~SDLK_SCANCODE_MASK);
    if (key >= 'a' && key <= 'z') return (SDL_Scancode)(SDL_SCANCODE_A + (key - 'a'));
    if (key >= '1' && key <= '9') return (SDL_Scancode)(SDL_SCANCODE_1 + (key - '1'));
    switch (key) {
    case '0': return SDL_SCANCODE_0;
    case SDLK_RETURN: return SDL_SCANCODE_RETURN;
    case SDLK_ESCAPE: return SDL_SCANCODE_ESCAPE;
    case SDLK_BACKSPACE: return SDL_SCANCODE_BACKSPACE;
    case SDLK_TAB: return SDL_SCANCODE_TAB;
    case SDLK_SPACE: return SDL_SCANCODE_SPACE;
    default: return SDL_SCANCODE_UNKNOWN;
    }
}
/* El nombre de una tecla, como lo da SDL3 («A», «Space», «Up», «Left Shift»…). */
static inline const char *SDL_GetScancodeName(SDL_Scancode scancode)
{
    static const char *const letters[] = { "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z" };
    static const char *const digits[] = { "1","2","3","4","5","6","7","8","9","0" };
    static const char *const fkeys[] = { "F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12" };
    static const char *const keypad[] = { "Keypad /","Keypad *","Keypad -","Keypad +","Keypad Enter","Keypad 1","Keypad 2","Keypad 3","Keypad 4","Keypad 5","Keypad 6","Keypad 7","Keypad 8","Keypad 9","Keypad 0","Keypad ." };
    if (scancode >= SDL_SCANCODE_A && scancode <= SDL_SCANCODE_Z) return letters[scancode - SDL_SCANCODE_A];
    if (scancode >= SDL_SCANCODE_1 && scancode <= SDL_SCANCODE_0) return digits[scancode - SDL_SCANCODE_1];
    if (scancode >= SDL_SCANCODE_F1 && scancode <= SDL_SCANCODE_F12) return fkeys[scancode - SDL_SCANCODE_F1];
    if (scancode >= SDL_SCANCODE_KP_DIVIDE && scancode <= SDL_SCANCODE_KP_PERIOD) return keypad[scancode - SDL_SCANCODE_KP_DIVIDE];
    switch (scancode) {
    case SDL_SCANCODE_RETURN: return "Return";
    case SDL_SCANCODE_ESCAPE: return "Escape";
    case SDL_SCANCODE_BACKSPACE: return "Backspace";
    case SDL_SCANCODE_TAB: return "Tab";
    case SDL_SCANCODE_SPACE: return "Space";
    case SDL_SCANCODE_PAUSE: return "Pause";
    case SDL_SCANCODE_RIGHT: return "Right";
    case SDL_SCANCODE_LEFT: return "Left";
    case SDL_SCANCODE_DOWN: return "Down";
    case SDL_SCANCODE_UP: return "Up";
    case SDL_SCANCODE_LCTRL: return "Left Ctrl";
    case SDL_SCANCODE_LSHIFT: return "Left Shift";
    case SDL_SCANCODE_LALT: return "Left Alt";
    case SDL_SCANCODE_RCTRL: return "Right Ctrl";
    case SDL_SCANCODE_RSHIFT: return "Right Shift";
    case SDL_SCANCODE_RALT: return "Right Alt";
    default: return "";
    }
}
static inline const char *SDL_GetKeyName(SDL_Keycode key) { return SDL_GetScancodeName(SDL_GetScancodeFromKey(key, NULL)); }

#endif
