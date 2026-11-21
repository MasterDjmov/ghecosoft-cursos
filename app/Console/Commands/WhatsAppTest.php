<?php

namespace App\Console\Commands;

use App\Support\WhatsAppAlert;
use Illuminate\Console\Command;

/** Prueba los avisos al WhatsApp (CallMeBot): manda un mensaje de prueba al número del .env. */
class WhatsAppTest extends Command
{
    protected $signature = 'app:whatsapp-test';

    protected $description = 'Manda un aviso de prueba al WhatsApp del docente (CallMeBot)';

    public function handle(): int
    {
        if (! WhatsAppAlert::enabled()) {
            $this->error('Faltan CALLMEBOT_PHONE y CALLMEBOT_APIKEY en el .env (ver docs/DEPLOY.md).');

            return self::FAILURE;
        }
        if (! WhatsAppAlert::send('*'.config('app.name').'*: prueba de avisos. Si te llegó, ya te van a avisar las cuentas nuevas y los pedidos de abono.')) {
            $this->error('CallMeBot no lo aceptó: revisá el número y la clave (detalle en storage/logs).');

            return self::FAILURE;
        }
        $this->info('Listo: revisá tu WhatsApp.');

        return self::SUCCESS;
    }
}
