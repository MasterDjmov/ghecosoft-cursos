<?php

use App\Enums\XpReason;
use App\Models\Branch;
use App\Models\Course;
use App\Models\Node;
use App\Models\RankingSnapshot;
use App\Models\User;
use App\Services\Ledger;
use App\Services\Ranking;
use App\Services\TreeEditor;
use Illuminate\Support\Facades\Cache;

/** Landing pública: cursos, "Próximamente" y top 10 de héroes (sin datos de acceso). */
function publicHero(string $username, string $name, ?string $hero, int $xp, array $overrides = []): User
{
    $user = User::factory()->create([
        'username' => $username, 'name' => $name, 'last_name' => 'Pérez', 'hero_name' => $hero,
        'cv_public' => true, 'birth_date' => now()->subYears(25), ...$overrides,
    ]);
    app(Ledger::class)->addXp($user, $xp, XpReason::ManualAdjustment, note: 'test');
    Ranking::forget();

    return $user;
}

test('a quien no entró le muestra la landing; a quien entró, su inicio', function () {
    $this->get('/')->assertOk()->assertSee('árbol de habilidades')->assertSee('Entrá a tu cuenta');
    $this->actingAs(User::factory()->create())->get('/')->assertRedirect(route('home'));
});

test('muestra los destacados y los "Próximamente", nunca los borradores', function () {
    makeCourse(['title' => 'Python destacado', 'is_featured' => true, 'syllabus' => "Bucles\nFunciones"]);
    ['course' => $other] = makeCourse(['title' => 'Otro publicado']);
    app(TreeEditor::class)->createCourse(['title' => 'C que viene', 'slug' => 'c', 'language' => 'c', 'is_upcoming' => true]);
    Course::create(['title' => 'Borrador secreto', 'slug' => 'secreto']);

    $this->get('/')->assertOk()
        ->assertSeeInOrder(['Python destacado', 'Bucles', 'Probar gratis', 'Próximamente', 'C que viene'])
        ->assertDontSee('catalog-'.$other->slug) // hay destacados: solo esos (su moneda sí se ve)
        ->assertDontSee('Borrador secreto');
});

test('el top muestra héroe, nombre de ranking y XP, nunca el usuario de login', function () {
    publicHero('login_secreto', 'Luna', 'Kirana', 500);
    publicHero('otro_login', 'Tomás', null, 300);
    User::factory()->create(['username' => 'privado', 'name' => 'Privada', 'cv_public' => false, 'xp_total' => 999]);
    publicHero('menor_login', 'Menor', 'Chiquito', 800, ['birth_date' => now()->subYears(14)]);

    $this->get('/')->assertOk()
        ->assertSeeInOrder(['Top 10 de héroes', 'Tomás P.', '300', 'Kirana', 'Luna P.', '500']) // podio: 2.º, 1.º, 3.º
        ->assertDontSee('login_secreto')
        ->assertDontSee('otro_login')
        ->assertDontSee('Privada')
        ->assertDontSee('Chiquito'); // menor sin autorización aprobada
});

test('la tendencia compara con la foto del día anterior, que se toma sola', function () {
    $climber = publicHero('sube', 'Ana', 'Subidora', 900);
    $faller = publicHero('baja', 'Beto', 'Bajador', 500);
    $newcomer = publicHero('nuevo', 'Caro', 'Recién', 100);
    RankingSnapshot::insert([
        ['taken_on' => today()->subDays(2)->toDateString(), 'user_id' => $climber->id, 'position' => 2],
        ['taken_on' => today()->subDays(2)->toDateString(), 'user_id' => $faller->id, 'position' => 1],
    ]);

    $top = app(Ranking::class)->publicTop();

    expect($top->firstWhere('hero', 'Subidora'))->toMatchArray(['position' => 1, 'trend' => 1, 'new' => false])
        ->and($top->firstWhere('hero', 'Bajador'))->toMatchArray(['position' => 2, 'trend' => -1])
        ->and($top->firstWhere('hero', 'Recién')['new'])->toBeTrue()
        ->and(RankingSnapshot::whereDate('taken_on', today())->count())->toBe(3);

    // La foto de hoy se toma una sola vez.
    app(Ranking::class)->publicTop();
    expect(RankingSnapshot::whereDate('taken_on', today())->count())->toBe(3);
});

test('el ranking sale bien del caché aunque el caché no deserialice clases', function () {
    config(['cache.stores.array.serialize' => true, 'cache.serializable_classes' => false]);
    Cache::forgetDriver('array');
    publicHero('uno', 'Luna', 'Kirana', 500);

    expect(app(Ranking::class)->global())->toHaveCount(1)
        ->and(app(Ranking::class)->global()->first()['hero'])->toBe('Kirana');
});

test('el temario completo se abre en un modal, con las Sendas como opcionales y sin títulos de clases', function () {
    ['course' => $course, 'topic1' => $topic1] = makeCourse(['syllabus' => implode("\n", ['Uno', 'Dos', 'Tres', 'Cuatro', 'Cinco', 'Referencias y `std::vector`', 'Siete <b>']), 'is_featured' => true]);
    $path = Branch::create(['course_id' => $course->id, 'code' => 'S01', 'title' => 'Senda de la Arena: videojuegos con pygame', 'kind' => 'path', 'position' => 5]);
    Node::create(['course_id' => $course->id, 'branch_id' => $path->id, 'parent_id' => $topic1->id, 'type' => 'topic', 'title' => 'Sprites secretos', 'price' => 5]);
    $hidden = Branch::create(['course_id' => $course->id, 'code' => 'S02', 'title' => 'Senda vacía: sin nodos', 'kind' => 'path', 'position' => 6]);

    $this->get('/')->assertOk()
        ->assertSee('data-test="syllabus-'.$course->slug.'"', false)
        ->assertSee('y 2 temas más · + 1 Senda opcional')
        ->assertSee('Referencias y <code>std::vector</code>', false)
        ->assertSee('Siete &lt;b&gt;', false)
        ->assertSee('Senda de la Arena')
        ->assertSee('videojuegos con pygame')
        ->assertDontSee('Senda vacía')
        ->assertDontSee('Sprites secretos');
});
