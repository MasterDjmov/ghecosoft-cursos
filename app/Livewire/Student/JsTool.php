<?php

namespace App\Livewire\Student;

use App\Enums\Language;
use App\Livewire\Student\Concerns\RendersToolPage;
use App\Models\Course;
use App\Models\User;
use Livewire\Attributes\Title;
use Livewire\Component;

/**
 * Herramientas → La caja de la Feria (D115): JavaScript suelto, para practicar fuera de las micro-misiones, con
 * ejemplos de todo lo que simula la caja (la consola, el reloj, el Puerto, las cookies, la página y el lienzo).
 * Corre en el navegador de quien la usa, en la caja sin mismo origen ni red. El staff la usa siempre (para probar
 * la caja antes de que exista el curso); el alumno, con el abono vigente de un curso de JavaScript.
 */
#[Title('La caja de la Feria')]
class JsTool extends Component
{
    use RendersToolPage;

    /** Los ejemplos: título, qué muestra, el código y, si es una página, su HTML. */
    public const EXAMPLES = [
        'consola' => [
            'title' => 'La consola',
            'about' => 'Valores, objetos y la coerción del Goblin. Probá también un error: escribí mal un nombre.',
            'code' => <<<'JS'
                const nima = { nombre: 'Nima', nivel: 1, inventario: ['soga', 'brújula', 'pan'] };
                console.log(`Hola, ${nima.nombre}`);
                console.log(nima);
                console.log('2' + 2, '2' * 2);   // el Goblin de la Coerción
                const precios = [2, 1, 3, 2];
                console.log(precios.map((p) => p * 10), precios.reduce((a, b) => a + b, 0));
                JS,
        ],
        'reloj' => [
            'title' => 'El reloj y las flechas de luz',
            'about' => 'setTimeout, setInterval y await avanzan con el reloj de la caja: 10 segundos pasan en un instante, y siempre igual.',
            'code' => <<<'JS'
                const esperar = (ms) => new Promise((listo) => setTimeout(listo, ms));

                console.log('Nima suelta la flecha…');
                setTimeout(() => console.log('…y la flecha llega (2 s después).'), 2000);

                let faroles = 0;
                const id = setInterval(() => {
                    faroles++;
                    console.log(`Farol ${faroles} prendido a los ${performance.now()} ms`);
                    if (faroles === 3) clearInterval(id);
                }, 500);

                await esperar(3000);
                console.log('Pasaron 3 segundos del reloj de la Feria.');
                JS,
        ],
        'puerto' => [
            'title' => 'El Puerto de Elefa (fetch sin internet)',
            'about' => 'fetch le pide al Puerto simulado (/puerto/hola, /puerto/puestos, /puerto/lento, /puerto/error, /puerto/login…). Mirá el Tablero: los pedidos y la cookie de la sesión.',
            'code' => <<<'JS'
                const respuesta = await fetch('/puerto/hola');
                const carta = await respuesta.json();
                console.log(carta.de, 'dice:', carta.mensaje);

                const puestos = await (await fetch('/puerto/puestos')).json();
                console.log(puestos.filter((p) => p.abierto).map((p) => p.nombre));

                // Iniciar sesión: el Puerto guarda una cookie HttpOnly (document.cookie no la ve).
                await fetch('/puerto/login', { method: 'POST', body: JSON.stringify({ usuario: 'nima', clave: 'luciernaga' }) });
                const perfil = await (await fetch('/puerto/perfil')).json();
                console.log('Sesión de', perfil.nombre, '· document.cookie:', JSON.stringify(document.cookie));

                localStorage.setItem('ultimaVisita', new Date().toISOString());
                document.cookie = 'tema=noche; max-age=3600';
                JS,
        ],
        'pagina' => [
            'title' => 'La página y los eventos',
            'about' => 'La página corre en vivo: tocá los botones. Lo que guarda queda en el Tablero.',
            'page' => <<<'HTML'
                <style>
                  body { font-family: system-ui, sans-serif; background: #0b1020; color: #f5f0e0; padding: 16px; }
                  .farol { display: inline-block; width: 36px; height: 36px; margin: 4px; border-radius: 50%; background: #333; transition: background .3s; }
                  .farol.prendido { background: #ffd400; box-shadow: 0 0 18px #ffd400; }
                  button { font-size: 16px; padding: 6px 12px; margin-top: 12px; }
                </style>
                <h1 id="cartel">La avenida está a oscuras</h1>
                <div id="faroles"><span class="farol"></span><span class="farol"></span><span class="farol"></span><span class="farol"></span></div>
                <button id="prender">Prender un farol</button> <button id="apagar">Apagar todo</button>
                HTML,
            'code' => <<<'JS'
                const cartel = document.querySelector('#cartel');
                const faroles = document.querySelectorAll('.farol');
                let prendidos = Number(localStorage.getItem('prendidos') ?? 0);

                function dibujar() {
                    faroles.forEach((farol, i) => farol.classList.toggle('prendido', i < prendidos));
                    cartel.textContent = prendidos === 0 ? 'La avenida está a oscuras' : `Faroles prendidos: ${prendidos}`;
                    localStorage.setItem('prendidos', prendidos);
                }

                document.querySelector('#prender').addEventListener('click', () => {
                    if (prendidos < faroles.length) prendidos++;
                    dibujar();
                });
                document.querySelector('#apagar').addEventListener('click', () => {
                    prendidos = 0;
                    dibujar();
                });
                dibujar();
                JS,
        ],
        'lienzo' => [
            'title' => 'El lienzo (canvas) y el juego',
            'about' => 'Una animación con requestAnimationFrame. Hacé click en la página y mové la luciérnaga con las flechas.',
            'page' => '<canvas id="feria" width="480" height="260" style="background:#0b1020;display:block;margin:auto"></canvas>',
            'code' => <<<'JS'
                const lienzo = document.querySelector('#feria');
                const ctx = lienzo.getContext('2d');
                const teclas = new Set();
                const luz = { x: 240, y: 130, velocidad: 180 };   // píxeles por segundo
                addEventListener('keydown', (e) => { teclas.add(e.key); e.preventDefault(); });
                addEventListener('keyup', (e) => teclas.delete(e.key));

                let antes = performance.now();
                function cuadro(ahora) {
                    const dt = (ahora - antes) / 1000;
                    antes = ahora;
                    if (teclas.has('ArrowRight')) luz.x += luz.velocidad * dt;
                    if (teclas.has('ArrowLeft')) luz.x -= luz.velocidad * dt;
                    if (teclas.has('ArrowUp')) luz.y -= luz.velocidad * dt;
                    if (teclas.has('ArrowDown')) luz.y += luz.velocidad * dt;

                    ctx.clearRect(0, 0, lienzo.width, lienzo.height);
                    const brillo = 10 + 4 * Math.sin(ahora / 200);
                    ctx.fillStyle = '#ffd400';
                    ctx.beginPath();
                    ctx.arc(luz.x, luz.y, brillo, 0, Math.PI * 2);
                    ctx.fill();
                    requestAnimationFrame(cuadro);
                }
                requestAnimationFrame(cuadro);
                JS,
        ],
    ];

    public static function allowed(?User $user): bool
    {
        if (! $user) {
            return false;
        }
        if ($user->isStaff()) {
            return true;
        }

        return Course::where('language', Language::JavaScript)->get()->contains(fn (Course $course) => $user->can('useJsTool', $course));
    }

    public function mount(): void
    {
        abort_unless(self::allowed(auth()->user()), 403);
    }

    public function render()
    {
        return $this->toolView('livewire.student.js-tool', [
            'examples' => self::EXAMPLES,
            'course' => Course::where('language', Language::JavaScript)->get()->first(fn (Course $course) => auth()->user()->can('useJsTool', $course) && $course->is_published),
        ]);
    }
}
