# Crónicas en Inglés · El piloto (borrador 1, para revisar)

El piloto de [../INGLES.md](../INGLES.md) § 5: **5 episodios de los Talleres de los Vitrales, de 4 misiones cada uno**, en dos versiones del mismo episodio: **Primaria (nivel 1)** y **Secundaria (nivel 4)**. La historia es la de [ingles.md](ingles.md): Ada escribe en el Gran Libro la crónica de Iris, y Eco repite lo que ella aprende.

Cuando el docente lo apruebe, esto se pasa al formato del importador (`cursos/ingles/`) en la fase de código.

## Cómo leer cada misión

- **Escena:** la de HTML que se reusa (`html/R00-N01-P1`), o una **nueva** de Ada y Eco (`NUEVA-01`, abajo).
- **Inglés / Español:** el texto de la historia. Cada palabra se toca y se escucha.
- **Palabras:** las nuevas, con su audio.
- **Ejercicio:** el escalón (E1–E8, INGLES.md § 4), la consigna y las respuestas. `{palabra}` es un hueco con su respuesta; `|` separa las respuestas válidas; **banco** son las fichas para arrastrar o tocar (con alguna de más); **letras** son las fichas para armar la palabra.
- **Criatura:** la que aparece si se equivoca (INGLES.md § 2).
- **Gheco:** la pista.
- **🎤:** la frase para «hablar», el extra opcional (INGLES.md § 4 bis).
- **Carta:** la que se gana para el grimorio.

Cada episodio abre con su **portada**: la escena nueva de Ada y Eco, un texto corto para escuchar y nada para resolver. Cierra con lo que **Eco repite**: las palabras del episodio, con su voz.

---

## Las 5 escenas nuevas (el marco de Ada y Eco)

Se generan en Stitch con las referencias de `REFS['ingles']` (Ada a los 11, Eco pichón y el Borrón chico) y van a `cursos/ingles/escenas/`. Las usan **las dos versiones**. En Secundaria son el recuerdo de Ada a los 15 («hace cuatro años…»), así que no hacen falta otras.

| ID | Escena | Pedido para Stitch |
|---|---|---|
| NUEVA-01 | Ada llega al balcón; nace Eco | Un balcón de piedra sobre una ciudad de ventanales de colores, al atardecer. Ada (11, pelo rojizo enrulado atado con un lápiz, pecas, capa corta azul petróleo) abre un libro grande de **páginas en blanco** sobre la baranda. De su tintero sale una gota de tinta azul que se vuelve un **pajarito redondo de tinta con brillos cian** (Eco pichón). Ada lo mira con la boca abierta. |
| NUEVA-02 | El Borrón se come los colores | La misma mesa del taller de vitrales. El libro de Ada abierto: en una página había manchas de colores y **una mancha de tinta negra con ojos** (el Borrón chico) se las está tragando y se ríe. Ada la señala, enojada. Eco, con las plumas erizadas, la persigue. |
| NUEVA-03 | Nora le enseña a Ada a leer con las manos | Un taller con luz de tarde. Nora (30, ciega, piel oscura, trenzas finas, túnica gris perla, bastón de vidrio) guía las manos de Ada sobre el plomo de un vitral. Ada tiene **los ojos cerrados** y sonríe. Eco, posado arriba del vitral, mira. |
| NUEVA-04 | Ada escribe su nombre en la terminal | La ventanilla de piedra del portal con una terminal de vidrio. Ada escribe con su **pluma de cristal**, y en el vidrio se ven **tres letras de luz cian sueltas**, sin palabras. Eco, en su hombro, abre el pico como si cantara. |
| NUEVA-05 | Tesela le da el permiso; el capítulo se colorea | El taller de Tesela. Tesela (22, pelo corto iridiscente violeta y cian, monóculo, sobretodo negro con vidrios) le da a Ada **una llave de vidrio de colores**. El libro de Ada, abierto en la mesa, tiene **una página llena de colores de vitral**, brillando. Eco vuela alrededor dejando una estela de luz. |

Para Stitch (ESCENAS.md): nada de texto ni letras legibles (en NUEVA-04 las letras son de luz y sin forma de palabra), un solo Eco y un solo Gheco si aparece.

---

# Primaria · nivel 1 (pre-A1, 6–7 años)

Frases de 3 a 5 palabras, presente, mucha repetición. Escalones: E1, E2 y E3. Los episodios 1–3 cierran con **E3** (letras) y los 4–5, con **E4** (escribir la palabra).

## Episodio 1 · *Iris Arrives* · Iris llega

**Portada (NUEVA-01).**
- **Inglés:** This is Ada. Ada has a big book. The pages are white. Look! A little bird! This is Eco. "Hello! Hello!"
- **Español:** Esta es Ada. Ada tiene un libro grande. Las páginas son blancas. ¡Mirá! ¡Un pajarito! Este es Eco. «¡Hola! ¡Hola!»

### M1 · Hello, Iris! (`html/R00-N01-P1`)
- **Inglés:** This is Iris. Iris is a girl. This is Gheco. Gheco is a gecko. Hello, Iris!
- **Español:** Esta es Iris. Iris es una chica. Este es Gheco. Gheco es un gecko. ¡Hola, Iris!
- **Palabras:** hello (hola) · this is (este es / esta es) · girl (chica) · gecko (gecko)
- **Ejercicio (E1 · escuchar):** «Tocá la palabra que dice la voz». Tres rondas: *gecko*, *girl*, *hello*. Opciones: hello · girl · gecko · book.
- **Criatura:** esqueleto. **Gheco:** «Escuchala de nuevo con 🐢: *gecko* suena casi como en castellano».
- 🎤 *Hello, Iris!* · **Carta:** hello = hola

### M2 · The Red Glass (`html/R00-N01-P2`)
- **Inglés:** This is Tesela. Tesela has a window. The glass is red. The glass is blue. The glass is yellow.
- **Español:** Esta es Tesela. Tesela tiene un vitral. El vidrio es rojo. El vidrio es azul. El vidrio es amarillo.
- **Palabras:** window (ventana, vitral) · glass (vidrio) · red · blue · yellow
- **Ejercicio (E2 · completar):** «Pintá el vitral: poné el nombre de cada color». Tres vidrios de color: 🟥 `{red}` · 🟦 `{blue}` · 🟨 `{yellow}`. **Banco:** red, blue, yellow, green.
- **Criatura:** slime. **Gheco:** «Tocá cada palabra del banco y escuchá cómo suena».
- 🎤 *The glass is red.* · **Carta:** los colores (red, blue, yellow)

### M3 · Oh No, Teo! (`html/R00-N01-P3`)
- **Inglés:** This is Teo. Teo runs. Oh no! The window falls. Now it is broken. Iris has a book. Teo has an orange glass.
- **Español:** Este es Teo. Teo corre. ¡Oh, no! El vitral se cae. Ahora está roto. Iris tiene un libro. Teo tiene un vidrio naranja.
- **Palabras:** runs (corre) · broken (roto) · book (libro) · orange (naranja) · a / an (un, una)
- **Ejercicio (E2 · completar):** «¿*a* o *an*?». `Iris has {a} book.` · `Teo has {an} orange glass.` · `Gheco is {a} gecko.` · `Teo has {a} red glass.` **Banco:** a, an (se reusan).
- **Criatura:** orco. **Gheco:** «*an* va antes de una palabra que empieza con a, e, i, o, u: *an orange*. Mirá: *a red glass*, pero *an orange glass*».
- 🎤 *Oh no!* · **Carta:** a / an

### M4 · The Big Door (`html/R00-N01-P4`) · cierre E3
- **Inglés:** Iris has a little glass. The glass falls! Tesela helps. Look! A big door. The door is closed.
- **Español:** Iris tiene un vidrio chiquito. ¡El vidrio se cae! Tesela ayuda. ¡Mirá! Una puerta grande. La puerta está cerrada.
- **Palabras:** little (chiquito) · big (grande) · door (puerta) · closed (cerrada) · look! (¡mirá!)
- **Ejercicio (E3 · letras):** «Armá la palabra». Dos palabras: `door` (letras: d, o, o, r, b, e) y `big` (letras: b, i, g, d, a).
- **Criatura:** slime (si falta o sobra una letra: «¡Casi!»). **Gheco:** «*door* tiene dos *o* juntas, como dos ojos que miran la puerta».
- 🎤 *The door is closed.* · **Carta:** big / little

**Eco repite:** *Hello! Red! Blue! Yellow! Big door!*

## Episodio 2 · *The Workshop Diary* · El diario del taller

**Portada (NUEVA-02).**
- **Inglés:** Oh no! A blot! The Blot eats the colors. No red! No blue! Ada is angry. Eco is angry too. Help Ada!
- **Español:** ¡Oh, no! ¡Un borrón! El Borrón se come los colores. ¡No hay rojo! ¡No hay azul! Ada está enojada. Eco también. ¡Ayudá a Ada!

### M1 · One, Two, Three (`html/R01-N01-P1`)
- **Inglés:** Tesela gives Iris a book. "Write the steps," she says. One, two, three! First, the lead. Then, the glass.
- **Español:** Tesela le da a Iris un libro. «Escribí los pasos», dice. ¡Uno, dos, tres! Primero, el plomo. Después, el vidrio.
- **Palabras:** one · two · three · four · five · first (primero) · then (después)
- **Ejercicio (E1 · escuchar):** «Tocá el número que dice la voz». Cuatro rondas: *three*, *one*, *five*, *two*. Opciones: 1 · 2 · 3 · 4 · 5.
- **Criatura:** esqueleto. **Gheco:** «Contá con los dedos: *one, two, three…*».
- 🎤 *One, two, three!* · **Carta:** numbers 1–5

### M2 · Ten Windows (`html/R01-N01-P2`)
- **Inglés:** Look! Many windows! Iris counts: six, seven, eight, nine, ten. The green window goes to the Valley. Gheco is on the window.
- **Español:** ¡Mirá! ¡Muchas ventanas! Iris cuenta: seis, siete, ocho, nueve, diez. La ventana verde va al Valle. Gheco está en la ventana.
- **Palabras:** six · seven · eight · nine · ten · green (verde) · many (muchas)
- **Ejercicio (E2 · completar):** «Seguí la cuenta de Iris». `six, {seven}, eight, {nine}, ten` y `one, two, {three}, four, {five}`. **Banco:** seven, nine, three, five, eight.
- **Criatura:** ogro (si los cambia de lugar). **Gheco:** «Escuchá la cuenta entera con 🔊 y fijate cuál falta».
- 🎤 *Ten windows!* · **Carta:** numbers 6–10

### M3 · Nora's Hands (`html/R01-N01-P3`)
- **Inglés:** This is Nora. Nora cannot see. Nora reads with her hands. "What is this picture?" she asks.
- **Español:** Esta es Nora. Nora no puede ver. Nora lee con las manos. «¿Qué es este dibujo?», pregunta.
- **Palabras:** hands (manos) · reads (lee) · picture (dibujo) · cannot see (no puede ver)
- **Ejercicio (E3 · letras):** «Armá la palabra que falta: *Nora reads with her ___*». `hands` (letras: h, a, n, d, s, e, t).
- **Criatura:** slime. **Gheco:** «Tiene cinco letras y termina en *s*, porque son dos manos».
- 🎤 *Nora reads with her hands.* · **Carta:** hands = manos

### M4 · In the Basket (`html/R01-N01-P4`) · cierre E3
- **Inglés:** Iris looks in the basket. Paper, paper, paper… and a pencil! And a drawing. The drawing is a round window.
- **Español:** Iris mira en el canasto. Papel, papel, papel… ¡y un lápiz! Y un dibujo. El dibujo es un vitral redondo.
- **Palabras:** basket (canasto) · paper (papel) · pencil (lápiz) · drawing (dibujo) · round (redondo)
- **Ejercicio (E3 · letras):** «¿Qué encontró Iris? Armá las palabras». `pencil` (letras: p, e, n, c, i, l, s, a) y `book` (letras: b, o, o, k, d).
- **Criatura:** slime. **Gheco:** «*pencil* se escribe con *c*, aunque suene como *s*».
- 🎤 *A pencil and a book.* · **Carta:** los objetos (book, pencil, basket)

**Eco repite:** *One, two, three! Pencil! Hands!* Ada colorea de nuevo lo que borró el Borrón.

## Episodio 3 · *Nora's Window* · El ventanal de Nora

**Portada (NUEVA-03).**
- **Inglés:** Nora takes Ada's hands. "Close your eyes," she says. Ada touches the window. It is cold. Eco sits on the window.
- **Español:** Nora toma las manos de Ada. «Cerrá los ojos», le dice. Ada toca el vitral. Está frío. Eco se sienta en el vitral.

### M1 · Top, Middle, Bottom (`html/R01-N02-P1`)
- **Inglés:** Nora touches the window with her fingers. Top… middle… bottom. "Where is the menu?" she asks.
- **Español:** Nora toca el vitral con los dedos. Arriba… al medio… abajo. «¿Dónde está el menú?», pregunta.
- **Palabras:** fingers (dedos) · top (arriba) · middle (medio) · bottom (abajo) · where (dónde)
- **Ejercicio (E2 · completar):** un vitral con tres franjas y una flecha en cada una: `{top}` · `{middle}` · `{bottom}`. **Banco:** top, middle, bottom, door.
- **Criatura:** esqueleto. **Gheco:** «*top* es la punta de arriba, como el trompo».
- 🎤 *Top, middle, bottom.* · **Carta:** top / middle / bottom

### M2 · Head, Body, Feet (`html/R01-N02-P2`)
- **Inglés:** The window has three parts. Tesela says: "A window is like you. The top is the head. The middle is the body. The bottom is the feet."
- **Español:** El vitral tiene tres partes. Tesela dice: «Un vitral es como vos. Arriba está la cabeza. En el medio, el cuerpo. Abajo, los pies».
- **Palabras:** head (cabeza) · body (cuerpo) · feet (pies) · parts (partes)
- **Ejercicio (E1 · escuchar):** «Tocá la parte que dice la voz». Un dibujo de Iris con tres zonas. Rondas: *feet*, *head*, *body*.
- **Criatura:** esqueleto. **Gheco:** «Tocate la cabeza mientras decís *head*. ¡Funciona!».
- 🎤 *This is my head.* · **Carta:** head, body, feet

### M3 · I See with My Eyes (`html/R01-N02-P3`)
- **Inglés:** Nora touches a square with one hand. Iris smiles. "I see with my eyes," says Iris. "I see with my hands," says Nora.
- **Español:** Nora toca un cuadro con una mano. Iris sonríe. «Yo veo con los ojos», dice Iris. «Yo veo con las manos», dice Nora.
- **Palabras:** eyes (ojos) · ears (orejas) · hand (mano) · smiles (sonríe) · I see (veo)
- **Ejercicio (E2 · completar):** `I see with my {eyes}.` · `I touch with my {hands}.` · `I hear with my {ears}.` · `I run with my {feet}.` **Banco:** eyes, hands, ears, feet, head.
- **Criatura:** esqueleto. **Gheco:** «Pensá: ¿con qué parte del cuerpo se hace?».
- 🎤 *I see with my eyes.* · **Carta:** eyes, ears

### M4 · Jump, Gheco! (`html/R01-N02-P4`) · cierre E3
- **Inglés:** Nora uses the keys. Click, click, click… so many doors! Gheco points with his finger. "Here! Jump!"
- **Español:** Nora usa las teclas. Clic, clic, clic… ¡cuántas puertas! Gheco señala con el dedo. «¡Acá! ¡Saltá!».
- **Palabras:** finger (dedo) · jump (saltar) · here (acá) · keys (teclas)
- **Ejercicio (E3 · letras):** `finger` (letras: f, i, n, g, e, r, a) y `feet` (letras: f, e, e, t, o).
- **Criatura:** slime. **Gheco:** «*feet* tiene dos *e*, como dos pies».
- 🎤 *Jump, Gheco!* · **Carta:** finger / fingers

**Eco repite:** *Head! Eyes! Hands! Jump!*

## Episodio 4 · *The Gate Terminal* · La terminal del portal

**Portada (NUEVA-04).**
- **Inglés:** A glass terminal! "What's your name?" it asks. Ada writes: A, D, A. "Hello, Ada!" Eco sings: "Ada! Ada!"
- **Español:** ¡Una terminal de vidrio! «¿Cómo te llamás?», pregunta. Ada escribe: A, D, A. «¡Hola, Ada!». Eco canta: «¡Ada! ¡Ada!».

### M1 · What's Your Name? (`html/R01-N03-P1`)
- **Inglés:** This is a terminal. It has two boxes. Nora touches it. "What is this box?" Iris writes: "Name".
- **Español:** Esto es una terminal. Tiene dos cajas. Nora la toca. «¿Qué es esta caja?». Iris escribe: «Nombre».
- **Palabras:** name (nombre) · box (caja) · what (qué) · what's your name? (¿cómo te llamás?)
- **Ejercicio (E2 · completar):** el diálogo: `What's your {name}?` / `My {name} {is} Iris.` **Banco:** name (se reusa), is, my, girl.
- **Criatura:** goblin (si pone otra palabra donde va *is*). **Gheco:** «*What's your name?* es la pregunta; *My name is…*, la respuesta».
- 🎤 *What's your name?* · **Carta:** What's your name? / My name is…

### M2 · My Name Is Teo (`html/R01-N03-P2`)
- **Inglés:** Teo presses the button. One, two, three times! "I'm in!" he says. "What's your name?" asks Tesela. "My name is Teo!"
- **Español:** Teo aprieta el botón. ¡Una, dos, tres veces! «¡Entré!», dice. «¿Cómo te llamás?», pregunta Tesela. «¡Me llamo Teo!».
- **Palabras:** button (botón) · times (veces) · I'm in! (¡entré!)
- **Ejercicio (E2 · ordenar):** «Armá lo que dice Teo». Fichas: name · Teo · My · is → `My name is Teo.`
- **Criatura:** ogro. **Gheco:** «Empieza con *My*, como «Mi…»».
- 🎤 *My name is Teo.* · **Carta:** My name is…

### M3 · How Old Are You? (`html/R01-N03-P3`)
- **Inglés:** The box asks: "How old are you?" Gheco writes "banana"! Ha, ha! It is a number box. Teo writes: "I am fifteen."
- **Español:** La caja pregunta: «¿Cuántos años tenés?». ¡Gheco escribe «banana»! ¡Ja, ja! Es una caja de números. Teo escribe: «Tengo quince».
- **Palabras:** how old are you? (¿cuántos años tenés?) · I am six (tengo seis) · number (número)
- **Ejercicio (E1 · escuchar):** «Tocá la edad que dice la voz». Rondas: *I am seven*, *I am six*, *I am nine*, *I am eight*. Opciones: 6 · 7 · 8 · 9 · 10.
- **Criatura:** esqueleto. **Gheco:** «En inglés no se «tiene» edad: se «es» de una edad. *I am six*».
- 🎤 *I am {edad}.* (patrón: `I am {número}`, en número o en palabra) · **Carta:** How old are you? / I am…

### M4 · A Letter to the Port (`html/R01-N03-P4`) · cierre E4
- **Inglés:** The letter flies to the Port. It says: "Hello! My name is Iris." Now write your letter!
- **Español:** La carta vuela al Puerto. Dice: «¡Hola! Me llamo Iris». ¡Ahora escribí tu carta!
- **Palabras:** letter (carta) · flies (vuela) · write (escribí)
- **Ejercicio (E4 · escribir):** «Escribí tu carta». `{Hello|Hi}! My {name} is ____.` Los dos primeros huecos tienen respuesta. El tercero es **libre** (patrón `My name is {nombre}`): vale cualquier nombre de 2 letras o más. Si el alumno tiene nombre en su cuenta, se le sugiere.
- **Criatura:** slime («*Helo*» → «¡Casi!»). **Gheco:** «*Hello* lleva dos *l*».
- 🎤 *My name is {nombre}.* · **Carta:** Hello! My name is…

**Eco repite:** *What's your name? My name is…* y dice el nombre del alumno con la voz del navegador.

## Episodio 5 · *The League Table* · La tabla de la Liga

**Portada (NUEVA-05).**
- **Inglés:** Tesela gives Ada a glass key. "You can write our story," she says. Look at the book! The first page is red, blue and yellow! Eco sings: "Thank you!"
- **Español:** Tesela le da a Ada una llave de vidrio. «Podés escribir nuestra historia», le dice. ¡Mirá el libro! ¡La primera página es roja, azul y amarilla! Eco canta: «¡Gracias!».

### M1 · I Am First! (`html/R01-N04-P1`)
- **Inglés:** Look! The League table. Oh no! The slime eats the table. Teo says: "I am first!"
- **Español:** ¡Mirá! La tabla de la Liga. ¡Oh, no! El slime se come la tabla. Teo dice: «¡Yo soy el primero!».
- **Palabras:** first (primero) · second (segundo) · third (tercero) · table (tabla)
- **Ejercicio (E2 · completar):** un podio con 1, 2 y 3: `1 {first}` · `2 {second}` · `3 {third}`. **Banco:** first, second, third, three.
- **Criatura:** esqueleto (si pone *three* en vez de *third*). **Gheco:** «*three* es el número; *third*, el puesto».
- 🎤 *I am first!* · **Carta:** first, second, third

### M2 · Ten Points! (`html/R01-N04-P2`)
- **Inglés:** Iris writes the table again. "Ten what?" asks Nora. "Ten points!" says Iris. Nora has nine points. Teo has seven points.
- **Español:** Iris vuelve a escribir la tabla. «¿Diez qué?», pregunta Nora. «¡Diez puntos!», dice Iris. Nora tiene nueve puntos. Teo tiene siete puntos.
- **Palabras:** points (puntos) · again (de nuevo) · what? (¿qué?)
- **Ejercicio (E2 · completar):** se ve la tabla con los números. `Iris has {ten} points.` · `Nora has {nine} points.` · `Teo has {seven} points.` **Banco:** ten, nine, seven, six.
- **Criatura:** esqueleto. **Gheco:** «Mirá la tabla y buscá el número de cada uno».
- 🎤 *Ten points!* · **Carta:** points

### M3 · Monday, Tuesday… (`html/R01-N04-P3`)
- **Inglés:** "What is this table?" asks Nora. Iris writes on top: "The League". The League plays every day: Monday, Tuesday, Wednesday, Thursday, Friday!
- **Español:** «¿De qué es esta tabla?», pregunta Nora. Iris escribe arriba: «La Liga». La Liga juega todos los días: ¡lunes, martes, miércoles, jueves, viernes!
- **Palabras:** Monday · Tuesday · Wednesday · Thursday · Friday · every day (todos los días)
- **Ejercicio (E2 · ordenar):** «Poné los días en orden». Fichas: Wednesday, Monday, Friday, Tuesday, Thursday → `Monday Tuesday Wednesday Thursday Friday`.
- **Criatura:** ogro. **Gheco:** «Todos terminan en *day*, que quiere decir «día»».
- 🎤 *Monday!* · **Carta:** los días de la semana

### M4 · Teo Is Third (`html/R01-N04-P4`) · cierre E4
- **Inglés:** "Who is this?" asks Nora. "Me! Teo!" Teo is not first. Iris is first. Nora is second. Teo is third!
- **Español:** «¿Quién es este?», pregunta Nora. «¡Yo! ¡Teo!». Teo no es el primero. Iris es la primera. Nora es la segunda. ¡Teo es el tercero!
- **Palabras:** who (quién) · me (yo) · not (no)
- **Ejercicio (E4 · escribir):** se ve la tabla. `Iris is {first}.` · `Teo is {third}.` Se tipea la palabra entera, sin fichas.
- **Criatura:** slime («*thrid*» → «¡Casi!»), esqueleto (*three*). **Gheco:** «*third*: t, h, i, r, d».
- 🎤 *Teo is third.* · **Carta:** Who is first?

**Eco repite:** *First! Second! Third! Monday! Thank you, Tesela!* Ada guarda la llave de vidrio. El capítulo de los Talleres queda de colores.

---

# Secundaria · nivel 4 (A2, 12–14 años)

El mismo episodio y la misma escena, contados por **Ada a los 15**, que pasa en limpio el primer capítulo que escribió a los 11. Narra en primera persona y en pasado. Son textos de 4 a 6 oraciones. Escalones: E4, E5 y E6, más E7 y E8 al cierre: los episodios 1–2 cierran con **E6** (dictado), los 3–4 con **E7** (responder) y el 5 con **E8** (transformar).

## Episodio 1 · *Iris Arrives* · Iris llega

**Portada (NUEVA-01, el recuerdo).**
- **Inglés:** Four years ago my book was empty. I was eleven, and I arrived at the Workshops with a blank page and a crystal pen. That day a drop of ink jumped out of my inkwell and became a bird. I called him Eco. This is the first chapter I ever wrote, and today I'm writing it again.
- **Español:** Hace cuatro años mi libro estaba vacío. Yo tenía once, y llegué a los Talleres con una página en blanco y una pluma de cristal. Ese día una gota de tinta saltó del tintero y se volvió un pájaro. Le puse Eco. Este es el primer capítulo que escribí en mi vida, y hoy lo vuelvo a escribir.

### M1 · The Stone Balcony (`html/R00-N01-P1`)
- **Inglés:** Iris wakes up on a stone balcony. She is holding a piece of colored glass. A small gecko made of light appears on her shoulder. "Hi! I am Gheco," he says. "This is Tesela. She is the master of the Workshops."
- **Español:** Iris se despierta en un balcón de piedra. Tiene en la mano un pedazo de vidrio de colores. Sobre su hombro aparece un gecko chiquito hecho de luz. «¡Hola! Soy Gheco», dice. «Ella es Tesela. Es la maestra de los Talleres».
- **Palabras:** wakes up (se despierta) · holding (sosteniendo) · shoulder (hombro) · master (maestra)
- **Ejercicio (E2 · completar):** «El verbo *to be*». `I {am} Gheco.` · `You {are} Iris.` · `Tesela {is} the master.` · `The windows {are} beautiful.` · `We {are} in the Workshops.` **Banco:** am, is, are (se reusan).
- **Criatura:** goblin. **Gheco:** «*I am*, *he/she/it is* y, con todos los demás, *are*».
- 🎤 *She is the master of the Workshops.* · **Carta:** to be (am / is / are)

### M2 · The Frame First (`html/R00-N01-P2`)
- **Inglés:** Tesela gives Iris a strip of lead. "A window without a title is just one more piece of glass," she says. In the Workshops, every window starts with its frame. Iris draws the frame first. Gheco watches from the table.
- **Español:** Tesela le da a Iris una tira de plomo. «Un vitral sin título es un vidrio más», dice. En los Talleres, todo vitral empieza por su marco. Iris dibuja primero el marco. Gheco mira desde la mesa.
- **Palabras:** strip (tira) · lead (plomo) · frame (marco) · watches (mira)
- **Ejercicio (E5 · escribir varias):** «Escribí el verbo en presente». `Tesela (give) {gives} Iris a strip of lead.` · `Every window (start) {starts} with its frame.` · `Gheco (watch) {watches} from the table.` · `The apprentices (work) {work} all day.`
- **Criatura:** goblin (*Gheco watch*). **Gheco:** «Con *he*, *she* o *it* el verbo suma *-s*. Si termina en *ch*, *sh*, *s* o *x*, suma *-es*: *watches*».
- 🎤 *Iris draws the frame first.* · **Carta:** presente simple: -s / -es

### M3 · Twelve Colors (`html/R00-N01-P3`)
- **Inglés:** Teo ran into the workshop with a window of twelve colors. "Look at what I made!" he shouted. Then the window fell apart in his hands. Iris looked at the pieces on the floor and wrote everything in her notebook.
- **Español:** Teo entró corriendo al taller con un vitral de doce colores. «¡Miren lo que hice!», gritó. Entonces el vitral se le desarmó en las manos. Iris miró los pedazos en el piso y anotó todo en su cuaderno.
- **Palabras:** ran (corrió, de *run*) · made (hizo, de *make*) · fell apart (se desarmó) · wrote (escribió, de *write*)
- **Ejercicio (E2 · completar):** «El verbo en pasado. Sobran palabras». `Teo {ran} into the workshop.` · `He {made} a window of twelve colors.` · `The window {fell} apart.` · `Iris {looked} at the pieces.` · `She {wrote} it in her notebook.` **Banco:** ran, made, fell, looked, wrote, runned, falled, writed.
- **Criatura:** goblin (*runned*, *falled*: el verbo irregular con *-ed*). **Gheco:** «Los irregulares no llevan *-ed*: hay que aprenderlos. *run* → *ran*, *fall* → *fell*, *write* → *wrote*».
- 🎤 *Look at what I made!* · **Carta:** pasado irregular (ran, made, fell, wrote)

### M4 · Glass Without Lead (`html/R00-N01-P4`) · cierre E6
- **Inglés:** Iris put her glass on an empty window, without lead. It slipped, fell and broke at one corner. Tesela picked it up. "A glass without lead is a glass on the floor," she said. At the back of the workshop there was a door with a lock that nobody opened.
- **Español:** Iris apoyó su vidrio en una ventana vacía, sin plomo. Resbaló, se cayó y se astilló en una punta. Tesela lo levantó. «Un vidrio sin plomo es un vidrio en el piso», dijo. Al fondo del taller había una puerta con candado que nadie abría.
- **Palabras:** slipped (resbaló) · broke (se rompió, de *break*) · lock (candado) · nobody (nadie)
- **Ejercicio (E6 · dictado):** «Escuchá lo que dijo Tesela y escribilo completo». `A glass without lead is a glass on the floor.` Se compara palabra por palabra, sin mayúsculas ni puntos, y se marcan las que ya están bien.
- **Criatura:** slime (ortografía), ogro (orden). **Gheco:** «Escuchala con 🐢 y escribí de a pedacitos: *a glass / without lead / is a glass / on the floor*».
- 🎤 *A glass without lead is a glass on the floor.* · **Carta:** la frase de Tesela

**Eco repite:** *Ran! Fell! Wrote! A glass without lead…*

## Episodio 2 · *The Workshop Diary* · El diario del taller

**Portada (NUEVA-02, el recuerdo).**
- **Inglés:** On my second day, the Blot appeared for the first time. It was small then, a black stain with eyes, and it ate every color on my page. I chased it with my pen, but it escaped into the margin, laughing.
- **Español:** En mi segundo día apareció el Borrón por primera vez. Entonces era chico, una mancha negra con ojos, y se comió todos los colores de mi página. Lo perseguí con la pluma, pero se escapó al margen, riéndose.

### M1 · Write the Steps (`html/R01-N01-P1`)
- **Inglés:** "Keep a diary of the workshop," Tesela told Iris, and gave her a blank notebook. "Write the steps of every job, in order. First, cut the glass. Then, put the lead around it. Finally, close the frame."
- **Español:** «Llevá un diario del taller», le dijo Tesela a Iris, y le dio un cuaderno en blanco. «Escribí los pasos de cada trabajo, en orden. Primero, cortá el vidrio. Después, poné el plomo alrededor. Por último, cerrá el marco».
- **Palabras:** keep (llevá, mantené) · cut (cortá) · around (alrededor) · finally (por último)
- **Ejercicio (E2 · ordenar):** «Ordená los pasos». Tres fichas de frase: *Then, put the lead around it.* · *Finally, close the frame.* · *First, cut the glass.*
- **Criatura:** ogro. **Gheco:** «*first* → *then* → *finally*: así se cuenta una secuencia».
- 🎤 *First, cut the glass.* · **Carta:** imperativos + first / then / finally

### M2 · Don't Say "Click Here" (`html/R01-N01-P2`)
- **Inglés:** Tesela pointed at the windows at the back. One opened onto the Serpent Valley, another onto the Messenger Port. "Every window connects to another," she said. "Don't say *click here*. Say where it goes."
- **Español:** Tesela señaló los ventanales del fondo. Uno daba al Valle de la Serpiente; otro, al Puerto de los Mensajeros. «Cada ventana conecta con otra», dijo. «No digas *clic acá*. Decí adónde va».
- **Palabras:** pointed at (señaló) · opened onto (daba a) · connects (conecta) · don't (no, en una orden)
- **Ejercicio (E5 · escribir varias):** «Escribí la orden, positiva o negativa». `(not / say) {Don't say|Do not say} "click here".` · `(look) {Look} at the Valley.` · `(not / touch) {Don't touch|Do not touch} the hot lead.` · `(open) {Open} the window.`
- **Criatura:** goblin (*No say*). **Gheco:** «La orden negativa es *Don't* + verbo: *Don't run*. Nunca *No run*».
- 🎤 *Don't say click here.* · **Carta:** Don't + verbo

### M3 · Describe the Picture (`html/R01-N01-P3`)
- **Inglés:** Nora is a glass artist. She can't see, but she reads the windows with her hands. She touched Iris's diary and asked about the drawing of the gecko. The drawing said nothing. "Describe it for me," she asked. "If you don't, it doesn't exist."
- **Español:** Nora es vitralista. No puede ver, pero lee los vitrales con las manos. Tocó el diario de Iris y preguntó por el dibujo del gecko. El dibujo no decía nada. «Describímelo», le pidió. «Si no, no existe».
- **Palabras:** describe (describir) · touched (tocó) · asked (preguntó, pidió) · exist (existir)
- **Ejercicio (E4 · escribir):** «Escribí lo que Iris le escribe a Nora debajo del dibujo». `Gheco, the {blue|light blue|cyan} gecko with {glasses|goggles}.` Sin banco: se escriben las dos palabras.
- **Criatura:** esqueleto. **Gheco:** «Los anteojos se dicen *glasses*: es la misma palabra que *vidrios*».
- 🎤 *Describe it for me.* · **Carta:** glass / glasses

### M4 · The Glassmaker's Sketch (`html/R01-N01-P4`) · cierre E6
- **Inglés:** Among the old sketches in the basket, Iris found one that wasn't hers: a round window, signed by someone called the Glassmaker. She showed it to Tesela. Tesela looked at it for a long time and didn't say a word.
- **Español:** Entre los bocetos viejos del canasto, Iris encontró uno que no era suyo: un vitral redondo, firmado por alguien que se hacía llamar el Vidriero. Se lo mostró a Tesela. Tesela lo miró un buen rato y no dijo ni una palabra.
- **Palabras:** among (entre) · sketch (boceto) · signed (firmado) · showed (mostró, de *show*)
- **Ejercicio (E6 · dictado):** `First she found the sketch, then she showed it to Tesela.`
- **Criatura:** slime, ogro. **Gheco:** «Hay dos verbos en pasado: uno irregular (*found*) y uno regular (*showed*)».
- 🎤 *She showed it to Tesela.* · **Carta:** the Glassmaker (el Vidriero)

**Eco repite:** *First! Then! Finally! Don't say click here!*

## Episodio 3 · *Nora's Window* · El ventanal de Nora

**Portada (NUEVA-03, el recuerdo).**
- **Inglés:** Nora was the first person who taught me to read without my eyes. She put my hands on the lead and said: "There is a story in every line." I didn't believe her. Then I felt it.
- **Español:** Nora fue la primera que me enseñó a leer sin los ojos. Me puso las manos sobre el plomo y me dijo: «Hay una historia en cada línea». No le creí. Después la sentí.

### M1 · There Is No Menu (`html/R01-N02-P1`)
- **Inglés:** Nora moved her fingers over the sketch, from top to bottom. "There are a lot of boxes here," she said, "but there is no menu. For me, they are all the same."
- **Español:** Nora pasó los dedos por el boceto, de arriba abajo. «Hay un montón de cajas acá», dijo, «pero no hay menú. Para mí son todas iguales».
- **Palabras:** there is (hay, con una) · there are (hay, con varias) · a lot of (un montón de) · the same (iguales)
- **Ejercicio (E2 · completar):** `There {is} a menu at the top.` · `There {are} twenty links.` · `There {is} no title.` · `There {are} three zones in the window.` **Banco:** is, are (se reusan).
- **Criatura:** goblin. **Gheco:** «Mirá lo que viene después: una cosa, *is*; varias, *are*».
- 🎤 *There is no menu.* · **Carta:** there is / there are

### M2 · Top, Middle, Bottom (`html/R01-N02-P2`)
- **Inglés:** The Guild's big window has three zones. At the top there is the cornice, in the middle there is the main panel, and at the bottom there is the base. Iris had already chosen the colors. Tesela took the pencil from her hand: "Name each zone first."
- **Español:** El gran ventanal del Gremio tiene tres zonas. Arriba está la cornisa; en el medio, el panel central, y abajo, el zócalo. Iris ya había elegido los colores. Tesela le sacó el lápiz de la mano: «Primero nombrá cada zona».
- **Palabras:** at the top (arriba) · in the middle (en el medio) · at the bottom (abajo) · took (sacó, de *take*)
- **Ejercicio (E5 · escribir varias):** «La preposición que falta». `The cornice is {at} the top.` · `The main panel is {in} the middle.` · `The base is {at} the bottom.` · `The pencil is {in} Tesela's hand.`
- **Criatura:** orco (cuando falta la palabra chica). **Gheco:** «Se dice *at the top* y *at the bottom*, pero *in the middle*».
- 🎤 *Name each zone first.* · **Carta:** at the top / in the middle / at the bottom

### M3 · On, Under, Next To (`html/R01-N02-P3`)
- **Inglés:** In the main panel there are two orders for the week. Nora touched one and asked: "Is this part of the window, or can I read it on its own?" Gheco was sitting on the frame, right next to her hand.
- **Español:** En el panel central hay dos encargos de la semana. Nora tocó uno y preguntó: «¿Esto es una parte del ventanal o se puede leer suelto?». Gheco estaba sentado en el marco, justo al lado de su mano.
- **Palabras:** orders (encargos) · on its own (suelto, por sí solo) · next to (al lado de) · under (debajo de)
- **Ejercicio (E2 · completar):** se ve la escena. `Gheco is {on} the frame.` · `Gheco is {next to} Nora's hand.` · `The orders are {in} the main panel.` · `The basket is {under} the table.` **Banco:** on, in, under, next to, between.
- **Criatura:** esqueleto. **Gheco:** «*on* es «encima, apoyado», e *in*, «adentro»».
- 🎤 *Gheco is next to Nora's hand.* · **Carta:** in / on / under / next to

### M4 · Twenty Links (`html/R01-N02-P4`) · cierre E7
- **Inglés:** Nora used the keyboard to move through the pages. Every time, she had to go through all the links of the menu before she reached the important part. "Twenty links," she sighed. "Every day." Gheco pointed at a shortcut at the end of the corridor.
- **Español:** Nora usaba el teclado para recorrer las páginas. Cada vez tenía que pasar por todos los enlaces del menú antes de llegar a lo importante. «Veinte enlaces», suspiró. «Todos los días». Gheco señaló un atajo al final del pasillo.
- **Palabras:** keyboard (teclado) · reached (llegó a) · sighed (suspiró) · shortcut (atajo)
- **Ejercicio (E7 · responder):** «Contestá con una oración completa».
  1. *How many links are there in the menu?* → patrón `there are {twenty|20} links`.
  2. *What is there at the end of the corridor?* → patrón `there is a {shortcut|door|sign}`.
- **Criatura:** troll (sin *there is/are*), goblin (*there is twenty*). **Gheco:** «Contestá con las palabras de la pregunta: *How many links are there?* → *There are…*».
- 🎤 *There are twenty links.* · **Carta:** How many…? / There are…

**Eco repite:** *There is! There are! At the top! Next to!*

## Episodio 4 · *The Gate Terminal* · La terminal del portal

**Portada (NUEVA-04, el recuerdo).**
- **Inglés:** At the gate there was a glass terminal that couldn't read my language. Could I write my own name in the Common Tongue? I tried. Three letters of light appeared on the glass, and the terminal said: "Hello, Ada."
- **Español:** En el portal había una terminal de vidrio que no podía leer mi idioma. ¿Podría escribir mi propio nombre en la Lengua Común? Probé. Aparecieron tres letras de luz en el vidrio, y la terminal dijo: «Hola, Ada».

### M1 · I Can't Read It (`html/R01-N03-P1`)
- **Inglés:** At the entrance of the portal there is a terminal that asks for a name and a password. Nora put her hand on it. "I can touch the boxes," she said, "but I can't read them. There are two boxes, but neither says what it is."
- **Español:** A la entrada del portal hay una terminal que pide nombre y contraseña. Nora apoyó la mano. «Puedo tocar las cajas», dijo, «pero no las puedo leer. Hay dos cajas, pero ninguna dice qué es».
- **Palabras:** password (contraseña) · can (puedo) · can't (no puedo) · neither (ninguna)
- **Ejercicio (E2 · completar):** `Nora {can} touch the boxes.` · `She {can't} read them.` · `Gheco {can} climb the wall.` · `Teo {can't} wait.` **Banco:** can, can't (se reusan).
- **Criatura:** goblin (*can to read*, en la pista). **Gheco:** «Después de *can* va el verbo solo: *can read*, nunca *can to read*».
- 🎤 *I can't read them.* · **Carta:** can / can't

### M2 · Can Teo Enter? (`html/R01-N03-P2`)
- **Inglés:** Teo left the terminal empty and pressed "Enter" three times, harder each time. The terminal accepted everything. "I'm in!" "With which user?" asked Tesela. Teo didn't know.
- **Español:** Teo dejó la terminal vacía y apretó «Entrar» tres veces, cada vez más fuerte. La terminal aceptaba todo. «¡Entré!». «¿Con qué usuario?», preguntó Tesela. Teo no sabía.
- **Palabras:** left (dejó, de *leave*) · harder (más fuerte) · accepted (aceptó) · which (cuál, qué)
- **Ejercicio (E2 · ordenar):** «Armá la pregunta de Tesela». Fichas: Teo · enter · Can · without · a · name → `Can Teo enter without a name?`
- **Criatura:** troll (si arranca con *Teo can…?*). **Gheco:** «En la pregunta, *can* pasa adelante: *Teo can enter* → *Can Teo enter?*».
- 🎤 *Can Teo enter without a name?* · **Carta:** preguntas con can

### M3 · Banana Is Not a Number (`html/R01-N03-P3`)
- **Inglés:** The order form asks for an email and how many windows the client wants. On a client's phone, the email box showed a keyboard without @, and in the number box you could type "a lot". Gheco tried to type "banana" in it.
- **Español:** El formulario de encargos pide el correo y cuántos vitrales quiere el cliente. En el celular de un cliente, el campo del correo mostraba un teclado sin @, y en el de la cantidad se podía escribir «un montón». Gheco probó escribir «banana».
- **Palabras:** order form (formulario de encargo) · email (correo) · how many (cuántos) · could (se podía, de *can*)
- **Ejercicio (E5 · escribir varias):** «*can*, *can't*, *could* o *couldn't*». `Now Gheco {can't|cannot} type letters in the number box.` · `Yesterday you {could} type "a lot".` · `{Can} you choose a number from 1 to 12?` · `The phone {couldn't|could not} show the @.`
- **Criatura:** goblin. **Gheco:** «*could* es el pasado de *can*».
- 🎤 *Can you choose a number?* · **Carta:** can / could

### M4 · A Letter to the Port (`html/R01-N03-P4`) · cierre E7
- **Inglés:** When the form is complete, Tesela explained, the message travels to the Messenger Port. There, Elefa receives it and answers. "We build the window; they build the answer." But the send button was written as a link.
- **Español:** Cuando el formulario está completo, le explicó Tesela, el mensaje viaja al Puerto de los Mensajeros. Ahí, Elefa lo recibe y lo contesta. «Nosotros armamos la ventanilla; ellos, la respuesta». Pero el botón de enviar estaba escrito como un enlace.
- **Palabras:** travels (viaja) · receives (recibe) · answers (contesta) · build (armamos)
- **Ejercicio (E7 · responder):** «Contestá con una oración completa».
  1. *Can Elefa answer the message?* → patrón `yes, {she|elefa} can`.
  2. *Where does the message travel?* → patrón `it travels to the {messenger port|port}` · `to the {messenger port|port}`.
  3. *What's your name and how old are you?* → patrón `my name is {nombre} and i am {número}` (se acepta *I'm*).
- **Criatura:** troll, goblin. **Gheco:** «Respuesta corta: *Yes, she can* / *No, she can't*. No hace falta repetir el verbo».
- 🎤 *Yes, she can.* · **Carta:** Yes, I can / No, I can't

**Eco repite:** *Can! Can't! Could! Yes, she can!*

## Episodio 5 · *The League Table* · La tabla de la Liga

**Portada (NUEVA-05, el recuerdo).**
- **Inglés:** On my last day in the Workshops, Tesela gave me a glass key. "Our story is safer in your book than in our windows," she said. The first chapter filled with color, and Eco flew around the page, prouder than me.
- **Español:** En mi último día en los Talleres, Tesela me dio una llave de vidrio. «Nuestra historia está más segura en tu libro que en nuestros vitrales», dijo. El primer capítulo se llenó de color, y Eco voló alrededor de la página, más orgulloso que yo.

### M1 · Who Was First? (`html/R01-N04-P1`)
- **Inglés:** At the entrance of the Workshops hangs the table of the Obsidian League. Last night the slime broke the rows, and the data were left loose. Teo swore he was first. In fact, Iris was first, Nora was second and Teo was third.
- **Español:** En la entrada de los Talleres cuelga la tabla de la Liga Obsidiana. Anoche el slime desarmó las filas y los datos quedaron sueltos. Teo juró que él estaba primero. En realidad, Iris estaba primera, Nora segunda y Teo tercero.
- **Palabras:** hangs (cuelga) · rows (filas) · swore (juró, de *swear*) · in fact (en realidad)
- **Ejercicio (E2 · completar):** se ve la tabla. `Iris was {first}.` · `Nora was {second}.` · `Teo was {third}.` · `Teo wasn't {first}.` **Banco:** first, second, third, fourth, three.
- **Criatura:** esqueleto. **Gheco:** «Los ordinales: *first*, *second*, *third*, y después *-th*: *fourth*, *fifth*».
- 🎤 *Teo was third.* · **Carta:** ordinales (first → fifth)

### M2 · More Points Than Teo (`html/R01-N04-P2`)
- **Inglés:** "Put it back together," Tesela asked, "so that it makes sense when you read it aloud." Nora tried it: "A hundred and twenty what? Years?" Iris has 120 points, Nora has 95 and Teo has 80. Teo's streak is two days; Iris's is five.
- **Español:** «Volvé a armarla», le pidió Tesela, «para que se entienda leyéndola en voz alta». Nora la probó: «¿Ciento veinte qué? ¿Años?». Iris tiene 120 puntos, Nora 95 y Teo 80. La racha de Teo es de dos días; la de Iris, de cinco.
- **Palabras:** aloud (en voz alta) · streak (racha) · more… than (más… que) · fewer… than (menos… que)
- **Ejercicio (E5 · escribir varias):** se ve la tabla. `Iris has {more} points than Nora.` · `Teo has {fewer|less} points than Nora.` · `Iris's streak is {longer} than Teo's.` · `Teo's streak is {shorter} than Iris's.`
- **Criatura:** goblin (*more long*). **Gheco:** «Palabra corta, *-er*: *longer*, *shorter*. *more* y *fewer* van con cantidades».
- 🎤 *Iris has more points than Nora.* · **Carta:** comparativos: -er / more / fewer

### M3 · More Important Than Numbers (`html/R01-N04-P3`)
- **Inglés:** "And what is this table about?" asked Nora. "Before the numbers, tell me what it is." For Nora, the title was more important than the numbers. Iris carved it into the stone above the table.
- **Español:** «¿Y de qué es esta tabla?», preguntó Nora. «Antes de los números, decime de qué se trata». Para Nora, el título era más importante que los números. Iris lo talló en la piedra arriba de la tabla.
- **Palabras:** about (sobre, de qué) · important (importante) · carved (talló) · above (arriba de)
- **Ejercicio (E4 · escribir):** «El comparativo». `important → {more important}` · `big → {bigger}` · `good → {better}` · `easy → {easier}`.
- **Criatura:** slime (*biger*), goblin (*gooder*). **Gheco:** «Palabra larga: *more* + palabra. Ojo con las raras: *good* → *better*. Las que terminan en *y* cambian a *-ier*».
- 🎤 *The title is more important than the numbers.* · **Carta:** comparativos irregulares (better, worse)

### M4 · Teo Wasn't First (`html/R01-N04-P4`) · cierre E8
- **Inglés:** Now the table had streaks and points. Nora asked about Teo's row: "Whose streak of two days is this?" "Mine," Teo protested from the back. "But I was first yesterday!"
- **Español:** Ahora la tabla tenía rachas y puntos. Nora preguntó por la fila de Teo: «¿De quién es esta racha de dos días?». «Mía», protestó Teo desde el fondo. «¡Pero ayer yo estaba primero!».
- **Palabras:** whose (de quién) · mine (mío, mía) · protested (protestó) · yesterday (ayer)
- **Ejercicio (E8 · transformar):** «Cambiá la frase como te pide».
  1. *Teo was first.* → **negativa**: `Teo wasn't first.` | `Teo was not first.`
  2. *Teo was first.* → **pregunta**: `Was Teo first?`
  3. *Iris has more points than Teo.* → **al revés**: `Teo has fewer points than Iris.` | `Teo has less points than Iris.`
  4. *Teo is third.* → **pasado**: `Teo was third.`
- **Criatura:** troll (la pregunta), goblin (el pasado), ogro (el orden). **Gheco:** «Con *was* no hace falta *did*: *Was Teo first?* / *Teo wasn't first*».
- 🎤 *Was Teo first?* · **Carta:** was / wasn't / Was…?

**Eco repite:** *First! More than! Better! Was Teo first? No!* Ada cierra el capítulo de los Talleres y Eco se le duerme encima.

---

## Para revisar

1. **El largo de Primaria.** ¿3 a 5 palabras por frase está bien para 6–7 años, o es mucho?
2. **El paso del nivel 1 al 4.** Secundaria salta de golpe a A2 narrado por Ada a los 15. ¿Se entiende como «el mismo episodio, más difícil»?
3. **Las escenas nuevas.** Son 5, una portada por episodio, compartidas entre Primaria y Secundaria. Las genero en Stitch cuando apruebes los textos.
4. **Lo que queda para la fase de código:** pasar esto al formato del importador, el comprobador `english.js` con estos tipos de ejercicio y la vista biblioteca. Ese diseño ya está en INGLES.md § 6.
