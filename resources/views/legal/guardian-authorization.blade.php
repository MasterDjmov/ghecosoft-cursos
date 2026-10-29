{{-- D114: modelo de autorización del adulto responsable (Ley 25.326 y art. 26 del Código Civil y Comercial). Cubre los datos, el CV público y el ranking general. --}}
<x-layouts::legal title="Autorización del adulto responsable">
    <article class="markdown print:text-black" data-test="guardian-authorization">
        <div class="flex flex-wrap items-center justify-between gap-3 print:hidden">
            <p class="text-sm text-ink-muted">Imprimila (o copiala a mano), firmala y subí una foto o el PDF en <em>Mi cuenta → Privacidad</em>.</p>
            <flux:button size="sm" icon="printer" x-data x-on:click="window.print()">Imprimir</flux:button>
        </div>

        <h1>Autorización del adulto responsable</h1>
        <p>{{ config('app.name') }}, de {{ config('legal.owner') }}{{ config('legal.owner_id') ? ' (CUIT '.config('legal.owner_id').')' : '' }}, {{ config('legal.city') }}.</p>

        <p>
            Yo, ................................................................, DNI ......................., en mi carácter de
            madre / padre / tutor (tachar lo que no corresponda) de ................................................................,
            DNI ......................., nacido/a el ...../...../.........., usuario en la plataforma ..............................,
        </p>

        <h2>Autorizo</h2>
        <ol>
            <li>
                <strong>El uso de la plataforma y de sus datos.</strong> Que use su cuenta y que la plataforma guarde y use sus datos (nombre,
                fecha de nacimiento, entregas, código, mensajes con el profe, progreso, accesos) para dar los cursos, corregirlo y mostrarle su
                avance, como explica la <a href="{{ route('legal.privacy') }}">Política de privacidad</a>, que leí.
            </li>
            <li>
                <strong>El CV público.</strong> Que active, si quiere, su CV público: una página con su nombre o apodo, sus cursos, insignias y
                trabajos, que puede ver cualquiera que tenga el link. Él o ella lo puede apagar cuando quiera.
            </li>
            <li>
                <strong>El ranking general.</strong> Que aparezca en el ranking de todos los alumnos, con su nombre o con el apodo que elija.
            </li>
        </ol>

        <h2>Sé que</h2>
        <ul>
            <li>Su código corre en su propio navegador; la plataforma no vende ni cede sus datos ni muestra publicidad.</li>
            <li>Puedo pedir en cualquier momento ver, corregir o borrar sus datos, o retirar esta autorización, escribiendo a {{ config('legal.email') }}. Al retirarla, el CV público y el ranking general se apagan.</li>
            <li>Los cursos tienen una parte presencial con el profe, que conoce a cada alumno.</li>
        </ul>

        <div class="mt-10 grid gap-10 sm:grid-cols-3 print:grid-cols-3">
            @foreach (['Firma del alumno/a', 'Firma y aclaración del adulto responsable', 'Firma del profe'] as $who)
                <div class="border-t border-ink-muted pt-1 text-center text-xs">{{ $who }}</div>
            @endforeach
        </div>
        <p class="mt-6 text-sm">Lugar y fecha: ................................................................</p>
    </article>
</x-layouts::legal>
