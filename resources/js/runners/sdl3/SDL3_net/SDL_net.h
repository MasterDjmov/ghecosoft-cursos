/* SDL3_net de la plataforma (D126): una RED DE MENTIRA. En la página no hay red de verdad (regla de la plataforma):
 * los juegos de la misma página se conectan entre sí por el número de puerto, como si fueran todos la misma compu
 * («localhost»). Así se aprende cliente y servidor igual; para jugar entre dos compus, se baja el juego.
 * Mismos nombres que SDL3_net 3.x (sockets de flujo, TCP). */
#ifndef SDL_NET_PLATAFORMA_H
#define SDL_NET_PLATAFORMA_H
#include <SDL3/SDL.h>

#define SDL_NET_MAJOR_VERSION 3
#define SDL_NET_MINOR_VERSION 2
#define SDL_NET_MICRO_VERSION 0

typedef enum NET_Status { NET_FAILURE = -1, NET_WAITING = 0, NET_SUCCESS = 1 } NET_Status;
typedef struct NET_Address { char host[256]; int refcount; } NET_Address;
typedef struct NET_StreamSocket NET_StreamSocket;
typedef struct NET_Server NET_Server;

SDLW_IMPORT(net_listen) int sdlw_net_listen(int port);
SDLW_IMPORT(net_unlisten) void sdlw_net_unlisten(int server);
SDLW_IMPORT(net_accept) int sdlw_net_accept(int server);
SDLW_IMPORT(net_connect) int sdlw_net_connect(int port);
SDLW_IMPORT(net_wait_connected) int sdlw_net_wait_connected(int sock, int timeout);
SDLW_IMPORT(net_status) int sdlw_net_status(int sock);
SDLW_IMPORT(net_write) bool sdlw_net_write(int sock, const void *buf, int length);
SDLW_IMPORT(net_read) int sdlw_net_read(int sock, void *buf, int length);
SDLW_IMPORT(net_close) void sdlw_net_close(int sock);
SDLW_IMPORT(net_wait_input) int sdlw_net_wait_input(const int *ids, int count, int timeout);

static inline int sdlw_net_id(const void *handle) { return (int)(uintptr_t)handle; }
static inline int NET_Version(void) { return SDL_VERSIONNUM(SDL_NET_MAJOR_VERSION, SDL_NET_MINOR_VERSION, SDL_NET_MICRO_VERSION); }
static inline bool NET_Init(void) { return true; }
static inline void NET_Quit(void) {}

/* Cualquier nombre «resuelve» en la red de mentira: todas las ventanas de la página son la misma compu. */
static inline NET_Address *NET_ResolveHostname(const char *host)
{
    if (!host || !*host) return NULL;
    NET_Address *a = (NET_Address *)calloc(1, sizeof(NET_Address));
    if (a) { SDL_strlcpy(a->host, host, sizeof a->host); a->refcount = 1; }
    return a;
}
static inline NET_Status NET_WaitUntilResolved(NET_Address *address, Sint32 timeout) { (void)timeout; return address ? NET_SUCCESS : NET_FAILURE; }
static inline NET_Status NET_GetAddressStatus(NET_Address *address) { return address ? NET_SUCCESS : NET_FAILURE; }
static inline const char *NET_GetAddressString(NET_Address *address) { return address ? address->host : NULL; }
static inline NET_Address *NET_RefAddress(NET_Address *address) { if (address) address->refcount++; return address; }
static inline void NET_UnrefAddress(NET_Address *address) { if (address && --address->refcount <= 0) free(address); }
static inline int NET_CompareAddresses(const NET_Address *a, const NET_Address *b) { return strcmp(a->host, b->host); }

static inline NET_Server *NET_CreateServer(NET_Address *addr, Uint16 port, SDL_PropertiesID props)
{
    (void)addr; (void)props;
    return (NET_Server *)(uintptr_t)sdlw_net_listen(port);
}
static inline void NET_DestroyServer(NET_Server *server) { if (server) sdlw_net_unlisten(sdlw_net_id(server)); }
/* No espera: si nadie se conectó todavía, deja *client_stream en NULL. */
static inline bool NET_AcceptClient(NET_Server *server, NET_StreamSocket **client_stream)
{
    if (!server || !client_stream) return false;
    *client_stream = (NET_StreamSocket *)(uintptr_t)sdlw_net_accept(sdlw_net_id(server));
    return true;
}
static inline NET_StreamSocket *NET_CreateClient(NET_Address *address, Uint16 port, SDL_PropertiesID props)
{
    (void)props;
    if (!address) return NULL;
    return (NET_StreamSocket *)(uintptr_t)sdlw_net_connect(port);
}
static inline NET_Status NET_WaitUntilConnected(NET_StreamSocket *sock, Sint32 timeout) { return sock ? (NET_Status)sdlw_net_wait_connected(sdlw_net_id(sock), timeout) : NET_FAILURE; }
static inline NET_Status NET_GetConnectionStatus(NET_StreamSocket *sock) { return sock ? (NET_Status)sdlw_net_status(sdlw_net_id(sock)) : NET_FAILURE; }
static inline bool NET_WriteToStreamSocket(NET_StreamSocket *sock, const void *buf, int buflen) { return sock && sdlw_net_write(sdlw_net_id(sock), buf, buflen); }
static inline int NET_GetStreamSocketPendingWrites(NET_StreamSocket *sock) { return sock ? 0 : -1; }
static inline int NET_WaitUntilStreamSocketDrained(NET_StreamSocket *sock, Sint32 timeout) { (void)timeout; return sock ? 0 : -1; }
/* Devuelve cuántos bytes leyó (0 si no llegó nada todavía) o -1 si la otra punta se fue. */
static inline int NET_ReadFromStreamSocket(NET_StreamSocket *sock, void *buf, int buflen) { return sock ? sdlw_net_read(sdlw_net_id(sock), buf, buflen) : -1; }
static inline void NET_DestroyStreamSocket(NET_StreamSocket *sock) { if (sock) sdlw_net_close(sdlw_net_id(sock)); }
static inline NET_Address *NET_GetStreamSocketAddress(NET_StreamSocket *sock) { return sock ? NET_ResolveHostname("127.0.0.1") : NULL; }
static inline int NET_WaitUntilInputAvailable(void **vsockets, int numsockets, Sint32 timeout)
{
    int ids[64];
    int n = numsockets < 64 ? numsockets : 64;
    for (int i = 0; i < n; i++) ids[i] = sdlw_net_id(vsockets[i]);
    return sdlw_net_wait_input(ids, n, timeout);
}

#endif
