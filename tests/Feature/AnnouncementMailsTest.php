<?php

use App\Livewire\Settings\Alerts;
use App\Models\User;
use App\Notifications\PlatformNotification;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\URL;
use Livewire\Livewire;

// D113: baja de los mails «Avisame» y borrado de los registros de acceso viejos.

function releaseNotice(): PlatformNotification
{
    return new PlatformNotification('course.released', '¡Ya salió C!', 'Pediste que te avisemos.', 'https://example.test', 'rocket-launch');
}

test('el mail de «Avisame» trae el remitente y el link de baja; los de la cuenta no', function () {
    $user = User::factory()->create(['email' => 'kira@example.test']);

    $mail = implode("\n", releaseNotice()->toMail($user)->outroLines);
    expect($mail)->toContain(config('legal.email'))->toContain('/avisos/baja/'.$user->id);

    $account = new PlatformNotification('submission.reviewed', 'Te corrigieron', 'Mirá la corrección.', 'https://example.test');
    expect($account->toMail($user)->outroLines)->toBe([]);
});

test('el link firmado pide confirmar y después los avisos quedan solo en la campanita', function () {
    $user = User::factory()->create(['email' => 'kira@example.test']);
    $url = URL::signedRoute('announcements.mute', $user);

    $this->get($url)->assertOk()->assertSee('data-test="mute-announcements-button"', false);
    expect($user->fresh()->announcements_muted_at)->toBeNull();

    $this->post($url)->assertOk()->assertSee('data-test="announcements-muted"', false);
    $user->refresh();
    expect($user->announcements_muted_at)->not->toBeNull()
        ->and(releaseNotice()->via($user))->toBe(['database']);

    // Los de la cuenta siguen por el canal de siempre.
    $account = new PlatformNotification('submission.reviewed', 'Te corrigieron', 'Mirá la corrección.', 'https://example.test');
    expect($account->via($user))->not->toBe([])->toContain('database');
});

test('sin firma o con otra cuenta en la firma, el link no sirve', function () {
    $user = User::factory()->create();
    $other = User::factory()->create();

    $this->get(route('announcements.mute', $user))->assertForbidden();
    $this->post(str_replace('/avisos/baja/'.$user->id, '/avisos/baja/'.$other->id, URL::signedRoute('announcements.mute', $user)))->assertForbidden();
    expect($other->fresh()->announcements_muted_at)->toBeNull();
});

test('en Mi cuenta → Avisos se apagan y se vuelven a prender', function () {
    $user = User::factory()->create(['email' => 'kira@example.test']);

    Livewire::actingAs($user)->test(Alerts::class)->assertSet('announcement_mails', true)
        ->set('announcement_mails', false)->call('save');
    expect($user->fresh()->announcements_muted_at)->not->toBeNull();

    Livewire::actingAs($user->fresh())->test(Alerts::class)->assertSet('announcement_mails', false)
        ->set('announcement_mails', true)->call('save');
    expect($user->fresh()->announcements_muted_at)->toBeNull();
});

test('app:prune-access-logs borra IP y navegador de más de 12 meses', function () {
    $user = User::factory()->create();
    DB::table('session_evictions')->insert([
        ['user_id' => $user->id, 'ip' => '1.1.1.1', 'user_agent' => 'viejo', 'created_at' => now()->subMonths(13)],
        ['user_id' => $user->id, 'ip' => '2.2.2.2', 'user_agent' => 'nuevo', 'created_at' => now()->subMonths(2)],
    ]);
    foreach ([now()->subMonths(13), now()->subDay()] as $day) {
        DB::table('user_accesses')->insert(['user_id' => $user->id, 'accessed_on' => $day->toDateString(), 'device' => 'mobile', 'os' => 'android', 'browser' => 'chrome', 'first_at' => $day, 'last_at' => $day]);
    }

    $this->artisan('app:prune-access-logs')->assertSuccessful();

    expect(DB::table('session_evictions')->pluck('user_agent')->all())->toBe(['nuevo'])
        ->and(DB::table('user_accesses')->count())->toBe(1);
});
