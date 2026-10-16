<?php

namespace App\Support;

/**
 * Lee el user agent sin paquetes: alcanza para separar celular, tablet y compu, y el sistema y el navegador
 * más comunes. Lo que no reconoce queda como «otro».
 */
class DeviceInfo
{
    /** @return array{device: string, os: string, browser: string} */
    public static function parse(?string $agent): array
    {
        $ua = (string) $agent;

        $os = match (true) {
            (bool) preg_match('/Windows/i', $ua) => 'windows',
            (bool) preg_match('/Android/i', $ua) => 'android',
            (bool) preg_match('/iPhone|iPad|iPod/i', $ua) => 'ios',
            (bool) preg_match('/CrOS/i', $ua) => 'chromeos',
            (bool) preg_match('/Mac OS X|Macintosh/i', $ua) => 'macos',
            (bool) preg_match('/Linux/i', $ua) => 'linux',
            default => 'otro',
        };

        $device = match (true) {
            (bool) preg_match('/iPad|Tablet|PlayBook|Silk/i', $ua) => 'tablet',
            $os === 'android' && ! preg_match('/Mobile/i', $ua) => 'tablet',
            (bool) preg_match('/Mobi|iPhone|iPod|Android/i', $ua) => 'mobile',
            $ua === '' => 'otro',
            default => 'desktop',
        };

        $browser = match (true) {
            (bool) preg_match('/Edg\//i', $ua) => 'edge',
            (bool) preg_match('/OPR\/|Opera/i', $ua) => 'opera',
            (bool) preg_match('/SamsungBrowser/i', $ua) => 'samsung',
            (bool) preg_match('/Firefox|FxiOS/i', $ua) => 'firefox',
            (bool) preg_match('/Chrome|CriOS/i', $ua) => 'chrome',
            (bool) preg_match('/Safari/i', $ua) => 'safari',
            default => 'otro',
        };

        return ['device' => $device, 'os' => $os, 'browser' => $browser];
    }
}
