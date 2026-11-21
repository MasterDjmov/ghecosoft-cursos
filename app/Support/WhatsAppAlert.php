<?php

namespace App\Support;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;
use Throwable;

/**
 * Avisos al WhatsApp del docente con CallMeBot (config services.callmebot). Solo el aviso corto (quién y qué, con
 * el link): nunca el mail, el teléfono ni otros datos del alumno, porque pasa por un servicio de afuera. Se manda
 * después de responder (no demora al alumno) y si falla no rompe nada: queda en el log.
 */
class WhatsAppAlert
{
    public static function enabled(): bool
    {
        return filled(config('services.callmebot.phone')) && filled(config('services.callmebot.apikey'));
    }

    /** Lo deja para después de responder la página. */
    public static function queue(string $text): void
    {
        if (self::enabled()) {
            dispatch(fn () => self::send($text))->afterResponse();
        }
    }

    /** Lo manda ya; devuelve si CallMeBot lo aceptó. */
    public static function send(string $text): bool
    {
        if (! self::enabled()) {
            return false;
        }

        try {
            $response = Http::timeout(10)->get('https://api.callmebot.com/whatsapp.php', [
                'phone' => config('services.callmebot.phone'),
                'text' => $text,
                'apikey' => config('services.callmebot.apikey'),
            ]);
            if ($response->successful()) {
                return true;
            }
            Log::warning('CallMeBot no mandó el aviso', ['status' => $response->status(), 'body' => mb_substr($response->body(), 0, 300)]);
        } catch (Throwable $e) {
            Log::warning('CallMeBot no respondió', ['error' => $e->getMessage()]);
        }

        return false;
    }
}
