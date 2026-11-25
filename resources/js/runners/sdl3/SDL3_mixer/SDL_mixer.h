/* SDL3_mixer de la plataforma (D126): música y efectos (WAV, OGG, MP3) que suenan con el audio del navegador.
 * Mismos nombres que SDL3_mixer 3.x: un mixer, audios cargados, pistas (tracks) y «disparar y olvidar». */
#ifndef SDL_MIXER_PLATAFORMA_H
#define SDL_MIXER_PLATAFORMA_H
#include <SDL3/SDL.h>

#define SDL_MIXER_MAJOR_VERSION 3
#define SDL_MIXER_MINOR_VERSION 1
#define SDL_MIXER_MICRO_VERSION 0
#define MIX_PROP_PLAY_LOOPS_NUMBER "SDL_mixer.play.loops"

typedef struct MIX_Mixer MIX_Mixer;
typedef struct MIX_Audio MIX_Audio;
typedef struct MIX_Track MIX_Track;

SDLW_IMPORT(mix_create) int sdlw_mix_create(void);
SDLW_IMPORT(mix_audio_pcm) int sdlw_mix_audio_pcm(int format, int channels, int freq, const void *data, int length);
SDLW_IMPORT(mix_audio_encoded) int sdlw_mix_audio_encoded(const void *data, int length);
SDLW_IMPORT(mix_audio_sine) int sdlw_mix_audio_sine(int hz, float amplitude, int ms);
SDLW_IMPORT(mix_track) int sdlw_mix_track(int mixer);
SDLW_IMPORT(mix_control) bool sdlw_mix_control(int what, int id, int arg, float value);

#define SDLW_MIX_SET_AUDIO 1
#define SDLW_MIX_PLAY 2
#define SDLW_MIX_PAUSE 3
#define SDLW_MIX_RESUME 4
#define SDLW_MIX_STOP 5
#define SDLW_MIX_GAIN 6
#define SDLW_MIX_PLAYING 7
#define SDLW_MIX_FIRE 8
#define SDLW_MIX_DESTROY_AUDIO 9
#define SDLW_MIX_DESTROY_TRACK 10
#define SDLW_MIX_DESTROY_MIXER 11
#define SDLW_MIX_MASTER_GAIN 12

static inline int sdlw_mix_id(const void *handle) { return (int)(uintptr_t)handle; }
static inline int MIX_Version(void) { return SDL_VERSIONNUM(SDL_MIXER_MAJOR_VERSION, SDL_MIXER_MINOR_VERSION, SDL_MIXER_MICRO_VERSION); }
static inline bool MIX_Init(void) { return true; }
static inline void MIX_Quit(void) {}
static inline MIX_Mixer *MIX_CreateMixerDevice(SDL_AudioDeviceID devid, const SDL_AudioSpec *spec)
{
    (void)devid; (void)spec;
    return (MIX_Mixer *)(uintptr_t)sdlw_mix_create();
}
static inline void MIX_DestroyMixer(MIX_Mixer *mixer) { if (mixer) sdlw_mix_control(SDLW_MIX_DESTROY_MIXER, sdlw_mix_id(mixer), 0, 0); }
static inline bool MIX_SetMasterGain(MIX_Mixer *mixer, float gain) { return mixer && sdlw_mix_control(SDLW_MIX_MASTER_GAIN, sdlw_mix_id(mixer), 0, gain); }
/* Un .wav lo lee la plataforma (como SDL_LoadWAV); un .ogg o .mp3 lo decodifica el navegador. */
static inline MIX_Audio *MIX_LoadAudio(MIX_Mixer *mixer, const char *path, bool predecode)
{
    (void)mixer; (void)predecode;
    SDL_AudioSpec spec;
    Uint8 *buf = NULL;
    Uint32 len = 0;
    if (SDL_LoadWAV(path, &spec, &buf, &len)) {
        int id = sdlw_mix_audio_pcm((int)spec.format, spec.channels, spec.freq, buf, (int)len);
        free(buf);
        return (MIX_Audio *)(uintptr_t)id;
    }
    size_t size = 0;
    void *data = SDL_LoadFile(path, &size);
    if (!data) return NULL;
    int id = sdlw_mix_audio_encoded(data, (int)size);
    free(data);
    return (MIX_Audio *)(uintptr_t)id;
}
static inline MIX_Audio *MIX_CreateSineWaveAudio(MIX_Mixer *mixer, int hz, float amplitude, Sint64 ms)
{
    (void)mixer;
    return (MIX_Audio *)(uintptr_t)sdlw_mix_audio_sine(hz, amplitude, (int)ms);
}
static inline void MIX_DestroyAudio(MIX_Audio *audio) { if (audio) sdlw_mix_control(SDLW_MIX_DESTROY_AUDIO, sdlw_mix_id(audio), 0, 0); }
static inline MIX_Track *MIX_CreateTrack(MIX_Mixer *mixer) { return mixer ? (MIX_Track *)(uintptr_t)sdlw_mix_track(sdlw_mix_id(mixer)) : NULL; }
static inline void MIX_DestroyTrack(MIX_Track *track) { if (track) sdlw_mix_control(SDLW_MIX_DESTROY_TRACK, sdlw_mix_id(track), 0, 0); }
static inline bool MIX_SetTrackAudio(MIX_Track *track, MIX_Audio *audio) { return track && sdlw_mix_control(SDLW_MIX_SET_AUDIO, sdlw_mix_id(track), sdlw_mix_id(audio), 0); }
/* Las vueltas: 0 = una vez, n = n vueltas más, -1 = para siempre (MIX_PROP_PLAY_LOOPS_NUMBER). */
static inline bool MIX_PlayTrack(MIX_Track *track, SDL_PropertiesID options)
{
    int loops = (int)SDL_GetNumberProperty(options, MIX_PROP_PLAY_LOOPS_NUMBER, 0);
    return track && sdlw_mix_control(SDLW_MIX_PLAY, sdlw_mix_id(track), loops, 0);
}
static inline bool MIX_PlayAudio(MIX_Mixer *mixer, MIX_Audio *audio) { return mixer && audio && sdlw_mix_control(SDLW_MIX_FIRE, sdlw_mix_id(mixer), sdlw_mix_id(audio), 0); }
static inline bool MIX_StopTrack(MIX_Track *track, Sint64 fade_out_frames) { (void)fade_out_frames; return track && sdlw_mix_control(SDLW_MIX_STOP, sdlw_mix_id(track), 0, 0); }
static inline bool MIX_PauseTrack(MIX_Track *track) { return track && sdlw_mix_control(SDLW_MIX_PAUSE, sdlw_mix_id(track), 0, 0); }
static inline bool MIX_ResumeTrack(MIX_Track *track) { return track && sdlw_mix_control(SDLW_MIX_RESUME, sdlw_mix_id(track), 0, 0); }
static inline bool MIX_TrackPlaying(MIX_Track *track) { return track && sdlw_mix_control(SDLW_MIX_PLAYING, sdlw_mix_id(track), 0, 0); }
static inline bool MIX_SetTrackGain(MIX_Track *track, float gain) { return track && sdlw_mix_control(SDLW_MIX_GAIN, sdlw_mix_id(track), 0, gain); }

#endif
