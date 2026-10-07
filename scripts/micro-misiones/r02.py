import textwrap


def m(**kw):
    for k in ("inicial", "solucion"):
        kw[k] = textwrap.dedent(kw[k]).lstrip("\n")
    return kw


NODOS = [
    {
        "titulo": "R02-N01 · Clases y objetos",
        "misiones": [
            m(id="R02-N01-P1", titulo="El primer molde",
              lugar="La Sala de los Moldes", personajes="Mia, Gheco, Sila",
              carta="Clase y objeto | class Orco: · def __init__(self, nombre, vida): · grum = Orco(\"Grum\", 40) · grum.vida",
              recompensa="xp 10, oro 10",
              escena="""
                  La Gran Biblioteca huele a tinta y a piedra mojada. Entre estantes que llegan al techo, una mujer alta, de anteojos redondos y un manojo de llaves al cinturón, acomoda moldes de bronce con forma de criatura.
                  —**Sila**, la Archivera. —No levanta la vista—. Acá nadie escribe cada orco por separado. Se escribe el **molde** una vez, y de él salen los que hagan falta. Probá.
              """,
              sugiere="`class Orco:` define el molde (la **clase**). Adentro, `__init__` se ejecuta **solo** cada vez que creás un orco: guarda sus datos en `self`, que es «este orco». `Orco(\"Grum\", 40)` crea un **objeto**.",
              desafio="Completá el nombre del método que arma cada orco.",
              inicial='''
                  class Orco:
                      def ___(self, nombre, vida):
                          self.nombre = nombre
                          self.vida = vida

                  grum = Orco("Grum", 40)
                  brak = Orco("Brak", 55)
                  print(grum.nombre, grum.vida)
                  print(brak.nombre, brak.vida)
              ''',
              solucion='''
                  class Orco:
                      def __init__(self, nombre, vida):
                          self.nombre = nombre
                          self.vida = vida

                  grum = Orco("Grum", 40)
                  brak = Orco("Brak", 55)
                  print(grum.nombre, grum.vida)
                  print(brak.nombre, brak.vida)
              ''',
              solucion_txt="`def __init__(self, nombre, vida):`.",
              al_superar="""
                  Del molde salen dos orquitos de luz, cada uno con su número de vida encima. Y entonces pasa algo nuevo: sobre tus manos aparecen **cubos de datos**, chiquitos, girando en el aire.
                  Sila levanta por fin la vista. —Mirá vos. Los moldes te reconocen.
              """,
              imagen=["La Gran Biblioteca del Bastión: estantes altísimos, escaleras móviles, moldes de bronce con forma de criaturas.",
                      "Sila, alta, de anteojos redondos y llaves al cinturón, mira por encima de un libro.",
                      "Sobre las manos de Mia flotan por primera vez cubos de datos cian.",
                      "Dos orquitos de luz con su vida encima: `40` y `55`."]),
            m(id="R02-N01-P2", titulo="Lo que sabe hacer",
              lugar="La Sala de los Moldes", personajes="Mia, Gheco, Sila",
              carta="Métodos | def recibir(self, danio): · grum.recibir(10) · self es el objeto que llama",
              recompensa="xp 10, oro 10",
              escena="""
                  —Un molde no guarda solo datos —dice Sila—. También dice qué **sabe hacer** la criatura. Un orco recibe golpes, por ejemplo. Y nunca queda con vida negativa: eso enloquece a los registros.
              """,
              sugiere="Un **método** es una función adentro de la clase. Su primer parámetro es `self`, y Python lo pasa solo: `grum.recibir(10)` es `Orco.recibir(grum, 10)`. Para que la vida no baje de 0, usá `max(0, ...)`.",
              desafio="Escribí lo que hace `recibir`.",
              inicial='''
                  class Orco:
                      def __init__(self, nombre, vida):
                          self.nombre = nombre
                          self.vida = vida

                      def recibir(self, danio):
                          ___

                  grum = Orco("Grum", 40)
                  grum.recibir(15)
                  print(grum.vida)
                  grum.recibir(30)
                  print(grum.vida)
              ''',
              solucion='''
                  class Orco:
                      def __init__(self, nombre, vida):
                          self.nombre = nombre
                          self.vida = vida

                      def recibir(self, danio):
                          self.vida = max(0, self.vida - danio)

                  grum = Orco("Grum", 40)
                  grum.recibir(15)
                  print(grum.vida)
                  grum.recibir(30)
                  print(grum.vida)
              ''',
              solucion_txt="`self.vida = max(0, self.vida - danio)`.",
              al_superar="El orquito de luz se tambalea y se desarma en chispas al llegar a 0. Gheco aplaude con la cola.",
              imagen=["Un orquito de luz que se desarma en chispas al recibir un golpe.",
                      "Mia con el pergamino abierto: `def recibir(self, danio):` brilla en verde.",
                      "Gheco aplaude con la cola, colgado de un estante."]),
            m(id="R02-N01-P3", titulo="Lo que comparten todos",
              lugar="La Sala de los Moldes", personajes="Mia, Gheco, Sila",
              carta="Atributo de clase | creados = 0 dentro de la clase · lo comparten todos · Orco.creados += 1",
              recompensa="xp 10, oro 10",
              escena="""
                  Sila te pasa un registro gastado. —Necesito saber cuántos orcos salieron de este molde. No quiero contarlos de a uno.
              """,
              sugiere="Lo que se escribe **en la clase**, fuera de los métodos, es de la **clase**: lo comparten todos los objetos. Para cambiarlo, nombrá la clase: `Orco.creados += 1`. Lo de `self.` es de cada objeto.",
              desafio="Cada vez que se crea un orco, sumá uno al contador de la clase.",
              inicial='''
                  class Orco:
                      creados = 0

                      def __init__(self, nombre):
                          self.nombre = nombre
                          ___

                  Orco("Grum")
                  Orco("Brak")
                  Orco("Zog")
                  print(f"Salieron del molde: {Orco.creados}")
              ''',
              solucion='''
                  class Orco:
                      creados = 0

                      def __init__(self, nombre):
                          self.nombre = nombre
                          Orco.creados += 1

                  Orco("Grum")
                  Orco("Brak")
                  Orco("Zog")
                  print(f"Salieron del molde: {Orco.creados}")
              ''',
              solucion_txt="`Orco.creados += 1`.",
              al_superar="—Tres. Igual que en mi registro —dice Sila, y por primera vez sonríe—. Alguien anda cambiando estos números. Por eso los cuento dos veces.",
              imagen=["Sila sostiene un registro gastado con números tachados.",
                      "Sobre el molde de bronce flota un contador de luz: `3`.",
                      "Mia, con los cubos de datos girando sobre su mano."]),
            m(id="R02-N01-P4", titulo="Cómo se ve en el registro",
              lugar="La Sala de los Moldes", personajes="Mia, Gheco, Sila",
              carta="__str__ | def __str__(self): return f\"...\" · lo usa print(objeto)",
              recompensa="xp 10, oro 10",
              escena="""
                  Imprimís un orco y el pergamino escribe `<__main__.Orco object at 0x7f3a…>`.
                  —Eso no lo entiende nadie —dice Sila—. Enseñale al molde cómo **presentarse**.
              """,
              sugiere="Los métodos con doble guion bajo le enseñan a tu clase a funcionar con Python. `__str__` devuelve el texto que muestra `print(objeto)`.",
              desafio="Completá el nombre del método para que `print` muestre la ficha.",
              inicial='''
                  class Orco:
                      def __init__(self, nombre, vida):
                          self.nombre = nombre
                          self.vida = vida

                      def ___(self):
                          return f"{self.nombre} ({self.vida} de vida)"

                  print(Orco("Grum", 40))
              ''',
              solucion='''
                  class Orco:
                      def __init__(self, nombre, vida):
                          self.nombre = nombre
                          self.vida = vida

                      def __str__(self):
                          return f"{self.nombre} ({self.vida} de vida)"

                  print(Orco("Grum", 40))
              ''',
              solucion_txt="`def __str__(self):`.",
              al_superar="El registro se reescribe solo, prolijo: «Grum (40 de vida)». Sila asiente y lo archiva.",
              imagen=["Un pergamino que pasa de un garabato `0x7f3a…` a una ficha prolija: «Grum (40 de vida)».",
                      "Sila lo archiva en un cajón de bronce."]),
            m(id="R02-N01-P5", titulo="La vida en porcentaje",
              lugar="La Sala de los Moldes", personajes="Mia, Gheco, Sila, Tilo",
              carta="@property | @property def porcentaje(self): · se usa sin paréntesis: tilo.porcentaje",
              recompensa="xp 15, oro 15",
              escena="""
                  Tilo entra corriendo con un raspón nuevo. —¿Cuánta vida me queda? Pero en porcentaje, que los números sueltos no los entiendo.
              """,
              sugiere="Con `@property` arriba, un método se usa **como un atributo**, sin paréntesis. Sirve para valores que se **calculan** con otros: `self.vida / self.vida_max`.",
              desafio="Poné lo que falta arriba de `porcentaje`.",
              inicial='''
                  class Personaje:
                      def __init__(self, nombre, vida_max):
                          self.nombre = nombre
                          self.vida = vida_max
                          self.vida_max = vida_max

                      ___
                      def porcentaje(self):
                          return self.vida / self.vida_max

                  tilo = Personaje("Tilo", 80)
                  tilo.vida -= 20
                  print(f"A {tilo.nombre} le queda {tilo.porcentaje:.0%}")
              ''',
              solucion='''
                  class Personaje:
                      def __init__(self, nombre, vida_max):
                          self.nombre = nombre
                          self.vida = vida_max
                          self.vida_max = vida_max

                      @property
                      def porcentaje(self):
                          return self.vida / self.vida_max

                  tilo = Personaje("Tilo", 80)
                  tilo.vida -= 20
                  print(f"A {tilo.nombre} le queda {tilo.porcentaje:.0%}")
              ''',
              solucion_txt="`@property`.",
              al_superar="—¡Setenta y cinco por ciento! —festeja Tilo—. Eso lo entiendo. —Y se va corriendo otra vez, a raspar el veinticinco que le queda.",
              imagen=["Tilo con una barra de vida flotando sobre la cabeza: `75%`.",
                      "Mia se ríe; Sila niega con la cabeza, divertida."]),
            m(id="R02-N01-P6", titulo="El molde rápido",
              lugar="La Sala de los Moldes", personajes="Mia, Gheco, Sila",
              carta="@dataclass | @dataclass class Item: nombre: str · valor: int = 0 · escribe __init__, __repr__ y __eq__",
              recompensa="xp 15, oro 15",
              escena="""
                  Sila te muestra una pila de moldes que solo **guardan datos**: libros, llaves, pociones.
                  —Para estos hay un atajo. Les decís qué campos tienen, y el molde se escribe solo.
              """,
              sugiere="`@dataclass` arriba de la clase escribe por vos `__init__`, `__repr__` y `__eq__` a partir de los campos anotados (`nombre: str`). Se importa con `from dataclasses import dataclass`.",
              desafio="Poné el decorador que falta.",
              inicial='''
                  from dataclasses import dataclass

                  ___
                  class Libro:
                      titulo: str
                      paginas: int = 100

                  libro = Libro("Crónicas del Valle", 320)
                  print(libro)
                  print(libro == Libro("Crónicas del Valle", 320))
              ''',
              solucion='''
                  from dataclasses import dataclass

                  @dataclass
                  class Libro:
                      titulo: str
                      paginas: int = 100

                  libro = Libro("Crónicas del Valle", 320)
                  print(libro)
                  print(libro == Libro("Crónicas del Valle", 320))
              ''',
              solucion_txt="`@dataclass`.",
              al_superar="""
                  El libro aparece entero en el pergamino, con su título y sus páginas. Sila lo guarda y baja la voz.
                  —Te voy a decir algo, Mia. Alguien está **mezclando los registros** de la Biblioteca. Y no sé quién.
              """,
              imagen=["Una pila de moldes de bronce con forma de libro, llave y poción.",
                      "Sila, seria, se inclina hacia Mia y le habla en voz baja.",
                      "Detrás, un estante con fichas tachadas y mezcladas."]),
        ],
    },
    {
        "titulo": "R02-N02 · Herencia y polimorfismo",
        "misiones": [
            m(id="R02-N02-P1", titulo="Lo común, una vez",
              lugar="El Ala de Estrategia", personajes="Mia, Gheco, Sila",
              carta="Herencia | class Heroe(Entidad): · hereda atributos y métodos · «un héroe ES UNA entidad»",
              recompensa="xp 10, oro 10",
              escena="""
                  El Ala de Estrategia es una mesa enorme con un mapa de batalla vivo: héroes, enemigos y torres de piedra que se mueven solos.
                  —Todos tienen vida y todos reciben daño —dice Sila—. No lo escribas tres veces. Escribilo **una**, y que los demás lo **hereden**.
              """,
              sugiere="`class Heroe(Entidad):` dice que `Heroe` **hereda** todo lo de `Entidad`: sus atributos y sus métodos. Se usa cuando la relación es «**es un**»: un héroe **es una** entidad.",
              desafio="Hacé que `Heroe` herede de `Entidad`.",
              inicial='''
                  class Entidad:
                      def __init__(self, nombre, vida):
                          self.nombre = nombre
                          self.vida = vida

                      def recibir(self, danio):
                          self.vida = max(0, self.vida - danio)

                  class Heroe(___):
                      pass

                  mia = Heroe("Mia", 100)
                  mia.recibir(25)
                  print(mia.nombre, mia.vida)
              ''',
              solucion='''
                  class Entidad:
                      def __init__(self, nombre, vida):
                          self.nombre = nombre
                          self.vida = vida

                      def recibir(self, danio):
                          self.vida = max(0, self.vida - danio)

                  class Heroe(Entidad):
                      pass

                  mia = Heroe("Mia", 100)
                  mia.recibir(25)
                  print(mia.nombre, mia.vida)
              ''',
              solucion_txt="`class Heroe(Entidad):`.",
              al_superar="Tu figurita aparece en el mapa de batalla, con su barra de vida. No escribiste nada de daño, y lo recibe igual.",
              imagen=["Una mesa-mapa de batalla viva, con figuras de luz de héroes, enemigos y torres.",
                      "La figurita de Mia, con su barra de vida en 75.",
                      "Sila señala el mapa con una regla larga."]),
            m(id="R02-N02-P2", titulo="No te olvides de la base",
              lugar="El Ala de Estrategia", personajes="Mia, Gheco, Sila",
              carta="super() | super().__init__(nombre, 100) · primero arma la base y después lo propio",
              recompensa="xp 10, oro 10",
              escena="""
                  Tu héroe necesita algo que la entidad no tiene: **pociones**. Le escribís su propio `__init__`… y de pronto la figurita no tiene nombre ni vida.
                  —Te olvidaste de llamar a la base —dice Sila—. Que arme lo suyo primero.
              """,
              sugiere="Si la subclase tiene su propio `__init__`, el de la base **no** se ejecuta solo. Llamalo con `super().__init__(...)` y después agregá lo propio.",
              desafio="Llamá al `__init__` de la base.",
              inicial='''
                  class Entidad:
                      def __init__(self, nombre, vida):
                          self.nombre = nombre
                          self.vida = vida

                  class Heroe(Entidad):
                      def __init__(self, nombre):
                          ___
                          self.pociones = 2

                  mia = Heroe("Mia")
                  print(mia.nombre, mia.vida, mia.pociones)
              ''',
              solucion='''
                  class Entidad:
                      def __init__(self, nombre, vida):
                          self.nombre = nombre
                          self.vida = vida

                  class Heroe(Entidad):
                      def __init__(self, nombre):
                          super().__init__(nombre, 100)
                          self.pociones = 2

                  mia = Heroe("Mia")
                  print(mia.nombre, mia.vida, mia.pociones)
              ''',
              solucion_txt="`super().__init__(nombre, 100)`.",
              al_superar="La figurita recupera su nombre y su vida, y ahora lleva dos frasquitos verdes en el cinturón.",
              imagen=["La figurita de Mia en el mapa, con dos frasquitos verdes al cinturón.",
                      "Una flecha de luz que sube de `Heroe` a `Entidad` con la palabra `super()`."]),
            m(id="R02-N02-P3", titulo="Cada uno a su manera",
              lugar="El Ala de Estrategia", personajes="Mia, Gheco, Sila",
              carta="Polimorfismo | la misma llamada (e.turno()), distinta respuesta · cada subclase redefine el método",
              recompensa="xp 10, oro 10",
              escena="""
                  —Ahora el turno —dice Sila—. El orco ataca, la arquera dispara. El mapa no pregunta quién es quién: a cada uno le dice «jugá tu turno».
                  Pero tu arquera se queda quieta: su método se llama distinto.
              """,
              sugiere="Una subclase puede **redefinir** un método de la base. Para que el bucle llame al de cada una, tiene que llamarse **igual**. Eso es el **polimorfismo**: la misma llamada, distintas respuestas.",
              desafio="Poné el nombre justo al método de la arquera.",
              inicial='''
                  class Entidad:
                      def __init__(self, nombre):
                          self.nombre = nombre

                      def turno(self):
                          return f"{self.nombre} espera"

                  class Orco(Entidad):
                      def turno(self):
                          return f"{self.nombre} ataca con el hacha"

                  class Arquera(Entidad):
                      def ___(self):
                          return f"{self.nombre} dispara una flecha"

                  for e in [Orco("Grum"), Arquera("Nima"), Entidad("Un aldeano")]:
                      print(e.turno())
              ''',
              solucion='''
                  class Entidad:
                      def __init__(self, nombre):
                          self.nombre = nombre

                      def turno(self):
                          return f"{self.nombre} espera"

                  class Orco(Entidad):
                      def turno(self):
                          return f"{self.nombre} ataca con el hacha"

                  class Arquera(Entidad):
                      def turno(self):
                          return f"{self.nombre} dispara una flecha"

                  for e in [Orco("Grum"), Arquera("Nima"), Entidad("Un aldeano")]:
                      print(e.turno())
              ''',
              solucion_txt="`def turno(self):`.",
              al_superar="En el mapa, cada figura juega a su manera: el orco levanta el hacha, la arquera tensa el arco y el aldeano… espera.",
              imagen=["Tres figuras de luz en el mapa: un orco con hacha, una arquera tensando el arco y un aldeano quieto.",
                      "Un mismo rayo que sale del pergamino de Mia hacia los tres: `turno()`."]),
            m(id="R02-N02-P4", titulo="La torre que no es entidad",
              lugar="El Ala de Estrategia", personajes="Mia, Gheco, Sila",
              criatura="orco",
              carta="Duck typing | no importa de qué clase viene, sino qué métodos tiene · AttributeError: le falta ese método",
              recompensa="xp 10, oro 10",
              escena="""
                  Sila pone en el mapa una **torre de piedra**. No es una entidad, no hereda de nadie. Pero cuando le toca el turno, el mapa explota: `AttributeError`. Detrás del humo, un **orco** se ríe.
                  —Los orcos nacen de **pedir lo que no está** —dice Gheco—. El mapa le pidió `turno` a la torre… y la torre tiene otro nombre.
              """,
              sugiere="En Python no hace falta heredar para entrar en el bucle: alcanza con **tener el método** que se usa. «Si camina como pato y hace cuac, es un pato.» Eso se llama **duck typing**.",
              desafio="Arreglá la torre para que juegue su turno como las demás.",
              inicial='''
                  class Orco:
                      def turno(self):
                          return "El orco ataca"

                  class Torre:
                      def disparar(self):
                          return "La torre lanza una piedra"

                  for e in [Orco(), Torre()]:
                      print(e.turno())
              ''',
              solucion='''
                  class Orco:
                      def turno(self):
                          return "El orco ataca"

                  class Torre:
                      def turno(self):
                          return "La torre lanza una piedra"

                  for e in [Orco(), Torre()]:
                      print(e.turno())
              ''',
              solucion_txt="Renombrar `disparar` a `turno`: el bucle llama a `turno()` en todos.",
              al_superar="La torre gira sobre sí misma y le tira una piedra al orco, que se va rengueando. Sila anota algo en su libreta: «la nueva entiende rápido».",
              imagen=["Una torre de piedra en el mapa lanza una piedra a un orco que huye rengueando.",
                      "Humo de un error que se disipa: `AttributeError` tachado.",
                      "Sila anota en su libreta."]),
            m(id="R02-N02-P5", titulo="El contrato",
              lugar="El Ala de Estrategia", personajes="Mia, Gheco, Sila",
              carta="Clase abstracta | class Entidad(ABC): · @abstractmethod def turno · sin turno: TypeError al crear",
              recompensa="xp 15, oro 15",
              escena="""
                  —Para que no vuelva a pasar —dice Sila—, la base deja **escrito el contrato**: toda entidad tiene que saber jugar su turno. Si alguien crea una que no sabe, el mapa no la acepta.
                  Probás con un gólem nuevo y el mapa lo rechaza: `TypeError`.
              """,
              sugiere="Con `ABC` y `@abstractmethod`, la base dice qué métodos **tiene** que tener toda subclase. Si falta alguno, crear el objeto da `TypeError` **enseguida**, no a mitad de la batalla.",
              desafio="Hacé que el gólem cumpla el contrato: que juegue su turno con «Gólem golpea el suelo».",
              inicial='''
                  from abc import ABC, abstractmethod

                  class Entidad(ABC):
                      @abstractmethod
                      def turno(self):
                          ...

                  class Golem(Entidad):
                      pass

                  print(Golem().turno())
              ''',
              solucion='''
                  from abc import ABC, abstractmethod

                  class Entidad(ABC):
                      @abstractmethod
                      def turno(self):
                          ...

                  class Golem(Entidad):
                      def turno(self):
                          return "Gólem golpea el suelo"

                  print(Golem().turno())
              ''',
              solucion_txt="Agregarle al gólem `def turno(self): return \"Gólem golpea el suelo\"`.",
              al_superar="""
                  El gólem de piedra entra al mapa y da un pisotón que hace saltar a todas las figuras.
                  Sila mira hacia abajo, hacia una escalera húmeda. —Los registros dañados vienen del **Sótano**. Mañana bajamos.
              """,
              imagen=["Un pequeño gólem de piedra en el mapa da un pisotón: todas las figuras saltan.",
                      "Sila señala una escalera de piedra que baja hacia la oscuridad, con humedad en los escalones."]),
        ],
    },
    {
        "titulo": "R02-N03 · Excepciones y archivos",
        "misiones": [
            m(id="R02-N03-P1", titulo="Intentar",
              lugar="El Sótano del Bastión", personajes="Mia, Gheco, Sila",
              carta="try / except | try: lo que puede fallar · except ValueError: qué hacer · el programa sigue",
              recompensa="xp 10, oro 10",
              escena="""
                  El Sótano gotea. Los pergaminos están húmedos, y en uno el nivel de un aventurero dice «tres» con letras. Lo convertís a número y el hechizo explota: `ValueError`.
                  —No te asustes —dice {mentor}, que bajó con ustedes—. **Intentá**, y tené preparado qué hacer si sale mal.
              """,
              sugiere="Lo que puede fallar va en `try:`. Si lanza el error que nombrás en `except`, Python salta ahí y el programa **sigue**. Si no falla, el `except` se saltea.",
              desafio="Atrapá el error de conversión: si el nivel no es un número, que valga 1.",
              inicial='''
                  for texto in ["7", "tres", "12"]:
                      try:
                          nivel = int(texto)
                      except ___:
                          nivel = 1
                      print(f"{texto} -> nivel {nivel}")
              ''',
              solucion='''
                  for texto in ["7", "tres", "12"]:
                      try:
                          nivel = int(texto)
                      except ValueError:
                          nivel = 1
                      print(f"{texto} -> nivel {nivel}")
              ''',
              solucion_txt="`except ValueError:`.",
              al_superar="El pergamino húmedo no explota: se queda quieto, con un «nivel 1» prolijo al lado del «tres». Y te das cuenta de algo raro: **el error no te dio miedo**.",
              imagen=["Un sótano de piedra húmedo, con goteras y pergaminos apilados.",
                      "Mia sostiene un pergamino mojado; de él sale un estallido de luz que se detiene en el aire, atrapado.",
                      "Ofidia, con una lámpara, la mira tranquila."]),
            m(id="R02-N03-P2", titulo="Lo que no está",
              lugar="El Sótano del Bastión", personajes="Mia, Gheco, Sila",
              carta="except ... as error | except KeyError as error: print(error) · atrapá lo que sabés manejar",
              recompensa="xp 10, oro 10",
              escena="""
                  Sila busca cosas en el inventario de un aventurero que no volvió: la espada está, el mapa no. Cada vez que pide algo que no está, salta un **orco**.
                  —Preguntá y, si no está, decí **qué** faltaba —dice Sila.
              """,
              sugiere="Pedirle a un diccionario una clave que no tiene lanza `KeyError`. Con `except KeyError as error:` guardás el error para mostrar qué clave faltaba.",
              desafio="Atrapá el error y mostrá qué faltó.",
              inicial='''
                  mochila = {"espada": 1, "antorcha": 3}
                  for cosa in ["espada", "mapa", "antorcha"]:
                      try:
                          print(f"{cosa}: {mochila[cosa]}")
                      except ___ as error:
                          print(f"Falta {error}")
              ''',
              solucion='''
                  mochila = {"espada": 1, "antorcha": 3}
                  for cosa in ["espada", "mapa", "antorcha"]:
                      try:
                          print(f"{cosa}: {mochila[cosa]}")
                      except KeyError as error:
                          print(f"Falta {error}")
              ''',
              solucion_txt="`except KeyError as error:`.",
              al_superar="El orco intenta salir de la mochila, pero tu `except` lo agarra de la oreja. Sila anota: «falta el mapa».",
              imagen=["Una mochila de cuero abierta sobre una mesa del sótano: una espada y antorchas; un hueco donde iba el mapa.",
                      "Un orco pequeño atrapado de la oreja por un lazo de luz que dice `except KeyError`."]),
            m(id="R02-N03-P3", titulo="Siempre se cierra",
              lugar="El Sótano del Bastión", personajes="Mia, Gheco, Ofidia",
              carta="else y finally | else: solo si NO hubo error · finally: SIEMPRE, con error o sin él",
              recompensa="xp 10, oro 10",
              escena="""
                  —Un buen mago, cuando abre un pergamino, **siempre** lo vuelve a cerrar —dice {mentor}—. Salga bien o salga mal.
              """,
              sugiere="Después del `except` pueden ir dos bloques más: `else:` corre **solo si no hubo error**, y `finally:` corre **siempre**. El `finally` es para lo que no se puede olvidar: cerrar, guardar, apagar.",
              desafio="Completá los dos bloques que faltan.",
              inicial='''
                  def abrir(texto):
                      try:
                          n = int(texto)
                      except ValueError:
                          print(f"{texto}: no se puede leer")
                      ___:
                          print(f"{texto}: página {n}")
                      ___:
                          print("pergamino cerrado")

                  abrir("4")
                  abrir("xx")
              ''',
              solucion='''
                  def abrir(texto):
                      try:
                          n = int(texto)
                      except ValueError:
                          print(f"{texto}: no se puede leer")
                      else:
                          print(f"{texto}: página {n}")
                      finally:
                          print("pergamino cerrado")

                  abrir("4")
                  abrir("xx")
              ''',
              solucion_txt="`else:` y `finally:`.",
              al_superar="Los dos pergaminos vuelven a su estante, enrollados y atados. Uno leído, el otro no, pero los dos **cerrados**.",
              imagen=["Dos pergaminos que se enrollan y se atan solos con cintas de luz.",
                      "Ofidia asiente, con la lámpara en alto."]),
            m(id="R02-N03-P4", titulo="El pergamino que no existe",
              lugar="El Sótano del Bastión", personajes="Mia, Gheco, Sila",
              carta="Archivos | with open(\"notas.txt\", \"w\", encoding=\"utf-8\") as f: · \"r\" leer · \"w\" escribir · \"a\" agregar",
              recompensa="xp 15, oro 15",
              item="Notas del Viajero",
              escena="""
                  En el fondo del Sótano hay un cajón con tu misma marca de agua: **un vitral**. Adentro, hojas a medio borrar. Copiás lo que se lee a un archivo nuevo antes de que la humedad se lo coma. Después buscás otra hoja que se nombra en ellas, «viajero.txt»… y no está.
              """,
              sugiere="`with open(nombre, \"w\", encoding=\"utf-8\") as f:` abre un archivo para **escribir** y lo **cierra solo** al terminar el bloque. Para leerlo, el modo es `\"r\"` (o ninguno). Si el archivo no existe, abrir para leer lanza `FileNotFoundError`.",
              desafio="Escribí las notas, leelas línea por línea, y atrapá el error del archivo que falta.",
              inicial='''
                  with open("notas.txt", "w", encoding="utf-8") as f:
                      f.write("la lengua mas clara\\n")
                      f.write("para quien llegue\\n")

                  with open("notas.txt", encoding="utf-8") as f:
                      for linea in f:
                          print(linea.strip())

                  try:
                      with open("viajero.txt", encoding="utf-8") as f:
                          print(f.read())
                  except ___:
                      print("No está: viajero.txt")
              ''',
              solucion='''
                  with open("notas.txt", "w", encoding="utf-8") as f:
                      f.write("la lengua mas clara\\n")
                      f.write("para quien llegue\\n")

                  with open("notas.txt", encoding="utf-8") as f:
                      for linea in f:
                          print(linea.strip())

                  try:
                      with open("viajero.txt", encoding="utf-8") as f:
                          print(f.read())
                  except FileNotFoundError:
                      print("No está: viajero.txt")
              ''',
              solucion_txt="`except FileNotFoundError:`.",
              al_superar="""
                  Dos frases, a salvo: «la lengua más clara» y «para quien llegue». Las **Notas del Viajero** van a tu mochila.
                  —Es la misma marca que tu pergamino —dice Gheco, muy bajito.
              """,
              imagen=["Un cajón de madera húmedo con un vitral grabado en la tapa; adentro, hojas a medio borrar.",
                      "Mia copia las frases al pergamino; las letras pasan de la hoja vieja a la nueva como luciérnagas.",
                      "Gheco, serio, mira la marca del vitral."]),
            m(id="R02-N03-P5", titulo="Avisar con nombre propio",
              lugar="El Sótano del Bastión", personajes="Mia, Gheco, Sila, Ofidia",
              carta="raise | class PergaminoRoto(Exception): pass · raise PergaminoRoto(\"...\") · se atrapa aparte",
              recompensa="xp 15, oro 20",
              item="Amuleto del Traceback",
              se_abre="el **Amuleto del Traceback**: una segunda vida en las expediciones (equipalo como accesorio).",
              escena="""
                  Sila quiere que el catálogo **avise** cuando le piden una página que no puede existir, en vez de devolver cualquier cosa.
                  —Que el error tenga **nombre** —dice {mentor}—. Así quien lo reciba sabe exactamente qué pasó.
              """,
              sugiere="Una excepción propia es una clase que hereda de `Exception`. Con `raise PergaminoRoto(\"…\")` tu función avisa que algo está mal, y quien la llama la atrapa con `except PergaminoRoto`.",
              desafio="Lanzá el error cuando la página sea negativa.",
              inicial='''
                  class PergaminoRoto(Exception):
                      pass

                  def leer(pagina):
                      if pagina < 0:
                          ___ PergaminoRoto(f"la página {pagina} no existe")
                      return f"Página {pagina}: legible"

                  for p in [3, -2]:
                      try:
                          print(leer(p))
                      except PergaminoRoto as error:
                          print(f"Aviso: {error}")
              ''',
              solucion='''
                  class PergaminoRoto(Exception):
                      pass

                  def leer(pagina):
                      if pagina < 0:
                          raise PergaminoRoto(f"la página {pagina} no existe")
                      return f"Página {pagina}: legible"

                  for p in [3, -2]:
                      try:
                          print(leer(p))
                      except PergaminoRoto as error:
                          print(f"Aviso: {error}")
              ''',
              solucion_txt="`raise PergaminoRoto(...)`.",
              al_superar="""
                  {mentor} saca de su manga un amuleto con forma de pergamino enroscado y te lo cuelga del cuello.
                  —El **Amuleto del Traceback**. Quien sabe leer su error, se levanta una vez más. —Y agrega—: Ya no le tenés miedo. Se te nota.
              """,
              imagen=["Ofidia cuelga un amuleto con forma de pergamino enroscado del cuello de Mia.",
                      "El amuleto brilla en violeta, con una línea de traceback grabada.",
                      "Sila y Gheco miran, contentos; el sótano está ordenado."]),
        ],
    },
    {
        "titulo": "R02-N04 · JSON y CSV: guardar la partida",
        "misiones": [
            m(id="R02-N04-P1", titulo="De diccionario a texto",
              lugar="El Archivo", personajes="Mia, Gheco, Sila",
              carta="json.dumps | json.dumps(datos, ensure_ascii=False) → texto · False se escribe false · None, null",
              recompensa="xp 10, oro 10",
              escena="""
                  En el Archivo, las crónicas se guardan en un idioma que cualquier mago del reino sabe leer.
                  —Se llama **JSON** —dice Sila—. Es casi igual a tus diccionarios, pero en texto. Pasá la primera nota del viajero.
              """,
              sugiere="`import json`. `json.dumps(datos)` convierte un diccionario (o lista) en **texto** JSON. Con `ensure_ascii=False`, los acentos quedan tal cual. Fijate: `False` pasa a `false` y `None` a `null`.",
              desafio="Convertí la nota a texto JSON.",
              inicial='''
                  import json

                  nota = {"autor": "el viajero", "página": 3, "legible": False, "fecha": None}
                  texto = json.___(nota, ensure_ascii=False)
                  print(texto)
                  print(type(texto).__name__)
              ''',
              solucion='''
                  import json

                  nota = {"autor": "el viajero", "página": 3, "legible": False, "fecha": None}
                  texto = json.dumps(nota, ensure_ascii=False)
                  print(texto)
                  print(type(texto).__name__)
              ''',
              solucion_txt="`json.dumps`.",
              al_superar="La nota se escribe en una tira de papel, en el idioma del Archivo. Sila la cuelga junto a otras mil.",
              imagen=["El Archivo: pasillos de tiras de papel colgadas como banderines, cada una con llaves `{}`.",
                      "Sila cuelga una tira nueva; Mia sostiene el pergamino con el texto JSON."]),
            m(id="R02-N04-P2", titulo="Y de vuelta",
              lugar="El Archivo", personajes="Mia, Gheco, Sila",
              carta="json.loads | json.loads(texto) → diccionario · después se usa como siempre: datos[\"clave\"]",
              recompensa="xp 10, oro 10",
              escena="""
                  Sila descuelga una tira vieja: la crónica de un aventurero que pasó hace años.
                  —Leela. Quiero saber el segundo objeto de su inventario.
              """,
              sugiere="`json.loads(texto)` hace el camino inverso: del **texto** JSON a diccionarios y listas de Python. Después se usan como siempre.",
              desafio="Convertí el texto y mostrá lo que se pide.",
              inicial='''
                  import json

                  texto = '{"heroe": "Nima", "nivel": 4, "inventario": ["soga", "brújula", "pan"]}'
                  datos = json.___(texto)
                  print(datos["heroe"], datos["nivel"] + 1)
                  print(datos["inventario"][1])
              ''',
              solucion='''
                  import json

                  texto = '{"heroe": "Nima", "nivel": 4, "inventario": ["soga", "brújula", "pan"]}'
                  datos = json.loads(texto)
                  print(datos["heroe"], datos["nivel"] + 1)
                  print(datos["inventario"][1])
              ''',
              solucion_txt="`json.loads`.",
              al_superar="Una brújula vieja. —Nima —dice Sila—. Una arquera que fue hacia las Forjas. Nunca volvió a escribir.",
              imagen=["Una tira de papel vieja que se convierte en un cofrecito con soga, brújula y pan.",
                      "Mia sostiene la brújula; Sila mira hacia lejos."]),
            m(id="R02-N04-P3", titulo="Guardar la partida",
              lugar="El Archivo", personajes="Mia, Gheco, Sila",
              carta="json.dump / json.load | con un archivo abierto · indent=2 lo hace legible · sin s: archivo; con s: texto",
              recompensa="xp 15, oro 15",
              escena="""
                  —Si tu partida no se puede guardar, se pierde al apagar la vela —dice Sila—. Guardala en un archivo y volvé a cargarla. Si sale igual, está bien guardada.
              """,
              sugiere="`json.dump(datos, f)` escribe **en un archivo** abierto; `json.load(f)` lee de uno. (Sin la `s`: archivo. Con la `s`: texto.) `indent=2` lo deja legible.",
              desafio="Guardá y volvé a cargar la partida.",
              inicial='''
                  import json

                  partida = {"heroe": "Mia", "nivel": 12, "oro": 340, "ítems": ["amuleto", "notas"]}

                  with open("partida.json", "w", encoding="utf-8") as f:
                      json.___(partida, f, indent=2, ensure_ascii=False)

                  with open("partida.json", encoding="utf-8") as f:
                      cargada = json.___(f)

                  print(cargada["heroe"], cargada["nivel"])
                  print(cargada == partida)
              ''',
              solucion='''
                  import json

                  partida = {"heroe": "Mia", "nivel": 12, "oro": 340, "ítems": ["amuleto", "notas"]}

                  with open("partida.json", "w", encoding="utf-8") as f:
                      json.dump(partida, f, indent=2, ensure_ascii=False)

                  with open("partida.json", encoding="utf-8") as f:
                      cargada = json.load(f)

                  print(cargada["heroe"], cargada["nivel"])
                  print(cargada == partida)
              ''',
              solucion_txt="`json.dump` y `json.load`.",
              al_superar="Tu partida queda guardada en el Archivo, en su propio cajón. Sila le pega una etiqueta: «Mia, la que llegó con el pergamino».",
              imagen=["Un cajón de archivo con una etiqueta escrita a mano: «Mia».",
                      "Adentro, un pergamino con el JSON de la partida, prolijo, con sangría."]),
            m(id="R02-N04-P4", titulo="El héroe al papel",
              lugar="El Archivo", personajes="Mia, Gheco, Sila, Tilo",
              carta="asdict y ** | asdict(heroe) → dict para json · Heroe(**datos) lo reconstruye",
              recompensa="xp 15, oro 15",
              escena="""
                  Tilo quiere que su ficha también quede guardada. Pero su ficha es una dataclass, y `json` no sabe qué hacer con ella.
                  —Pasala a diccionario para guardarla —dice Sila—, y al cargarla, reconstruila.
              """,
              sugiere="`asdict(objeto)` convierte una dataclass en diccionario. Al cargar, `Heroe(**datos)` la arma otra vez: el `**` reparte el diccionario como argumentos por nombre.",
              desafio="Completá la conversión y la reconstrucción.",
              inicial='''
                  import json
                  from dataclasses import dataclass, asdict

                  @dataclass
                  class Heroe:
                      nombre: str
                      nivel: int

                  tilo = Heroe("Tilo", 3)
                  texto = json.dumps(___(tilo))
                  print(texto)

                  datos = json.loads(texto)
                  copia = Heroe(___datos)
                  print(copia)
                  print(copia == tilo)
              ''',
              solucion='''
                  import json
                  from dataclasses import dataclass, asdict

                  @dataclass
                  class Heroe:
                      nombre: str
                      nivel: int

                  tilo = Heroe("Tilo", 3)
                  texto = json.dumps(asdict(tilo))
                  print(texto)

                  datos = json.loads(texto)
                  copia = Heroe(**datos)
                  print(copia)
                  print(copia == tilo)
              ''',
              solucion_txt="`asdict(tilo)` y `Heroe(**datos)`.",
              al_superar="—¡Estoy en el Archivo! —grita Tilo, tan fuerte que tres archiveros le chistan a la vez.",
              imagen=["Tilo, emocionado, señala su cajón en el Archivo; tres archiveros le chistan.",
                      "Sila se tapa la cara con la mano, divertida."]),
            m(id="R02-N04-P5", titulo="La planilla de Baldo",
              lugar="El Archivo", personajes="Mia, Gheco, Sila",
              criatura="goblin",
              carta="CSV | csv.writer(f).writerow([...]) · csv.DictReader(f) · al leer, TODO es texto: convertí",
              recompensa="xp 15, oro 15",
              escena="""
                  Baldo mandó sus ventas en una **planilla**: un CSV, columnas separadas por comas. Querés sumar las cantidades, y el pergamino escribe `"325"`. Un **goblin** salta de entre las columnas.
                  —Mezclaste tipos otra vez —dice Gheco—. Al leer un CSV, **todo** viene como texto.
              """,
              sugiere="`csv.writer(f)` escribe filas; `csv.DictReader(f)` lee cada fila como un diccionario con los nombres de la primera línea. Ojo: todo lo que se lee es `str`. Para sumar, convertí con `int()`.",
              desafio="Arreglá la suma.",
              inicial='''
                  import csv

                  with open("ventas.csv", "w", newline="", encoding="utf-8") as f:
                      escritor = csv.writer(f)
                      escritor.writerow(["producto", "cantidad"])
                      escritor.writerow(["poción", 3])
                      escritor.writerow(["soga", 2])
                      escritor.writerow(["pan", 5])

                  total = 0
                  with open("ventas.csv", newline="", encoding="utf-8") as f:
                      for fila in csv.DictReader(f):
                          total += fila["cantidad"]
                  print(f"Vendió {total} cosas")
              ''',
              solucion='''
                  import csv

                  with open("ventas.csv", "w", newline="", encoding="utf-8") as f:
                      escritor = csv.writer(f)
                      escritor.writerow(["producto", "cantidad"])
                      escritor.writerow(["poción", 3])
                      escritor.writerow(["soga", 2])
                      escritor.writerow(["pan", 5])

                  total = 0
                  with open("ventas.csv", newline="", encoding="utf-8") as f:
                      for fila in csv.DictReader(f):
                          total += int(fila["cantidad"])
                  print(f"Vendió {total} cosas")
              ''',
              solucion_txt="`total += int(fila[\"cantidad\"])`.",
              al_superar="""
                  Diez cosas. El goblin se escurre entre las columnas y desaparece.
                  Pero cuando volvés a mirar las copias de las notas del viajero… **cambiaron**. Una palabra tachada, un número donde había una letra. Sila palidece. —Alguien las está corrompiendo. Desde **la Bóveda**.
              """,
              imagen=["Una planilla de luz con columnas `producto` y `cantidad`; un goblin se escurre entre las filas.",
                      "Las copias de las notas del viajero, con palabras tachadas y números raros.",
                      "Sila, pálida, mira hacia una puerta de hierro al fondo del Archivo."]),
        ],
    },
    {
        "titulo": "R02-N05 · Jefe: el Archivista Corrupto",
        "misiones": [
            m(id="R02-N05-P1", titulo="El campo que falta",
              lugar="La Bóveda", personajes="Mia, Gheco, Sila",
              criatura="orco",
              carta="Revisar antes de usar | \"vida\" in registro · registro.get(\"vida\") → None si falta",
              recompensa="xp 15, oro 15",
              escena="""
                  La Bóveda es redonda y oscura. En el centro flota el **Archivista Corrupto**: una figura hecha de hojas arrancadas, con tinta que le chorrea de los dedos. Te tira registros a los que les **borró campos**, y de cada hueco sale un **orco**.
              """,
              sugiere="Antes de usar una clave que puede faltar, preguntá: `\"vida\" in registro`. O usá `registro.get(\"vida\")`, que devuelve `None` en vez de explotar.",
              desafio="Mostrá la vida de cada uno, o avisá si el campo falta.",
              inicial='''
                  registros = [
                      {"nombre": "Nima", "vida": 80},
                      {"nombre": "Brak"},
                      {"nombre": "Sila", "vida": 95},
                  ]
                  for r in registros:
                      if ___:
                          print(f"{r['nombre']}: {r['vida']}")
                      else:
                          print(f"{r['nombre']}: le borraron la vida")
              ''',
              solucion='''
                  registros = [
                      {"nombre": "Nima", "vida": 80},
                      {"nombre": "Brak"},
                      {"nombre": "Sila", "vida": 95},
                  ]
                  for r in registros:
                      if "vida" in r:
                          print(f"{r['nombre']}: {r['vida']}")
                      else:
                          print(f"{r['nombre']}: le borraron la vida")
              ''',
              solucion_txt="`if \"vida\" in r:`.",
              al_superar="El orco del hueco se queda sin nada que agarrar y se disuelve en tinta. El Archivista chilla con un ruido de papel que se rompe.",
              imagen=["La Bóveda redonda y oscura; en el centro, el Archivista Corrupto: una figura de hojas arrancadas con tinta chorreando de los dedos.",
                      "Un orco de tinta que se disuelve en el aire.",
                      "Mia, firme, con los cubos de datos girando sobre sus manos."]),
            m(id="R02-N05-P2", titulo="Palabras en lugar de números",
              lugar="La Bóveda", personajes="Mia, Gheco, Sila",
              criatura="goblin",
              carta="isinstance | isinstance(valor, int) · revisá el tipo de lo que viene de afuera",
              recompensa="xp 15, oro 15",
              escena="""
                  —¡Mucha! —grita el Archivista, y en un registro la vida dice `"mucha"` en vez de un número. Del papel salta un **goblin**.
              """,
              sugiere="Lo que viene de afuera puede tener **el tipo equivocado**. `isinstance(valor, int)` pregunta si es un entero antes de hacer cuentas con él.",
              desafio="Sumá solo las vidas que son números.",
              inicial='''
                  vidas = [80, "mucha", 95, "???", 40]
                  total = 0
                  for v in vidas:
                      if ___:
                          total += v
                      else:
                          print(f"Descartado: {v}")
                  print(f"Vida total: {total}")
              ''',
              solucion='''
                  vidas = [80, "mucha", 95, "???", 40]
                  total = 0
                  for v in vidas:
                      if isinstance(v, int):
                          total += v
                      else:
                          print(f"Descartado: {v}")
                  print(f"Vida total: {total}")
              ''',
              solucion_txt="`if isinstance(v, int):`.",
              al_superar="Los goblins se quedan con las palabras y vos con los números. El Archivista retrocede un paso: le arrancaste dos hojas.",
              imagen=["Dos goblins de tinta se llevan las palabras «mucha» y «???».",
                      "El Archivista retrocede; dos hojas se le desprenden del cuerpo."]),
            m(id="R02-N05-P3", titulo="El pergamino cortado",
              lugar="La Bóveda", personajes="Mia, Gheco, Sila",
              criatura="slime",
              carta="JSONDecodeError | try: json.loads(texto) · except json.JSONDecodeError: el texto está roto",
              recompensa="xp 15, oro 15",
              escena="""
                  El Archivista rompe un pergamino por la mitad y te lo tira. El JSON queda **cortado**, sin cerrar, y del corte gotea un **slime**.
                  —Si lo leés así, explota —dice Sila—. Separá lo sano de lo roto.
              """,
              sugiere="Si el texto no es un JSON válido, `json.loads` lanza `json.JSONDecodeError`. Atrapalo y seguí con el resto.",
              desafio="Leé los pergaminos que se puedan y contá los rotos.",
              inicial='''
                  import json

                  pergaminos = ['{"nombre": "Nima"}', '{"nombre": "Br', '{"nombre": "Tilo"}']
                  rotos = 0
                  for texto in pergaminos:
                      try:
                          print(json.loads(texto)["nombre"])
                      except ___:
                          rotos += 1
                  print(f"Rotos: {rotos}")
              ''',
              solucion='''
                  import json

                  pergaminos = ['{"nombre": "Nima"}', '{"nombre": "Br', '{"nombre": "Tilo"}']
                  rotos = 0
                  for texto in pergaminos:
                      try:
                          print(json.loads(texto)["nombre"])
                      except json.JSONDecodeError:
                          rotos += 1
                  print(f"Rotos: {rotos}")
              ''',
              solucion_txt="`except json.JSONDecodeError:`.",
              al_superar="El slime se evapora. Los dos pergaminos sanos vuelven a su estante; el roto queda apartado, con una etiqueta: «reparar».",
              imagen=["Un pergamino partido al medio del que gotea un slime verde que se evapora.",
                      "Dos pergaminos sanos vuelan a su estante."]),
            m(id="R02-N05-P4", titulo="Validar al crear",
              lugar="La Bóveda", personajes="Mia, Gheco, Sila, Ofidia",
              criatura="ogro",
              carta="__post_init__ | en una dataclass, corre después de __init__ · ahí se valida y se lanza el error",
              recompensa="xp 20, oro 20",
              escena="""
                  El Archivista ya no rompe registros: ahora los **inventa**. Un héroe de nivel 900, otro de nivel -3. Corren sin error… y todo da mal. Es un **ogro**.
                  —No dejes entrar lo que no tiene sentido —dice {mentor}—. Revisalo **al crearlo**, no después.
              """,
              sugiere="En una dataclass, `__post_init__` se ejecuta justo después del `__init__` que escribe Python. Es el lugar para revisar los datos y lanzar un error si no tienen sentido.",
              desafio="Escribí el nombre del método que valida.",
              inicial='''
                  from dataclasses import dataclass

                  @dataclass
                  class Heroe:
                      nombre: str
                      nivel: int

                      def ___(self):
                          if not 1 <= self.nivel <= 50:
                              raise ValueError(f"{self.nombre}: nivel {self.nivel} fuera de rango")

                  for nombre, nivel in [("Mia", 12), ("Falso", 900), ("Tilo", 3), ("Nadie", -3)]:
                      try:
                          print(Heroe(nombre, nivel))
                      except ValueError as error:
                          print(f"Rechazado: {error}")
              ''',
              solucion='''
                  from dataclasses import dataclass

                  @dataclass
                  class Heroe:
                      nombre: str
                      nivel: int

                      def __post_init__(self):
                          if not 1 <= self.nivel <= 50:
                              raise ValueError(f"{self.nombre}: nivel {self.nivel} fuera de rango")

                  for nombre, nivel in [("Mia", 12), ("Falso", 900), ("Tilo", 3), ("Nadie", -3)]:
                      try:
                          print(Heroe(nombre, nivel))
                      except ValueError as error:
                          print(f"Rechazado: {error}")
              ''',
              solucion_txt="`def __post_init__(self):`.",
              al_superar="Los héroes inventados se deshacen en la puerta, antes de entrar. El Archivista se encoge: ya no le queda de qué estar hecho.",
              imagen=["Una puerta de luz en la Bóveda: dos héroes de tinta se deshacen al tocarla; Mia y Tilo pasan.",
                      "El Archivista, más chico, encogido."]),
            m(id="R02-N05-P5", titulo="El error que se traduce",
              lugar="La Bóveda", personajes="Mia, Gheco, Sila, Ofidia",
              criatura="dragón",
              carta="@classmethod y raise from | def desde_json(cls, texto): · raise PergaminoCorrupto(...) from error",
              recompensa="xp 25, oro 30",
              item="Pluma del Archivista",
              escena="""
                  Al Archivista le queda una sola hoja: la última nota del viajero. Para salvarla, la Biblioteca tiene que poder **armarla desde el JSON** y, si viene rota, avisar con **su propio** error, no con uno que nadie entiende.
              """,
              sugiere="Un `@classmethod` recibe la **clase** (`cls`) en vez del objeto: sirve para crear objetos de otra forma, como `Nota.desde_json(texto)`. Y `raise MiError(...) from error` traduce un error de bajo nivel a uno tuyo, sin perder el original.",
              desafio="Completá el decorador y la traducción del error.",
              inicial='''
                  import json
                  from dataclasses import dataclass

                  class PergaminoCorrupto(Exception):
                      pass

                  @dataclass
                  class Nota:
                      autor: str
                      texto: str

                      ___
                      def desde_json(cls, crudo):
                          try:
                              return cls(**json.loads(crudo))
                          except json.JSONDecodeError as error:
                              raise PergaminoCorrupto("la nota viene cortada") ___ error

                  for crudo in ['{"autor": "el viajero", "texto": "yo le debo una pieza"}', '{"autor": "el vi']:
                      try:
                          print(Nota.desde_json(crudo))
                      except PergaminoCorrupto as error:
                          print(f"Aviso: {error}")
              ''',
              solucion='''
                  import json
                  from dataclasses import dataclass

                  class PergaminoCorrupto(Exception):
                      pass

                  @dataclass
                  class Nota:
                      autor: str
                      texto: str

                      @classmethod
                      def desde_json(cls, crudo):
                          try:
                              return cls(**json.loads(crudo))
                          except json.JSONDecodeError as error:
                              raise PergaminoCorrupto("la nota viene cortada") from error

                  for crudo in ['{"autor": "el viajero", "texto": "yo le debo una pieza"}', '{"autor": "el vi']:
                      try:
                          print(Nota.desde_json(crudo))
                      except PergaminoCorrupto as error:
                          print(f"Aviso: {error}")
              ''',
              solucion_txt="`@classmethod` y `raise ... from error`.",
              al_superar="""
                  La última hoja se arma entera y el Archivista se deshace en papel picado que cae como nieve. Entre los papelitos, una **pluma de plata** que todavía escribe sola: la **Pluma del Archivista**.
                  Mirás tu túnica: las runas se encendieron **hasta los hombros**.
                  Las notas del viajero, ahora enteras, terminan así: «La lengua más clara es para escribir instrucciones que cualquiera pueda seguir. **La Torre del Reloj guarda el tiempo del Valle; yo le debo una pieza.**»
              """,
              imagen=["El Archivista Corrupto se deshace en papel picado que cae como nieve en la Bóveda.",
                      "Mia sostiene una pluma de plata que escribe sola en el aire.",
                      "Su túnica, con las runas encendidas en violeta hasta los hombros.",
                      "Sila lee en voz alta la última nota; a lo lejos, por una ventana, se ve la Torre del Reloj."]),
        ],
    },
]
