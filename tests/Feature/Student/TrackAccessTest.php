<?php

use App\Models\User;
use App\Support\DeviceInfo;
use Illuminate\Support\Facades\DB;

/* Desde dónde entran los alumnos: una fila por día y dispositivo; el staff no se anota. */

test('lee celular, tablet y compu del user agent', function () {
    expect(DeviceInfo::parse('Mozilla/5.0 (Linux; Android 13; SM-A135M) AppleWebKit/537.36 Chrome/120.0 Mobile Safari/537.36'))
        ->toBe(['device' => 'mobile', 'os' => 'android', 'browser' => 'chrome'])
        ->and(DeviceInfo::parse('Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Version/17.0 Safari/604.1'))
        ->toBe(['device' => 'tablet', 'os' => 'ios', 'browser' => 'safari'])
        ->and(DeviceInfo::parse('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36 Edg/120.0'))
        ->toBe(['device' => 'desktop', 'os' => 'windows', 'browser' => 'edge'])
        ->and(DeviceInfo::parse(null)['device'])->toBe('otro');
});

test('anota al alumno una vez por sesión y por día, y no al staff', function () {
    $student = User::factory()->create();
    $phone = ['User-Agent' => 'Mozilla/5.0 (Linux; Android 13) Chrome/120.0 Mobile Safari/537.36'];

    $this->actingAs($student)->withHeaders($phone)->get(route('student.worlds'));
    $this->actingAs($student)->withHeaders($phone)->get(route('student.worlds'));

    $rows = DB::table('user_accesses')->where('user_id', $student->id)->get();
    expect($rows)->toHaveCount(1)
        ->and($rows->first()->device)->toBe('mobile')
        ->and($rows->first()->requests)->toBe(1);

    $admin = User::factory()->admin()->create();
    $this->actingAs($admin)->get(route('admin.dashboard'));
    expect(DB::table('user_accesses')->where('user_id', $admin->id)->exists())->toBeFalse();
});
