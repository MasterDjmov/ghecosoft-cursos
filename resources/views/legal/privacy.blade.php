{{-- D112: Política de privacidad (Ley 25.326). Al cambiar algo que el alumno acepta, subir config('legal.version'). --}}
<x-layouts::legal title="Política de privacidad">
    <article class="markdown" data-test="legal-privacy">
        <h1>Política de privacidad</h1>
        <p class="text-sm text-ink-muted">Versión del {{ \Illuminate\Support\Carbon::parse(config('legal.version'))->format('d/m/Y') }}</p>

        <p>
            Esta política explica qué datos personales guarda {{ config('app.name') }}, para qué los usa, quién los ve y cómo podés
            consultarlos, corregirlos o pedir que se borren, según la Ley 25.326 de Protección de los Datos Personales.
        </p>

        <h2>1. Quién es el responsable</h2>
        <p>
            El responsable de los datos es {{ config('legal.owner') }}{{ config('legal.owner_id') ? ' (CUIT '.config('legal.owner_id').')' : '' }}, {{ config('legal.city') }}.
            Para cualquier consulta sobre tus datos escribí a <a href="mailto:{{ config('legal.email') }}">{{ config('legal.email') }}</a>.
        </p>

        <h2>2. Qué datos guardamos y para qué</h2>
        <ul>
            <li><strong>Tu cuenta:</strong> nombre, apellido, usuario y clave; email y teléfono si los cargás. Sirven para que entres, recuperes la clave y el profe te pueda escribir. La clave se guarda cifrada (con hash): nadie la puede leer, ni el profe.</li>
            <li><strong>Datos personales opcionales:</strong> fecha de nacimiento (para saber si sos menor y pedir la autorización de tu adulto responsable), DNI y foto o avatar.</li>
            <li><strong>Pagos:</strong> el comprobante de la transferencia que subís y el mensaje que lo acompaña, para aprobar tu abono. No guardamos tarjetas ni claves bancarias.</li>
            <li><strong>Lo que hacés en los cursos:</strong> tus entregas y tu código, los mensajes con el profe, las micro-misiones resueltas (también las respuestas equivocadas), los temas que visitás, tus monedas, experiencia, insignias e ítems del juego. Sirven para corregirte, mostrarte tu progreso y mejorar los cursos con estadísticas.</li>
            <li><strong>Accesos:</strong> el tipo de dispositivo, el sistema y el navegador con que entrás, y la dirección IP de tu sesión. Sirven para la seguridad de tu cuenta (una sola sesión abierta) y para saber si se usa más el celular o la compu.</li>
            <li><strong>Autorización de menores:</strong> la nota firmada por vos, tu adulto responsable y el profe.</li>
        </ul>
        <p>Solo pedimos lo necesario para dar los cursos. Los datos marcados como opcionales los podés dejar vacíos.</p>
        <p>
            Los mails de tu cuenta (entregas, pagos, abono) son parte del servicio. Los avisos de cursos nuevos que pediste con «Avisame»
            traen un link para no recibirlos más, y también los podés apagar en <em>Mi cuenta → Avisos</em>.
        </p>

        <h2>3. Quién ve tus datos</h2>
        <ul>
            <li><strong>El profe y los docentes de tu comisión</strong> ven tus datos de cuenta, tu progreso, tus entregas y tus mensajes en el curso que dan.</li>
            <li><strong>Tus compañeros</strong> ven en el ranking de tu curso tu nombre con la inicial del apellido, o el apodo que elijas. Nunca se muestra tu usuario.</li>
            <li><strong>Cualquier persona</strong> ve tu CV y te ve en el ranking general solo si vos lo hacés público (y si sos menor, con la autorización aprobada). El CV nunca muestra tu código ni los comentarios del profe.</li>
        </ul>

        <h2>4. Con quién se comparten</h2>
        <p>No vendemos ni cedemos tus datos, no mostramos publicidad y no usamos herramientas de seguimiento de terceros. Para funcionar usamos estos servicios:</p>
        <ul>
            <li><strong>El servicio de alojamiento</strong> donde está la plataforma y sus copias de seguridad.</li>
            <li><strong>Gmail (Google)</strong> para mandar los avisos por email, si cargaste uno. Google puede guardar esos mails fuera de la Argentina.</li>
            <li><strong>Google Fonts</strong>: en el curso de HTML y CSS, la vista previa de tu página puede pedir tipografías a Google desde tu navegador.</li>
        </ul>
        <p>El código que escribís se ejecuta en tu propio navegador, no en nuestros servidores.</p>

        <h2>5. Cookies y almacenamiento</h2>
        <p>
            Usamos solo las cookies necesarias para mantener tu sesión abierta y proteger los formularios. Algunas preferencias
            (por ejemplo, qué pestaña dejaste abierta) se guardan en tu navegador. No usamos cookies de publicidad ni de análisis de terceros.
        </p>

        <h2>6. Cuánto tiempo los guardamos</h2>
        <p>
            Mientras tu cuenta exista. Si pedís que la borremos, borramos o anonimizamos tus datos dentro de los 30 días, salvo lo que la ley
            nos obligue a conservar (por ejemplo, los comprobantes de pago). Las copias de seguridad se renuevan solas y las más viejas se borran a los 14 días.
            Los registros de acceso (IP, dispositivo y navegador) se borran a los 12 meses.
        </p>

        <h2>7. Cómo los cuidamos</h2>
        <p>
            Conexión cifrada (HTTPS), claves con hash, acceso según el rol (cada docente ve solo a sus alumnos), archivos privados que se
            entregan solo a quien corresponde, doble factor disponible en <em>Mi cuenta → Seguridad</em> y copias de seguridad diarias.
            Ningún sistema es invulnerable: si hubiera un incidente que afecte tus datos, te avisamos y te contamos qué pasó y qué hicimos.
        </p>

        <h2>8. Menores de edad</h2>
        <p>
            Hay cursos pensados para chicos (las Crónicas en Inglés de Primaria, desde los 6 años). Si tenés menos de 13 años, la cuenta la
            crea tu adulto responsable o el profe junto con él. Si tenés entre 13 y 17, usala con conocimiento de tu adulto responsable.
            En todos los casos, para tener el CV público o aparecer en el ranking general hace falta la nota firmada por tu adulto responsable.
            El adulto responsable puede pedir en cualquier momento ver, corregir o borrar los datos del menor.
        </p>

        <h2>9. Tus derechos</h2>
        <ul>
            <li><strong>Acceso:</strong> saber qué datos tuyos tenemos, gratis cada seis meses. Te respondemos dentro de los 10 días corridos.</li>
            <li><strong>Rectificación y actualización:</strong> corregir lo que esté mal. Lo podés hacer vos en <em>Mi cuenta → Datos personales</em>.</li>
            <li><strong>Supresión:</strong> pedir que borremos tu cuenta y tus datos. Rectificación y supresión se resuelven dentro de los 5 días hábiles.</li>
            <li><strong>Privacidad del CV y del ranking:</strong> lo manejás vos en <em>Mi cuenta → Privacidad</em>.</li>
        </ul>
        <p>Para pedir acceso o supresión, escribí a <a href="mailto:{{ config('legal.email') }}">{{ config('legal.email') }}</a> desde el email de tu cuenta, o pedíselo al profe.</p>
        <p class="text-sm text-ink-muted">
            El titular de los datos personales tiene la facultad de ejercer el derecho de acceso a los mismos en forma gratuita a intervalos no
            inferiores a seis meses, salvo que se acredite un interés legítimo al efecto conforme lo establecido en el artículo 14, inciso 3 de la
            Ley Nº 25.326. La AGENCIA DE ACCESO A LA INFORMACIÓN PÚBLICA, en su carácter de Órgano de Control de la Ley Nº 25.326, tiene la
            atribución de atender las denuncias y reclamos que interpongan quienes resulten afectados en sus derechos por incumplimiento de las
            normas vigentes en materia de protección de datos personales.
        </p>

        <h2>10. Cambios en esta política</h2>
        <p>Si la cambiamos, te avisamos en la plataforma y te pedimos que la aceptes de nuevo cuando el cambio sea importante. Arriba figura la fecha de la versión vigente.</p>

        <p>Ver también los <a href="{{ route('legal.terms') }}">Términos y condiciones</a>.</p>
    </article>
</x-layouts::legal>
