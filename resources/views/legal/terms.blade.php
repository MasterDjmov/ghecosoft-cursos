{{-- D112: Términos y condiciones (Ley 24.240 de Defensa del Consumidor). Al cambiar algo que el alumno acepta, subir config('legal.version'). --}}
<x-layouts::legal title="Términos y condiciones">
    <article class="markdown" data-test="legal-terms">
        <h1>Términos y condiciones</h1>
        <p class="text-sm text-ink-muted">Versión del {{ \Illuminate\Support\Carbon::parse(config('legal.version'))->format('d/m/Y') }}</p>

        <p>
            Estos términos explican cómo funciona {{ config('app.name') }}, de {{ config('legal.owner') }}{{ config('legal.owner_id') ? ' (CUIT '.config('legal.owner_id').')' : '' }}, {{ config('legal.city') }}.
            Al crear tu cuenta los aceptás. Si sos menor, leelos con tu adulto responsable.
        </p>

        <h2>1. Qué es la plataforma</h2>
        <p>
            Cursos de programación y de inglés organizados como un árbol de temas, con prácticas que corrige el profe, micro-misiones que
            se comprueban solas y un juego (héroe, monedas, experiencia, ítems y ranking) para acompañar el estudio. Los cursos y sus
            contenidos pueden cambiar o ampliarse con el tiempo.
        </p>

        <h2>2. Tu cuenta</h2>
        <ul>
            <li>Los datos que cargás tienen que ser reales. La cuenta es personal: no la compartas ni le pases tu clave a nadie.</li>
            <li>Sos responsable de lo que se haga con tu cuenta. Si creés que alguien entró sin permiso, cambiá la clave y avisale al profe.</li>
            <li>Si tenés menos de 13 años, la cuenta la crea tu adulto responsable o el profe junto con él (ver la <a href="{{ route('legal.privacy') }}">Política de privacidad</a>).</li>
        </ul>

        <h2>3. El abono</h2>
        <ul>
            <li>Cada curso tiene su propio abono. El primer tema (la clase 0) se puede probar gratis antes de pagar.</li>
            <li>El profe te informa el precio final en pesos antes de que pagues. Pagás por transferencia u otro medio que acuerden y subís el comprobante desde el curso.</li>
            <li>El abono dura los días que indica el curso (normalmente 30) y empieza a correr cuando el profe aprueba el pago.</li>
            <li><strong>No se renueva solo</strong>: no hay débitos automáticos. Si querés seguir, pedís la renovación y pagás otra vez.</li>
            <li>Con el abono vencido podés repasar lo que ya abriste, pero no abrir temas nuevos ni entregar.</li>
        </ul>

        <h2>4. Arrepentimiento y baja</h2>
        <ul>
            <li>
                <strong>Arrepentimiento:</strong> tenés {{ config('legal.withdrawal_days') }} días corridos desde que se aprueba tu pago para arrepentirte,
                sin dar motivos, y te devolvemos todo lo que pagaste (art. 34 de la Ley 24.240 y art. 1110 del Código Civil y Comercial).
                Lo pedís con el <a href="{{ route('legal.withdrawal') }}">botón de arrepentimiento</a>, sin necesidad de entrar a tu cuenta.
            </li>
            <li>
                <strong>Baja:</strong> podés darte de baja cuando quieras con el <a href="{{ route('legal.cancellation') }}">botón de baja</a>.
                Pasado el plazo de arrepentimiento, el abono en curso no se reintegra, salvo que no hayamos podido darte el servicio por causas nuestras.
            </li>
            <li>En los dos casos recibís un código de trámite en el momento, y el profe te escribe para coordinar la devolución o la baja.</li>
        </ul>

        <h2>5. Monedas, experiencia y juego</h2>
        <p>
            Las monedas de cada curso, la experiencia, el oro, los ítems, las insignias y el ranking son parte del juego: no tienen valor en
            dinero, no se compran, no se venden ni se pasan a otra cuenta. Podemos ajustarlos para mantener el juego parejo o corregir errores.
        </p>

        <h2>6. Uso permitido</h2>
        <ul>
            <li>Las entregas tienen que ser tuyas. No copies soluciones de otros ni pases las tuyas para que otro las entregue.</li>
            <li>No intentes romper la plataforma, entrar a cuentas ajenas ni usar el código de las prácticas para dañar a nadie.</li>
            <li>En los mensajes, tratá bien al profe y a tus compañeros. Nada de contenido ofensivo, violento o inapropiado para chicos.</li>
        </ul>

        <h2>7. Suspensión</h2>
        <p>
            Si no se cumplen estos términos, podemos pausar o cerrar la cuenta. Antes te avisamos y te escuchamos, salvo que haga falta
            actuar enseguida para proteger a otros alumnos o a la plataforma.
        </p>

        <h2>8. Propiedad intelectual</h2>
        <ul>
            <li>Los cursos, los textos, las historias, los personajes y las imágenes son de {{ config('legal.owner') }} y están protegidos por la Ley 11.723. Los podés usar para estudiar, no copiarlos ni publicarlos. Si encontrás contenido de la plataforma publicado sin permiso, o creés que algo de acá usa una obra tuya, escribinos a {{ config('legal.email') }} y lo revisamos.</li>
            <li>El código y los trabajos que escribís son tuyos. Nos das permiso para guardarlos, corregirlos y mostrarte tu progreso.</li>
            <li>Si creés que algo publicado acá usa una obra tuya sin permiso, escribinos a <a href="mailto:{{ config('legal.email') }}">{{ config('legal.email') }}</a> y lo revisamos.</li>
        </ul>

        <h2>9. Disponibilidad y responsabilidad</h2>
        <p>
            Hacemos lo posible para que la plataforma ande siempre, pero puede haber cortes o mantenimientos (te avisamos en la plataforma).
            Los cursos enseñan, pero no garantizan un trabajo ni un resultado. El código de las prácticas corre en tu navegador: guardá
            copias de lo que te importe. Nada de esto limita tus derechos como consumidor.
        </p>

        <h2>10. Cambios en estos términos</h2>
        <p>Si los cambiamos, te avisamos en la plataforma. Los cambios importantes te los pedimos aceptar de nuevo. Nunca cambian un abono que ya pagaste.</p>

        <h2>11. Ley y reclamos</h2>
        <p>
            Rigen las leyes de la República Argentina. Ante cualquier problema, escribinos primero a
            <a href="mailto:{{ config('legal.email') }}">{{ config('legal.email') }}</a>. También podés reclamar ante la Defensa del Consumidor
            de tu provincia o en la Ventanilla Única Federal (argentina.gob.ar/produccion/defensadelconsumidor), y ante los tribunales de tu domicilio.
        </p>

        <p>Ver también la <a href="{{ route('legal.privacy') }}">Política de privacidad</a>.</p>
    </article>
</x-layouts::legal>
