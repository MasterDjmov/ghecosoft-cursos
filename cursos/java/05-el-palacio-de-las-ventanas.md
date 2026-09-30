# RAMA R05 · El Palacio de las Ventanas: aplicaciones de escritorio

```meta
tipo: tronco
posicion: 5
```

## R05-N01 · La primera ventana: JFrame, componentes y eventos

```meta
tipo: tema
padre: R04-N08
precio: 10
criatura: slime
ejecutable: no
temas: gui.swing, gui.eventos, gui.componentes
```

### Crónica

En la cima de la capital se levanta el **Palacio de las Ventanas**. Adentro no hay pergaminos ni consolas: hay paneles de vidrio con botones, casilleros para escribir y carteles que cambian cuando alguien toca algo. Cualquier persona del Imperio, sepa o no programar, puede usarlos.

—Hasta ahora tus programas hablaban por la consola —dice {mentor}—. Acá aprendés a construir **ventanas**. Pero tienen una regla nueva: ya no decidís vos el orden de las cosas. El usuario hace clic cuando quiere, y tu programa **reacciona**, {heroe}.

### Objetivos

- Crear una ventana con `JFrame` y armar su contenido en un `JPanel`.
- Usar los componentes básicos: `JLabel`, `JTextField` y `JButton`.
- Reaccionar a eventos con `ActionListener` (con lambdas).
- Mostrar mensajes con `JOptionPane`.
- Entender el hilo de eventos (EDT) y por qué la ventana se crea con `SwingUtilities.invokeLater`.

### Antes de empezar

- Lambdas y clases anónimas (rama 3).
- Clases, herencia y composición (rama 2).

### Explicación

#### Swing
**Swing** es la biblioteca de Java para aplicaciones de escritorio: viene con el JDK
(no hay que instalar nada) y funciona igual en Linux, Windows y macOS. Sus clases están
en `javax.swing` y empiezan con `J`: `JFrame`, `JButton`, `JTable`. (Existe también
JavaFX, más moderna, pero Swing es la que pide la cátedra y la que usa el editor de
NetBeans.)

#### La ventana y su contenido
- `JFrame` es la **ventana**: tiene título, borde y los botones de cerrar y minimizar.
- `JPanel` es un **panel**: un contenedor donde se ponen los componentes.
- Los **componentes** son los controles: `JLabel` (texto fijo), `JTextField` (una línea
  para escribir), `JButton` (un botón).

La forma prolija es armar el contenido en una clase que **extiende `JPanel`**, y
ponerla en el `JFrame`:
```java
class PanelSaludo extends JPanel {
    private final JTextField campoNombre = new JTextField(12);
    private final JLabel resultado = new JLabel("Escribí tu nombre");

    PanelSaludo() {
        JButton saludar = new JButton("Saludar");
        add(new JLabel("Nombre:"));
        add(campoNombre);
        add(saludar);
        add(resultado);
        saludar.addActionListener(e -> resultado.setText("¡Hola, " + campoNombre.getText().trim() + "!"));
    }
}
```

#### Eventos: el programa reacciona
Cuando el usuario hace clic, Swing **avisa** a quien esté escuchando. Se registra un
*listener* con `addActionListener`; lo más cómodo es una lambda:
```java
boton.addActionListener(e -> hacerAlgo());
```
El `ActionListener` es una interfaz funcional con un solo método,
`actionPerformed(ActionEvent e)`. En un `JTextField`, el mismo evento se dispara al
apretar **Enter**.

#### El hilo de eventos (EDT)
Swing no es *thread-safe*: todo lo que toca la interfaz tiene que ejecutarse en un
hilo especial, el **hilo de despacho de eventos** (EDT). Los listeners ya corren ahí.
Para crear la ventana desde `main`, se le pide al EDT que lo haga:
```java
public static void main(String[] args) {
    SwingUtilities.invokeLater(() -> {
        JFrame ventana = new JFrame("Palacio de las Ventanas");
        ventana.setContentPane(new PanelSaludo());
        ventana.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);   // cerrar la ventana termina el programa
        ventana.pack();                                           // tamaño justo para el contenido
        ventana.setLocationRelativeTo(null);                      // centrada en la pantalla
        ventana.setVisible(true);                                 // recién ahora se muestra
    });
}
```
Si una tarea tarda (una consulta a la base), **no** va en el EDT: congela la ventana.
Eso se resuelve con `SwingWorker`, más adelante en esta rama.

#### Mensajes rápidos: `JOptionPane`
```java
JOptionPane.showMessageDialog(this, "Guardado");                              // un aviso
JOptionPane.showMessageDialog(this, "Falta el nombre", "Error", JOptionPane.ERROR_MESSAGE);
int r = JOptionPane.showConfirmDialog(this, "¿Borrar el héroe?");            // sí / no / cancelar
String texto = JOptionPane.showInputDialog(this, "¿Cuántas pociones?");      // pedir un dato
```

#### Leer y validar lo que se escribe
`campo.getText()` devuelve siempre un `String`. Si esperás un número, convertilo con
`Integer.parseInt` dentro de un `try`/`catch` y, si falla, avisá con un mensaje en la
ventana (no con `System.out`, que el usuario no ve).

#### Cómo ejecutar
Igual que cualquier programa: `java Palacio.java`. Se abre una ventana y el programa
sigue corriendo hasta que la cerrás.

> **Si venís de la consola.** En la consola, el programa pregunta y espera. En una
> ventana, el programa arma todo y **se queda esperando eventos**: el orden lo decide
> el usuario. Por eso el código se organiza en "qué hago cuando tocan este botón".

### Código de ejemplo

```java
/*
 * La primera ventana: la calculadora de tasas del Palacio.
 * Ejecutar con: java Palacio.java
 */
import java.awt.Color;
import java.awt.FlowLayout;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;

public class Palacio {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame ventana = new JFrame("Palacio de las Ventanas · Tasas");
            ventana.setContentPane(new PanelTasas());
            ventana.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            ventana.pack();
            ventana.setLocationRelativeTo(null);
            ventana.setVisible(true);
        });
    }
}

class PanelTasas extends JPanel {
    private final JTextField campoKilos = new JTextField(6);
    private final JLabel resultado = new JLabel("Ingresá la carga y tocá Calcular");

    PanelTasas() {
        setLayout(new FlowLayout(FlowLayout.LEFT, 10, 10));
        JButton calcular = new JButton("Calcular");
        JButton limpiar = new JButton("Limpiar");

        add(new JLabel("Carga (kg):"));
        add(campoKilos);
        add(calcular);
        add(limpiar);
        add(resultado);

        calcular.addActionListener(e -> calcular());
        campoKilos.addActionListener(e -> calcular());        // Enter en el campo también calcula
        limpiar.addActionListener(e -> {
            campoKilos.setText("");
            resultado.setText("Ingresá la carga y tocá Calcular");
            resultado.setForeground(Color.BLACK);
            campoKilos.requestFocusInWindow();
        });
    }

    private void calcular() {
        String texto = campoKilos.getText().trim();
        try {
            int kilos = Integer.parseInt(texto);
            if (kilos < 0) {
                throw new NumberFormatException();
            }
            int tasa = kilos <= 50 ? 5 : 5 + (kilos - 50) / 10;
            resultado.setText("Tasa: " + tasa + " denarios");
            resultado.setForeground(new Color(0, 110, 0));
        } catch (NumberFormatException ex) {
            resultado.setText("Carga inválida");
            resultado.setForeground(Color.RED);
            JOptionPane.showMessageDialog(this, "'" + texto + "' no es una carga válida", "Error", JOptionPane.ERROR_MESSAGE);
        }
    }
}
```

### ¿Para qué sirve?

Los sistemas de gestión que se usan en comercios, estudios contables, consultorios y oficinas públicas suelen ser aplicaciones de escritorio con ventanas: formularios de alta, listados y botones. La cátedra evalúa exactamente eso, y la lógica de eventos es la misma que vas a encontrar en Android, en la web y en los videojuegos.

### Errores habituales

**Slime: la ventana que no aparece.** Te olvidaste `setVisible(true)` (o lo llamaste
antes de agregar los componentes y no se ven hasta que la redimensionás: llamalo al
final).

**Ogro: el programa que no termina.** Sin `setDefaultCloseOperation(EXIT_ON_CLOSE)`, al
cerrar la ventana el programa sigue corriendo invisible.

**Ogro: la ventana diminuta o gigante.** Usá `pack()` para que se ajuste al contenido,
en lugar de un `setSize` fijo.

**Goblin: el número que no es número.** `Integer.parseInt(campo.getText())` con el campo
vacío lanza `NumberFormatException`; el listener se corta y el usuario no ve nada.
Atrapala y avisá en la ventana.

**Troll: tocar la interfaz desde otro hilo.** Crear o modificar componentes fuera del
EDT produce errores raros y aleatorios. Creá la ventana con `SwingUtilities.invokeLater`.

**Slime: sin pantalla.** `java.awt.HeadlessException` si ejecutás un programa con
ventanas en un servidor sin entorno gráfico.

### Misión R05-N01-M1 · El conversor de monedas

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Hacé una ventana para convertir pesos a denarios (1 denario = 250 pesos) y al revés:
un campo para el monto, dos botones (`Pesos → Denarios` y `Denarios → Pesos`) y una
etiqueta con el resultado con 2 decimales. Si el monto no es un número positivo, mostrá
un `JOptionPane` de error y dejá el foco en el campo. El contenido va en una clase que
extiende `JPanel` y la ventana se crea con `SwingUtilities.invokeLater`.

#### Criterio de aprobación

- El contenido es un `JPanel` propio y la ventana se crea en el EDT.
- Los dos botones tienen su listener (con lambdas).
- Valida el monto y avisa con `JOptionPane`.

#### Solución de referencia

```java
// Mision 1 - El conversor de monedas: JPanel propio, dos botones y validacion.
import java.util.Locale;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;

public class Conversor {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Cambista del Imperio");
            f.setContentPane(new PanelConversor());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

class PanelConversor extends JPanel {
    static final double PESOS_POR_DENARIO = 250;
    private final JTextField monto = new JTextField(8);
    private final JLabel resultado = new JLabel(" ");

    PanelConversor() {
        JButton aDenarios = new JButton("Pesos → Denarios");
        JButton aPesos = new JButton("Denarios → Pesos");
        add(new JLabel("Monto:"));
        add(monto);
        add(aDenarios);
        add(aPesos);
        add(resultado);
        aDenarios.addActionListener(e -> convertir(true));
        aPesos.addActionListener(e -> convertir(false));
    }

    private void convertir(boolean haciaDenarios) {
        double valor;
        try {
            valor = Double.parseDouble(monto.getText().trim());
            if (valor <= 0) {
                throw new NumberFormatException();
            }
        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(this, "Ingresá un monto positivo", "Monto inválido", JOptionPane.ERROR_MESSAGE);
            monto.requestFocusInWindow();
            return;
        }
        if (haciaDenarios) {
            resultado.setText(String.format("%.2f pesos = %.2f denarios", valor, valor / PESOS_POR_DENARIO));
        } else {
            resultado.setText(String.format("%.2f denarios = %.2f pesos", valor, valor * PESOS_POR_DENARIO));
        }
    }
}
```

### Misión R05-N01-M2 · El contador de la puerta

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El guardia de la puerta cuenta quién entra y quién sale. Hacé una ventana con una
etiqueta grande que muestre cuántas personas hay adentro, y tres botones: `Entra`
(suma 1), `Sale` (resta 1, sin bajar de 0) y `Reiniciar` (pregunta con
`showConfirmDialog` y, si confirma, vuelve a 0). Cuando hay **más de 10** personas, la
etiqueta se pone roja y el botón `Entra` se deshabilita (`setEnabled(false)`) hasta
que alguien salga.

#### Criterio de aprobación

- El estado (cuántos hay) es un atributo del panel.
- Los botones se habilitan o deshabilitan según el estado.
- `Reiniciar` pide confirmación.

#### Solución de referencia

```java
// Mision 2 - El contador de la puerta: estado en el panel y botones que se habilitan.
import java.awt.Color;
import java.awt.Font;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.SwingUtilities;

public class ContadorPuerta {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Puerta norte");
            f.setContentPane(new PanelContador());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

class PanelContador extends JPanel {
    static final int MAXIMO = 10;
    private int adentro = 0;
    private final JLabel cartel = new JLabel("0");
    private final JButton entra = new JButton("Entra");
    private final JButton sale = new JButton("Sale");

    PanelContador() {
        cartel.setFont(cartel.getFont().deriveFont(Font.BOLD, 32f));
        JButton reiniciar = new JButton("Reiniciar");
        add(cartel);
        add(entra);
        add(sale);
        add(reiniciar);
        entra.addActionListener(e -> cambiar(1));
        sale.addActionListener(e -> cambiar(-1));
        reiniciar.addActionListener(e -> {
            int r = JOptionPane.showConfirmDialog(this, "¿Volver el contador a 0?", "Reiniciar", JOptionPane.YES_NO_OPTION);
            if (r == JOptionPane.YES_OPTION) {
                adentro = 0;
                actualizar();
            }
        });
        actualizar();
    }

    private void cambiar(int delta) {
        adentro = Math.max(0, adentro + delta);
        actualizar();
    }

    private void actualizar() {
        cartel.setText(String.valueOf(adentro));
        cartel.setForeground(adentro > MAXIMO ? Color.RED : Color.BLACK);
        entra.setEnabled(adentro <= MAXIMO);
        sale.setEnabled(adentro > 0);
    }
}
```

### Misión R05-N01-M3 · La ficha del recluta

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Hacé un formulario con tres campos (nombre, edad y ciudad) y un botón `Registrar`. Al
tocarlo, validá: el nombre no vacío, la edad un número entre 16 y 60. Si hay errores,
mostralos **todos juntos** en un solo `JOptionPane` (uno por línea). Si está todo bien,
agregá la ficha a un `JTextArea` de solo lectura (`setEditable(false)`) que muestra los
registrados, limpiá los campos y dejá el foco en el nombre.

#### Criterio de aprobación

- Junta los errores en una lista y los muestra juntos.
- El `JTextArea` es de solo lectura y va acumulando fichas.

#### Solución de referencia

```java
// Mision 3 - La ficha del recluta: validar todo junto y acumular en un JTextArea.
import java.awt.BorderLayout;
import java.awt.GridLayout;
import java.util.ArrayList;
import java.util.List;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;

public class FichaRecluta {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Registro de reclutas");
            f.setContentPane(new PanelFicha());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

class PanelFicha extends JPanel {
    private final JTextField nombre = new JTextField(14);
    private final JTextField edad = new JTextField(4);
    private final JTextField ciudad = new JTextField(14);
    private final JTextArea registrados = new JTextArea(6, 28);

    PanelFicha() {
        super(new BorderLayout(8, 8));
        JPanel form = new JPanel(new GridLayout(4, 2, 6, 6));
        form.add(new JLabel("Nombre:"));
        form.add(nombre);
        form.add(new JLabel("Edad:"));
        form.add(edad);
        form.add(new JLabel("Ciudad:"));
        form.add(ciudad);
        JButton registrar = new JButton("Registrar");
        form.add(new JLabel());
        form.add(registrar);
        registrados.setEditable(false);
        add(form, BorderLayout.NORTH);
        add(new JScrollPane(registrados), BorderLayout.CENTER);
        registrar.addActionListener(e -> registrar());
    }

    private void registrar() {
        List<String> errores = new ArrayList<>();
        if (nombre.getText().isBlank()) {
            errores.add("Falta el nombre.");
        }
        int anios = -1;
        try {
            anios = Integer.parseInt(edad.getText().trim());
            if (anios < 16 || anios > 60) {
                errores.add("La edad tiene que estar entre 16 y 60.");
            }
        } catch (NumberFormatException ex) {
            errores.add("La edad tiene que ser un número.");
        }
        if (!errores.isEmpty()) {
            JOptionPane.showMessageDialog(this, String.join("\n", errores), "Revisá la ficha", JOptionPane.WARNING_MESSAGE);
            return;
        }
        registrados.append(nombre.getText().trim() + ", " + anios + " años, " + (ciudad.getText().isBlank() ? "sin ciudad" : ciudad.getText().trim()) + "\n");
        nombre.setText("");
        edad.setText("");
        ciudad.setText("");
        nombre.requestFocusInWindow();
    }
}
```

### Encargo R05-N01-E1 · La calculadora del almacén

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Hacé la calculadora de un almacén: campos para el precio unitario y la cantidad, una
casilla de verificación (`JCheckBox`) "Paga con tarjeta" (recargo del 10 %) y un botón
`Agregar`. Cada ítem agregado suma al total, que se muestra en una etiqueta con 2
decimales, y aparece en un `JTextArea`. Un botón `Nueva venta` limpia todo. Validá los
números con mensajes.

#### Criterio de aprobación

- Usa `JCheckBox` (`isSelected()`) para el recargo.
- El total se acumula y se reinicia con `Nueva venta`.

#### Solución de referencia

```java
// Encargo - La calculadora del almacen.
import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.util.Locale;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;

public class CalculadoraAlmacen {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Almacén");
            f.setContentPane(new PanelAlmacen());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

class PanelAlmacen extends JPanel {
    private final JTextField precio = new JTextField(7);
    private final JTextField cantidad = new JTextField(4);
    private final JCheckBox tarjeta = new JCheckBox("Paga con tarjeta (+10%)");
    private final JTextArea detalle = new JTextArea(6, 30);
    private final JLabel total = new JLabel("Total: $0.00");
    private double suma = 0;

    PanelAlmacen() {
        super(new BorderLayout(6, 6));
        JPanel arriba = new JPanel(new FlowLayout(FlowLayout.LEFT));
        JButton agregar = new JButton("Agregar");
        JButton nueva = new JButton("Nueva venta");
        arriba.add(new JLabel("Precio:"));
        arriba.add(precio);
        arriba.add(new JLabel("Cant.:"));
        arriba.add(cantidad);
        arriba.add(agregar);
        JPanel abajo = new JPanel(new FlowLayout(FlowLayout.LEFT));
        abajo.add(tarjeta);
        abajo.add(nueva);
        abajo.add(total);
        detalle.setEditable(false);
        add(arriba, BorderLayout.NORTH);
        add(new JScrollPane(detalle), BorderLayout.CENTER);
        add(abajo, BorderLayout.SOUTH);
        agregar.addActionListener(e -> agregar());
        nueva.addActionListener(e -> {
            suma = 0;
            detalle.setText("");
            total.setText("Total: $0.00");
        });
        tarjeta.addActionListener(e -> mostrarTotal());
    }

    private void agregar() {
        try {
            double p = Double.parseDouble(precio.getText().trim());
            int c = Integer.parseInt(cantidad.getText().trim());
            if (p <= 0 || c <= 0) {
                throw new NumberFormatException();
            }
            suma += p * c;
            detalle.append(String.format("%d x %.2f = %.2f%n", c, p, p * c));
            precio.setText("");
            cantidad.setText("");
            mostrarTotal();
        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(this, "Precio y cantidad tienen que ser números positivos");
        }
    }

    private void mostrarTotal() {
        double t = tarjeta.isSelected() ? suma * 1.10 : suma;
        total.setText(String.format("Total: $%.2f", t));
    }
}
```

### Prueba del sello

#### ¿Qué diferencia hay entre un `JFrame` y un `JPanel`?

El `JFrame` es la ventana (con título y borde); el `JPanel` es un contenedor para ubicar componentes dentro de la ventana.

#### ¿Cómo se hace que un botón haga algo?

Registrándole un `ActionListener`, por ejemplo con `boton.addActionListener(e -> hacerAlgo())`.

#### ¿Por qué la ventana se crea dentro de `SwingUtilities.invokeLater`?

Porque todo lo de Swing tiene que ejecutarse en el hilo de eventos (EDT).

#### ¿Qué pasa si no ponés `setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)`?

Al cerrar la ventana, el programa sigue corriendo sin que se vea.

#### ¿Cómo mostrás un error al usuario en una aplicación con ventanas?

Con un `JOptionPane.showMessageDialog` (o un cartel en la ventana), no con `System.out`.

### Soluciones (docente)

Sale de `18-Java/33-Swing-Primera-Ventana` (unidad 2: GUI básica). Corrige lo que marcó la auditoría: las lambdas ya están explicadas (rama 3) y el EDT se presenta desde el primer ejemplo. Las prácticas de Swing no tienen salida esperada: se corrigen ejecutándolas; el súper test las compila y crea cada panel sin pantalla para detectar errores al armarlo.

## R05-N02 · Layouts: ordenar la ventana

```meta
tipo: tema
padre: R05-N01
precio: 10
criatura: ogre
temas: gui.layouts
usa: gui.swing
```

### Crónica

En el salón de vitrales del Palacio, cada panel está ordenado según una regla: uno pone todo en fila, otro divide el espacio en norte, sur, este, oeste y centro, otro arma una grilla perfecta. Cuando alguien agranda la ventana, cada regla acomoda sus piezas sola.

—No pongas cada botón en una coordenada fija —dice {mentor}—: en otra pantalla, con otra letra, todo se superpone. Elegí una **regla de acomodo** y dejala trabajar, {heroe}. Combinando reglas simples se arma cualquier ventana.

### Objetivos

- Entender qué es un *layout manager* y por qué no conviene posicionar a mano.
- Usar `FlowLayout`, `BorderLayout`, `GridLayout` y `BoxLayout`.
- Armar formularios con `GridBagLayout`.
- Combinar paneles anidados, cada uno con su layout.
- Usar bordes y espacios para que la ventana respire.

### Antes de empezar

- La primera ventana: JFrame, componentes y eventos.

### Explicación

#### Los *layout managers*
Cada contenedor (`JPanel`, el contenido del `JFrame`) tiene un **administrador de
diseño** que decide dónde va cada componente y de qué tamaño, y lo recalcula cuando la
ventana cambia de tamaño. Se elige con `setLayout(...)` o en el constructor del panel:
`new JPanel(new BorderLayout())`.

#### `FlowLayout`: en fila
Pone los componentes uno al lado del otro, como palabras en un renglón, y baja al
siguiente si no entran. Es el de defecto de `JPanel`.
```java
JPanel botones = new JPanel(new FlowLayout(FlowLayout.RIGHT, 8, 4));   // alineados a la derecha, con separación
```

#### `BorderLayout`: cinco zonas
Divide el espacio en `NORTH`, `SOUTH`, `EAST`, `WEST` y `CENTER`. El centro se queda
con todo el espacio que sobra. Es el de defecto del contenido de un `JFrame` y el más
usado para la estructura general: barra arriba, lista a la izquierda, contenido en el
centro, botones abajo.
```java
setLayout(new BorderLayout(8, 8));
add(titulo, BorderLayout.NORTH);
add(new JScrollPane(lista), BorderLayout.CENTER);
add(botones, BorderLayout.SOUTH);
```
En cada zona entra **un** componente: para poner varios, se pone un panel con los
varios adentro.

#### `GridLayout`: una grilla pareja
Filas y columnas del mismo tamaño. Ideal para teclados, tableros y formularios
simples de dos columnas.
```java
JPanel teclado = new JPanel(new GridLayout(4, 3, 4, 4));   // 4 filas, 3 columnas, separación 4
```

#### `BoxLayout`: en columna (o en fila)
Apila los componentes vertical u horizontalmente, respetando su tamaño preferido. Con
`Box.createVerticalStrut(10)` se agrega un espacio fijo y con
`Box.createVerticalGlue()`, un espacio que se estira.
```java
JPanel columna = new JPanel();
columna.setLayout(new BoxLayout(columna, BoxLayout.Y_AXIS));
```

#### `GridBagLayout`: formularios flexibles
El más poderoso (y el más largo de escribir): una grilla donde cada componente ocupa
una o varias celdas, con su alineación y con qué parte del espacio sobrante se estira.
Cada componente se agrega con un `GridBagConstraints`:
```java
JPanel form = new JPanel(new GridBagLayout());
GridBagConstraints c = new GridBagConstraints();
c.insets = new Insets(4, 4, 4, 4);        // margen alrededor
c.gridx = 0; c.gridy = 0; c.anchor = GridBagConstraints.LINE_END;
form.add(new JLabel("Nombre:"), c);
c.gridx = 1; c.fill = GridBagConstraints.HORIZONTAL; c.weightx = 1;   // se estira a lo ancho
form.add(campoNombre, c);
```
| Propiedad | Qué hace |
|---|---|
| `gridx`, `gridy` | columna y fila (desde 0) |
| `gridwidth` | cuántas columnas ocupa |
| `fill` | si se estira para llenar su celda (`HORIZONTAL`, `VERTICAL`, `BOTH`) |
| `weightx`, `weighty` | cuánto del espacio sobrante toma (0 = nada) |
| `anchor` | dónde se ubica dentro de la celda |
| `insets` | margen alrededor |

El editor visual de NetBeans usa otro, `GroupLayout`, que genera código largo pensado
para no editarse a mano (lo vas a reconocer en el nodo del estilo de la cátedra).

#### Paneles anidados
La clave es **combinar**: un `BorderLayout` general, con un `FlowLayout` de botones al
sur, un `GridBagLayout` de formulario al norte y una tabla en el centro.

#### Bordes y espacios
```java
panel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));      // margen interno
panel.setBorder(BorderFactory.createTitledBorder("Datos del héroe"));  // un recuadro con título
```

#### ¿Y `setLayout(null)` con coordenadas?
Se puede (`setBounds(x, y, ancho, alto)`), pero la ventana no se adapta al tamaño, a
otras pantallas ni a otras letras. Solo tiene sentido en casos muy especiales, como un
juego que dibuja todo.

### Código de ejemplo

```java
/*
 * Layouts: el salón de vitrales. Cada zona usa un layout distinto.
 */
import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.GridLayout;
import java.awt.Insets;
import javax.swing.BorderFactory;
import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;

public class SalonVitrales {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Salón de vitrales · Layouts");
            f.setContentPane(new PanelVitrales());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

class PanelVitrales extends JPanel {
    PanelVitrales() {
        super(new BorderLayout(10, 10));                       // estructura general
        setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        // NORTE: un formulario con GridBagLayout
        JPanel form = new JPanel(new GridBagLayout());
        form.setBorder(BorderFactory.createTitledBorder("Datos del viajero"));
        String[] etiquetas = {"Nombre:", "Ciudad de origen:", "Oficio:"};
        for (int fila = 0; fila < etiquetas.length; fila++) {
            GridBagConstraints c = new GridBagConstraints();
            c.insets = new Insets(4, 4, 4, 4);
            c.gridx = 0;
            c.gridy = fila;
            c.anchor = GridBagConstraints.LINE_END;
            form.add(new JLabel(etiquetas[fila]), c);
            c.gridx = 1;
            c.fill = GridBagConstraints.HORIZONTAL;
            c.weightx = 1;
            form.add(new JTextField(18), c);
        }
        add(form, BorderLayout.NORTH);

        // OESTE: una columna de botones con BoxLayout
        JPanel columna = new JPanel();
        columna.setLayout(new BoxLayout(columna, BoxLayout.Y_AXIS));
        for (String s : new String[]{"Nuevo", "Buscar", "Borrar"}) {
            columna.add(new JButton(s));
            columna.add(Box.createVerticalStrut(6));
        }
        add(columna, BorderLayout.WEST);

        // CENTRO: un teclado con GridLayout
        JPanel teclado = new JPanel(new GridLayout(4, 3, 4, 4));
        for (String t : new String[]{"7", "8", "9", "4", "5", "6", "1", "2", "3", "C", "0", "OK"}) {
            teclado.add(new JButton(t));
        }
        add(teclado, BorderLayout.CENTER);

        // SUR: botones alineados a la derecha con FlowLayout
        JPanel botones = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        botones.add(new JButton("Cancelar"));
        botones.add(new JButton("Guardar"));
        add(botones, BorderLayout.SOUTH);
    }
}
```

### ¿Para qué sirve?

Una aplicación que se ve bien en tu pantalla y se desarma en la del cliente es una aplicación que no se puede entregar. Los layouts hacen que las ventanas se adapten a cualquier tamaño, resolución y sistema operativo, y son la misma idea que las grillas y cajas del diseño web (CSS Grid y Flexbox).

### Errores habituales

**Ogro: dos componentes en la misma zona del `BorderLayout`.** El segundo reemplaza al
primero: solo se ve uno. Poné un panel con los dos adentro.

**Ogro: el campo que no se estira.** En `GridBagLayout`, sin `fill = HORIZONTAL` y
`weightx > 0`, el campo queda de su tamaño mínimo aunque sobre espacio.

**Ogro: los `GridBagConstraints` reutilizados.** Si usás el mismo objeto para varios
componentes y no reiniciás las propiedades, un `fill` o un `gridwidth` de uno se le
aplica al siguiente.

**Slime: `BoxLayout` con el panel equivocado.** `new BoxLayout(otroPanel, …)` asignado
a un panel distinto: `BoxLayout can't be shared`.

**Ogro: posiciones fijas.** Con `setLayout(null)`, en otra pantalla los textos se cortan
o se superponen.

### Misión R05-N02-M1 · El teclado del cajero

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Hacé el teclado de un cajero: un visor arriba (un `JTextField` no editable, con el
texto alineado a la derecha), un teclado numérico de 4×3 en el centro (`GridLayout`,
con `1` a `9`, `←` para borrar el último dígito, `0` y `C` para borrar todo) y una fila
de botones abajo (`Cancelar` y `Aceptar`, a la derecha). `Aceptar` muestra el número
ingresado en un `JOptionPane`. El visor no admite más de 8 dígitos.

#### Criterio de aprobación

- `BorderLayout` para la estructura, `GridLayout` para el teclado y `FlowLayout` para los botones.
- Los 12 botones del teclado comparten un mismo listener (usá `e.getActionCommand()`).

#### Solución de referencia

```java
// Mision 1 - El teclado del cajero: BorderLayout + GridLayout + FlowLayout.
import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;

public class TecladoCajero {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Cajero");
            f.setContentPane(new PanelTeclado());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

class PanelTeclado extends JPanel {
    private final JTextField visor = new JTextField(10);

    PanelTeclado() {
        super(new BorderLayout(6, 6));
        setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));
        visor.setEditable(false);
        visor.setHorizontalAlignment(JTextField.RIGHT);
        add(visor, BorderLayout.NORTH);

        JPanel teclas = new JPanel(new GridLayout(4, 3, 4, 4));
        for (String t : new String[]{"1", "2", "3", "4", "5", "6", "7", "8", "9", "←", "0", "C"}) {
            JButton b = new JButton(t);
            b.addActionListener(this::tecla);
            teclas.add(b);
        }
        add(teclas, BorderLayout.CENTER);

        JPanel botones = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        JButton cancelar = new JButton("Cancelar");
        JButton aceptar = new JButton("Aceptar");
        botones.add(cancelar);
        botones.add(aceptar);
        add(botones, BorderLayout.SOUTH);
        cancelar.addActionListener(e -> visor.setText(""));
        aceptar.addActionListener(e -> JOptionPane.showMessageDialog(this, "Ingresaste: " + (visor.getText().isEmpty() ? "nada" : visor.getText())));
    }

    private void tecla(ActionEvent e) {
        String t = e.getActionCommand();
        String actual = visor.getText();
        switch (t) {
            case "C" -> visor.setText("");
            case "←" -> visor.setText(actual.isEmpty() ? "" : actual.substring(0, actual.length() - 1));
            default -> {
                if (actual.length() < 8) {
                    visor.setText(actual + t);
                }
            }
        }
    }
}
```

### Misión R05-N02-M2 · El formulario del gremio

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Hacé con `GridBagLayout` el formulario de alta de un miembro del gremio: etiquetas a la
derecha y campos que se estiran a lo ancho para **nombre**, **email** y **teléfono**; una
fila con **dirección** que ocupa las dos columnas de campos (`gridwidth = 2`) y un
`JTextArea` de **observaciones** que se estira también a lo alto (`weighty`). Abajo, los
botones `Limpiar` y `Guardar` a la derecha. `Guardar` muestra un resumen de lo cargado.
Poné un borde con título al formulario.

#### Criterio de aprobación

- Usa `GridBagLayout` con `fill`, `weightx`, `weighty`, `gridwidth` e `insets`.
- El área de observaciones crece al agrandar la ventana.

#### Solución de referencia

```java
// Mision 2 - El formulario del gremio: GridBagLayout completo.
import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Insets;
import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JComponent;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;

public class FormularioGremio {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Alta de miembro");
            f.setContentPane(new PanelGremio());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

class PanelGremio extends JPanel {
    private final JTextField nombre = new JTextField(16);
    private final JTextField email = new JTextField(16);
    private final JTextField telefono = new JTextField(10);
    private final JTextField direccion = new JTextField(24);
    private final JTextArea observaciones = new JTextArea(4, 24);

    PanelGremio() {
        super(new BorderLayout(6, 6));
        setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));
        JPanel form = new JPanel(new GridBagLayout());
        form.setBorder(BorderFactory.createTitledBorder("Datos del miembro"));
        fila(form, 0, "Nombre:", nombre, 1, 0);
        fila(form, 1, "Email:", email, 1, 0);
        fila(form, 2, "Teléfono:", telefono, 1, 0);
        fila(form, 3, "Dirección:", direccion, 2, 0);
        fila(form, 4, "Observaciones:", new JScrollPane(observaciones), 2, 1);
        add(form, BorderLayout.CENTER);

        JPanel botones = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        JButton limpiar = new JButton("Limpiar");
        JButton guardar = new JButton("Guardar");
        botones.add(limpiar);
        botones.add(guardar);
        add(botones, BorderLayout.SOUTH);
        limpiar.addActionListener(e -> {
            for (JTextField t : new JTextField[]{nombre, email, telefono, direccion}) {
                t.setText("");
            }
            observaciones.setText("");
        });
        guardar.addActionListener(e -> JOptionPane.showMessageDialog(this,
                "Nombre: " + nombre.getText() + "\nEmail: " + email.getText() + "\nTeléfono: " + telefono.getText()
                        + "\nDirección: " + direccion.getText() + "\nObservaciones: " + observaciones.getText()));
    }

    private void fila(JPanel form, int y, String etiqueta, JComponent campo, int ancho, double pesoY) {
        GridBagConstraints c = new GridBagConstraints();
        c.insets = new Insets(4, 4, 4, 4);
        c.gridx = 0;
        c.gridy = y;
        c.anchor = pesoY > 0 ? GridBagConstraints.FIRST_LINE_END : GridBagConstraints.LINE_END;
        form.add(new JLabel(etiqueta), c);
        c = new GridBagConstraints();
        c.insets = new Insets(4, 4, 4, 4);
        c.gridx = 1;
        c.gridy = y;
        c.gridwidth = ancho;
        c.weightx = 1;
        c.weighty = pesoY;
        c.fill = pesoY > 0 ? GridBagConstraints.BOTH : GridBagConstraints.HORIZONTAL;
        form.add(campo, c);
    }
}
```

### Misión R05-N02-M3 · El tablero del tres en raya

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Hacé un **tres en raya** para dos jugadores: un cartel arriba que diga de quién es el
turno, un tablero de 3×3 botones en el centro (`GridLayout`) y un botón `Reiniciar`
abajo. Al tocar un botón vacío se pone `X` u `O` según el turno; si alguien completa una
fila, columna o diagonal, el cartel anuncia el ganador y se deshabilitan los botones; si
se llena sin ganador, es empate. La lógica del ganador va en un método aparte que
recibe el estado del tablero.

#### Criterio de aprobación

- El tablero es un `GridLayout` de 3×3 dentro de un `BorderLayout`.
- La lógica de ganador está separada de los botones.

#### Solución de referencia

```java
// Mision 3 - El tablero del tres en raya: GridLayout y la logica separada.
import java.awt.BorderLayout;
import java.awt.Font;
import java.awt.GridLayout;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.SwingConstants;
import javax.swing.SwingUtilities;

public class TresEnRaya {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Tres en raya del Palacio");
            f.setContentPane(new PanelTateti());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

class PanelTateti extends JPanel {
    private final JButton[] casillas = new JButton[9];
    private final JLabel cartel = new JLabel("", SwingConstants.CENTER);
    private char turno = 'X';

    PanelTateti() {
        super(new BorderLayout(6, 6));
        JPanel tablero = new JPanel(new GridLayout(3, 3, 3, 3));
        for (int i = 0; i < 9; i++) {
            JButton b = new JButton(" ");
            b.setFont(b.getFont().deriveFont(Font.BOLD, 28f));
            int posicion = i;
            b.addActionListener(e -> jugar(posicion));
            casillas[i] = b;
            tablero.add(b);
        }
        JButton reiniciar = new JButton("Reiniciar");
        reiniciar.addActionListener(e -> reiniciar());
        add(cartel, BorderLayout.NORTH);
        add(tablero, BorderLayout.CENTER);
        add(reiniciar, BorderLayout.SOUTH);
        reiniciar();
    }

    private void jugar(int i) {
        if (!casillas[i].getText().isBlank()) {
            return;
        }
        casillas[i].setText(String.valueOf(turno));
        char[] estado = new char[9];
        for (int k = 0; k < 9; k++) {
            estado[k] = casillas[k].getText().charAt(0);
        }
        char ganador = ganador(estado);
        if (ganador != ' ') {
            cartel.setText("¡Ganó " + ganador + "!");
            habilitar(false);
        } else if (new String(estado).indexOf(' ') < 0) {
            cartel.setText("Empate");
        } else {
            turno = turno == 'X' ? 'O' : 'X';
            cartel.setText("Turno de " + turno);
        }
    }

    static char ganador(char[] t) {
        int[][] lineas = {{0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {0, 3, 6}, {1, 4, 7}, {2, 5, 8}, {0, 4, 8}, {2, 4, 6}};
        for (int[] l : lineas) {
            if (t[l[0]] != ' ' && t[l[0]] == t[l[1]] && t[l[1]] == t[l[2]]) {
                return t[l[0]];
            }
        }
        return ' ';
    }

    private void reiniciar() {
        for (JButton b : casillas) {
            b.setText(" ");
        }
        habilitar(true);
        turno = 'X';
        cartel.setText("Turno de X");
    }

    private void habilitar(boolean si) {
        for (JButton b : casillas) {
            b.setEnabled(si);
        }
    }
}
```

### Encargo R05-N02-E1 · La pantalla de login

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Diseñá la pantalla de ingreso de un sistema de gestión: un título grande arriba
centrado, en el medio un formulario (`GridBagLayout`) con usuario y contraseña
(`JPasswordField`) y una casilla "Recordarme", y abajo el botón `Ingresar` ocupando todo
el ancho. Con `Enter` en la contraseña también se ingresa. Si el usuario es `admin` y la
clave `admin123`, mostrá "Acceso concedido"; si no, "Usuario o clave incorrectos" y
borrá la clave. La clave se lee con `getPassword()` (devuelve un `char[]`).

#### Criterio de aprobación

- Usa `JPasswordField` y compara con `getPassword()`.
- El diseño combina al menos dos layouts y se adapta al agrandar.

#### Solución de referencia

```java
// Encargo - La pantalla de login: JPasswordField y layouts combinados.
import java.awt.BorderLayout;
import java.awt.Font;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Insets;
import java.util.Arrays;
import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JPasswordField;
import javax.swing.JTextField;
import javax.swing.SwingConstants;
import javax.swing.SwingUtilities;

public class Login {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Ingreso");
            f.setContentPane(new PanelLogin());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

class PanelLogin extends JPanel {
    private final JTextField usuario = new JTextField(14);
    private final JPasswordField clave = new JPasswordField(14);

    PanelLogin() {
        super(new BorderLayout(10, 10));
        setBorder(BorderFactory.createEmptyBorder(16, 16, 16, 16));
        JLabel titulo = new JLabel("Sistema del Imperio", SwingConstants.CENTER);
        titulo.setFont(titulo.getFont().deriveFont(Font.BOLD, 20f));
        add(titulo, BorderLayout.NORTH);

        JPanel form = new JPanel(new GridBagLayout());
        GridBagConstraints c = new GridBagConstraints();
        c.insets = new Insets(4, 4, 4, 4);
        c.anchor = GridBagConstraints.LINE_END;
        form.add(new JLabel("Usuario:"), c);
        c.gridy = 1;
        form.add(new JLabel("Contraseña:"), c);
        c = new GridBagConstraints();
        c.insets = new Insets(4, 4, 4, 4);
        c.gridx = 1;
        c.fill = GridBagConstraints.HORIZONTAL;
        c.weightx = 1;
        form.add(usuario, c);
        c.gridy = 1;
        form.add(clave, c);
        c.gridy = 2;
        form.add(new JCheckBox("Recordarme"), c);
        add(form, BorderLayout.CENTER);

        JButton ingresar = new JButton("Ingresar");
        add(ingresar, BorderLayout.SOUTH);
        ingresar.addActionListener(e -> ingresar());
        clave.addActionListener(e -> ingresar());
    }

    private void ingresar() {
        char[] ingresada = clave.getPassword();
        boolean ok = usuario.getText().equals("admin") && Arrays.equals(ingresada, "admin123".toCharArray());
        Arrays.fill(ingresada, '\0');
        if (ok) {
            JOptionPane.showMessageDialog(this, "Acceso concedido");
        } else {
            JOptionPane.showMessageDialog(this, "Usuario o clave incorrectos", "Ingreso", JOptionPane.ERROR_MESSAGE);
            clave.setText("");
            clave.requestFocusInWindow();
        }
    }
}
```

### Prueba del sello

#### ¿Por qué no conviene ubicar los componentes con coordenadas fijas?

Porque la ventana no se adapta a otros tamaños, pantallas ni letras: los textos se cortan o se superponen.

#### ¿Cuántos componentes entran en cada zona de un `BorderLayout`?

Uno. Para poner varios, se pone un panel con los varios adentro.

#### ¿Qué layout usarías para un teclado numérico?

`GridLayout`, que arma una grilla de celdas iguales.

#### En `GridBagLayout`, ¿qué hacen `fill` y `weightx`?

`fill` hace que el componente llene su celda; `weightx` indica cuánto del espacio horizontal sobrante toma la columna.

#### ¿Cómo se arman ventanas complejas con layouts simples?

Anidando paneles, cada uno con su propio layout.

### Soluciones (docente)

Nodo nuevo (el 34 del índice de `18-Java` estaba por crear), unidad 6. La auditoría marcaba que el capítulo solo usaba `BoxLayout` y `FlowLayout`: acá están los cinco que pide el programa. El editor de NetBeans genera `GroupLayout`, que se reconoce en el nodo del estilo de la cátedra.

## R05-N03 · Componentes: listas, opciones y controles

```meta
tipo: tema
padre: R05-N02
precio: 10
criatura: goblin
ejecutable: no
temas: gui.componentes
usa: gui.swing
```

### Crónica

En la armería del Palacio, un escribiente llena formularios de pedido: elige el tipo de arma de una lista desplegable, marca con un círculo si es para infantería o caballería, tilda los accesorios, desliza una barra para el tamaño. Nada se escribe a mano: todo se **elige**.

—Si le pedís a la gente que escriba "arquero", alguien va a escribir "arqero" —dice {mentor}—. Cuando las respuestas posibles son conocidas, **ofrecelas**: listas, opciones y controles, {heroe}. Y después, leé bien lo que eligieron.

### Objetivos

- Usar `JComboBox`, `JRadioButton` con `ButtonGroup`, `JCheckBox`, `JList`, `JSlider`, `JSpinner` y `JTextArea`.
- **Leer** el valor de cada componente y reaccionar a sus cambios.
- Llenar listas y combos con objetos propios.
- Usar `JProgressBar` para mostrar un avance.

### Antes de empezar

- Layouts: ordenar la ventana.

### Explicación

#### Qué componente para qué dato
| Dato | Componente | Cómo se lee |
|---|---|---|
| uno entre varios, en una lista desplegable | `JComboBox<T>` | `(T) combo.getSelectedItem()` o `getSelectedIndex()` |
| uno entre pocos, todos a la vista | `JRadioButton` + `ButtonGroup` | `radio.isSelected()` |
| sí o no | `JCheckBox` | `check.isSelected()` |
| uno o varios de una lista | `JList<T>` | `getSelectedValue()` / `getSelectedValuesList()` |
| un número en un rango, arrastrando | `JSlider` | `slider.getValue()` |
| un número con flechitas | `JSpinner` | `(Integer) spinner.getValue()` |
| texto largo | `JTextArea` (en un `JScrollPane`) | `area.getText()` |
| un avance | `JProgressBar` | se escribe con `setValue` |

#### Combos y listas con objetos propios
Un `JComboBox` o una `JList` pueden guardar **objetos**; muestran lo que devuelve su
`toString()` y te devuelven el objeto elegido:
```java
JComboBox<Clase> combo = new JComboBox<>(Clase.values());   // un enum: muestra INFANTE, ARQUERO…
Clase elegida = (Clase) combo.getSelectedItem();
```
Para una lista que cambia, se usa un modelo:
```java
DefaultListModel<String> modelo = new DefaultListModel<>();
JList<String> lista = new JList<>(modelo);
modelo.addElement("Kira");          // la lista se actualiza sola
modelo.removeElement("Kira");
```

#### Botones de opción: `ButtonGroup`
Los `JRadioButton` solo se excluyen entre sí si están en el mismo `ButtonGroup`:
```java
JRadioButton infanteria = new JRadioButton("Infantería", true);
JRadioButton caballeria = new JRadioButton("Caballería");
ButtonGroup grupo = new ButtonGroup();
grupo.add(infanteria);
grupo.add(caballeria);
```
El `ButtonGroup` no es un componente visual: igual hay que agregar cada radio al panel.

#### Reaccionar a los cambios
| Componente | Evento | Listener |
|---|---|---|
| `JComboBox`, `JCheckBox`, `JRadioButton` | al cambiar la elección | `addActionListener` |
| `JList` | al cambiar la selección | `addListSelectionListener(e -> …)` (con `if (!e.getValueIsAdjusting())`) |
| `JSlider`, `JSpinner` | al moverse | `addChangeListener(e -> …)` |
| `JTextField` / `JTextArea` | al escribir | `getDocument().addDocumentListener(…)` |

Con estos eventos se puede recalcular un precio o un resumen **en vivo**, sin un botón.

#### Barras con scroll
Un `JTextArea` o una `JList` con muchas filas van siempre dentro de un `JScrollPane`:
`add(new JScrollPane(lista))`. Sin él, lo que no entra no se ve.

### Código de ejemplo

```java
/*
 * Componentes: el formulario de pedidos de la armería.
 * Todo se elige, y el resumen se recalcula en vivo.
 */
import java.awt.BorderLayout;
import java.awt.GridLayout;
import java.util.List;
import javax.swing.BorderFactory;
import javax.swing.ButtonGroup;
import javax.swing.DefaultListModel;
import javax.swing.JCheckBox;
import javax.swing.JComboBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JPanel;
import javax.swing.JProgressBar;
import javax.swing.JRadioButton;
import javax.swing.JScrollPane;
import javax.swing.JSlider;
import javax.swing.JSpinner;
import javax.swing.JTextArea;
import javax.swing.ListSelectionModel;
import javax.swing.SpinnerNumberModel;
import javax.swing.SwingUtilities;

public class Armeria {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Armería del Palacio");
            f.setContentPane(new PanelArmeria());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

enum Arma {
    ESPADA(900), LANZA(700), ARCO(1100);

    final int precio;

    Arma(int precio) {
        this.precio = precio;
    }
}

class PanelArmeria extends JPanel {
    private final JComboBox<Arma> arma = new JComboBox<>(Arma.values());
    private final JRadioButton infanteria = new JRadioButton("Infantería", true);
    private final JRadioButton caballeria = new JRadioButton("Caballería (+20%)");
    private final JCheckBox grabado = new JCheckBox("Grabado (+150)");
    private final JCheckBox funda = new JCheckBox("Funda (+80)");
    private final DefaultListModel<String> modeloEscuadras = new DefaultListModel<>();
    private final JList<String> escuadras = new JList<>(modeloEscuadras);
    private final JSlider calidad = new JSlider(1, 5, 3);
    private final JSpinner cantidad = new JSpinner(new SpinnerNumberModel(10, 1, 500, 1));
    private final JTextArea resumen = new JTextArea(6, 30);
    private final JProgressBar presupuesto = new JProgressBar(0, 50_000);

    PanelArmeria() {
        super(new BorderLayout(8, 8));
        setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));
        ButtonGroup tipo = new ButtonGroup();
        tipo.add(infanteria);
        tipo.add(caballeria);
        for (String e : new String[]{"Guardia Norte", "Guardia Sur", "Escolta Real"}) {
            modeloEscuadras.addElement(e);
        }
        escuadras.setSelectionMode(ListSelectionModel.MULTIPLE_INTERVAL_SELECTION);
        escuadras.setSelectedIndex(0);
        calidad.setMajorTickSpacing(1);
        calidad.setPaintTicks(true);
        calidad.setPaintLabels(true);
        resumen.setEditable(false);
        presupuesto.setStringPainted(true);

        JPanel controles = new JPanel(new GridLayout(0, 2, 6, 6));
        controles.add(new JLabel("Arma:"));
        controles.add(arma);
        controles.add(infanteria);
        controles.add(caballeria);
        controles.add(grabado);
        controles.add(funda);
        controles.add(new JLabel("Calidad:"));
        controles.add(calidad);
        controles.add(new JLabel("Cantidad:"));
        controles.add(cantidad);
        add(controles, BorderLayout.NORTH);
        add(new JScrollPane(escuadras), BorderLayout.WEST);
        add(new JScrollPane(resumen), BorderLayout.CENTER);
        add(presupuesto, BorderLayout.SOUTH);

        // Cualquier cambio recalcula el resumen en vivo
        arma.addActionListener(e -> recalcular());
        infanteria.addActionListener(e -> recalcular());
        caballeria.addActionListener(e -> recalcular());
        grabado.addActionListener(e -> recalcular());
        funda.addActionListener(e -> recalcular());
        calidad.addChangeListener(e -> recalcular());
        cantidad.addChangeListener(e -> recalcular());
        escuadras.addListSelectionListener(e -> {
            if (!e.getValueIsAdjusting()) {
                recalcular();
            }
        });
        recalcular();
    }

    private void recalcular() {
        Arma elegida = (Arma) arma.getSelectedItem();
        int unidades = (Integer) cantidad.getValue();
        double precio = elegida.precio * (1 + (calidad.getValue() - 3) * 0.15);
        if (caballeria.isSelected()) {
            precio *= 1.2;
        }
        if (grabado.isSelected()) {
            precio += 150;
        }
        if (funda.isSelected()) {
            precio += 80;
        }
        List<String> destino = escuadras.getSelectedValuesList();
        int total = (int) Math.round(precio * unidades);
        resumen.setText(unidades + " × " + elegida + " de calidad " + calidad.getValue() + "\n"
                + (caballeria.isSelected() ? "para caballería" : "para infantería") + "\n"
                + "Destino: " + (destino.isEmpty() ? "sin elegir" : String.join(", ", destino)) + "\n"
                + "Precio unitario: " + Math.round(precio) + "\nTotal: " + total + " denarios");
        presupuesto.setValue(Math.min(total, presupuesto.getMaximum()));
        presupuesto.setString(total > presupuesto.getMaximum() ? "¡Supera el presupuesto!" : total + " / 50000");
    }
}
```

### ¿Para qué sirve?

Los formularios reales están llenos de estos controles: la provincia en un combo, el sexo o el tipo de cliente en botones de opción, "acepto los términos" en una casilla, los productos en una lista, la cantidad con flechitas. Elegir el componente correcto evita errores de carga y hace que un sistema se use rápido, sin leer un manual.

### Errores habituales

**Ogro: los radios que no se excluyen.** Si no están en el mismo `ButtonGroup`, se
pueden marcar los dos a la vez.

**Goblin: el casting de `getSelectedItem()`.** Devuelve `Object`: hay que convertirlo
al tipo del combo. Si el combo está vacío, devuelve `null`.

**Ogro: la lista que no se actualiza.** Si creaste la `JList` con un array, agregarle
elementos no cambia nada. Usá un `DefaultListModel` y modificá el modelo.

**Ogro: el evento de la lista que llega dos veces.** Sin `if
(!e.getValueIsAdjusting())`, el listener corre mientras el usuario todavía está
arrastrando la selección.

**Slime: el área sin scroll.** Un `JTextArea` sin `JScrollPane` crece hasta tapar todo
o esconde el texto que no entra.

### Misión R05-N03-M1 · El pedido de la posada

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Hacé el formulario de pedidos de la posada: un `JComboBox` con los platos (un `enum`
con precio), `JRadioButton` para el tamaño (chico, mediano +20 %, grande +40 %), dos
`JCheckBox` de agregados (pan +300, bebida +600) y un `JSpinner` para la cantidad (1 a
20). El total se recalcula **en vivo** con cada cambio y se muestra en una etiqueta.

#### Criterio de aprobación

- Los radios están en un `ButtonGroup`.
- Todos los controles recalculan el total con su listener.
- El combo guarda los valores de un `enum`.

#### Solución de referencia

```java
// Mision 1 - El pedido de la posada: combo, radios, checks y spinner con total en vivo.
import java.awt.GridLayout;
import javax.swing.BorderFactory;
import javax.swing.ButtonGroup;
import javax.swing.JCheckBox;
import javax.swing.JComboBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JRadioButton;
import javax.swing.JSpinner;
import javax.swing.SpinnerNumberModel;
import javax.swing.SwingUtilities;

public class PedidoPosada {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Posada La Taza");
            f.setContentPane(new PanelPedido());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

enum Plato {
    GUISO(2500), EMPANADAS(1800), SOPA(1500);

    final int precio;

    Plato(int precio) {
        this.precio = precio;
    }
}

class PanelPedido extends JPanel {
    private final JComboBox<Plato> plato = new JComboBox<>(Plato.values());
    private final JRadioButton chico = new JRadioButton("Chico", true);
    private final JRadioButton mediano = new JRadioButton("Mediano (+20%)");
    private final JRadioButton grande = new JRadioButton("Grande (+40%)");
    private final JCheckBox pan = new JCheckBox("Pan (+300)");
    private final JCheckBox bebida = new JCheckBox("Bebida (+600)");
    private final JSpinner cantidad = new JSpinner(new SpinnerNumberModel(1, 1, 20, 1));
    private final JLabel total = new JLabel();

    PanelPedido() {
        super(new GridLayout(0, 2, 6, 6));
        setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        ButtonGroup tamanio = new ButtonGroup();
        tamanio.add(chico);
        tamanio.add(mediano);
        tamanio.add(grande);
        add(new JLabel("Plato:"));
        add(plato);
        add(chico);
        add(mediano);
        add(grande);
        add(new JLabel());
        add(pan);
        add(bebida);
        add(new JLabel("Cantidad:"));
        add(cantidad);
        add(new JLabel("Total:"));
        add(total);
        for (javax.swing.AbstractButton b : new javax.swing.AbstractButton[]{chico, mediano, grande, pan, bebida}) {
            b.addActionListener(e -> recalcular());
        }
        plato.addActionListener(e -> recalcular());
        cantidad.addChangeListener(e -> recalcular());
        recalcular();
    }

    private void recalcular() {
        double unitario = ((Plato) plato.getSelectedItem()).precio;
        if (mediano.isSelected()) {
            unitario *= 1.2;
        } else if (grande.isSelected()) {
            unitario *= 1.4;
        }
        if (pan.isSelected()) {
            unitario += 300;
        }
        if (bebida.isSelected()) {
            unitario += 600;
        }
        total.setText(Math.round(unitario * (Integer) cantidad.getValue()) + " denarios");
    }
}
```

### Misión R05-N03-M2 · Las dos listas del reclutador

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Hacé una ventana con **dos listas**: a la izquierda los aspirantes, a la derecha los
elegidos, y en el medio botones `>` (pasa los seleccionados a elegidos), `<` (los
devuelve) y `>>` (pasa todos). Las dos listas usan `DefaultListModel` y permiten
selección múltiple. Abajo, una etiqueta dice cuántos elegidos hay y, si son más de 4,
se pone en rojo. Un campo de texto con `Enter` agrega un aspirante nuevo (sin
repetidos).

#### Criterio de aprobación

- Dos `JList` con `DefaultListModel` y selección múltiple.
- Los botones mueven los elementos entre modelos.
- La etiqueta se actualiza con cada cambio.

#### Solución de referencia

```java
// Mision 2 - Las dos listas del reclutador: DefaultListModel y seleccion multiple.
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.GridLayout;
import java.util.List;
import javax.swing.BorderFactory;
import javax.swing.DefaultListModel;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;

public class Reclutador {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Reclutador");
            f.setContentPane(new PanelReclutador());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

class PanelReclutador extends JPanel {
    private final DefaultListModel<String> aspirantes = new DefaultListModel<>();
    private final DefaultListModel<String> elegidos = new DefaultListModel<>();
    private final JList<String> listaAspirantes = new JList<>(aspirantes);
    private final JList<String> listaElegidos = new JList<>(elegidos);
    private final JLabel estado = new JLabel();

    PanelReclutador() {
        super(new BorderLayout(6, 6));
        setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));
        for (String a : new String[]{"Pip", "Nara", "Olmo", "Ada", "Tomás", "Lía"}) {
            aspirantes.addElement(a);
        }
        JButton pasar = new JButton(">");
        JButton devolver = new JButton("<");
        JButton todos = new JButton(">>");
        JPanel medio = new JPanel(new GridLayout(3, 1, 4, 4));
        medio.add(pasar);
        medio.add(devolver);
        medio.add(todos);
        JPanel listas = new JPanel(new BorderLayout(6, 6));
        listas.add(new JScrollPane(listaAspirantes), BorderLayout.WEST);
        listas.add(medio, BorderLayout.CENTER);
        listas.add(new JScrollPane(listaElegidos), BorderLayout.EAST);
        listaAspirantes.setVisibleRowCount(8);
        listaElegidos.setVisibleRowCount(8);
        listaAspirantes.setPrototypeCellValue("XXXXXXXXXXXX");
        listaElegidos.setPrototypeCellValue("XXXXXXXXXXXX");
        JTextField nuevo = new JTextField(12);
        JPanel abajo = new JPanel();
        abajo.add(new JLabel("Nuevo:"));
        abajo.add(nuevo);
        abajo.add(estado);
        add(listas, BorderLayout.CENTER);
        add(abajo, BorderLayout.SOUTH);

        pasar.addActionListener(e -> mover(listaAspirantes.getSelectedValuesList(), aspirantes, elegidos));
        devolver.addActionListener(e -> mover(listaElegidos.getSelectedValuesList(), elegidos, aspirantes));
        todos.addActionListener(e -> mover(java.util.Collections.list(aspirantes.elements()), aspirantes, elegidos));
        nuevo.addActionListener(e -> {
            String nombre = nuevo.getText().trim();
            if (!nombre.isEmpty() && !aspirantes.contains(nombre) && !elegidos.contains(nombre)) {
                aspirantes.addElement(nombre);
            }
            nuevo.setText("");
        });
        actualizar();
    }

    private void mover(List<String> quienes, DefaultListModel<String> desde, DefaultListModel<String> hacia) {
        for (String q : quienes) {
            desde.removeElement(q);
            hacia.addElement(q);
        }
        actualizar();
    }

    private void actualizar() {
        estado.setText("Elegidos: " + elegidos.size());
        estado.setForeground(elegidos.size() > 4 ? Color.RED : Color.BLACK);
    }
}
```

### Misión R05-N03-M3 · El panel de sonido

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Hacé el panel de configuración de sonido del Arcade: tres `JSlider` (volumen general,
música y efectos, de 0 a 100, con marcas cada 25), una `JCheckBox` "Silencio" que
**deshabilita** los tres sliders, y una `JProgressBar` que muestra el volumen real de la
música (general × música / 100). Cada slider muestra su valor en una etiqueta al lado.
Un botón `Restaurar` pone los valores de fábrica (80, 60, 70).

#### Criterio de aprobación

- Los sliders usan `addChangeListener` y actualizan sus etiquetas.
- La casilla habilita y deshabilita los sliders.
- La barra de progreso refleja el cálculo.

#### Solución de referencia

```java
// Mision 3 - El panel de sonido: JSlider, JCheckBox y JProgressBar.
import java.awt.BorderLayout;
import java.awt.GridLayout;
import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JProgressBar;
import javax.swing.JSlider;
import javax.swing.SwingUtilities;

public class PanelDeSonido {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Sonido");
            f.setContentPane(new PanelSonido());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

class PanelSonido extends JPanel {
    private final JSlider general = crear();
    private final JSlider musica = crear();
    private final JSlider efectos = crear();
    private final JLabel vGeneral = new JLabel();
    private final JLabel vMusica = new JLabel();
    private final JLabel vEfectos = new JLabel();
    private final JCheckBox silencio = new JCheckBox("Silencio");
    private final JProgressBar real = new JProgressBar(0, 100);

    PanelSonido() {
        super(new BorderLayout(6, 6));
        setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));
        JPanel filas = new JPanel(new GridLayout(3, 3, 6, 6));
        filas.add(new JLabel("General"));
        filas.add(general);
        filas.add(vGeneral);
        filas.add(new JLabel("Música"));
        filas.add(musica);
        filas.add(vMusica);
        filas.add(new JLabel("Efectos"));
        filas.add(efectos);
        filas.add(vEfectos);
        real.setStringPainted(true);
        JButton restaurar = new JButton("Restaurar");
        JPanel abajo = new JPanel(new BorderLayout(6, 6));
        abajo.add(silencio, BorderLayout.WEST);
        abajo.add(real, BorderLayout.CENTER);
        abajo.add(restaurar, BorderLayout.EAST);
        add(filas, BorderLayout.CENTER);
        add(abajo, BorderLayout.SOUTH);

        for (JSlider s : new JSlider[]{general, musica, efectos}) {
            s.addChangeListener(e -> actualizar());
        }
        silencio.addActionListener(e -> actualizar());
        restaurar.addActionListener(e -> {
            general.setValue(80);
            musica.setValue(60);
            efectos.setValue(70);
            silencio.setSelected(false);
            actualizar();
        });
        restaurar.doClick();
    }

    private static JSlider crear() {
        JSlider s = new JSlider(0, 100, 50);
        s.setMajorTickSpacing(25);
        s.setPaintTicks(true);
        return s;
    }

    private void actualizar() {
        vGeneral.setText(general.getValue() + "%");
        vMusica.setText(musica.getValue() + "%");
        vEfectos.setText(efectos.getValue() + "%");
        boolean activo = !silencio.isSelected();
        for (JSlider s : new JSlider[]{general, musica, efectos}) {
            s.setEnabled(activo);
        }
        int volumen = activo ? general.getValue() * musica.getValue() / 100 : 0;
        real.setValue(volumen);
        real.setString("Música real: " + volumen + "%");
    }
}
```

### Encargo R05-N03-E1 · La encuesta del cliente

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Hacé una encuesta de satisfacción para un comercio: un combo con la sucursal, botones
de opción para la atención (1 a 5 estrellas), casillas para "volvería", "recomendaría"
y "fue rápido", un `JTextArea` para comentarios (con un contador de caracteres que se
actualiza al escribir, máximo 200) y un botón `Enviar` que valida (que haya elegido
estrellas y que el comentario no pase de 200) y muestra un resumen en un `JOptionPane`.

#### Criterio de aprobación

- El contador de caracteres usa un `DocumentListener`.
- Se leen todos los controles para armar el resumen.

#### Solución de referencia

```java
// Encargo - La encuesta del cliente: todos los controles y un DocumentListener.
import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.awt.GridLayout;
import java.util.ArrayList;
import java.util.List;
import javax.swing.BorderFactory;
import javax.swing.ButtonGroup;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JComboBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JRadioButton;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.SwingUtilities;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;

public class Encuesta {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Encuesta");
            f.setContentPane(new PanelEncuesta());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

class PanelEncuesta extends JPanel {
    private final JComboBox<String> sucursal = new JComboBox<>(new String[]{"Centro", "Norte", "Shopping"});
    private final JRadioButton[] estrellas = new JRadioButton[5];
    private final ButtonGroup grupoEstrellas = new ButtonGroup();
    private final JCheckBox volveria = new JCheckBox("Volvería");
    private final JCheckBox recomendaria = new JCheckBox("Recomendaría");
    private final JCheckBox rapido = new JCheckBox("Fue rápido");
    private final JTextArea comentario = new JTextArea(4, 30);
    private final JLabel contador = new JLabel("0 / 200");

    PanelEncuesta() {
        super(new BorderLayout(6, 6));
        setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));
        JPanel arriba = new JPanel(new GridLayout(0, 1, 4, 4));
        JPanel filaSucursal = new JPanel(new FlowLayout(FlowLayout.LEFT));
        filaSucursal.add(new JLabel("Sucursal:"));
        filaSucursal.add(sucursal);
        arriba.add(filaSucursal);
        JPanel filaEstrellas = new JPanel(new FlowLayout(FlowLayout.LEFT));
        filaEstrellas.add(new JLabel("Atención:"));
        for (int i = 0; i < 5; i++) {
            estrellas[i] = new JRadioButton((i + 1) + "★");
            grupoEstrellas.add(estrellas[i]);
            filaEstrellas.add(estrellas[i]);
        }
        arriba.add(filaEstrellas);
        JPanel filaChecks = new JPanel(new FlowLayout(FlowLayout.LEFT));
        filaChecks.add(volveria);
        filaChecks.add(recomendaria);
        filaChecks.add(rapido);
        arriba.add(filaChecks);
        add(arriba, BorderLayout.NORTH);
        add(new JScrollPane(comentario), BorderLayout.CENTER);
        JButton enviar = new JButton("Enviar");
        JPanel abajo = new JPanel(new BorderLayout());
        abajo.add(contador, BorderLayout.WEST);
        abajo.add(enviar, BorderLayout.EAST);
        add(abajo, BorderLayout.SOUTH);

        comentario.getDocument().addDocumentListener(new DocumentListener() {
            @Override
            public void insertUpdate(DocumentEvent e) {
                contar();
            }

            @Override
            public void removeUpdate(DocumentEvent e) {
                contar();
            }

            @Override
            public void changedUpdate(DocumentEvent e) {
                contar();
            }
        });
        enviar.addActionListener(e -> enviar());
    }

    private void contar() {
        contador.setText(comentario.getText().length() + " / 200");
    }

    private void enviar() {
        int elegidas = 0;
        for (int i = 0; i < 5; i++) {
            if (estrellas[i].isSelected()) {
                elegidas = i + 1;
            }
        }
        if (elegidas == 0 || comentario.getText().length() > 200) {
            JOptionPane.showMessageDialog(this, "Elegí las estrellas y dejá un comentario de hasta 200 caracteres");
            return;
        }
        List<String> marcas = new ArrayList<>();
        for (JCheckBox c : new JCheckBox[]{volveria, recomendaria, rapido}) {
            if (c.isSelected()) {
                marcas.add(c.getText());
            }
        }
        JOptionPane.showMessageDialog(this, "Sucursal " + sucursal.getSelectedItem() + ", " + elegidas + " estrellas\n"
                + (marcas.isEmpty() ? "sin marcas" : String.join(", ", marcas)) + "\n" + comentario.getText());
    }
}
```

### Prueba del sello

#### ¿Qué hace un `ButtonGroup`?

Hace que los `JRadioButton` que contiene se excluyan entre sí: solo uno puede estar marcado.

#### ¿Cómo se lee el valor elegido en un `JComboBox<Clase>`?

Con `(Clase) combo.getSelectedItem()` (o `getSelectedIndex()` para la posición).

#### ¿Por qué se usa `DefaultListModel` con una `JList`?

Para poder agregar y quitar elementos y que la lista se actualice sola.

#### ¿Qué listener usás para reaccionar a un `JSlider`?

Un `ChangeListener`, con `addChangeListener`.

#### ¿Qué hay que poner alrededor de un `JTextArea` para que tenga barras de desplazamiento?

Un `JScrollPane`.

### Soluciones (docente)

Sale de `18-Java/35-Swing-Componentes` (unidad 6). Corrige lo que marcó la auditoría: el ejemplo original ponía casi todos los componentes pero no leía el valor de la mayoría; acá cada control se lee y alimenta un cálculo en vivo.

## R05-N04 · Tablas, árboles y diálogos

```meta
tipo: tema
padre: R05-N03
precio: 10
criatura: troll
ejecutable: no
temas: gui.tablas-arboles, gui.menus-dialogos
usa: gui.swing
```

### Crónica

En la biblioteca del Palacio hay dos maneras de ver la misma información: una **tabla** enorme donde cada fila es un héroe y cada columna un dato, que se puede ordenar tocando el encabezado; y un **árbol** que muestra los clanes, y dentro de cada clan, sus héroes, y dentro de cada héroe, sus partidas.

—Una tabla responde "¿quiénes son y qué tienen?"; un árbol, "¿qué pertenece a qué?" —dice {mentor}—. En el Palacio, {heroe}, las dos se alimentan de un **modelo**: la tabla solo muestra lo que el modelo dice.

### Objetivos

- Mostrar datos en una `JTable` con un `TableModel` propio.
- Ordenar y seleccionar filas, y reaccionar a la selección.
- Mostrar jerarquías con un `JTree`.
- Usar diálogos: `JOptionPane` y `JFileChooser`.

### Antes de empezar

- Componentes: listas, opciones y controles.
- Colecciones y `record` (ramas 2 y 3).

### Explicación

#### `JTable` y su modelo
Una `JTable` no guarda datos: los **pide** a un **modelo** (`TableModel`). La forma
prolija es escribir un modelo que envuelve una lista de objetos, extendiendo
`AbstractTableModel`:
```java
class ModeloHeroes extends AbstractTableModel {
    private final String[] columnas = {"Nombre", "Clase", "Vida"};
    private final List<Heroe> heroes = new ArrayList<>();

    @Override public int getRowCount() { return heroes.size(); }
    @Override public int getColumnCount() { return columnas.length; }
    @Override public String getColumnName(int c) { return columnas[c]; }

    @Override
    public Object getValueAt(int fila, int col) {
        Heroe h = heroes.get(fila);
        return switch (col) {
            case 0 -> h.nombre();
            case 1 -> h.clase();
            default -> h.vida();
        };
    }

    void agregar(Heroe h) {
        heroes.add(h);
        fireTableRowsInserted(heroes.size() - 1, heroes.size() - 1);   // avisa a la tabla
    }
}
JTable tabla = new JTable(new ModeloHeroes());
add(new JScrollPane(tabla));                   // con scroll y encabezado
```
Cada vez que el modelo cambia, **avisa** con un `fire…`: `fireTableDataChanged()` (todo
cambió), `fireTableRowsInserted`, `fireTableRowsDeleted`, `fireTableRowsUpdated`.

Si `getColumnClass` devuelve `Integer.class` para una columna, la tabla la alinea a la
derecha y la ordena como número.

(`DefaultTableModel`, el que usa NetBeans, guarda filas de `Object[]`: sirve para algo
rápido, pero con un modelo propio los datos son objetos de verdad.)

#### Ordenar y seleccionar
```java
tabla.setAutoCreateRowSorter(true);     // tocar el encabezado ordena
tabla.getSelectionModel().addListSelectionListener(e -> {
    int vista = tabla.getSelectedRow();
    if (!e.getValueIsAdjusting() && vista >= 0) {
        int fila = tabla.convertRowIndexToModel(vista);   // con orden, la fila visible no es la del modelo
        Heroe h = modelo.get(fila);
        …
    }
});
```

#### `JTree`: jerarquías
Un árbol se arma con nodos `DefaultMutableTreeNode`, cada uno con un objeto adentro
(se muestra su `toString`):
```java
DefaultMutableTreeNode raiz = new DefaultMutableTreeNode("Imperio");
DefaultMutableTreeNode clan = new DefaultMutableTreeNode("Clan del Valle");
clan.add(new DefaultMutableTreeNode("Kira"));
raiz.add(clan);
JTree arbol = new JTree(raiz);
arbol.addTreeSelectionListener(e -> {
    DefaultMutableTreeNode nodo = (DefaultMutableTreeNode) arbol.getLastSelectedPathComponent();
    …
});
```
Si cambiás los nodos después de crear el árbol, avisale al modelo:
`((DefaultTreeModel) arbol.getModel()).reload();`.

#### Diálogos
`JOptionPane` para avisos, confirmaciones y preguntas (lo viste en el primer nodo), y
también para elegir entre opciones:
```java
Object elegido = JOptionPane.showInputDialog(this, "Clase:", "Nuevo héroe",
        JOptionPane.QUESTION_MESSAGE, null, new String[]{"arquera", "mago"}, "arquera");
```
`JFileChooser` para elegir un archivo:
```java
JFileChooser selector = new JFileChooser();
selector.setFileFilter(new FileNameExtensionFilter("Archivos CSV", "csv"));
if (selector.showOpenDialog(this) == JFileChooser.APPROVE_OPTION) {
    Path ruta = selector.getSelectedFile().toPath();
    …
}
```
(`showSaveDialog` para guardar.)

### Código de ejemplo

```java
/*
 * Tablas, árboles y diálogos: la biblioteca del Palacio.
 */
import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.util.ArrayList;
import java.util.List;
import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JSplitPane;
import javax.swing.JTable;
import javax.swing.JTree;
import javax.swing.SwingUtilities;
import javax.swing.table.AbstractTableModel;
import javax.swing.tree.DefaultMutableTreeNode;

public class BibliotecaPalacio {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Biblioteca del Palacio");
            f.setContentPane(new PanelBiblioteca());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

record Heroe(String nombre, String clan, String clase, int vida) { }

class ModeloHeroes extends AbstractTableModel {
    private final String[] columnas = {"Nombre", "Clan", "Clase", "Vida"};
    private final List<Heroe> heroes = new ArrayList<>();

    @Override
    public int getRowCount() {
        return heroes.size();
    }

    @Override
    public int getColumnCount() {
        return columnas.length;
    }

    @Override
    public String getColumnName(int c) {
        return columnas[c];
    }

    @Override
    public Class<?> getColumnClass(int c) {
        return c == 3 ? Integer.class : String.class;
    }

    @Override
    public Object getValueAt(int fila, int col) {
        Heroe h = heroes.get(fila);
        return switch (col) {
            case 0 -> h.nombre();
            case 1 -> h.clan();
            case 2 -> h.clase();
            default -> h.vida();
        };
    }

    Heroe get(int fila) {
        return heroes.get(fila);
    }

    List<Heroe> todos() {
        return heroes;
    }

    void agregar(Heroe h) {
        heroes.add(h);
        fireTableRowsInserted(heroes.size() - 1, heroes.size() - 1);
    }

    void quitar(int fila) {
        heroes.remove(fila);
        fireTableRowsDeleted(fila, fila);
    }
}

class PanelBiblioteca extends JPanel {
    private final ModeloHeroes modelo = new ModeloHeroes();
    private final JTable tabla = new JTable(modelo);
    private final DefaultMutableTreeNode raiz = new DefaultMutableTreeNode("Imperio");
    private final JTree arbol = new JTree(raiz);
    private final JLabel detalle = new JLabel("Elegí un héroe");

    PanelBiblioteca() {
        super(new BorderLayout(6, 6));
        setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));
        modelo.agregar(new Heroe("Kira", "Valle", "arquera", 30));
        modelo.agregar(new Heroe("Bron", "Forjas", "guerrero", 45));
        modelo.agregar(new Heroe("Lía", "Valle", "maga", 20));
        modelo.agregar(new Heroe("Nara", "Ciudadela", "paladina", 40));
        tabla.setAutoCreateRowSorter(true);
        tabla.setPreferredScrollableViewportSize(new java.awt.Dimension(360, 120));
        armarArbol();

        JSplitPane division = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT, new JScrollPane(arbol), new JScrollPane(tabla));
        division.setDividerLocation(150);
        add(division, BorderLayout.CENTER);

        JPanel abajo = new JPanel(new FlowLayout(FlowLayout.LEFT));
        JButton nuevo = new JButton("Nuevo");
        JButton borrar = new JButton("Borrar");
        abajo.add(nuevo);
        abajo.add(borrar);
        abajo.add(detalle);
        add(abajo, BorderLayout.SOUTH);

        tabla.getSelectionModel().addListSelectionListener(e -> {
            int vista = tabla.getSelectedRow();
            if (!e.getValueIsAdjusting() && vista >= 0) {
                Heroe h = modelo.get(tabla.convertRowIndexToModel(vista));
                detalle.setText(h.nombre() + ", " + h.clase() + " del clan " + h.clan());
            }
        });
        nuevo.addActionListener(e -> nuevo());
        borrar.addActionListener(e -> borrar());
    }

    private void armarArbol() {
        raiz.removeAllChildren();
        for (Heroe h : modelo.todos()) {
            DefaultMutableTreeNode clan = null;
            for (int i = 0; i < raiz.getChildCount(); i++) {
                DefaultMutableTreeNode n = (DefaultMutableTreeNode) raiz.getChildAt(i);
                if (n.getUserObject().equals("Clan " + h.clan())) {
                    clan = n;
                }
            }
            if (clan == null) {
                clan = new DefaultMutableTreeNode("Clan " + h.clan());
                raiz.add(clan);
            }
            clan.add(new DefaultMutableTreeNode(h.nombre()));
        }
        ((javax.swing.tree.DefaultTreeModel) arbol.getModel()).reload();
        for (int i = 0; i < arbol.getRowCount(); i++) {
            arbol.expandRow(i);
        }
    }

    private void nuevo() {
        String nombre = JOptionPane.showInputDialog(this, "Nombre del héroe:");
        if (nombre == null || nombre.isBlank()) {
            return;
        }
        Object clan = JOptionPane.showInputDialog(this, "Clan:", "Nuevo héroe", JOptionPane.QUESTION_MESSAGE, null,
                new String[]{"Valle", "Forjas", "Ciudadela"}, "Valle");
        if (clan != null) {
            modelo.agregar(new Heroe(nombre.trim(), clan.toString(), "aprendiz", 20));
            armarArbol();
        }
    }

    private void borrar() {
        int vista = tabla.getSelectedRow();
        if (vista < 0) {
            JOptionPane.showMessageDialog(this, "Elegí una fila");
            return;
        }
        int fila = tabla.convertRowIndexToModel(vista);
        if (JOptionPane.showConfirmDialog(this, "¿Borrar a " + modelo.get(fila).nombre() + "?") == JOptionPane.YES_OPTION) {
            modelo.quitar(fila);
            armarArbol();
        }
    }
}
```

### ¿Para qué sirve?

La `JTable` es la pieza central de casi cualquier sistema de gestión de escritorio: el listado de clientes, de productos, de facturas, con filtros y orden. El árbol aparece en exploradores de archivos, organigramas y categorías de productos. Separar el **modelo** (los datos) de la **vista** (la tabla) es la idea que vas a generalizar en el nodo del estilo MVC de la cátedra.

### Errores habituales

**Ogro: la tabla que no se actualiza.** Si cambiás la lista del modelo y no llamás a un
`fire…`, la tabla sigue mostrando lo de antes.

**Troll: la fila equivocada al ordenar.** Con `setAutoCreateRowSorter`, la fila
seleccionada en la vista no es la del modelo. Convertila con `convertRowIndexToModel`
antes de usarla (o vas a borrar a otro héroe).

**Slime: la tabla sin encabezado.** Si ponés la `JTable` directamente en el panel, sin
`JScrollPane`, no se ven los títulos de las columnas.

**Orco: la selección vacía.** `getSelectedRow()` devuelve `-1` si no hay nada
seleccionado: usarla como índice corta con `IndexOutOfBoundsException`.

**Ogro: el árbol que no cambia.** Después de modificar los nodos hay que avisar con
`reload()` del `DefaultTreeModel`.

### Misión R05-N04-M1 · La tabla del inventario

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Hacé una ventana con una `JTable` de productos (código, nombre, precio, stock) con un
modelo propio que extiende `AbstractTableModel` y envuelve una lista de `record
Producto`. La tabla se puede ordenar. Abajo, un formulario pequeño para agregar un
producto (validado) y un botón `Borrar` para la fila seleccionada (con confirmación y
`convertRowIndexToModel`). Una etiqueta muestra el valor total del stock (precio ×
stock de todos), que se actualiza con cada cambio.

#### Criterio de aprobación

- Modelo propio con `getValueAt`, `getColumnName` y `getColumnClass`.
- Agregar y borrar usan los `fire…` correspondientes.
- Borrar funciona bien aun con la tabla ordenada.

#### Solución de referencia

```java
// Mision 1 - La tabla del inventario: AbstractTableModel propio, ordenamiento y ABM.
import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;
import javax.swing.table.AbstractTableModel;

public class TablaInventario {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Inventario");
            f.setContentPane(new PanelInventario());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

record Producto(String codigo, String nombre, double precio, int stock) { }

class ModeloProductos extends AbstractTableModel {
    private final String[] columnas = {"Código", "Nombre", "Precio", "Stock"};
    private final List<Producto> productos = new ArrayList<>();

    @Override
    public int getRowCount() {
        return productos.size();
    }

    @Override
    public int getColumnCount() {
        return columnas.length;
    }

    @Override
    public String getColumnName(int c) {
        return columnas[c];
    }

    @Override
    public Class<?> getColumnClass(int c) {
        return switch (c) {
            case 2 -> Double.class;
            case 3 -> Integer.class;
            default -> String.class;
        };
    }

    @Override
    public Object getValueAt(int fila, int col) {
        Producto p = productos.get(fila);
        return switch (col) {
            case 0 -> p.codigo();
            case 1 -> p.nombre();
            case 2 -> p.precio();
            default -> p.stock();
        };
    }

    Producto get(int fila) {
        return productos.get(fila);
    }

    void agregar(Producto p) {
        productos.add(p);
        fireTableRowsInserted(productos.size() - 1, productos.size() - 1);
    }

    void quitar(int fila) {
        productos.remove(fila);
        fireTableRowsDeleted(fila, fila);
    }

    double valorTotal() {
        double total = 0;
        for (Producto p : productos) {
            total += p.precio() * p.stock();
        }
        return total;
    }
}

class PanelInventario extends JPanel {
    private final ModeloProductos modelo = new ModeloProductos();
    private final JTable tabla = new JTable(modelo);
    private final JTextField codigo = new JTextField(5);
    private final JTextField nombre = new JTextField(10);
    private final JTextField precio = new JTextField(6);
    private final JTextField stock = new JTextField(4);
    private final JLabel total = new JLabel();

    PanelInventario() {
        super(new BorderLayout(6, 6));
        setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));
        modelo.agregar(new Producto("YER", "Yerba", 4200.5, 20));
        modelo.agregar(new Producto("AZU", "Azúcar", 1350, 35));
        tabla.setAutoCreateRowSorter(true);
        tabla.setPreferredScrollableViewportSize(new java.awt.Dimension(420, 110));
        add(new JScrollPane(tabla), BorderLayout.CENTER);
        JPanel form = new JPanel(new FlowLayout(FlowLayout.LEFT));
        JButton agregar = new JButton("Agregar");
        JButton borrar = new JButton("Borrar");
        form.add(new JLabel("Cód"));
        form.add(codigo);
        form.add(new JLabel("Nombre"));
        form.add(nombre);
        form.add(new JLabel("Precio"));
        form.add(precio);
        form.add(new JLabel("Stock"));
        form.add(stock);
        form.add(agregar);
        form.add(borrar);
        JPanel abajo = new JPanel(new BorderLayout());
        abajo.add(form, BorderLayout.CENTER);
        abajo.add(total, BorderLayout.SOUTH);
        add(abajo, BorderLayout.SOUTH);
        agregar.addActionListener(e -> agregar());
        borrar.addActionListener(e -> borrar());
        actualizarTotal();
    }

    private void agregar() {
        try {
            if (codigo.getText().isBlank() || nombre.getText().isBlank()) {
                throw new IllegalArgumentException("código y nombre son obligatorios");
            }
            double p = Double.parseDouble(precio.getText().trim());
            int s = Integer.parseInt(stock.getText().trim());
            if (p <= 0 || s < 0) {
                throw new IllegalArgumentException("precio positivo y stock no negativo");
            }
            modelo.agregar(new Producto(codigo.getText().trim(), nombre.getText().trim(), p, s));
            for (JTextField t : new JTextField[]{codigo, nombre, precio, stock}) {
                t.setText("");
            }
            actualizarTotal();
        } catch (IllegalArgumentException ex) {
            JOptionPane.showMessageDialog(this, "Datos inválidos: " + ex.getMessage());
        }
    }

    private void borrar() {
        int vista = tabla.getSelectedRow();
        if (vista < 0) {
            JOptionPane.showMessageDialog(this, "Elegí un producto");
            return;
        }
        int fila = tabla.convertRowIndexToModel(vista);
        if (JOptionPane.showConfirmDialog(this, "¿Borrar " + modelo.get(fila).nombre() + "?") == JOptionPane.YES_OPTION) {
            modelo.quitar(fila);
            actualizarTotal();
        }
    }

    private void actualizarTotal() {
        total.setText(String.format("Valor del stock: $%.2f", modelo.valorTotal()));
    }
}
```

### Misión R05-N04-M2 · El árbol genealógico del clan

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Hacé una ventana con un `JTree` a la izquierda (el clan, con sus miembros y los hijos
de cada miembro) y, a la derecha, un panel que muestra el detalle del nodo elegido:
nombre, cuántos descendientes tiene (contando todos los niveles, con un método
recursivo) y su profundidad (`getLevel()`). Un botón `Agregar hijo` le agrega un nodo
hijo al seleccionado (pidiendo el nombre con `JOptionPane`) y expande la rama.

#### Criterio de aprobación

- El árbol se arma con `DefaultMutableTreeNode` y se actualiza con `reload` o `nodesWereInserted`.
- Los descendientes se cuentan con un método recursivo.

#### Solución de referencia

```java
// Mision 2 - El arbol genealogico del clan: JTree, seleccion y recursion.
import java.awt.BorderLayout;
import java.awt.GridLayout;
import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTree;
import javax.swing.SwingUtilities;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.DefaultTreeModel;
import javax.swing.tree.TreePath;

public class ArbolClan {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Clan del Valle");
            f.setContentPane(new PanelClan());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

class PanelClan extends JPanel {
    private final DefaultMutableTreeNode raiz = new DefaultMutableTreeNode("Ofidia (fundadora)");
    private final DefaultTreeModel modelo = new DefaultTreeModel(raiz);
    private final JTree arbol = new JTree(modelo);
    private final JLabel nombre = new JLabel("-");
    private final JLabel descendientes = new JLabel("-");
    private final JLabel nivel = new JLabel("-");

    PanelClan() {
        super(new BorderLayout(8, 8));
        setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));
        DefaultMutableTreeNode kira = new DefaultMutableTreeNode("Kira");
        DefaultMutableTreeNode lia = new DefaultMutableTreeNode("Lía");
        kira.add(new DefaultMutableTreeNode("Pip"));
        lia.add(new DefaultMutableTreeNode("Ada"));
        lia.add(new DefaultMutableTreeNode("Tomás"));
        raiz.add(kira);
        raiz.add(lia);
        for (int i = 0; i < arbol.getRowCount(); i++) {
            arbol.expandRow(i);
        }
        JPanel detalle = new JPanel(new GridLayout(4, 2, 4, 4));
        detalle.setBorder(BorderFactory.createTitledBorder("Detalle"));
        detalle.add(new JLabel("Nombre:"));
        detalle.add(nombre);
        detalle.add(new JLabel("Descendientes:"));
        detalle.add(descendientes);
        detalle.add(new JLabel("Generación:"));
        detalle.add(nivel);
        JButton agregar = new JButton("Agregar hijo");
        detalle.add(agregar);
        JScrollPane izquierda = new JScrollPane(arbol);
        izquierda.setPreferredSize(new java.awt.Dimension(180, 180));
        add(izquierda, BorderLayout.WEST);
        add(detalle, BorderLayout.CENTER);

        arbol.addTreeSelectionListener(e -> mostrar());
        agregar.addActionListener(e -> agregarHijo());
    }

    private DefaultMutableTreeNode seleccionado() {
        return (DefaultMutableTreeNode) arbol.getLastSelectedPathComponent();
    }

    private void mostrar() {
        DefaultMutableTreeNode n = seleccionado();
        if (n == null) {
            return;
        }
        nombre.setText(n.getUserObject().toString());
        descendientes.setText(String.valueOf(contarDescendientes(n)));
        nivel.setText(String.valueOf(n.getLevel() + 1));
    }

    static int contarDescendientes(DefaultMutableTreeNode n) {
        int total = 0;
        for (int i = 0; i < n.getChildCount(); i++) {
            total += 1 + contarDescendientes((DefaultMutableTreeNode) n.getChildAt(i));
        }
        return total;
    }

    private void agregarHijo() {
        DefaultMutableTreeNode padre = seleccionado();
        if (padre == null) {
            JOptionPane.showMessageDialog(this, "Elegí a quién agregarle un hijo");
            return;
        }
        String hijo = JOptionPane.showInputDialog(this, "Nombre del hijo de " + padre + ":");
        if (hijo != null && !hijo.isBlank()) {
            DefaultMutableTreeNode nuevo = new DefaultMutableTreeNode(hijo.trim());
            padre.add(nuevo);
            modelo.nodesWereInserted(padre, new int[]{padre.getChildCount() - 1});
            arbol.expandPath(new TreePath(padre.getPath()));
            mostrar();
        }
    }
}
```

### Misión R05-N04-M3 · El visor de CSV

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Hacé un visor de archivos CSV: un botón `Abrir` que usa `JFileChooser` (con filtro
para `.csv`) y carga el archivo en una `JTable` genérica: la primera línea son los
nombres de las columnas y el resto, las filas (separadas por `;`). Usá un
`AbstractTableModel` que guarde las columnas y una lista de filas `String[]`. Si una
línea tiene menos campos, completá con vacíos; si el archivo no se puede leer, mostrá un
`JOptionPane` de error. Una etiqueta abajo dice cuántas filas y columnas se cargaron.

#### Criterio de aprobación

- Usa `JFileChooser` con `FileNameExtensionFilter`.
- El modelo es genérico (sirve para cualquier CSV) y avisa con `fireTableStructureChanged`.
- Los errores de lectura se informan sin cortar el programa.

#### Solución de referencia

```java
// Mision 3 - El visor de CSV: JFileChooser y un TableModel generico.
import java.awt.BorderLayout;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.SwingUtilities;
import javax.swing.filechooser.FileNameExtensionFilter;
import javax.swing.table.AbstractTableModel;

public class VisorCsv {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Visor de CSV");
            f.setContentPane(new PanelVisor());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

class ModeloCsv extends AbstractTableModel {
    private String[] columnas = {};
    private final List<String[]> filas = new ArrayList<>();

    @Override
    public int getRowCount() {
        return filas.size();
    }

    @Override
    public int getColumnCount() {
        return columnas.length;
    }

    @Override
    public String getColumnName(int c) {
        return columnas[c];
    }

    @Override
    public Object getValueAt(int f, int c) {
        return filas.get(f)[c];
    }

    void cargar(List<String> lineas) {
        filas.clear();
        columnas = lineas.isEmpty() ? new String[]{} : lineas.get(0).split(";", -1);
        for (String l : lineas.subList(Math.min(1, lineas.size()), lineas.size())) {
            filas.add(Arrays.copyOf(l.split(";", -1), columnas.length));
        }
        for (String[] f : filas) {
            for (int i = 0; i < f.length; i++) {
                if (f[i] == null) {
                    f[i] = "";
                }
            }
        }
        fireTableStructureChanged();
    }
}

class PanelVisor extends JPanel {
    private final ModeloCsv modelo = new ModeloCsv();
    private final JLabel estado = new JLabel("Ningún archivo abierto");

    PanelVisor() {
        super(new BorderLayout(6, 6));
        setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));
        JButton abrir = new JButton("Abrir…");
        JTable tabla = new JTable(modelo);
        tabla.setPreferredScrollableViewportSize(new java.awt.Dimension(420, 150));
        add(abrir, BorderLayout.NORTH);
        add(new JScrollPane(tabla), BorderLayout.CENTER);
        add(estado, BorderLayout.SOUTH);
        abrir.addActionListener(e -> abrir());
    }

    private void abrir() {
        JFileChooser selector = new JFileChooser();
        selector.setFileFilter(new FileNameExtensionFilter("Archivos CSV", "csv"));
        if (selector.showOpenDialog(this) != JFileChooser.APPROVE_OPTION) {
            return;
        }
        Path ruta = selector.getSelectedFile().toPath();
        try {
            modelo.cargar(Files.readAllLines(ruta));
            estado.setText(ruta.getFileName() + ": " + modelo.getRowCount() + " filas, " + modelo.getColumnCount() + " columnas");
        } catch (IOException ex) {
            JOptionPane.showMessageDialog(this, "No se pudo leer el archivo: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }
}
```

### Encargo R05-N04-E1 · La agenda de la veterinaria

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Una veterinaria quiere ver sus turnos en una tabla (hora, mascota, especie, dueño) y
filtrar por especie con un combo arriba (`Todas`, `perro`, `gato`, `otro`). Usá un
`TableRowSorter` con un `RowFilter` para filtrar sin cambiar el modelo. Un doble clic en
una fila muestra un `JOptionPane` con el detalle del turno. Cargá al menos 6 turnos de
ejemplo.

#### Criterio de aprobación

- El filtro usa `TableRowSorter` y `RowFilter.regexFilter` (o uno propio).
- El doble clic usa un `MouseListener` y `convertRowIndexToModel`.

#### Solución de referencia

```java
// Encargo - La agenda de la veterinaria: TableRowSorter, RowFilter y doble clic.
import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import javax.swing.BorderFactory;
import javax.swing.JComboBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.RowFilter;
import javax.swing.SwingUtilities;
import javax.swing.table.DefaultTableModel;
import javax.swing.table.TableRowSorter;

public class Veterinaria {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Veterinaria · Turnos");
            f.setContentPane(new PanelTurnos());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

class PanelTurnos extends JPanel {
    PanelTurnos() {
        super(new BorderLayout(6, 6));
        setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));
        String[] columnas = {"Hora", "Mascota", "Especie", "Dueño"};
        Object[][] datos = {
            {"09:00", "Firulais", "perro", "Marta"}, {"09:30", "Michi", "gato", "Juan"},
            {"10:00", "Rex", "perro", "Ana"}, {"10:30", "Pancho", "otro", "Leo"},
            {"11:00", "Luna", "gato", "Sofía"}, {"11:30", "Toby", "perro", "Pedro"},
        };
        DefaultTableModel modelo = new DefaultTableModel(datos, columnas) {
            @Override
            public boolean isCellEditable(int f, int c) {
                return false;
            }
        };
        JTable tabla = new JTable(modelo);
        TableRowSorter<DefaultTableModel> ordenador = new TableRowSorter<>(modelo);
        tabla.setRowSorter(ordenador);
        tabla.setPreferredScrollableViewportSize(new java.awt.Dimension(380, 120));

        JComboBox<String> especie = new JComboBox<>(new String[]{"Todas", "perro", "gato", "otro"});
        JPanel arriba = new JPanel(new FlowLayout(FlowLayout.LEFT));
        arriba.add(new JLabel("Especie:"));
        arriba.add(especie);
        add(arriba, BorderLayout.NORTH);
        add(new JScrollPane(tabla), BorderLayout.CENTER);

        especie.addActionListener(e -> {
            String elegida = (String) especie.getSelectedItem();
            ordenador.setRowFilter("Todas".equals(elegida) ? null : RowFilter.regexFilter("^" + elegida + "$", 2));
        });
        tabla.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                int vista = tabla.getSelectedRow();
                if (e.getClickCount() == 2 && vista >= 0) {
                    int fila = tabla.convertRowIndexToModel(vista);
                    JOptionPane.showMessageDialog(PanelTurnos.this, "Turno de las " + modelo.getValueAt(fila, 0) + ": "
                            + modelo.getValueAt(fila, 1) + " (" + modelo.getValueAt(fila, 2) + "), de " + modelo.getValueAt(fila, 3));
                }
            }
        });
    }
}
```

### Prueba del sello

#### ¿Qué guarda una `JTable`?

Nada: le pide los datos a su `TableModel`.

#### ¿Qué hay que hacer después de modificar los datos del modelo?

Avisar a la tabla con un `fire…` (`fireTableRowsInserted`, `fireTableDataChanged`, etc.).

#### ¿Por qué hace falta `convertRowIndexToModel` si la tabla está ordenada?

Porque la fila visible no coincide con la posición en el modelo; sin convertir, se usa el dato de otra fila.

#### ¿Con qué clase se arman los nodos de un `JTree`?

Con `DefaultMutableTreeNode`.

#### ¿Qué devuelve `showOpenDialog` de un `JFileChooser` si el usuario eligió un archivo?

`JFileChooser.APPROVE_OPTION`; el archivo se obtiene con `getSelectedFile()`.

### Soluciones (docente)

Sale de `18-Java/37-MDI-Tablas-Arboles` (el 36 por crear), unidad 6. El modelo propio reemplaza al `DefaultTableModel` de filas `Object[]` que usaba el original; el `DefaultTableModel` se muestra igual en el encargo porque es el que genera NetBeans.

## R05-N05 · MDI y menús

```meta
tipo: tema
padre: R05-N04
precio: 10
criatura: ogre
ejecutable: no
temas: gui.menus-dialogos
usa: gui.swing
```

### Crónica

El salón del trono del Palacio tiene una sola ventana enorme, y adentro, muchas ventanitas: el registro de héroes, la tesorería, el mapa. Se abren, se mueven, se superponen y se cierran sin salir del salón. Arriba de todo, un menú con todas las puertas del Palacio.

—Un sistema de gestión no es una ventana: es un **escritorio** con muchas —dice {mentor}—. Una ventana principal con su **menú**, y adentro las ventanas de cada tarea. Así trabajan los sistemas del Imperio, {heroe}, y así los pide la cátedra.

### Objetivos

- Armar una barra de menú con `JMenuBar`, `JMenu` y `JMenuItem`, con atajos de teclado.
- Crear una aplicación MDI con `JDesktopPane` y `JInternalFrame`.
- Evitar abrir dos veces la misma ventana interna.
- Usar una barra de herramientas y una barra de estado.

### Antes de empezar

- Tablas, árboles y diálogos.

### Explicación

#### El menú
```java
JMenuBar barra = new JMenuBar();
JMenu archivo = new JMenu("Archivo");
archivo.setMnemonic(KeyEvent.VK_A);                     // Alt+A abre el menú
JMenuItem salir = new JMenuItem("Salir");
salir.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_Q, InputEvent.CTRL_DOWN_MASK));   // Ctrl+Q
salir.addActionListener(e -> System.exit(0));
archivo.add(salir);
barra.add(archivo);
ventana.setJMenuBar(barra);
```
Los ítems funcionan como botones (`addActionListener`). También existen
`JCheckBoxMenuItem`, `JRadioButtonMenuItem` y separadores (`menu.addSeparator()`).
Si un ítem no aplica en un momento, se deshabilita con `setEnabled(false)`.

#### MDI: ventanas dentro de una ventana
**MDI** (*Multiple Document Interface*) es una ventana principal con un **escritorio**
(`JDesktopPane`) donde viven **ventanas internas** (`JInternalFrame`):
```java
JDesktopPane escritorio = new JDesktopPane();
ventana.setContentPane(escritorio);

JInternalFrame interna = new JInternalFrame("Héroes",
        true,    // se puede redimensionar
        true,    // se puede cerrar
        true,    // se puede maximizar
        true);   // se puede minimizar
interna.setContentPane(new PanelHeroes());
interna.pack();
interna.setVisible(true);
escritorio.add(interna);
```
Una `JInternalFrame` se usa como un `JFrame` (título, contenido, `pack`), pero vive y se
mueve dentro del escritorio.

#### No abrir dos veces la misma ventana
Si el usuario toca dos veces "Héroes" en el menú, lo lógico es traer al frente la que
ya está abierta:
```java
private JInternalFrame heroes;

void abrirHeroes() {
    if (heroes == null || heroes.isClosed()) {
        heroes = crearVentanaHeroes();
        escritorio.add(heroes);
    }
    heroes.setVisible(true);
    try {
        heroes.setSelected(true);           // al frente y con el foco
    } catch (java.beans.PropertyVetoException ignorada) {
    }
}
```

#### Barra de herramientas y barra de estado
Una `JToolBar` con botones de acceso rápido va arriba (`BorderLayout.NORTH`) y una
etiqueta con el estado del sistema, abajo. Con un escritorio MDI, se arma un panel con
`BorderLayout`, el escritorio en el centro y las barras en los bordes.

#### Diálogos modales propios
Un `JDialog` es una ventana secundaria; si es **modal**, bloquea la principal hasta que
se cierra (como un formulario de alta que tiene que completarse o cancelarse).

### Código de ejemplo

```java
/*
 * MDI y menús: el salón del trono. Un escritorio con ventanas internas.
 */
import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.event.InputEvent;
import java.awt.event.KeyEvent;
import java.beans.PropertyVetoException;
import javax.swing.JButton;
import javax.swing.JDesktopPane;
import javax.swing.JFrame;
import javax.swing.JInternalFrame;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JTextArea;
import javax.swing.JToolBar;
import javax.swing.KeyStroke;
import javax.swing.SwingUtilities;

public class SalonTrono {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Salón del trono");
            PanelTrono trono = new PanelTrono();
            f.setContentPane(trono);
            f.setJMenuBar(trono.crearMenu());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.setSize(800, 560);
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

class PanelTrono extends JPanel {
    private final JDesktopPane escritorio = new JDesktopPane();
    private final JLabel estado = new JLabel(" Listo");
    private JInternalFrame heroes;
    private JInternalFrame notas;

    PanelTrono() {
        super(new BorderLayout());
        setPreferredSize(new Dimension(760, 480));
        JToolBar herramientas = new JToolBar();
        JButton bHeroes = new JButton("Héroes");
        JButton bNotas = new JButton("Notas");
        herramientas.add(bHeroes);
        herramientas.add(bNotas);
        bHeroes.addActionListener(e -> abrirHeroes());
        bNotas.addActionListener(e -> abrirNotas());
        add(herramientas, BorderLayout.NORTH);
        add(escritorio, BorderLayout.CENTER);
        add(estado, BorderLayout.SOUTH);
        abrirHeroes();
    }

    JMenuBar crearMenu() {
        JMenuBar barra = new JMenuBar();
        JMenu archivo = new JMenu("Archivo");
        archivo.setMnemonic(KeyEvent.VK_A);
        JMenuItem salir = new JMenuItem("Salir");
        salir.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_Q, InputEvent.CTRL_DOWN_MASK));
        salir.addActionListener(e -> System.exit(0));
        archivo.add(salir);

        JMenu ventanas = new JMenu("Ventanas");
        ventanas.setMnemonic(KeyEvent.VK_V);
        JMenuItem mHeroes = new JMenuItem("Registro de héroes");
        mHeroes.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_H, InputEvent.CTRL_DOWN_MASK));
        mHeroes.addActionListener(e -> abrirHeroes());
        JMenuItem mNotas = new JMenuItem("Notas del día");
        mNotas.addActionListener(e -> abrirNotas());
        JMenuItem cerrarTodas = new JMenuItem("Cerrar todas");
        cerrarTodas.addActionListener(e -> {
            for (JInternalFrame v : escritorio.getAllFrames()) {
                v.dispose();
            }
            estado.setText(" Todas las ventanas cerradas");
        });
        ventanas.add(mHeroes);
        ventanas.add(mNotas);
        ventanas.addSeparator();
        ventanas.add(cerrarTodas);

        JMenu ayuda = new JMenu("Ayuda");
        JMenuItem acerca = new JMenuItem("Acerca de…");
        acerca.addActionListener(e -> JOptionPane.showMessageDialog(this, "Sistema del Palacio · versión 1.0"));
        ayuda.add(acerca);

        barra.add(archivo);
        barra.add(ventanas);
        barra.add(ayuda);
        return barra;
    }

    private void abrirHeroes() {
        if (heroes == null || heroes.isClosed()) {
            heroes = new JInternalFrame("Registro de héroes", true, true, true, true);
            String[] columnas = {"Nombre", "Clase", "Vida"};
            Object[][] datos = {{"Kira", "arquera", 30}, {"Bron", "guerrero", 45}, {"Lía", "maga", 20}};
            heroes.setContentPane(new JScrollPane(new JTable(datos, columnas)));
            heroes.setSize(340, 160);
            heroes.setLocation(20, 20);
            escritorio.add(heroes);
        }
        mostrar(heroes);
    }

    private void abrirNotas() {
        if (notas == null || notas.isClosed()) {
            notas = new JInternalFrame("Notas del día", true, true, true, true);
            notas.setContentPane(new JScrollPane(new JTextArea("Revisar la tesorería.\nRecibir a la embajada del Valle.")));
            notas.setSize(300, 180);
            notas.setLocation(220, 120);
            escritorio.add(notas);
        }
        mostrar(notas);
    }

    private void mostrar(JInternalFrame v) {
        v.setVisible(true);
        try {
            v.setSelected(true);
        } catch (PropertyVetoException ignorada) {
            // la ventana no aceptó el foco: no pasa nada
        }
        estado.setText(" Abierta: " + v.getTitle());
    }
}
```

### ¿Para qué sirve?

La mayoría de los sistemas de gestión de escritorio (contables, de stock, de facturación) tienen esta forma: una ventana principal con menú y barra de herramientas, y ventanas internas para cada módulo. Es el estilo del caso práctico de la cátedra (menú con "Alumnos", "Profesores", "Actas") y el que genera NetBeans con su plantilla de aplicación MDI.

### Errores habituales

**Ogro: la ventana interna invisible.** Un `JInternalFrame` nace oculto y sin tamaño:
falta `setVisible(true)` y `pack()` o `setSize`.

**Ogro: abrir diez veces la misma ventana.** Si cada clic en el menú crea una
`JInternalFrame` nueva, se apilan copias. Guardala en un atributo y reutilizala.

**Slime: el menú que no aparece.** El `JMenuBar` se pone con `setJMenuBar` en el
`JFrame`, no con `add`.

**Ogro: el escritorio sin tamaño.** Un `JDesktopPane` no tiene tamaño preferido: si
usás `pack()` en la ventana principal, queda chiquito. Dale un tamaño a la ventana o al
panel.

**Esqueleto: `PropertyVetoException`.** `setSelected(true)` declara esa excepción
checked: hay que atraparla (normalmente se ignora).

### Misión R05-N05-M1 · El sistema de la posada

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Armá la ventana principal del sistema de la posada: un menú `Archivo` (Salir con
`Ctrl+Q`), un menú `Módulos` con `Habitaciones`, `Huéspedes` y `Caja`, cada uno con su
atajo, y un menú `Ayuda`. Cada módulo abre una `JInternalFrame` con un contenido simple
(una tabla o un texto), **sin abrirla dos veces**. Una barra de estado abajo muestra
cuántas ventanas hay abiertas cada vez que se abre una.

#### Criterio de aprobación

- Menú con atajos (`setAccelerator`) y mnemónicos.
- Ninguna ventana interna se abre dos veces.
- La barra de estado se actualiza.

#### Solución de referencia

```java
// Mision 1 - El sistema de la posada: menu con atajos y ventanas internas sin duplicados.
import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.event.InputEvent;
import java.awt.event.KeyEvent;
import java.beans.PropertyVetoException;
import java.util.HashMap;
import java.util.Map;
import javax.swing.JComponent;
import javax.swing.JDesktopPane;
import javax.swing.JFrame;
import javax.swing.JInternalFrame;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.KeyStroke;
import javax.swing.SwingUtilities;

public class SistemaPosada {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Posada La Taza · Sistema");
            PanelPosada p = new PanelPosada();
            f.setContentPane(p);
            f.setJMenuBar(p.menu());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.setSize(760, 520);
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

class PanelPosada extends JPanel {
    private final JDesktopPane escritorio = new JDesktopPane();
    private final JLabel estado = new JLabel(" Sin ventanas abiertas");
    private final Map<String, JInternalFrame> abiertas = new HashMap<>();

    PanelPosada() {
        super(new BorderLayout());
        setPreferredSize(new Dimension(740, 460));
        add(escritorio, BorderLayout.CENTER);
        add(estado, BorderLayout.SOUTH);
    }

    JMenuBar menu() {
        JMenuBar barra = new JMenuBar();
        JMenu archivo = new JMenu("Archivo");
        archivo.setMnemonic(KeyEvent.VK_A);
        JMenuItem salir = new JMenuItem("Salir");
        salir.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_Q, InputEvent.CTRL_DOWN_MASK));
        salir.addActionListener(e -> System.exit(0));
        archivo.add(salir);

        JMenu modulos = new JMenu("Módulos");
        modulos.setMnemonic(KeyEvent.VK_M);
        modulos.add(item("Habitaciones", KeyEvent.VK_1, () -> new JScrollPane(new JTable(
                new Object[][]{{"101", "simple", "libre"}, {"102", "doble", "ocupada"}}, new String[]{"N°", "Tipo", "Estado"}))));
        modulos.add(item("Huéspedes", KeyEvent.VK_2, () -> new JScrollPane(new JTable(
                new Object[][]{{"Kira", "102"}, {"Bron", "205"}}, new String[]{"Nombre", "Habitación"}))));
        modulos.add(item("Caja", KeyEvent.VK_3, () -> new JLabel("Caja del día: 48 500 denarios", JLabel.CENTER)));

        JMenu ayuda = new JMenu("Ayuda");
        JMenuItem acerca = new JMenuItem("Acerca de…");
        acerca.addActionListener(e -> JOptionPane.showMessageDialog(this, "Sistema de la posada"));
        ayuda.add(acerca);

        barra.add(archivo);
        barra.add(modulos);
        barra.add(ayuda);
        return barra;
    }

    private JMenuItem item(String titulo, int tecla, java.util.function.Supplier<JComponent> contenido) {
        JMenuItem i = new JMenuItem(titulo);
        i.setAccelerator(KeyStroke.getKeyStroke(tecla, InputEvent.CTRL_DOWN_MASK));
        i.addActionListener(e -> abrir(titulo, contenido));
        return i;
    }

    private void abrir(String titulo, java.util.function.Supplier<JComponent> contenido) {
        JInternalFrame v = abiertas.get(titulo);
        if (v == null || v.isClosed()) {
            v = new JInternalFrame(titulo, true, true, true, true);
            v.setContentPane(contenido.get());
            v.setSize(320, 160);
            v.setLocation(20 + abiertas.size() * 30, 20 + abiertas.size() * 30);
            escritorio.add(v);
            abiertas.put(titulo, v);
        }
        v.setVisible(true);
        try {
            v.setSelected(true);
        } catch (PropertyVetoException ignorada) {
            // sin foco, igual se muestra
        }
        long cuantas = abiertas.values().stream().filter(x -> !x.isClosed()).count();
        estado.setText(" Ventanas abiertas: " + cuantas);
    }
}
```

### Misión R05-N05-M2 · El diálogo de alta

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Hacé una ventana con una tabla de huéspedes y un botón `Nuevo…` que abre un **`JDialog`
modal** propio con el formulario (nombre, documento, noches) y los botones `Aceptar` y
`Cancelar`. El diálogo valida los datos; si se acepta, **devuelve** un `record Huesped`
a la ventana principal, que lo agrega a la tabla. Si se cancela, no pasa nada. El
diálogo se centra sobre la ventana principal.

#### Criterio de aprobación

- El diálogo es modal y valida antes de cerrarse.
- La ventana principal recibe el resultado del diálogo (por ejemplo, con un método `Huesped mostrar()` que devuelve `null` si se canceló).

#### Solución de referencia

```java
// Mision 2 - El dialogo de alta: un JDialog modal que devuelve un resultado.
import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.awt.GridLayout;
import java.awt.Window;
import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;
import javax.swing.table.DefaultTableModel;

public class AltaHuesped {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Huéspedes");
            f.setContentPane(new PanelHuespedes());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

record Huesped(String nombre, String documento, int noches) { }

class PanelHuespedes extends JPanel {
    private final DefaultTableModel modelo = new DefaultTableModel(new String[]{"Nombre", "Documento", "Noches"}, 0);

    PanelHuespedes() {
        super(new BorderLayout(6, 6));
        setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));
        JTable tabla = new JTable(modelo);
        tabla.setPreferredScrollableViewportSize(new java.awt.Dimension(360, 120));
        JButton nuevo = new JButton("Nuevo…");
        add(new JScrollPane(tabla), BorderLayout.CENTER);
        add(nuevo, BorderLayout.SOUTH);
        nuevo.addActionListener(e -> {
            Huesped h = new DialogoHuesped(SwingUtilities.getWindowAncestor(this)).mostrar();
            if (h != null) {
                modelo.addRow(new Object[]{h.nombre(), h.documento(), h.noches()});
            }
        });
    }
}

class DialogoHuesped extends JDialog {
    private final JTextField nombre = new JTextField(14);
    private final JTextField documento = new JTextField(10);
    private final JTextField noches = new JTextField(4);
    private Huesped resultado;

    DialogoHuesped(Window duenio) {
        super(duenio, "Nuevo huésped", ModalityType.APPLICATION_MODAL);
        JPanel form = new JPanel(new GridLayout(3, 2, 6, 6));
        form.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        form.add(new JLabel("Nombre:"));
        form.add(nombre);
        form.add(new JLabel("Documento:"));
        form.add(documento);
        form.add(new JLabel("Noches:"));
        form.add(noches);
        JPanel botones = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        JButton cancelar = new JButton("Cancelar");
        JButton aceptar = new JButton("Aceptar");
        botones.add(cancelar);
        botones.add(aceptar);
        add(form, BorderLayout.CENTER);
        add(botones, BorderLayout.SOUTH);
        getRootPane().setDefaultButton(aceptar);
        cancelar.addActionListener(e -> dispose());
        aceptar.addActionListener(e -> aceptar());
        pack();
        setLocationRelativeTo(duenio);
    }

    private void aceptar() {
        try {
            int n = Integer.parseInt(noches.getText().trim());
            if (nombre.getText().isBlank() || !documento.getText().trim().matches("\\d{7,8}") || n <= 0) {
                throw new IllegalArgumentException();
            }
            resultado = new Huesped(nombre.getText().trim(), documento.getText().trim(), n);
            dispose();
        } catch (IllegalArgumentException ex) {
            JOptionPane.showMessageDialog(this, "Revisá los datos: nombre, documento de 7 u 8 dígitos y noches positivas");
        }
    }

    Huesped mostrar() {
        setVisible(true);      // modal: se queda acá hasta que el diálogo se cierra
        return resultado;
    }
}
```

### Misión R05-N05-M3 · El menú que se adapta

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Hacé un pequeño editor de notas con menú `Archivo` (Nuevo, Guardar, Salir), `Edición`
(Mayúsculas, Minúsculas) y `Ver` con un `JCheckBoxMenuItem` "Ajustar líneas" y tres
`JRadioButtonMenuItem` de tamaño de letra (chica, mediana, grande) en un `ButtonGroup`.
`Guardar` se **habilita** solo cuando hay cambios sin guardar (detectalos con un
`DocumentListener`) y el título de la ventana muestra un `*` cuando hay cambios. Guardar
solo marca como guardado (no hace falta escribir el archivo).

#### Criterio de aprobación

- Usa `JCheckBoxMenuItem` y `JRadioButtonMenuItem` con `ButtonGroup`.
- El ítem Guardar y el título reflejan si hay cambios.

#### Solución de referencia

```java
// Mision 3 - El menu que se adapta: items que se habilitan y menus con opciones.
import java.awt.BorderLayout;
import java.awt.Font;
import java.awt.event.InputEvent;
import java.awt.event.KeyEvent;
import javax.swing.ButtonGroup;
import javax.swing.JCheckBoxMenuItem;
import javax.swing.JFrame;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JPanel;
import javax.swing.JRadioButtonMenuItem;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.KeyStroke;
import javax.swing.SwingUtilities;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;

public class EditorNotas {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame();
            PanelEditor editor = new PanelEditor(f);
            f.setContentPane(editor);
            f.setJMenuBar(editor.menu());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

class PanelEditor extends JPanel {
    private final JTextArea texto = new JTextArea(12, 40);
    private final JMenuItem guardar = new JMenuItem("Guardar");
    private final JFrame ventana;
    private boolean cambios = false;

    PanelEditor() {
        this(null);
    }

    PanelEditor(JFrame ventana) {
        super(new BorderLayout());
        this.ventana = ventana;
        add(new JScrollPane(texto), BorderLayout.CENTER);
        texto.getDocument().addDocumentListener(new DocumentListener() {
            @Override
            public void insertUpdate(DocumentEvent e) {
                marcar(true);
            }

            @Override
            public void removeUpdate(DocumentEvent e) {
                marcar(true);
            }

            @Override
            public void changedUpdate(DocumentEvent e) {
                marcar(true);
            }
        });
        marcar(false);
    }

    JMenuBar menu() {
        JMenuBar barra = new JMenuBar();
        JMenu archivo = new JMenu("Archivo");
        JMenuItem nuevo = new JMenuItem("Nuevo");
        nuevo.addActionListener(e -> {
            texto.setText("");
            marcar(false);
        });
        guardar.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_S, InputEvent.CTRL_DOWN_MASK));
        guardar.addActionListener(e -> marcar(false));
        JMenuItem salir = new JMenuItem("Salir");
        salir.addActionListener(e -> System.exit(0));
        archivo.add(nuevo);
        archivo.add(guardar);
        archivo.addSeparator();
        archivo.add(salir);

        JMenu edicion = new JMenu("Edición");
        JMenuItem mayus = new JMenuItem("Mayúsculas");
        mayus.addActionListener(e -> texto.setText(texto.getText().toUpperCase()));
        JMenuItem minus = new JMenuItem("Minúsculas");
        minus.addActionListener(e -> texto.setText(texto.getText().toLowerCase()));
        edicion.add(mayus);
        edicion.add(minus);

        JMenu ver = new JMenu("Ver");
        JCheckBoxMenuItem ajustar = new JCheckBoxMenuItem("Ajustar líneas");
        ajustar.addActionListener(e -> {
            texto.setLineWrap(ajustar.isSelected());
            texto.setWrapStyleWord(ajustar.isSelected());
        });
        ver.add(ajustar);
        ver.addSeparator();
        ButtonGroup tamanios = new ButtonGroup();
        int[] puntos = {12, 16, 22};
        String[] nombres = {"Letra chica", "Letra mediana", "Letra grande"};
        for (int i = 0; i < puntos.length; i++) {
            JRadioButtonMenuItem opcion = new JRadioButtonMenuItem(nombres[i], i == 0);
            float tam = puntos[i];
            opcion.addActionListener(e -> texto.setFont(texto.getFont().deriveFont(Font.PLAIN, tam)));
            tamanios.add(opcion);
            ver.add(opcion);
        }
        barra.add(archivo);
        barra.add(edicion);
        barra.add(ver);
        return barra;
    }

    private void marcar(boolean hayCambios) {
        cambios = hayCambios;
        guardar.setEnabled(cambios);
        if (ventana != null) {
            ventana.setTitle((cambios ? "* " : "") + "Notas del Palacio");
        }
    }
}
```

### Encargo R05-N05-E1 · El panel de control del kiosco

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Armá la ventana principal (MDI) del sistema de un kiosco: menú `Ventas` (Nueva venta,
Historial), `Stock` (Productos, Reponer) y `Sistema` (Salir), una barra de herramientas
con botones para las tareas más usadas y una barra de estado con la fecha fija
`29/09/2026` y el usuario `admin`. Cada opción abre su ventana interna (sin duplicados)
con un contenido de ejemplo; `Reponer` abre un diálogo modal que pide producto y
cantidad y la muestra en la barra de estado.

#### Criterio de aprobación

- MDI con menú, barra de herramientas y barra de estado.
- Ventanas internas sin duplicados y un diálogo modal.

#### Solución de referencia

```java
// Encargo - El panel de control del kiosco: MDI completo.
import java.awt.BorderLayout;
import java.awt.Dimension;
import java.beans.PropertyVetoException;
import java.util.HashMap;
import java.util.Map;
import javax.swing.JButton;
import javax.swing.JDesktopPane;
import javax.swing.JFrame;
import javax.swing.JInternalFrame;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JToolBar;
import javax.swing.SwingUtilities;

public class Kiosco {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Kiosco El Farol");
            PanelKiosco p = new PanelKiosco();
            f.setContentPane(p);
            f.setJMenuBar(p.menu());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.setSize(780, 520);
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

class PanelKiosco extends JPanel {
    private final JDesktopPane escritorio = new JDesktopPane();
    private final JLabel estado = new JLabel(" 29/09/2026 · usuario admin");
    private final Map<String, JInternalFrame> ventanas = new HashMap<>();

    PanelKiosco() {
        super(new BorderLayout());
        setPreferredSize(new Dimension(760, 460));
        JToolBar barra = new JToolBar();
        JButton venta = new JButton("Nueva venta");
        JButton productos = new JButton("Productos");
        barra.add(venta);
        barra.add(productos);
        venta.addActionListener(e -> abrir("Nueva venta"));
        productos.addActionListener(e -> abrir("Productos"));
        add(barra, BorderLayout.NORTH);
        add(escritorio, BorderLayout.CENTER);
        add(estado, BorderLayout.SOUTH);
    }

    JMenuBar menu() {
        JMenuBar mb = new JMenuBar();
        JMenu ventas = new JMenu("Ventas");
        ventas.add(opcion("Nueva venta"));
        ventas.add(opcion("Historial"));
        JMenu stock = new JMenu("Stock");
        stock.add(opcion("Productos"));
        JMenuItem reponer = new JMenuItem("Reponer…");
        reponer.addActionListener(e -> reponer());
        stock.add(reponer);
        JMenu sistema = new JMenu("Sistema");
        JMenuItem salir = new JMenuItem("Salir");
        salir.addActionListener(e -> System.exit(0));
        sistema.add(salir);
        mb.add(ventas);
        mb.add(stock);
        mb.add(sistema);
        return mb;
    }

    private JMenuItem opcion(String titulo) {
        JMenuItem i = new JMenuItem(titulo);
        i.addActionListener(e -> abrir(titulo));
        return i;
    }

    private void abrir(String titulo) {
        JInternalFrame v = ventanas.get(titulo);
        if (v == null || v.isClosed()) {
            v = new JInternalFrame(titulo, true, true, true, true);
            v.setContentPane(new JScrollPane(new JTable(new Object[][]{{"Alfajor", 900, 40}, {"Agua", 1100, 12}},
                    new String[]{"Producto", "Precio", "Stock"})));
            v.setSize(320, 150);
            v.setLocation(20 + ventanas.size() * 25, 20 + ventanas.size() * 25);
            escritorio.add(v);
            ventanas.put(titulo, v);
        }
        v.setVisible(true);
        try {
            v.setSelected(true);
        } catch (PropertyVetoException ignorada) {
            // sin foco
        }
    }

    private void reponer() {
        String producto = JOptionPane.showInputDialog(this, "Producto a reponer:");
        if (producto == null || producto.isBlank()) {
            return;
        }
        String cantidad = JOptionPane.showInputDialog(this, "Cantidad:");
        if (cantidad != null && cantidad.trim().matches("\\d+")) {
            estado.setText(" 29/09/2026 · usuario admin · se repusieron " + cantidad.trim() + " de " + producto.trim());
        }
    }
}
```

### Prueba del sello

#### ¿Con qué método se pone la barra de menú en un `JFrame`?

`setJMenuBar(barra)`.

#### ¿Qué diferencia hay entre `setMnemonic` y `setAccelerator`?

El mnemónico abre el menú con Alt + una letra; el acelerador ejecuta el ítem directamente con una combinación (como Ctrl+Q) sin abrir el menú.

#### ¿Qué es una aplicación MDI?

Una ventana principal con un escritorio (`JDesktopPane`) donde se abren ventanas internas (`JInternalFrame`).

#### ¿Cómo se evita abrir dos veces la misma ventana interna?

Guardándola en un atributo (o un mapa) y reutilizándola si no está cerrada.

#### ¿Qué hace un `JDialog` modal?

Bloquea la ventana principal hasta que el diálogo se cierra.

### Soluciones (docente)

Sale de `18-Java/37-MDI-Tablas-Arboles` (unidad 6), la parte de MDI y menús. El editor de la misión 3 tiene un constructor vacío solo para que el súper test pueda crear el panel sin ventana.

## R05-N06 · SwingWorker: la base sin congelar la ventana

```meta
tipo: tema
padre: R05-N05
precio: 10
criatura: troll
ejecutable: no
temas: conc.ui-hilo
usa: gui.swing, sql.desde-codigo
```

### Crónica

El registro de héroes del Palacio le pide a la Bóveda los datos de diez mil viajeros. Mientras tanto, la ventana se queda **congelada**: no se mueve, no responde, se pone gris. El escribiente cree que se colgó y la cierra a los golpes.

—El que atiende la ventana no puede ir a la Bóveda —dice {mentor}—: mientras baja y sube, nadie atiende. Mandá a un **mensajero** a buscar los datos y que el que atiende siga atendiendo. Cuando el mensajero vuelve, se muestran, {heroe}.

### Objetivos

- Entender por qué una tarea larga en el hilo de eventos congela la ventana.
- Hacer consultas a la base en segundo plano con `SwingWorker`.
- Mostrar el progreso y el resultado en la ventana de forma segura.
- Manejar los errores de una tarea en segundo plano.

### Antes de empezar

- MDI y menús.
- DAO y JDBC (rama 4).

### Explicación

#### El problema: un solo hilo atiende la ventana
Todos los eventos de Swing (clics, dibujar, escribir) los atiende **un solo hilo**, el
EDT. Si un listener hace algo que tarda (una consulta a la base, leer un archivo
grande, una conexión a internet), el EDT queda ocupado y la ventana no se redibuja ni
responde hasta que termina.

La regla tiene dos partes:
1. Lo que **tarda** va en **otro hilo**.
2. Lo que **toca la interfaz** va **solo en el EDT**.

#### `SwingWorker`
`SwingWorker` resuelve las dos partes a la vez:
```java
new SwingWorker<List<Heroe>, Void>() {
    @Override
    protected List<Heroe> doInBackground() throws Exception {
        return dao.listar();               // corre en OTRO hilo: acá va lo que tarda
    }

    @Override
    protected void done() {                // corre en el EDT cuando termina
        try {
            modelo.setDatos(get());        // get() devuelve el resultado (o lanza la excepción)
            estado.setText("Listo");
        } catch (Exception e) {
            estado.setText("Error: " + e.getCause().getMessage());
        }
    }
}.execute();
```
- Los dos tipos son: el **resultado** (`List<Heroe>`) y los **avances intermedios**
  (`Void` si no hay).
- **Nunca** toques componentes en `doInBackground`: no está en el EDT.
- `get()` en `done()` devuelve el resultado; si `doInBackground` lanzó una excepción,
  `get()` lanza una `ExecutionException` con la original como causa.

#### Progreso
Para informar el avance, se usan `setProgress(0..100)` o `publish(...)` desde
`doInBackground`, y se reciben en el EDT:
```java
@Override
protected Void doInBackground() throws Exception {
    for (int i = 0; i < total; i++) {
        procesar(i);
        setProgress(100 * (i + 1) / total);
    }
    return null;
}
…
worker.addPropertyChangeListener(e -> {
    if ("progress".equals(e.getPropertyName())) {
        barra.setValue((Integer) e.getNewValue());
    }
});
```

#### Mientras trabaja
Mientras la tarea corre, conviene deshabilitar el botón que la lanzó (para que no la
lancen diez veces) y mostrar un mensaje o una barra de progreso. En `done()` se vuelve a
habilitar.

### Código de ejemplo

Cargá primero las tablas con `psql … -f schema.sql`. La consulta simula una espera de
un segundo con `pg_sleep`, para que se note que la ventana no se congela.

`schema.sql`

```sql
DROP TABLE IF EXISTS viajero;
CREATE TABLE viajero (id SERIAL PRIMARY KEY, nombre VARCHAR(30) NOT NULL, ciudad VARCHAR(20));
INSERT INTO viajero (nombre, ciudad) VALUES ('Kira Valdez', 'Valle'), ('Bron Tallo', 'Forjas'), ('Lía Ferrari', 'Valle'), ('Nara Kel', 'Ciudadela');
```

```java
/*
 * SwingWorker: el mensajero que va a la Bóveda sin congelar la ventana.
 * Ejecutar con: java -cp postgresql-42.7.4.jar Mensajero.java
 */
import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutionException;
import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JProgressBar;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.SwingUtilities;
import javax.swing.SwingWorker;
import javax.swing.table.DefaultTableModel;

public class Mensajero {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Registro de viajeros");
            f.setContentPane(new PanelViajeros());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

record Viajero(String nombre, String ciudad) { }

class ViajeroDAO {
    List<Viajero> listar() throws SQLException {
        List<Viajero> lista = new ArrayList<>();
        try (Connection con = Conexion.abrir();
             PreparedStatement ps = con.prepareStatement("SELECT nombre, ciudad FROM viajero, pg_sleep(1) ORDER BY nombre");
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                lista.add(new Viajero(rs.getString(1), rs.getString(2)));
            }
        }
        return lista;
    }
}

class PanelViajeros extends JPanel {
    private final DefaultTableModel modelo = new DefaultTableModel(new String[]{"Nombre", "Ciudad"}, 0);
    private final JButton cargar = new JButton("Cargar de la Bóveda");
    private final JProgressBar ocupado = new JProgressBar();
    private final JLabel estado = new JLabel("Sin datos");
    private final ViajeroDAO dao = new ViajeroDAO();

    PanelViajeros() {
        super(new BorderLayout(6, 6));
        setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));
        JTable tabla = new JTable(modelo);
        tabla.setPreferredScrollableViewportSize(new java.awt.Dimension(340, 110));
        JPanel arriba = new JPanel(new FlowLayout(FlowLayout.LEFT));
        arriba.add(cargar);
        arriba.add(ocupado);
        add(arriba, BorderLayout.NORTH);
        add(new JScrollPane(tabla), BorderLayout.CENTER);
        add(estado, BorderLayout.SOUTH);
        cargar.addActionListener(e -> cargar());
    }

    private void cargar() {
        cargar.setEnabled(false);
        ocupado.setIndeterminate(true);
        estado.setText("Consultando la Bóveda… (la ventana sigue respondiendo)");
        new SwingWorker<List<Viajero>, Void>() {
            @Override
            protected List<Viajero> doInBackground() throws SQLException {
                return dao.listar();                        // otro hilo: la consulta que tarda
            }

            @Override
            protected void done() {                         // EDT: mostrar el resultado
                ocupado.setIndeterminate(false);
                cargar.setEnabled(true);
                try {
                    List<Viajero> viajeros = get();
                    modelo.setRowCount(0);
                    for (Viajero v : viajeros) {
                        modelo.addRow(new Object[]{v.nombre(), v.ciudad()});
                    }
                    estado.setText(viajeros.size() + " viajeros cargados");
                } catch (InterruptedException | ExecutionException ex) {
                    estado.setText("Error: " + ex.getCause().getMessage());
                }
            }
        }.execute();
    }
}

final class Conexion {
    static final String URL = "jdbc:postgresql://localhost:5432/imperio";
    static final String USUARIO = "imperio";
    static final String CLAVE = "imperio";

    static Connection abrir() throws SQLException {
        return DriverManager.getConnection(URL, USUARIO, CLAVE);
    }
}
```

### ¿Para qué sirve?

Cualquier aplicación que consulta una base, descarga algo o procesa archivos necesita hacerlo sin congelar la pantalla: un usuario que ve una ventana gris la cierra, y con razón. `SwingWorker` es la herramienta estándar de Swing para eso, y la idea (tarea larga en otro hilo, resultado en el hilo de la interfaz) es la misma en Android, JavaFX y la web.

### Errores habituales

**Troll: la consulta en el listener.** `boton.addActionListener(e -> tabla.setModel(dao.listar()))`
congela la ventana mientras la base responde. Va en un `SwingWorker`.

**Troll: tocar la interfaz desde `doInBackground`.** `modelo.addRow(…)` desde otro hilo
produce errores aleatorios y difíciles de reproducir. Actualizá la interfaz en `done()`
(o en `process()`).

**Ogro: el error que desaparece.** Si no llamás a `get()` en `done()`, la excepción de
`doInBackground` se pierde en silencio. Llamalo siempre, dentro de un `try`.

**Ogro: lanzar la tarea diez veces.** Deshabilitá el botón mientras trabaja.

**Slime: reutilizar un `SwingWorker`.** Cada `SwingWorker` se ejecuta **una sola vez**:
para repetir la tarea, creá uno nuevo.

### Misión R05-N06-M1 · El buscador que no se congela

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Hacé un buscador de productos con un campo de texto, un botón `Buscar` y una tabla. La
búsqueda (con `ILIKE` y `PreparedStatement` sobre la tabla de `schema.sql`, que incluye
un `pg_sleep` para simular demora) corre en un `SwingWorker`. Mientras busca: el botón
se deshabilita, la barra de progreso queda indeterminada y un cartel dice "Buscando…".
Si hay un error (por ejemplo, la base apagada), el cartel lo muestra en rojo.

`schema.sql`

```sql
DROP TABLE IF EXISTS producto;
CREATE TABLE producto (codigo VARCHAR(5) PRIMARY KEY, nombre VARCHAR(30) NOT NULL, precio NUMERIC(10, 2) NOT NULL);
INSERT INTO producto VALUES ('YER', 'Yerba 1 kg', 4200.5), ('AZU', 'Azúcar 1 kg', 1350), ('YOG', 'Yogur', 900), ('HAR', 'Harina 1 kg', 980);
```

#### Criterio de aprobación

- La consulta corre en `doInBackground` y la tabla se llena en `done()`.
- El botón se deshabilita mientras busca y el error se muestra.

#### Solución de referencia

`schema.sql`

```sql
DROP TABLE IF EXISTS producto;
CREATE TABLE producto (codigo VARCHAR(5) PRIMARY KEY, nombre VARCHAR(30) NOT NULL, precio NUMERIC(10, 2) NOT NULL);
INSERT INTO producto VALUES ('YER', 'Yerba 1 kg', 4200.5), ('AZU', 'Azúcar 1 kg', 1350), ('YOG', 'Yogur', 900), ('HAR', 'Harina 1 kg', 980);
```

```java
// Mision 1 - El buscador que no se congela: SwingWorker con PreparedStatement.
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.FlowLayout;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JProgressBar;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;
import javax.swing.SwingWorker;
import javax.swing.table.DefaultTableModel;

public class BuscadorProductos {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Buscador");
            f.setContentPane(new PanelBuscador());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

class PanelBuscador extends JPanel {
    private final JTextField texto = new JTextField(14);
    private final JButton buscar = new JButton("Buscar");
    private final JProgressBar barra = new JProgressBar();
    private final JLabel estado = new JLabel(" ");
    private final DefaultTableModel modelo = new DefaultTableModel(new String[]{"Código", "Nombre", "Precio"}, 0);

    PanelBuscador() {
        super(new BorderLayout(6, 6));
        setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));
        JPanel arriba = new JPanel(new FlowLayout(FlowLayout.LEFT));
        arriba.add(texto);
        arriba.add(buscar);
        arriba.add(barra);
        JTable tabla = new JTable(modelo);
        tabla.setPreferredScrollableViewportSize(new java.awt.Dimension(360, 110));
        add(arriba, BorderLayout.NORTH);
        add(new JScrollPane(tabla), BorderLayout.CENTER);
        add(estado, BorderLayout.SOUTH);
        buscar.addActionListener(e -> buscar());
        texto.addActionListener(e -> buscar());
    }

    private void buscar() {
        String filtro = texto.getText().trim();
        buscar.setEnabled(false);
        barra.setIndeterminate(true);
        estado.setForeground(Color.BLACK);
        estado.setText("Buscando…");
        new SwingWorker<List<Object[]>, Void>() {
            @Override
            protected List<Object[]> doInBackground() throws SQLException {
                List<Object[]> filas = new ArrayList<>();
                try (Connection con = Conexion.abrir();
                     PreparedStatement ps = con.prepareStatement("SELECT codigo, nombre, precio FROM producto, pg_sleep(1) WHERE nombre ILIKE ? ORDER BY nombre")) {
                    ps.setString(1, "%" + filtro + "%");
                    try (ResultSet rs = ps.executeQuery()) {
                        while (rs.next()) {
                            filas.add(new Object[]{rs.getString(1), rs.getString(2), rs.getBigDecimal(3)});
                        }
                    }
                }
                return filas;
            }

            @Override
            protected void done() {
                barra.setIndeterminate(false);
                buscar.setEnabled(true);
                try {
                    List<Object[]> filas = get();
                    modelo.setRowCount(0);
                    filas.forEach(modelo::addRow);
                    estado.setText(filas.size() + " resultados");
                } catch (Exception ex) {
                    estado.setForeground(Color.RED);
                    estado.setText("Error: " + (ex.getCause() != null ? ex.getCause().getMessage() : ex.getMessage()));
                }
            }
        }.execute();
    }
}

final class Conexion {
    static final String URL = "jdbc:postgresql://localhost:5432/imperio";
    static final String USUARIO = "imperio";
    static final String CLAVE = "imperio";

    static Connection abrir() throws SQLException {
        return DriverManager.getConnection(URL, USUARIO, CLAVE);
    }
}
```

### Misión R05-N06-M2 · La barra de la importación

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Hacé una ventana que "importa" 50 registros en segundo plano: un botón `Importar`, una
`JProgressBar` de 0 a 100 y un área de texto donde se van agregando las líneas
procesadas. El `SwingWorker<Integer, String>` procesa cada registro (simulá la demora con
`Thread.sleep(40)`), llama a `setProgress` y **publica** cada línea con `publish`, que se
muestra en `process()`. Al terminar, `done()` muestra cuántos se importaron. Un botón
`Cancelar` llama a `cancel(true)` y el área lo informa.

#### Criterio de aprobación

- Usa `setProgress` + `PropertyChangeListener` para la barra y `publish`/`process` para las líneas.
- Se puede cancelar y lo informa.

#### Solución de referencia

```java
// Mision 2 - La barra de la importacion: progreso, publish/process y cancelacion.
import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.util.List;
import java.util.concurrent.CancellationException;
import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JProgressBar;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.SwingUtilities;
import javax.swing.SwingWorker;

public class Importacion {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Importación");
            f.setContentPane(new PanelImportacion());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

class PanelImportacion extends JPanel {
    private final JProgressBar barra = new JProgressBar(0, 100);
    private final JTextArea registro = new JTextArea(8, 32);
    private final JButton importar = new JButton("Importar");
    private final JButton cancelar = new JButton("Cancelar");
    private SwingWorker<Integer, String> tarea;

    PanelImportacion() {
        super(new BorderLayout(6, 6));
        setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));
        barra.setStringPainted(true);
        registro.setEditable(false);
        cancelar.setEnabled(false);
        JPanel arriba = new JPanel(new FlowLayout(FlowLayout.LEFT));
        arriba.add(importar);
        arriba.add(cancelar);
        add(arriba, BorderLayout.NORTH);
        add(new JScrollPane(registro), BorderLayout.CENTER);
        add(barra, BorderLayout.SOUTH);
        importar.addActionListener(e -> iniciar());
        cancelar.addActionListener(e -> tarea.cancel(true));
    }

    private void iniciar() {
        registro.setText("");
        importar.setEnabled(false);
        cancelar.setEnabled(true);
        tarea = new SwingWorker<>() {
            @Override
            protected Integer doInBackground() throws Exception {
                int total = 50;
                for (int i = 1; i <= total; i++) {
                    Thread.sleep(40);
                    publish("Registro " + i + " importado");
                    setProgress(100 * i / total);
                }
                return total;
            }

            @Override
            protected void process(List<String> lineas) {
                for (String l : lineas) {
                    registro.append(l + "\n");
                }
            }

            @Override
            protected void done() {
                importar.setEnabled(true);
                cancelar.setEnabled(false);
                try {
                    registro.append("Listo: " + get() + " registros\n");
                } catch (CancellationException ex) {
                    registro.append("Importación cancelada\n");
                } catch (Exception ex) {
                    registro.append("Error: " + ex.getMessage() + "\n");
                }
            }
        };
        tarea.addPropertyChangeListener(e -> {
            if ("progress".equals(e.getPropertyName())) {
                barra.setValue((Integer) e.getNewValue());
            }
        });
        tarea.execute();
    }
}
```

### Misión R05-N06-M3 · El ABM que no se traba

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Hacé una ventana con la tabla de socios (de `schema.sql`), un formulario para dar de
alta (nombre y categoría en un combo) y un botón `Borrar` para la fila seleccionada.
**Todas** las operaciones con la base (listar, insertar, borrar) corren en
`SwingWorker`, a través de un `SocioDAO`. Después de cada alta o baja, la tabla se
recarga (también en segundo plano). Los errores de la base se muestran en un
`JOptionPane`.

`schema.sql`

```sql
DROP TABLE IF EXISTS socio;
CREATE TABLE socio (numero SERIAL PRIMARY KEY, nombre VARCHAR(40) NOT NULL, categoria VARCHAR(20) NOT NULL);
INSERT INTO socio (nombre, categoria) VALUES ('Marta Díaz', 'activo'), ('Juan Pérez', 'cadete');
```

#### Criterio de aprobación

- Ninguna consulta corre en el EDT.
- Las operaciones usan un DAO y recargan la tabla al terminar.

#### Solución de referencia

`schema.sql`

```sql
DROP TABLE IF EXISTS socio;
CREATE TABLE socio (numero SERIAL PRIMARY KEY, nombre VARCHAR(40) NOT NULL, categoria VARCHAR(20) NOT NULL);
INSERT INTO socio (nombre, categoria) VALUES ('Marta Díaz', 'activo'), ('Juan Pérez', 'cadete');
```

```java
// Mision 3 - El ABM que no se traba: DAO + SwingWorker para cada operacion.
import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;
import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;
import javax.swing.SwingWorker;
import javax.swing.table.DefaultTableModel;

public class AbmSocios {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Socios del club");
            f.setContentPane(new PanelSocios());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

record Socio(int numero, String nombre, String categoria) { }

class SocioDAO {
    List<Socio> listar() throws SQLException {
        List<Socio> lista = new ArrayList<>();
        try (Connection con = Conexion.abrir();
             PreparedStatement ps = con.prepareStatement("SELECT numero, nombre, categoria FROM socio ORDER BY numero");
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                lista.add(new Socio(rs.getInt(1), rs.getString(2), rs.getString(3)));
            }
        }
        return lista;
    }

    void insertar(String nombre, String categoria) throws SQLException {
        try (Connection con = Conexion.abrir();
             PreparedStatement ps = con.prepareStatement("INSERT INTO socio (nombre, categoria) VALUES (?, ?)")) {
            ps.setString(1, nombre);
            ps.setString(2, categoria);
            ps.executeUpdate();
        }
    }

    void borrar(int numero) throws SQLException {
        try (Connection con = Conexion.abrir();
             PreparedStatement ps = con.prepareStatement("DELETE FROM socio WHERE numero = ?")) {
            ps.setInt(1, numero);
            ps.executeUpdate();
        }
    }
}

class PanelSocios extends JPanel {
    private final SocioDAO dao = new SocioDAO();
    private final DefaultTableModel modelo = new DefaultTableModel(new String[]{"N°", "Nombre", "Categoría"}, 0);
    private final JTable tabla = new JTable(modelo);
    private final JTextField nombre = new JTextField(12);
    private final JComboBox<String> categoria = new JComboBox<>(new String[]{"activo", "cadete", "vitalicio"});
    private final JLabel estado = new JLabel(" ");

    PanelSocios() {
        super(new BorderLayout(6, 6));
        setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));
        tabla.setPreferredScrollableViewportSize(new java.awt.Dimension(360, 110));
        JPanel form = new JPanel(new FlowLayout(FlowLayout.LEFT));
        JButton alta = new JButton("Alta");
        JButton borrar = new JButton("Borrar");
        form.add(nombre);
        form.add(categoria);
        form.add(alta);
        form.add(borrar);
        add(new JScrollPane(tabla), BorderLayout.CENTER);
        JPanel abajo = new JPanel(new BorderLayout());
        abajo.add(form, BorderLayout.CENTER);
        abajo.add(estado, BorderLayout.SOUTH);
        add(abajo, BorderLayout.SOUTH);
        alta.addActionListener(e -> {
            String n = nombre.getText().trim();
            if (n.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Falta el nombre");
                return;
            }
            enSegundoPlano(() -> {
                dao.insertar(n, (String) categoria.getSelectedItem());
                return null;
            }, "Socio agregado");
            nombre.setText("");
        });
        borrar.addActionListener(e -> {
            int fila = tabla.getSelectedRow();
            if (fila < 0) {
                JOptionPane.showMessageDialog(this, "Elegí un socio");
                return;
            }
            int numero = (Integer) modelo.getValueAt(fila, 0);
            enSegundoPlano(() -> {
                dao.borrar(numero);
                return null;
            }, "Socio " + numero + " borrado");
        });
        recargar();
    }

    private void enSegundoPlano(Callable<Void> operacion, String mensaje) {
        estado.setText("Guardando…");
        new SwingWorker<Void, Void>() {
            @Override
            protected Void doInBackground() throws Exception {
                return operacion.call();
            }

            @Override
            protected void done() {
                try {
                    get();
                    estado.setText(mensaje);
                    recargar();
                } catch (Exception ex) {
                    JOptionPane.showMessageDialog(PanelSocios.this, "Error: " + ex.getCause().getMessage());
                }
            }
        }.execute();
    }

    private void recargar() {
        new SwingWorker<List<Socio>, Void>() {
            @Override
            protected List<Socio> doInBackground() throws SQLException {
                return dao.listar();
            }

            @Override
            protected void done() {
                try {
                    modelo.setRowCount(0);
                    for (Socio s : get()) {
                        modelo.addRow(new Object[]{s.numero(), s.nombre(), s.categoria()});
                    }
                } catch (Exception ex) {
                    estado.setText("Error al cargar: " + ex.getCause().getMessage());
                }
            }
        }.execute();
    }
}

final class Conexion {
    static final String URL = "jdbc:postgresql://localhost:5432/imperio";
    static final String USUARIO = "imperio";
    static final String CLAVE = "imperio";

    static Connection abrir() throws SQLException {
        return DriverManager.getConnection(URL, USUARIO, CLAVE);
    }
}
```

### Encargo R05-N06-E1 · El reporte que tarda

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un comercio genera un reporte de ventas que tarda. Hacé una ventana con un combo de mes
(1 a 12), un botón `Generar` y un área de texto. El reporte (simulado: recorre los 30
días del mes con `Thread.sleep(30)` y suma una venta calculada con `new Random(mes * 100
+ dia).nextInt(50_000)`) corre en un `SwingWorker<String, Integer>` que publica el día que
va procesando, y la ventana muestra "Procesando día N…" mientras tanto. Al final, el área
muestra el total del mes, el mejor día y el promedio diario.

#### Criterio de aprobación

- El cálculo corre en segundo plano y publica el avance.
- El resultado se muestra en `done()`.

#### Solución de referencia

```java
// Encargo - El reporte que tarda: SwingWorker con avance.
import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.util.List;
import java.util.Random;
import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.SwingUtilities;
import javax.swing.SwingWorker;

public class ReporteVentas {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Reporte de ventas");
            f.setContentPane(new PanelReporte());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

class PanelReporte extends JPanel {
    private final JComboBox<Integer> mes = new JComboBox<>();
    private final JButton generar = new JButton("Generar");
    private final JLabel estado = new JLabel(" ");
    private final JTextArea resultado = new JTextArea(6, 30);

    PanelReporte() {
        super(new BorderLayout(6, 6));
        setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));
        for (int m = 1; m <= 12; m++) {
            mes.addItem(m);
        }
        resultado.setEditable(false);
        JPanel arriba = new JPanel(new FlowLayout(FlowLayout.LEFT));
        arriba.add(new JLabel("Mes:"));
        arriba.add(mes);
        arriba.add(generar);
        arriba.add(estado);
        add(arriba, BorderLayout.NORTH);
        add(new JScrollPane(resultado), BorderLayout.CENTER);
        generar.addActionListener(e -> generar());
    }

    private void generar() {
        int m = (Integer) mes.getSelectedItem();
        generar.setEnabled(false);
        new SwingWorker<String, Integer>() {
            @Override
            protected String doInBackground() throws Exception {
                long total = 0;
                int mejorDia = 1;
                int mejorVenta = -1;
                for (int dia = 1; dia <= 30; dia++) {
                    Thread.sleep(30);
                    int venta = new Random(m * 100L + dia).nextInt(50_000);
                    total += venta;
                    if (venta > mejorVenta) {
                        mejorVenta = venta;
                        mejorDia = dia;
                    }
                    publish(dia);
                }
                return "Mes " + m + "\nTotal: " + total + "\nMejor día: " + mejorDia + " (" + mejorVenta + ")\nPromedio diario: " + total / 30;
            }

            @Override
            protected void process(List<Integer> dias) {
                estado.setText("Procesando día " + dias.get(dias.size() - 1) + "…");
            }

            @Override
            protected void done() {
                generar.setEnabled(true);
                try {
                    resultado.setText(get());
                    estado.setText("Listo");
                } catch (Exception ex) {
                    estado.setText("Error: " + ex.getMessage());
                }
            }
        }.execute();
    }
}
```

### Prueba del sello

#### ¿Por qué una consulta a la base dentro de un `ActionListener` congela la ventana?

Porque el listener corre en el hilo de eventos (EDT), que es el único que redibuja y atiende la ventana; mientras la consulta tarda, nadie la atiende.

#### ¿En qué hilo corre `doInBackground()` y en cuál `done()`?

`doInBackground()` en un hilo aparte; `done()` en el EDT.

#### ¿Por qué no se pueden tocar componentes desde `doInBackground()`?

Porque Swing no es seguro para varios hilos: solo el EDT puede modificar la interfaz.

#### ¿Qué pasa con una excepción lanzada en `doInBackground()`?

Se guarda; al llamar a `get()` en `done()` aparece como `ExecutionException`, con la original como causa.

#### ¿Para qué sirven `publish` y `process`?

Para mandar resultados parciales desde el hilo de fondo y mostrarlos en el EDT mientras la tarea sigue.

### Soluciones (docente)

Nodo nuevo, unidades 5 y 6. Corrige el problema que marcó la auditoría en el proyecto MDI original, que consultaba la base desde el hilo de la interfaz. El `pg_sleep(1)` en las consultas es para que en clase se note que la ventana sigue respondiendo; se puede quitar.

## R05-N07 · MVC al estilo de la cátedra

```meta
tipo: tema
padre: R05-N06
precio: 10
criatura: skeleton
ejecutable: no
temas: diseno.capas
usa: gui.swing, sql.desde-codigo
```

### Crónica

En la biblioteca del Palacio, {mentor} extiende sobre la mesa el plano de un sistema entero: cuatro salas separadas por paredes gruesas. En una viven los **datos** (los moldes), en otra los **mensajeros** que bajan a la Bóveda, en otra los **capataces** que deciden qué se hace, y en la última las **ventanas** que ve la gente.

—Cuando todo está mezclado —el SQL en el botón, la regla del negocio en la ventana— cada cambio rompe tres cosas —dice—. Separalo así, {heroe}, y vas a poder cambiar una ventana sin tocar la Bóveda. Y además, es exactamente como lo pide la cátedra.

### Objetivos

- Organizar una aplicación de escritorio en capas: modelo, acceso a datos, controlador y vista.
- Reconocer la estructura de paquetes de la cátedra (`DAO`, `Modelo`, `Controlador`, `visual`).
- Leer el código que genera el editor de formularios de NetBeans.
- Leer la configuración de la conexión desde un `.properties`.
- Evitar los errores típicos del estilo NetBeans.

### Antes de empezar

- SwingWorker y todo lo anterior de la rama.
- DAO y transacciones (rama 4).

### Explicación

#### MVC
**MVC** (Modelo-Vista-Controlador) separa una aplicación en tres responsabilidades:
| Parte | Qué hace | Qué **no** hace |
|---|---|---|
| **Modelo** | los datos y las reglas del dominio (`Aula`, `Alumno`) | no sabe que existen ventanas |
| **Vista** | muestra y captura lo que hace el usuario | no tiene SQL ni reglas del negocio |
| **Controlador** | recibe lo que hizo el usuario, valida, usa el acceso a datos y le dice a la vista qué mostrar | no dibuja |

A eso se suma la capa de **acceso a datos** (los DAO de la rama anterior), que en un
MVC prolijo es parte del modelo.

#### La estructura de la cátedra
El material de *Paradigmas y Lenguajes III* organiza los proyectos así:
```
DAO/          → ConexionBD: la clase que abre la conexión a PostgreSQL
Modelo/       → los POJO/beans: Aula, Profesor, Alumno (atributos, constructores, getters y setters)
Controlador/  → una clase por módulo con las validaciones y el SQL (AulaControlador…)
visual/       → las ventanas (JFrame / JInternalFrame) hechas con el editor de NetBeans
```
En este curso usamos los mismos nombres **en minúscula** (`dao`, `modelo`,
`controlador`, `visual`), que es la convención de Java para paquetes; en un examen,
usá los que pida la cátedra: el código es el mismo.

En el estilo de la cátedra, el **controlador tiene el SQL**. En un MVC estricto el SQL
va en un DAO y el controlador lo usa; las dos formas funcionan, y conviene conocer las
dos. En los ejemplos de este nodo el controlador valida y **delega** en un DAO.

#### La conexión, en un solo lugar
La cátedra usa una clase con un método estático:
```java
package dao;

public final class ConexionBD {
    public static Connection obtener() throws SQLException {
        Properties p = new Properties();
        try (BufferedReader r = Files.newBufferedReader(Path.of("db.properties"))) {
            p.load(r);
        } catch (IOException e) {
            throw new SQLException("no se pudo leer db.properties", e);
        }
        return DriverManager.getConnection(p.getProperty("url"), p.getProperty("usuario"), p.getProperty("clave"));
    }
}
```
Con `db.properties` junto al programa:
```
url=jdbc:postgresql://localhost:5432/imperio
usuario=imperio
clave=imperio
```
(El material de la cátedra escribe los datos en el código y agrega
`Class.forName("org.postgresql.Driver")`; desde Java 6 no hace falta: el driver se
registra solo si está en el classpath.)

#### El código que genera NetBeans
Con el editor visual de NetBeans (*GUI Builder*) se arrastran componentes y NetBeans
escribe el código. Una ventana generada se ve así:
```java
public class FrmAula extends javax.swing.JInternalFrame {

    public FrmAula() {
        initComponents();                   // arma la ventana: lo genera NetBeans
        // tu código de inicio va acá, después de initComponents()
    }

    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">
    private void initComponents() {
        jLabel1 = new javax.swing.JLabel();
        txtNumero = new javax.swing.JTextField();
        btnGuardar = new javax.swing.JButton();
        jLabel1.setText("Número:");
        btnGuardar.setText("Guardar");
        btnGuardar.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnGuardarActionPerformed(evt);
            }
        });
        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        // … decenas de líneas de GroupLayout …
        pack();
    }// </editor-fold>

    private void btnGuardarActionPerformed(java.awt.event.ActionEvent evt) {
        // TU código para el botón va acá
    }

    // Variables declaration - do not modify
    private javax.swing.JButton btnGuardar;
    private javax.swing.JLabel jLabel1;
    private javax.swing.JTextField txtNumero;
    // End of variables declaration
}
```
Cómo leerlo:
- `initComponents()` y la declaración de variables los escribe NetBeans: **no se editan
  a mano** (NetBeans los regenera y pisa los cambios). Se cambian desde el editor visual.
- Cada evento que agregás en el editor crea un método `nombreComponenteEvento(evt)`: ahí
  va tu código.
- Los listeners son **clases anónimas** (que ya conocés): hacen lo mismo que una lambda.
- El layout es `GroupLayout`, pensado para el editor, no para escribirlo a mano.
- Renombrá los componentes (`txtNumero`, `btnGuardar`) en lugar de dejar `jTextField1`.

#### Errores típicos del estilo NetBeans
El material de la cátedra tiene algunos errores que conviene no repetir:
1. **Los `?` que no coinciden**: un `INSERT … VALUES (?)` con `ps.setString(2, …)`. Contá
   los signos y numerá desde 1.
2. **La línea que carga la tabla, comentada**: se ejecuta la consulta pero nunca se hace
   `tabla.setModel(modelo)`.
3. **Componentes que no existen**: copiar código de un formulario a otro y usar
   `txtNombre` donde el formulario tiene otro nombre.
4. **La conexión duplicada**: una sola clase de conexión en el paquete de acceso a datos.
5. **El `rs.close()` que falta** o las conexiones que nunca se cierran: usá `try` con
   recursos.

### Código de ejemplo

Un ABM de aulas en cuatro paquetes (la regla de la cátedra: número y capacidad
distintos de cero, y el número no se repite). Cargá `schema.sql`, dejá `db.properties`
en la carpeta desde donde ejecutás, y compilá con el driver en el classpath.

`schema.sql`

```sql
DROP TABLE IF EXISTS aula;
CREATE TABLE aula (numero INTEGER PRIMARY KEY, capacidad INTEGER NOT NULL);
INSERT INTO aula VALUES (101, 40), (102, 25);
```

`db.properties`

```
url=jdbc:postgresql://localhost:5432/imperio
usuario=imperio
clave=imperio
```

`src/modelo/Aula.java`

```java
package modelo;

/** Bean de la cátedra: atributos privados, constructores, getters y setters. */
public class Aula {
    private int numero;
    private int capacidad;

    public Aula() {
    }

    public Aula(int numero, int capacidad) {
        this.numero = numero;
        this.capacidad = capacidad;
    }

    public int getNumero() {
        return numero;
    }

    public void setNumero(int numero) {
        this.numero = numero;
    }

    public int getCapacidad() {
        return capacidad;
    }

    public void setCapacidad(int capacidad) {
        this.capacidad = capacidad;
    }
}
```

`src/dao/ConexionBD.java`

```java
package dao;

import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.Properties;

/** La única clase de conexión del proyecto. Lee los datos de db.properties. */
public final class ConexionBD {
    private ConexionBD() {
    }

    public static Connection obtener() throws SQLException {
        Properties p = new Properties();
        try (BufferedReader r = Files.newBufferedReader(Path.of("db.properties"))) {
            p.load(r);
        } catch (IOException e) {
            throw new SQLException("no se pudo leer db.properties", e);
        }
        return DriverManager.getConnection(p.getProperty("url"), p.getProperty("usuario"), p.getProperty("clave"));
    }
}
```

`src/dao/AulaDAO.java`

```java
package dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import modelo.Aula;

public class AulaDAO {
    public List<Aula> listar() throws SQLException {
        List<Aula> lista = new ArrayList<>();
        try (Connection con = ConexionBD.obtener();
             PreparedStatement ps = con.prepareStatement("SELECT numero, capacidad FROM aula ORDER BY numero");
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                lista.add(new Aula(rs.getInt("numero"), rs.getInt("capacidad")));
            }
        }
        return lista;
    }

    public boolean existe(int numero) throws SQLException {
        try (Connection con = ConexionBD.obtener();
             PreparedStatement ps = con.prepareStatement("SELECT COUNT(*) FROM aula WHERE numero = ?")) {
            ps.setInt(1, numero);
            try (ResultSet rs = ps.executeQuery()) {
                rs.next();
                return rs.getInt(1) > 0;
            }
        }
    }

    public void insertar(Aula a) throws SQLException {
        try (Connection con = ConexionBD.obtener();
             PreparedStatement ps = con.prepareStatement("INSERT INTO aula (numero, capacidad) VALUES (?, ?)")) {
            ps.setInt(1, a.getNumero());
            ps.setInt(2, a.getCapacidad());
            ps.executeUpdate();
        }
    }
}
```

`src/controlador/AulaControlador.java`

```java
package controlador;

import dao.AulaDAO;
import java.sql.SQLException;
import java.util.List;
import modelo.Aula;

/** Las reglas del negocio viven acá, antes de tocar la base. */
public class AulaControlador {
    private final AulaDAO dao = new AulaDAO();

    public List<Aula> listar() throws SQLException {
        return dao.listar();
    }

    public void registrar(String textoNumero, String textoCapacidad) throws SQLException {
        int numero;
        int capacidad;
        try {
            numero = Integer.parseInt(textoNumero.trim());
            capacidad = Integer.parseInt(textoCapacidad.trim());
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException("número y capacidad tienen que ser enteros");
        }
        if (numero == 0 || capacidad == 0) {
            throw new IllegalArgumentException("número y capacidad no pueden ser 0");
        }
        if (dao.existe(numero)) {
            throw new IllegalArgumentException("ya existe el aula " + numero);
        }
        dao.insertar(new Aula(numero, capacidad));
    }
}
```

`src/visual/PanelAula.java`

```java
package visual;

import controlador.AulaControlador;
import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.sql.SQLException;
import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.table.DefaultTableModel;
import modelo.Aula;

/** La vista: muestra y captura. No tiene SQL ni reglas. */
public class PanelAula extends JPanel {
    private final AulaControlador controlador = new AulaControlador();
    private final DefaultTableModel modelo = new DefaultTableModel(new String[]{"Número", "Capacidad"}, 0);
    private final JTextField txtNumero = new JTextField(5);
    private final JTextField txtCapacidad = new JTextField(5);

    public PanelAula() {
        super(new BorderLayout(6, 6));
        setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));
        JTable tablaAula = new JTable(modelo);
        tablaAula.setPreferredScrollableViewportSize(new java.awt.Dimension(260, 100));
        JPanel form = new JPanel(new FlowLayout(FlowLayout.LEFT));
        JButton btnGuardar = new JButton("Guardar");
        form.add(new JLabel("Número:"));
        form.add(txtNumero);
        form.add(new JLabel("Capacidad:"));
        form.add(txtCapacidad);
        form.add(btnGuardar);
        add(new JScrollPane(tablaAula), BorderLayout.CENTER);
        add(form, BorderLayout.SOUTH);
        btnGuardar.addActionListener(e -> guardar());
        traerRegistros();
    }

    private void traerRegistros() {
        try {
            modelo.setRowCount(0);
            for (Aula a : controlador.listar()) {
                modelo.addRow(new Object[]{a.getNumero(), a.getCapacidad()});
            }
        } catch (SQLException e) {
            JOptionPane.showMessageDialog(this, "No se pudo leer la base: " + e.getMessage());
        }
    }

    private void guardar() {
        try {
            controlador.registrar(txtNumero.getText(), txtCapacidad.getText());
            traerRegistros();
            txtNumero.setText("");
            txtCapacidad.setText("");
            JOptionPane.showMessageDialog(this, "Registro exitoso");
        } catch (IllegalArgumentException e) {
            JOptionPane.showMessageDialog(this, e.getMessage(), "Revisá los datos", JOptionPane.WARNING_MESSAGE);
        } catch (SQLException e) {
            JOptionPane.showMessageDialog(this, "Error de base de datos: " + e.getMessage());
        }
    }
}
```

`src/visual/FrmPrincipal.java`

```java
package visual;

import java.awt.Dimension;
import javax.swing.JDesktopPane;
import javax.swing.JFrame;
import javax.swing.JInternalFrame;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.SwingUtilities;

/** Ventana principal MDI con el menú de módulos. */
public class FrmPrincipal extends JFrame {
    private final JDesktopPane mdi = new JDesktopPane();

    public FrmPrincipal() {
        super("Sistema de Aulas");
        setContentPane(mdi);
        mdi.setPreferredSize(new Dimension(640, 420));
        JMenuBar barra = new JMenuBar();
        JMenu modulos = new JMenu("Módulos");
        JMenuItem miAulas = new JMenuItem("Aulas");
        miAulas.addActionListener(e -> abrirAulas());
        modulos.add(miAulas);
        barra.add(modulos);
        setJMenuBar(barra);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        pack();
        setLocationRelativeTo(null);
    }

    private void abrirAulas() {
        JInternalFrame form = new JInternalFrame("Aulas", true, true, true, true);
        form.setContentPane(new PanelAula());
        form.pack();
        form.setVisible(true);
        mdi.add(form);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new FrmPrincipal().setVisible(true));
    }
}
```

Para compilar y ejecutar (desde la carpeta del proyecto):
```bash
javac -cp postgresql-42.7.4.jar -d out $(find src -name "*.java")
java -cp "out:postgresql-42.7.4.jar" visual.FrmPrincipal
```

### ¿Para qué sirve?

Esta es la forma en que se organizan los sistemas de escritorio profesionales y la que la cátedra evalúa en el caso práctico del final. La separación en capas permite cambiar la base de datos, rediseñar una ventana o agregar una validación tocando **un solo lugar**, y permite probar el controlador sin abrir ninguna ventana.

### Errores habituales

**Dragón: el SQL en el botón.** `btnGuardarActionPerformed` con `DriverManager`,
`PreparedStatement` y la regla del negocio adentro: cualquier cambio obliga a tocar la
ventana. El botón solo llama al controlador.

**Esqueleto: `db.properties` que no se encuentra.** `NoSuchFileException: db.properties`:
se busca en la carpeta desde donde ejecutás el programa (en NetBeans, la carpeta del
proyecto).

**Ogro: editar `initComponents()` a mano.** NetBeans lo regenera y borra los cambios.
Tu código va en el constructor (después de `initComponents()`) o en los métodos de
eventos.

**Slime: los `?` y los `setX` que no coinciden.** `The column index is out of range: 2,
number of columns: 1`.

**Ogro: la tabla que no se llena.** Revisá que `tabla.setModel(modelo)` no esté
comentado y que el modelo sea el mismo al que le agregás filas.

### Misión R05-N07-M1 · El ABM de profesores

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Siguiendo la estructura del ejemplo (cuatro paquetes), hacé el ABM de **profesores**:
`modelo.Profesor` (id, apellido y nombre, email), `dao.ProfesorDAO` (listar, insertar
con id generado, eliminar), `controlador.ProfesorControlador` (el apellido y nombre no
puede estar vacío ni pasar de 50 caracteres, y el email tiene que tener `@`) y
`visual.PanelProfesor` con la tabla, el formulario y los botones `Guardar` y `Eliminar`
(con confirmación). La conexión sale de `db.properties`. Entregá un zip con `src/`,
`schema.sql` y `db.properties`.

#### Criterio de aprobación

- Cuatro paquetes con las responsabilidades separadas: la vista no tiene SQL ni validaciones.
- Las validaciones están en el controlador y se muestran en la vista.
- La conexión se lee de `db.properties`.

#### Solución de referencia

`schema.sql`

```sql
DROP TABLE IF EXISTS profesor;
CREATE TABLE profesor (id SERIAL PRIMARY KEY, apellido_nombre VARCHAR(50) NOT NULL, email VARCHAR(60) NOT NULL);
INSERT INTO profesor (apellido_nombre, email) VALUES ('Kaffa, Arquitecta', 'kaffa@imperio.edu');
```

`db.properties`

```
url=jdbc:postgresql://localhost:5432/imperio
usuario=imperio
clave=imperio
```

`src/modelo/Profesor.java`

```java
package modelo;

public class Profesor {
    private int id;
    private String apellidoNombre;
    private String email;

    public Profesor() {
    }

    public Profesor(int id, String apellidoNombre, String email) {
        this.id = id;
        this.apellidoNombre = apellidoNombre;
        this.email = email;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getApellidoNombre() {
        return apellidoNombre;
    }

    public void setApellidoNombre(String apellidoNombre) {
        this.apellidoNombre = apellidoNombre;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }
}
```

`src/dao/ConexionBD.java`

```java
package dao;

import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.Properties;

public final class ConexionBD {
    private ConexionBD() {
    }

    public static Connection obtener() throws SQLException {
        Properties p = new Properties();
        try (BufferedReader r = Files.newBufferedReader(Path.of("db.properties"))) {
            p.load(r);
        } catch (IOException e) {
            throw new SQLException("no se pudo leer db.properties", e);
        }
        return DriverManager.getConnection(p.getProperty("url"), p.getProperty("usuario"), p.getProperty("clave"));
    }
}
```

`src/dao/ProfesorDAO.java`

```java
package dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;
import modelo.Profesor;

public class ProfesorDAO {
    public List<Profesor> listar() throws SQLException {
        List<Profesor> lista = new ArrayList<>();
        try (Connection con = ConexionBD.obtener();
             PreparedStatement ps = con.prepareStatement("SELECT id, apellido_nombre, email FROM profesor ORDER BY apellido_nombre");
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                lista.add(new Profesor(rs.getInt(1), rs.getString(2), rs.getString(3)));
            }
        }
        return lista;
    }

    public void insertar(Profesor p) throws SQLException {
        try (Connection con = ConexionBD.obtener();
             PreparedStatement ps = con.prepareStatement("INSERT INTO profesor (apellido_nombre, email) VALUES (?, ?)", Statement.RETURN_GENERATED_KEYS)) {
            ps.setString(1, p.getApellidoNombre());
            ps.setString(2, p.getEmail());
            ps.executeUpdate();
            try (ResultSet k = ps.getGeneratedKeys()) {
                k.next();
                p.setId(k.getInt(1));
            }
        }
    }

    public void eliminar(int id) throws SQLException {
        try (Connection con = ConexionBD.obtener();
             PreparedStatement ps = con.prepareStatement("DELETE FROM profesor WHERE id = ?")) {
            ps.setInt(1, id);
            ps.executeUpdate();
        }
    }
}
```

`src/controlador/ProfesorControlador.java`

```java
package controlador;

import dao.ProfesorDAO;
import java.sql.SQLException;
import java.util.List;
import modelo.Profesor;

public class ProfesorControlador {
    private final ProfesorDAO dao = new ProfesorDAO();

    public List<Profesor> listar() throws SQLException {
        return dao.listar();
    }

    public void registrar(String apellidoNombre, String email) throws SQLException {
        String an = apellidoNombre.trim();
        if (an.isEmpty() || an.length() > 50) {
            throw new IllegalArgumentException("el apellido y nombre es obligatorio (hasta 50 caracteres)");
        }
        if (!email.contains("@")) {
            throw new IllegalArgumentException("el email no es válido");
        }
        dao.insertar(new Profesor(0, an, email.trim()));
    }

    public void eliminar(int id) throws SQLException {
        dao.eliminar(id);
    }
}
```

`src/visual/PanelProfesor.java`

```java
package visual;

import controlador.ProfesorControlador;
import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;
import javax.swing.table.DefaultTableModel;
import modelo.Profesor;

public class PanelProfesor extends JPanel {
    private final ProfesorControlador controlador = new ProfesorControlador();
    private final DefaultTableModel modelo = new DefaultTableModel(new String[]{"Apellido y nombre", "Email"}, 0);
    private final JTable tabla = new JTable(modelo);
    private final List<Integer> idsOcultos = new ArrayList<>();
    private final JTextField txtNombre = new JTextField(14);
    private final JTextField txtEmail = new JTextField(14);

    public PanelProfesor() {
        super(new BorderLayout(6, 6));
        setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));
        tabla.setPreferredScrollableViewportSize(new java.awt.Dimension(380, 110));
        JPanel form = new JPanel(new FlowLayout(FlowLayout.LEFT));
        JButton btnGuardar = new JButton("Guardar");
        JButton btnEliminar = new JButton("Eliminar");
        form.add(new JLabel("Apellido y nombre:"));
        form.add(txtNombre);
        form.add(new JLabel("Email:"));
        form.add(txtEmail);
        form.add(btnGuardar);
        form.add(btnEliminar);
        add(new JScrollPane(tabla), BorderLayout.CENTER);
        add(form, BorderLayout.SOUTH);
        btnGuardar.addActionListener(e -> guardar());
        btnEliminar.addActionListener(e -> eliminar());
        traerRegistros();
    }

    private void traerRegistros() {
        try {
            modelo.setRowCount(0);
            idsOcultos.clear();
            for (Profesor p : controlador.listar()) {
                modelo.addRow(new Object[]{p.getApellidoNombre(), p.getEmail()});
                idsOcultos.add(p.getId());
            }
        } catch (SQLException e) {
            JOptionPane.showMessageDialog(this, "Error de base de datos: " + e.getMessage());
        }
    }

    private void guardar() {
        try {
            controlador.registrar(txtNombre.getText(), txtEmail.getText());
            txtNombre.setText("");
            txtEmail.setText("");
            traerRegistros();
        } catch (IllegalArgumentException e) {
            JOptionPane.showMessageDialog(this, e.getMessage());
        } catch (SQLException e) {
            JOptionPane.showMessageDialog(this, "Error de base de datos: " + e.getMessage());
        }
    }

    private void eliminar() {
        int fila = tabla.getSelectedRow();
        if (fila < 0) {
            JOptionPane.showMessageDialog(this, "Elegí un profesor");
            return;
        }
        if (JOptionPane.showConfirmDialog(this, "¿Eliminar a " + modelo.getValueAt(fila, 0) + "?") == JOptionPane.YES_OPTION) {
            try {
                controlador.eliminar(idsOcultos.get(fila));
                traerRegistros();
            } catch (SQLException e) {
                JOptionPane.showMessageDialog(this, "Error de base de datos: " + e.getMessage());
            }
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Profesores");
            f.setContentPane(new PanelProfesor());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setVisible(true);
        });
    }
}
```

### Misión R05-N07-M2 · El controlador probado

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 4
xp: 10
```

#### Consigna

Una ventaja de MVC es poder **probar el controlador sin ventanas ni base**. Para eso,
el controlador no crea su DAO: lo **recibe** en el constructor, a través de una
interfaz. Escribí `AulaRepositorio` (una interfaz con `existe(int)`, `insertar(Aula)` y
`listar()`), un `AulaControlador` que la recibe, y un repositorio **en memoria** para las
pruebas. Después, `AulaControladorTest` con JUnit: registra bien, rechaza número 0,
rechaza capacidad 0, rechaza texto no numérico y rechaza un número repetido.

#### Criterio de aprobación

- El controlador recibe el repositorio por constructor (inyección de dependencias).
- Las pruebas usan el repositorio en memoria y pasan todas.

#### Solución de referencia

`Aula.java`

```java
public record Aula(int numero, int capacidad) { }
```

`AulaRepositorio.java`

```java
import java.util.List;

public interface AulaRepositorio {
    boolean existe(int numero) throws Exception;

    void insertar(Aula aula) throws Exception;

    List<Aula> listar() throws Exception;
}
```

`RepositorioEnMemoria.java`

```java
import java.util.ArrayList;
import java.util.List;

public class RepositorioEnMemoria implements AulaRepositorio {
    private final List<Aula> aulas = new ArrayList<>();

    @Override
    public boolean existe(int numero) {
        return aulas.stream().anyMatch(a -> a.numero() == numero);
    }

    @Override
    public void insertar(Aula aula) {
        aulas.add(aula);
    }

    @Override
    public List<Aula> listar() {
        return List.copyOf(aulas);
    }
}
```

`AulaControlador.java`

```java
public class AulaControlador {
    private final AulaRepositorio repositorio;

    public AulaControlador(AulaRepositorio repositorio) {
        this.repositorio = repositorio;
    }

    public void registrar(String textoNumero, String textoCapacidad) throws Exception {
        int numero;
        int capacidad;
        try {
            numero = Integer.parseInt(textoNumero.trim());
            capacidad = Integer.parseInt(textoCapacidad.trim());
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException("número y capacidad tienen que ser enteros");
        }
        if (numero == 0 || capacidad == 0) {
            throw new IllegalArgumentException("número y capacidad no pueden ser 0");
        }
        if (repositorio.existe(numero)) {
            throw new IllegalArgumentException("ya existe el aula " + numero);
        }
        repositorio.insertar(new Aula(numero, capacidad));
    }
}
```

`AulaControladorTest.java`

```java
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class AulaControladorTest {
    private RepositorioEnMemoria repo;
    private AulaControlador controlador;

    @BeforeEach
    void preparar() {
        repo = new RepositorioEnMemoria();
        controlador = new AulaControlador(repo);
    }

    @Test
    void registraUnAulaValida() throws Exception {
        controlador.registrar("101", " 40 ");
        assertEquals(List.of(new Aula(101, 40)), repo.listar());
    }

    @Test
    void rechazaElNumeroCero() {
        assertThrows(IllegalArgumentException.class, () -> controlador.registrar("0", "40"));
    }

    @Test
    void rechazaLaCapacidadCero() {
        assertThrows(IllegalArgumentException.class, () -> controlador.registrar("101", "0"));
    }

    @Test
    void rechazaTextoNoNumerico() {
        assertThrows(IllegalArgumentException.class, () -> controlador.registrar("ciento uno", "40"));
    }

    @Test
    void rechazaUnNumeroRepetido() throws Exception {
        controlador.registrar("101", "40");
        IllegalArgumentException e = assertThrows(IllegalArgumentException.class, () -> controlador.registrar("101", "25"));
        assertEquals("ya existe el aula 101", e.getMessage());
    }
}
```

### Misión R05-N07-M3 · Los errores del formulario

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Este panel, copiado de un formulario de NetBeans, tiene los **cuatro errores típicos**
del estilo: un `?` que no coincide con los `setX`, la línea que carga el modelo en la
tabla comentada, un componente que se usa con otro nombre y un `ResultSet` que nunca se
cierra. Corregilo (dejá un comentario en cada corrección) para que compile y funcione
con la tabla `genero` de `schema.sql`.

```java
public class PanelGenero extends JPanel {
    private final DefaultTableModel modelo = new DefaultTableModel(new String[]{"Id", "Género"}, 0);
    private final JTable tablaGenero = new JTable();
    private final JTextField txtGenero = new JTextField(12);

    public PanelGenero() {
        JButton btnGuardar = new JButton("Guardar");
        add(new JScrollPane(tablaGenero));
        add(txtGenero);
        add(btnGuardar);
        btnGuardar.addActionListener(e -> insertarGenero());
        traerRegistros();
    }

    void traerRegistros() {
        try (Connection con = Conexion.abrir()) {
            PreparedStatement ps = con.prepareStatement("SELECT id, nombre FROM genero ORDER BY id");
            ResultSet rs = ps.executeQuery();
            modelo.setRowCount(0);
            while (rs.next()) {
                modelo.addRow(new Object[]{rs.getInt(1), rs.getString(2)});
            }
            // tablaGenero.setModel(modelo);
        } catch (SQLException e) {
            JOptionPane.showMessageDialog(this, e.getMessage());
        }
    }

    void insertarGenero() {
        try (Connection con = Conexion.abrir();
             PreparedStatement ps = con.prepareStatement("INSERT INTO genero (nombre) VALUES (?)")) {
            ps.setString(2, txtNombre.getText());
            ps.execute();
            traerRegistros();
        } catch (SQLException e) {
            JOptionPane.showMessageDialog(this, e.getMessage());
        }
    }
}
```

`schema.sql`

```sql
DROP TABLE IF EXISTS genero;
CREATE TABLE genero (id SERIAL PRIMARY KEY, nombre VARCHAR(30) NOT NULL);
INSERT INTO genero (nombre) VALUES ('aventura'), ('misterio');
```

#### Criterio de aprobación

- Los cuatro errores están corregidos y comentados.
- El panel compila, carga la tabla y permite agregar géneros.

#### Solución de referencia

`schema.sql`

```sql
DROP TABLE IF EXISTS genero;
CREATE TABLE genero (id SERIAL PRIMARY KEY, nombre VARCHAR(30) NOT NULL);
INSERT INTO genero (nombre) VALUES ('aventura'), ('misterio');
```

```java
// Mision 3 - Los errores del formulario: los cuatro errores tipicos del estilo NetBeans.
import java.awt.FlowLayout;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;
import javax.swing.table.DefaultTableModel;

public class Generos {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Géneros");
            f.setContentPane(new PanelGenero());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setVisible(true);
        });
    }
}

class PanelGenero extends JPanel {
    private final DefaultTableModel modelo = new DefaultTableModel(new String[]{"Id", "Género"}, 0);
    private final JTable tablaGenero = new JTable();
    private final JTextField txtGenero = new JTextField(12);

    public PanelGenero() {
        super(new FlowLayout(FlowLayout.LEFT));
        JButton btnGuardar = new JButton("Guardar");
        tablaGenero.setPreferredScrollableViewportSize(new java.awt.Dimension(220, 90));
        add(new JScrollPane(tablaGenero));
        add(txtGenero);
        add(btnGuardar);
        btnGuardar.addActionListener(e -> insertarGenero());
        tablaGenero.setModel(modelo);          // Error 2: esta línea estaba comentada y la tabla nunca mostraba nada
        traerRegistros();
    }

    void traerRegistros() {
        // Error 4: el PreparedStatement y el ResultSet no se cerraban: ahora van en el try con recursos
        try (Connection con = Conexion.abrir();
             PreparedStatement ps = con.prepareStatement("SELECT id, nombre FROM genero ORDER BY id");
             ResultSet rs = ps.executeQuery()) {
            modelo.setRowCount(0);
            while (rs.next()) {
                modelo.addRow(new Object[]{rs.getInt(1), rs.getString(2)});
            }
        } catch (SQLException e) {
            JOptionPane.showMessageDialog(this, e.getMessage());
        }
    }

    void insertarGenero() {
        try (Connection con = Conexion.abrir();
             PreparedStatement ps = con.prepareStatement("INSERT INTO genero (nombre) VALUES (?)")) {
            // Error 1: había un solo ? y se usaba setString(2, ...): los indices empiezan en 1
            // Error 3: el campo se llama txtGenero, no txtNombre (copiado de otro formulario)
            ps.setString(1, txtGenero.getText().trim());
            ps.execute();
            txtGenero.setText("");
            traerRegistros();
        } catch (SQLException e) {
            JOptionPane.showMessageDialog(this, e.getMessage());
        }
    }
}

final class Conexion {
    static final String URL = "jdbc:postgresql://localhost:5432/imperio";
    static final String USUARIO = "imperio";
    static final String CLAVE = "imperio";

    static Connection abrir() throws SQLException {
        return DriverManager.getConnection(URL, USUARIO, CLAVE);
    }
}
```

### Encargo R05-N07-E1 · El login con la base

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 1
xp: 15
```

#### Consigna

Agregale al sistema de aulas del ejemplo una **ventana de ingreso** (como la del caso de
la cátedra): `modelo.Usuario`, `dao.UsuarioDAO` (buscar por usuario),
`controlador.UsuarioControlador` (valida usuario y clave contra la base; tres intentos
fallidos cierran la aplicación) y `visual.PanelLogin`. Si el ingreso es correcto, se
cierra el login y se abre `FrmPrincipal`. Las claves se guardan como texto en este
ejercicio (en un sistema real, con un *hash*).

#### Criterio de aprobación

- El login respeta las capas: la vista no consulta la base.
- Tres intentos fallidos terminan la aplicación.

#### Solución de referencia

`schema.sql`

```sql
DROP TABLE IF EXISTS usuario;
CREATE TABLE usuario (usuario VARCHAR(20) PRIMARY KEY, clave VARCHAR(30) NOT NULL, nombre VARCHAR(40) NOT NULL);
INSERT INTO usuario VALUES ('kaffa', 'cafe123', 'Kaffa');
```

`db.properties`

```
url=jdbc:postgresql://localhost:5432/imperio
usuario=imperio
clave=imperio
```

`src/modelo/Usuario.java`

```java
package modelo;

public class Usuario {
    private String usuario;
    private String clave;
    private String nombre;

    public Usuario() {
    }

    public Usuario(String usuario, String clave, String nombre) {
        this.usuario = usuario;
        this.clave = clave;
        this.nombre = nombre;
    }

    public String getUsuario() {
        return usuario;
    }

    public String getClave() {
        return clave;
    }

    public String getNombre() {
        return nombre;
    }
}
```

`src/dao/ConexionBD.java`

```java
package dao;

import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.Properties;

public final class ConexionBD {
    private ConexionBD() {
    }

    public static Connection obtener() throws SQLException {
        Properties p = new Properties();
        try (BufferedReader r = Files.newBufferedReader(Path.of("db.properties"))) {
            p.load(r);
        } catch (IOException e) {
            throw new SQLException("no se pudo leer db.properties", e);
        }
        return DriverManager.getConnection(p.getProperty("url"), p.getProperty("usuario"), p.getProperty("clave"));
    }
}
```

`src/dao/UsuarioDAO.java`

```java
package dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import modelo.Usuario;

public class UsuarioDAO {
    /** Devuelve el usuario o null si no existe (el controlador decide qué hacer). */
    public Usuario buscar(String usuario) throws SQLException {
        try (Connection con = ConexionBD.obtener();
             PreparedStatement ps = con.prepareStatement("SELECT usuario, clave, nombre FROM usuario WHERE usuario = ?")) {
            ps.setString(1, usuario);
            try (ResultSet rs = ps.executeQuery()) {
                return rs.next() ? new Usuario(rs.getString(1), rs.getString(2), rs.getString(3)) : null;
            }
        }
    }
}
```

`src/controlador/UsuarioControlador.java`

```java
package controlador;

import dao.UsuarioDAO;
import java.sql.SQLException;
import java.util.Arrays;
import modelo.Usuario;

public class UsuarioControlador {
    public static final int MAX_INTENTOS = 3;
    private final UsuarioDAO dao = new UsuarioDAO();
    private int fallidos = 0;

    /** Devuelve el usuario si la clave es correcta; si no, lanza una excepción con el motivo. */
    public Usuario ingresar(String usuario, char[] clave) throws SQLException {
        Usuario u = dao.buscar(usuario.trim());
        boolean ok = u != null && Arrays.equals(u.getClave().toCharArray(), clave);
        Arrays.fill(clave, '\0');
        if (!ok) {
            fallidos++;
            throw new IllegalArgumentException("usuario o clave incorrectos (" + (MAX_INTENTOS - fallidos) + " intentos restantes)");
        }
        fallidos = 0;
        return u;
    }

    public boolean agotoIntentos() {
        return fallidos >= MAX_INTENTOS;
    }
}
```

`src/visual/PanelLogin.java`

```java
package visual;

import controlador.UsuarioControlador;
import java.awt.GridLayout;
import java.sql.SQLException;
import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JPasswordField;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;
import modelo.Usuario;

public class PanelLogin extends JPanel {
    private final UsuarioControlador controlador = new UsuarioControlador();
    private final JTextField txtUsuario = new JTextField(12);
    private final JPasswordField txtClave = new JPasswordField(12);

    public PanelLogin() {
        super(new GridLayout(3, 2, 6, 6));
        setBorder(BorderFactory.createEmptyBorder(12, 12, 12, 12));
        JButton btnIngresar = new JButton("Ingresar");
        add(new JLabel("Usuario:"));
        add(txtUsuario);
        add(new JLabel("Clave:"));
        add(txtClave);
        add(new JLabel());
        add(btnIngresar);
        btnIngresar.addActionListener(e -> ingresar());
        txtClave.addActionListener(e -> ingresar());
    }

    private void ingresar() {
        try {
            Usuario u = controlador.ingresar(txtUsuario.getText(), txtClave.getPassword());
            JOptionPane.showMessageDialog(this, "Hola, " + u.getNombre());
            SwingUtilities.getWindowAncestor(this).dispose();
            new FrmPrincipal().setVisible(true);
        } catch (IllegalArgumentException e) {
            txtClave.setText("");
            JOptionPane.showMessageDialog(this, e.getMessage());
            if (controlador.agotoIntentos()) {
                System.exit(0);
            }
        } catch (SQLException e) {
            JOptionPane.showMessageDialog(this, "Error de base de datos: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Ingreso");
            f.setContentPane(new PanelLogin());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}
```

`src/visual/FrmPrincipal.java`

```java
package visual;

import java.awt.Dimension;
import javax.swing.JDesktopPane;
import javax.swing.JFrame;
import javax.swing.JMenu;
import javax.swing.JMenuBar;

public class FrmPrincipal extends JFrame {
    public FrmPrincipal() {
        super("Sistema de Aulas");
        JDesktopPane mdi = new JDesktopPane();
        mdi.setPreferredSize(new Dimension(640, 420));
        setContentPane(mdi);
        JMenuBar barra = new JMenuBar();
        barra.add(new JMenu("Módulos"));
        setJMenuBar(barra);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        pack();
        setLocationRelativeTo(null);
    }
}
```

### Prueba del sello

#### ¿Qué hace cada parte de MVC?

El modelo guarda los datos y las reglas del dominio; la vista muestra y captura lo que hace el usuario; el controlador recibe las acciones, valida, usa el acceso a datos y decide qué mostrar.

#### ¿Qué paquetes usa la cátedra y qué va en cada uno?

`DAO` (la conexión), `Modelo` (los beans), `Controlador` (validaciones y SQL de cada módulo) y `visual` (las ventanas de NetBeans).

#### ¿Por qué no se edita `initComponents()` a mano?

Porque lo genera NetBeans desde el editor visual y lo vuelve a escribir, borrando los cambios.

#### ¿Qué ventaja tiene que el controlador reciba el repositorio por constructor?

Que se puede probar con un repositorio en memoria, sin base de datos ni ventanas.

#### ¿Dónde conviene guardar los datos de la conexión?

En un archivo de configuración (`db.properties`), leído por una sola clase de conexión.

### Soluciones (docente)

Nodo nuevo (el 38 del índice de `18-Java` estaba por crear), unidades 5 y 6. Sigue la estructura de paquetes del material de la cátedra (`Extra/curso-final-paradigmas3-v2.md`, bloque A) con los nombres en minúscula, y corrige en la misión 3 los cuatro errores que la guía encontró en ese material. El súper test compila los proyectos, corre las pruebas de la misión 2 y crea cada panel sin pantalla.

## R05-N08 · Jefe final: el Dragón del Imperio

```meta
tipo: jefe
padre: R05-N07
precio: 10
criatura: dragon
insignia: Sello del Dragón
insignia_descripcion: Venciste al Dragón del Imperio: construiste un sistema de escritorio completo, de la base a las ventanas.
usa: diseno.capas, gui.swing, sql.desde-codigo
```

### Crónica

El Tribunal Imperial se reúne en la cima del Palacio. Sobre la mesa, un solo pergamino: *Registración de Actas de Examen*. Es el examen que el Imperio le toma a cada arquitecto antes de darle su sello. Detrás de los jueces, enroscado alrededor de la torre, duerme el **Dragón del Imperio**, hecho de todas las piezas que aprendiste: clases, colecciones, SQL, transacciones y ventanas.

—No hay truco nuevo —dice {mentor}, apoyándote una mano en el hombro—. Todo lo que necesitás ya lo sabés. Diseñá la base, escribí los modelos, poné las reglas en los controladores, guardá cada acta en una transacción y armá las ventanas. Pieza por pieza, {heroe}. Así cae un dragón.

### Objetivos

- Resolver un caso completo al estilo del final de la cátedra: modelo, base de datos, acceso a datos, controladores y vistas.
- Modelar con herencia (`ActaDeExamen` extiende `Formulario`) y composición (el acta tiene profesores y registros).
- Guardar una entidad compuesta en varias tablas dentro de una transacción.
- Construir las ventanas del caso: ingreso, principal MDI, ABM y el formulario del acta.

### Antes de empezar

- Todo el curso, en especial DAO y transacciones (rama 4) y MVC al estilo de la cátedra.

### Explicación

#### El caso: Registración de Actas de Examen
Una facultad registra las **actas de examen**. Cada acta tiene una fecha, la carrera, la
materia, el **aula** donde se toma, uno o más **profesores** (el tribunal) y los
**registros**: cada alumno inscripto con su nota (de 1 a 10) o **ausente**. Además, se
guarda quién cargó el acta y cuándo.

Reglas del enunciado:
- el número y la capacidad del aula no pueden ser 0, y el número no se repite;
- un acta tiene al menos un profesor;
- la cantidad de alumnos no puede superar la capacidad del aula;
- cada nota es de 1 a 10, o el alumno está ausente;
- un alumno no puede aparecer dos veces en la misma acta.

#### El modelo
Como en el diagrama de la cátedra, el acta **es un** formulario (herencia) y **tiene**
profesores y registros (composición):
```java
public class Formulario {
    protected int id;
    protected LocalDate fecha;
    protected String usuario;
    …
}

public class ActaDeExamen extends Formulario {
    private String carrera;
    private String materia;
    private Aula aula;
    private final List<Profesor> profesores = new ArrayList<>();
    private final List<Registro> registros = new ArrayList<>();
    …
}
```
Un `Registro` asocia un alumno con su nota; la nota es un `Integer` que puede ser
`null` para decir "ausente" (y en la base, `NULL`).

#### La base
```
aula(numero PK, capacidad)
profesor(id PK, apellido_nombre)
alumno(matricula PK, apellido_nombre)
acta(id PK, fecha, usuario, fecha_carga, carrera, materia, aula_numero → aula)
acta_profesor(acta_id → acta, profesor_id → profesor)        PK (acta_id, profesor_id)
registro(acta_id → acta, matricula → alumno, nota NULL o 1..10)  PK (acta_id, matricula)
```
Las restricciones hacen cumplir las reglas que puede cumplir la base (notas de 1 a 10,
alumnos sin repetir en un acta); las demás (capacidad del aula, al menos un profesor)
las valida el controlador **antes** de guardar.

#### Guardar un acta: una transacción, tres tablas
```java
con.setAutoCommit(false);
try {
    int id = insertarCabecera(con, acta);         // acta
    for (Profesor p : acta.getProfesores()) {     // acta_profesor
        insertarProfesor(con, id, p);
    }
    for (Registro r : acta.getRegistros()) {      // registro
        insertarRegistro(con, id, r);
    }
    con.commit();
} catch (SQLException e) {
    con.rollback();                               // si falla uno, no queda nada
    throw …;
}
```
Es exactamente el punto de la unidad 5: guardar un acta toca tres tablas, y si falla el
último registro no puede quedar un acta a medias.

#### Las ventanas del caso
1. **Ingreso** (usuario y clave).
2. **Principal MDI** con el menú de módulos.
3. **ABM** de aulas, profesores y alumnos (como el nodo anterior).
4. **Formulario del acta**, el más complejo: un `JComboBox` para el aula, una `JList` de
   selección múltiple para los profesores, y una `JTable` para los registros donde se
   agregan alumnos y se carga la nota (o se marca ausente).

#### Cómo encararlo
Con el mismo orden de siempre: **base** (script que se pueda volver a correr) →
**modelo** → **DAO/controladores** (probá cada uno desde un `main` o con JUnit) →
**ventanas** de a una. No empieces por la ventana del acta: es la última pieza.

### Código de ejemplo

El corazón del caso, sin ventanas: el modelo, el controlador que valida y guarda un acta
en una transacción, y un resumen con `JOIN`. Cargá `schema.sql` y ejecutalo con el
driver en el classpath.

`schema.sql`

```sql
DROP TABLE IF EXISTS registro;
DROP TABLE IF EXISTS acta_profesor;
DROP TABLE IF EXISTS acta;
DROP TABLE IF EXISTS alumno;
DROP TABLE IF EXISTS profesor;
DROP TABLE IF EXISTS aula;
CREATE TABLE aula (numero INTEGER PRIMARY KEY CHECK (numero <> 0), capacidad INTEGER NOT NULL CHECK (capacidad > 0));
CREATE TABLE profesor (id SERIAL PRIMARY KEY, apellido_nombre VARCHAR(50) NOT NULL);
CREATE TABLE alumno (matricula VARCHAR(10) PRIMARY KEY, apellido_nombre VARCHAR(50) NOT NULL);
CREATE TABLE acta (id SERIAL PRIMARY KEY, fecha DATE NOT NULL, usuario VARCHAR(20) NOT NULL,
                   fecha_carga DATE NOT NULL DEFAULT CURRENT_DATE, carrera VARCHAR(40) NOT NULL,
                   materia VARCHAR(40) NOT NULL, aula_numero INTEGER NOT NULL REFERENCES aula(numero));
CREATE TABLE acta_profesor (acta_id INTEGER REFERENCES acta(id) ON DELETE CASCADE, profesor_id INTEGER REFERENCES profesor(id),
                            PRIMARY KEY (acta_id, profesor_id));
CREATE TABLE registro (acta_id INTEGER REFERENCES acta(id) ON DELETE CASCADE, matricula VARCHAR(10) REFERENCES alumno(matricula),
                       nota INTEGER CHECK (nota BETWEEN 1 AND 10), PRIMARY KEY (acta_id, matricula));
INSERT INTO aula VALUES (101, 40), (5, 3);
INSERT INTO profesor (apellido_nombre) VALUES ('Kaffa, Arquitecta'), ('Ferrum, Maese'), ('Ofidia, Serpiente');
INSERT INTO alumno VALUES ('A-001', 'Valdez, Kira'), ('A-002', 'Tallo, Bron'), ('A-003', 'Ferrari, Lía'), ('A-004', 'Nuez, Pip');
```

```java
/*
 * Jefe final: el corazón de las Actas de Examen.
 * Modelo con herencia, controlador con reglas, una transacción sobre tres tablas y un resumen con JOIN.
 */
import java.sql.Connection;
import java.sql.Date;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Set;

public class Actas {
    public static void main(String[] args) throws SQLException {
        Locale.setDefault(Locale.US);
        ActaControlador controlador = new ActaControlador();

        ActaDeExamen acta = new ActaDeExamen(LocalDate.of(2026, 12, 10), "kaffa", "Licenciatura en Sistemas",
                "Paradigmas y Lenguajes III", new Aula(101, 40));
        acta.agregarProfesor(new Profesor(1, "Kaffa, Arquitecta"));
        acta.agregarProfesor(new Profesor(2, "Ferrum, Maese"));
        acta.agregarRegistro(new Registro(new Alumno("A-001", "Valdez, Kira"), 9));
        acta.agregarRegistro(new Registro(new Alumno("A-002", "Tallo, Bron"), 4));
        acta.agregarRegistro(new Registro(new Alumno("A-003", "Ferrari, Lía"), null));   // ausente
        acta.agregarRegistro(new Registro(new Alumno("A-004", "Nuez, Pip"), 2));
        intentar(controlador, acta);
        System.out.println(controlador.resumen(acta.getId()));

        // Una regla del controlador: el aula 5 tiene capacidad para 3 y el acta trae 4 alumnos
        ActaDeExamen llena = new ActaDeExamen(LocalDate.of(2026, 12, 11), "kaffa", "Licenciatura en Sistemas", "Álgebra", new Aula(5, 3));
        llena.agregarProfesor(new Profesor(3, "Ofidia, Serpiente"));
        for (String m : new String[]{"A-001", "A-002", "A-003", "A-004"}) {
            llena.agregarRegistro(new Registro(new Alumno(m, m), 7));
        }
        intentar(controlador, llena);

        // Una regla de la base: la nota 11 viola el CHECK y la transacción deshace todo el acta
        ActaDeExamen mala = new ActaDeExamen(LocalDate.of(2026, 12, 12), "kaffa", "Licenciatura en Sistemas", "Bases de Datos", new Aula(101, 40));
        mala.agregarProfesor(new Profesor(1, "Kaffa, Arquitecta"));
        mala.agregarRegistro(new Registro(new Alumno("A-001", "Valdez, Kira"), 8));
        mala.agregarRegistro(new Registro(new Alumno("A-002", "Tallo, Bron"), 11));
        intentar(controlador, mala);
        System.out.println("Actas guardadas en la base: " + controlador.cantidadDeActas());
    }

    static void intentar(ActaControlador c, ActaDeExamen acta) {
        try {
            c.guardar(acta);
            System.out.println("Acta " + acta.getId() + " de " + acta.getMateria() + ": guardada");
        } catch (IllegalArgumentException e) {
            System.out.println("Acta de " + acta.getMateria() + " rechazada: " + e.getMessage());
        } catch (SQLException e) {
            System.out.println("Acta de " + acta.getMateria() + " deshecha por la base (" + e.getSQLState() + ")");
        }
    }
}

class Formulario {
    protected int id;
    protected LocalDate fecha;
    protected String usuario;

    Formulario(LocalDate fecha, String usuario) {
        this.fecha = fecha;
        this.usuario = usuario;
    }

    int getId() {
        return id;
    }

    void setId(int id) {
        this.id = id;
    }
}

class ActaDeExamen extends Formulario {
    private final String carrera;
    private final String materia;
    private final Aula aula;
    private final List<Profesor> profesores = new ArrayList<>();
    private final List<Registro> registros = new ArrayList<>();

    ActaDeExamen(LocalDate fecha, String usuario, String carrera, String materia, Aula aula) {
        super(fecha, usuario);
        this.carrera = carrera;
        this.materia = materia;
        this.aula = aula;
    }

    void agregarProfesor(Profesor p) {
        profesores.add(p);
    }

    void agregarRegistro(Registro r) {
        registros.add(r);
    }

    String getCarrera() {
        return carrera;
    }

    String getMateria() {
        return materia;
    }

    Aula getAula() {
        return aula;
    }

    List<Profesor> getProfesores() {
        return profesores;
    }

    List<Registro> getRegistros() {
        return registros;
    }
}

record Aula(int numero, int capacidad) { }

record Profesor(int id, String apellidoNombre) { }

record Alumno(String matricula, String apellidoNombre) { }

record Registro(Alumno alumno, Integer nota) {
    boolean ausente() {
        return nota == null;
    }
}

class ActaControlador {
    void guardar(ActaDeExamen acta) throws SQLException {
        validar(acta);
        try (Connection con = Conexion.abrir()) {
            con.setAutoCommit(false);
            try {
                String sqlActa = "INSERT INTO acta (fecha, usuario, carrera, materia, aula_numero) VALUES (?, ?, ?, ?, ?)";
                try (PreparedStatement ps = con.prepareStatement(sqlActa, Statement.RETURN_GENERATED_KEYS)) {
                    ps.setDate(1, Date.valueOf(acta.fecha));
                    ps.setString(2, acta.usuario);
                    ps.setString(3, acta.getCarrera());
                    ps.setString(4, acta.getMateria());
                    ps.setInt(5, acta.getAula().numero());
                    ps.executeUpdate();
                    try (ResultSet k = ps.getGeneratedKeys()) {
                        k.next();
                        acta.setId(k.getInt(1));
                    }
                }
                try (PreparedStatement ps = con.prepareStatement("INSERT INTO acta_profesor (acta_id, profesor_id) VALUES (?, ?)")) {
                    for (Profesor p : acta.getProfesores()) {
                        ps.setInt(1, acta.getId());
                        ps.setInt(2, p.id());
                        ps.executeUpdate();
                    }
                }
                try (PreparedStatement ps = con.prepareStatement("INSERT INTO registro (acta_id, matricula, nota) VALUES (?, ?, ?)")) {
                    for (Registro r : acta.getRegistros()) {
                        ps.setInt(1, acta.getId());
                        ps.setString(2, r.alumno().matricula());
                        ps.setObject(3, r.nota());          // null = ausente
                        ps.executeUpdate();
                    }
                }
                con.commit();
            } catch (SQLException e) {
                con.rollback();
                acta.setId(0);
                throw e;
            }
        }
    }

    private void validar(ActaDeExamen acta) {
        if (acta.getProfesores().isEmpty()) {
            throw new IllegalArgumentException("el acta necesita al menos un profesor");
        }
        if (acta.getRegistros().size() > acta.getAula().capacidad()) {
            throw new IllegalArgumentException("el aula " + acta.getAula().numero() + " tiene capacidad para "
                    + acta.getAula().capacidad() + " y hay " + acta.getRegistros().size() + " alumnos");
        }
        Set<String> matriculas = new HashSet<>();
        for (Registro r : acta.getRegistros()) {
            if (!matriculas.add(r.alumno().matricula())) {
                throw new IllegalArgumentException("el alumno " + r.alumno().matricula() + " está dos veces");
            }
        }
    }

    String resumen(int actaId) throws SQLException {
        String sql = "SELECT a.materia, a.aula_numero, "
                + "(SELECT string_agg(p.apellido_nombre, ' / ' ORDER BY p.apellido_nombre) FROM acta_profesor ap "
                + " JOIN profesor p ON p.id = ap.profesor_id WHERE ap.acta_id = a.id) AS tribunal, "
                + "COUNT(r.matricula) AS inscriptos, COUNT(r.nota) AS presentes, "
                + "COUNT(*) FILTER (WHERE r.nota >= 4) AS aprobados, ROUND(AVG(r.nota), 2) AS promedio "
                + "FROM acta a LEFT JOIN registro r ON r.acta_id = a.id WHERE a.id = ? GROUP BY a.id";
        try (Connection con = Conexion.abrir(); PreparedStatement ps = con.prepareStatement(sql)) {
            ps.setInt(1, actaId);
            try (ResultSet rs = ps.executeQuery()) {
                rs.next();
                return String.format("  %s, aula %d%n  Tribunal: %s%n  Inscriptos %d, presentes %d, aprobados %d, promedio %.2f",
                        rs.getString("materia"), rs.getInt("aula_numero"), rs.getString("tribunal"), rs.getInt("inscriptos"),
                        rs.getInt("presentes"), rs.getInt("aprobados"), rs.getDouble("promedio"));
            }
        }
    }

    int cantidadDeActas() throws SQLException {
        try (Connection con = Conexion.abrir(); PreparedStatement ps = con.prepareStatement("SELECT COUNT(*) FROM acta");
             ResultSet rs = ps.executeQuery()) {
            rs.next();
            return rs.getInt(1);
        }
    }
}

final class Conexion {
    static final String URL = "jdbc:postgresql://localhost:5432/imperio";
    static final String USUARIO = "imperio";
    static final String CLAVE = "imperio";

    static Connection abrir() throws SQLException {
        return DriverManager.getConnection(URL, USUARIO, CLAVE);
    }
}
```

### Salida esperada

```
Acta 1 de Paradigmas y Lenguajes III: guardada
  Paradigmas y Lenguajes III, aula 101
  Tribunal: Ferrum, Maese / Kaffa, Arquitecta
  Inscriptos 4, presentes 3, aprobados 2, promedio 5.00
Acta de Álgebra rechazada: el aula 5 tiene capacidad para 3 y hay 4 alumnos
Acta de Bases de Datos deshecha por la base (23514)
Actas guardadas en la base: 1
```

### ¿Para qué sirve?

Este es el tipo de sistema que se pide en los exámenes finales, en las pasantías y en los primeros trabajos: un sistema de gestión con base de datos, reglas del negocio y ventanas para cargar y consultar. Si lo podés construir entero, pieza por pieza, podés construir el sistema de un consultorio, de un club o de un comercio.

### Errores habituales

**Dragón: empezar por la ventana del acta.** Es la pieza que depende de todas las
demás. Primero la base, el modelo y el controlador probados.

**Troll: el acta a medias.** Guardar la cabecera en una conexión y los registros en otra
(o sin `setAutoCommit(false)`) deja actas sin alumnos cuando algo falla.

**Goblin: el ausente como 0.** Si el ausente se guarda como nota 0, el promedio da mal
y el `CHECK (nota BETWEEN 1 AND 10)` lo rechaza. El ausente es `NULL`
(`ps.setObject(3, null)` o `ps.setNull(3, Types.INTEGER)`).

**Ogro: las reglas solo en la ventana.** Si la validación de la capacidad está en el
botón, otra pantalla (o una prueba) puede saltearla. Va en el controlador.

**Orco: la fila de la tabla que no es la del modelo.** En el formulario del acta, si la
tabla de registros se puede ordenar, convertí los índices antes de tocar el modelo.

### Misión R05-N08-M1 · La Registración de Actas de Examen

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 6
xp: 40
```

#### Consigna

Construí el sistema completo de actas, con la base de `schema.sql` del ejemplo y la
estructura de cuatro paquetes (`modelo`, `dao`, `controlador`, `visual`):

1. **Ventana principal MDI** con menú `Datos` (Aulas, Profesores, Alumnos) y `Actas`
   (Nueva acta, Consultar).
2. **ABM de aulas** con las reglas del enunciado (número y capacidad distintos de 0,
   número sin repetir).
3. **Formulario de nueva acta**: fecha (texto `aaaa-mm-dd`), carrera, materia, un
   `JComboBox` con las aulas, una `JList` de selección múltiple con los profesores, y una
   `JTable` de registros: se elige un alumno de un combo, se escribe la nota (o se marca
   la casilla "Ausente") y se agrega; un botón quita el registro seleccionado. `Guardar`
   valida con el controlador y guarda **en una transacción**.
4. **Consulta**: una tabla con todas las actas (fecha, materia, aula, inscriptos,
   aprobados) que se carga en un `SwingWorker`.

Entregá un zip con `src/`, `schema.sql`, `db.properties` y un `LEEME.txt` con cómo
compilar y ejecutar.

#### Criterio de aprobación

- La estructura de capas se respeta: las ventanas no tienen SQL.
- `ActaDeExamen` extiende `Formulario` y compone sus profesores y registros.
- El acta se guarda en una transacción y se validan todas las reglas del enunciado.
- La consulta no congela la ventana.

#### Solución de referencia

`db.properties`

```
url=jdbc:postgresql://localhost:5432/imperio
usuario=imperio
clave=imperio
```

`schema.sql`

```sql
DROP TABLE IF EXISTS registro;
DROP TABLE IF EXISTS acta_profesor;
DROP TABLE IF EXISTS acta;
DROP TABLE IF EXISTS alumno;
DROP TABLE IF EXISTS profesor;
DROP TABLE IF EXISTS aula;
CREATE TABLE aula (numero INTEGER PRIMARY KEY CHECK (numero <> 0), capacidad INTEGER NOT NULL CHECK (capacidad > 0));
CREATE TABLE profesor (id SERIAL PRIMARY KEY, apellido_nombre VARCHAR(50) NOT NULL);
CREATE TABLE alumno (matricula VARCHAR(10) PRIMARY KEY, apellido_nombre VARCHAR(50) NOT NULL);
CREATE TABLE acta (id SERIAL PRIMARY KEY, fecha DATE NOT NULL, usuario VARCHAR(20) NOT NULL,
                   fecha_carga DATE NOT NULL DEFAULT CURRENT_DATE, carrera VARCHAR(40) NOT NULL,
                   materia VARCHAR(40) NOT NULL, aula_numero INTEGER NOT NULL REFERENCES aula(numero));
CREATE TABLE acta_profesor (acta_id INTEGER REFERENCES acta(id) ON DELETE CASCADE, profesor_id INTEGER REFERENCES profesor(id),
                            PRIMARY KEY (acta_id, profesor_id));
CREATE TABLE registro (acta_id INTEGER REFERENCES acta(id) ON DELETE CASCADE, matricula VARCHAR(10) REFERENCES alumno(matricula),
                       nota INTEGER CHECK (nota BETWEEN 1 AND 10), PRIMARY KEY (acta_id, matricula));
INSERT INTO aula VALUES (101, 40), (5, 3);
INSERT INTO profesor (apellido_nombre) VALUES ('Kaffa, Arquitecta'), ('Ferrum, Maese'), ('Ofidia, Serpiente');
INSERT INTO alumno VALUES ('A-001', 'Valdez, Kira'), ('A-002', 'Tallo, Bron'), ('A-003', 'Ferrari, Lía'), ('A-004', 'Nuez, Pip');
```

`src/modelo/Formulario.java`

```java
package modelo;

import java.time.LocalDate;

public class Formulario {
    protected int id;
    protected LocalDate fecha;
    protected String usuario;

    public Formulario(LocalDate fecha, String usuario) {
        this.fecha = fecha;
        this.usuario = usuario;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public LocalDate getFecha() {
        return fecha;
    }

    public String getUsuario() {
        return usuario;
    }
}
```

`src/modelo/ActaDeExamen.java`

```java
package modelo;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

public class ActaDeExamen extends Formulario {
    private final String carrera;
    private final String materia;
    private final Aula aula;
    private final List<Profesor> profesores = new ArrayList<>();
    private final List<Registro> registros = new ArrayList<>();

    public ActaDeExamen(LocalDate fecha, String usuario, String carrera, String materia, Aula aula) {
        super(fecha, usuario);
        this.carrera = carrera;
        this.materia = materia;
        this.aula = aula;
    }

    public String getCarrera() {
        return carrera;
    }

    public String getMateria() {
        return materia;
    }

    public Aula getAula() {
        return aula;
    }

    public List<Profesor> getProfesores() {
        return profesores;
    }

    public List<Registro> getRegistros() {
        return registros;
    }
}
```

`src/modelo/Aula.java`

```java
package modelo;

public record Aula(int numero, int capacidad) {
    @Override
    public String toString() {
        return "Aula " + numero + " (" + capacidad + ")";
    }
}
```

`src/modelo/Profesor.java`

```java
package modelo;

public record Profesor(int id, String apellidoNombre) {
    @Override
    public String toString() {
        return apellidoNombre;
    }
}
```

`src/modelo/Alumno.java`

```java
package modelo;

public record Alumno(String matricula, String apellidoNombre) {
    @Override
    public String toString() {
        return matricula + " " + apellidoNombre;
    }
}
```

`src/modelo/Registro.java`

```java
package modelo;

/** Un alumno en un acta; la nota null significa ausente. */
public record Registro(Alumno alumno, Integer nota) {
    public boolean ausente() {
        return nota == null;
    }
}
```

`src/dao/ConexionBD.java`

```java
package dao;

import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.Properties;

public final class ConexionBD {
    private ConexionBD() {
    }

    public static Connection obtener() throws SQLException {
        Properties p = new Properties();
        try (BufferedReader r = Files.newBufferedReader(Path.of("db.properties"))) {
            p.load(r);
        } catch (IOException e) {
            throw new SQLException("no se pudo leer db.properties", e);
        }
        return DriverManager.getConnection(p.getProperty("url"), p.getProperty("usuario"), p.getProperty("clave"));
    }
}
```

`src/dao/DatosDAO.java`

```java
package dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import modelo.Alumno;
import modelo.Aula;
import modelo.Profesor;

/** Lecturas y altas de las tablas de datos (aulas, profesores, alumnos). */
public class DatosDAO {
    public List<Aula> aulas() throws SQLException {
        List<Aula> lista = new ArrayList<>();
        try (Connection con = ConexionBD.obtener();
             PreparedStatement ps = con.prepareStatement("SELECT numero, capacidad FROM aula ORDER BY numero");
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                lista.add(new Aula(rs.getInt(1), rs.getInt(2)));
            }
        }
        return lista;
    }

    public boolean existeAula(int numero) throws SQLException {
        try (Connection con = ConexionBD.obtener(); PreparedStatement ps = con.prepareStatement("SELECT 1 FROM aula WHERE numero = ?")) {
            ps.setInt(1, numero);
            try (ResultSet rs = ps.executeQuery()) {
                return rs.next();
            }
        }
    }

    public void insertarAula(Aula a) throws SQLException {
        try (Connection con = ConexionBD.obtener();
             PreparedStatement ps = con.prepareStatement("INSERT INTO aula (numero, capacidad) VALUES (?, ?)")) {
            ps.setInt(1, a.numero());
            ps.setInt(2, a.capacidad());
            ps.executeUpdate();
        }
    }

    public List<Profesor> profesores() throws SQLException {
        List<Profesor> lista = new ArrayList<>();
        try (Connection con = ConexionBD.obtener();
             PreparedStatement ps = con.prepareStatement("SELECT id, apellido_nombre FROM profesor ORDER BY apellido_nombre");
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                lista.add(new Profesor(rs.getInt(1), rs.getString(2)));
            }
        }
        return lista;
    }

    public List<Alumno> alumnos() throws SQLException {
        List<Alumno> lista = new ArrayList<>();
        try (Connection con = ConexionBD.obtener();
             PreparedStatement ps = con.prepareStatement("SELECT matricula, apellido_nombre FROM alumno ORDER BY apellido_nombre");
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                lista.add(new Alumno(rs.getString(1), rs.getString(2)));
            }
        }
        return lista;
    }
}
```

`src/dao/ActaDAO.java`

```java
package dao;

import java.sql.Connection;
import java.sql.Date;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;
import modelo.ActaDeExamen;
import modelo.Profesor;
import modelo.Registro;

public class ActaDAO {
    /** Guarda cabecera, tribunal y registros en una sola transacción. */
    public void guardar(ActaDeExamen acta) throws SQLException {
        try (Connection con = ConexionBD.obtener()) {
            con.setAutoCommit(false);
            try {
                try (PreparedStatement ps = con.prepareStatement(
                        "INSERT INTO acta (fecha, usuario, carrera, materia, aula_numero) VALUES (?, ?, ?, ?, ?)", Statement.RETURN_GENERATED_KEYS)) {
                    ps.setDate(1, Date.valueOf(acta.getFecha()));
                    ps.setString(2, acta.getUsuario());
                    ps.setString(3, acta.getCarrera());
                    ps.setString(4, acta.getMateria());
                    ps.setInt(5, acta.getAula().numero());
                    ps.executeUpdate();
                    try (ResultSet k = ps.getGeneratedKeys()) {
                        k.next();
                        acta.setId(k.getInt(1));
                    }
                }
                try (PreparedStatement ps = con.prepareStatement("INSERT INTO acta_profesor (acta_id, profesor_id) VALUES (?, ?)")) {
                    for (Profesor p : acta.getProfesores()) {
                        ps.setInt(1, acta.getId());
                        ps.setInt(2, p.id());
                        ps.executeUpdate();
                    }
                }
                try (PreparedStatement ps = con.prepareStatement("INSERT INTO registro (acta_id, matricula, nota) VALUES (?, ?, ?)")) {
                    for (Registro r : acta.getRegistros()) {
                        ps.setInt(1, acta.getId());
                        ps.setString(2, r.alumno().matricula());
                        ps.setObject(3, r.nota());
                        ps.executeUpdate();
                    }
                }
                con.commit();
            } catch (SQLException e) {
                con.rollback();
                acta.setId(0);
                throw e;
            }
        }
    }

    /** Filas para la consulta: fecha, materia, aula, inscriptos, aprobados. */
    public List<Object[]> resumenes() throws SQLException {
        String sql = "SELECT a.fecha, a.materia, a.aula_numero, COUNT(r.matricula), COUNT(*) FILTER (WHERE r.nota >= 4) "
                + "FROM acta a LEFT JOIN registro r ON r.acta_id = a.id GROUP BY a.id ORDER BY a.fecha, a.id";
        List<Object[]> filas = new ArrayList<>();
        try (Connection con = ConexionBD.obtener(); PreparedStatement ps = con.prepareStatement(sql); ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                filas.add(new Object[]{rs.getDate(1).toLocalDate(), rs.getString(2), rs.getInt(3), rs.getInt(4), rs.getInt(5)});
            }
        }
        return filas;
    }
}
```

`src/controlador/AulaControlador.java`

```java
package controlador;

import dao.DatosDAO;
import java.sql.SQLException;
import modelo.Aula;

public class AulaControlador {
    private final DatosDAO dao = new DatosDAO();

    public void registrar(String textoNumero, String textoCapacidad) throws SQLException {
        int numero;
        int capacidad;
        try {
            numero = Integer.parseInt(textoNumero.trim());
            capacidad = Integer.parseInt(textoCapacidad.trim());
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException("número y capacidad tienen que ser enteros");
        }
        if (numero == 0 || capacidad == 0) {
            throw new IllegalArgumentException("número y capacidad no pueden ser 0");
        }
        if (dao.existeAula(numero)) {
            throw new IllegalArgumentException("ya existe el aula " + numero);
        }
        dao.insertarAula(new Aula(numero, capacidad));
    }
}
```

`src/controlador/ActaControlador.java`

```java
package controlador;

import dao.ActaDAO;
import java.sql.SQLException;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import modelo.ActaDeExamen;
import modelo.Registro;

public class ActaControlador {
    private final ActaDAO dao = new ActaDAO();

    public void guardar(ActaDeExamen acta) throws SQLException {
        if (acta.getCarrera().isBlank() || acta.getMateria().isBlank()) {
            throw new IllegalArgumentException("faltan la carrera o la materia");
        }
        if (acta.getProfesores().isEmpty()) {
            throw new IllegalArgumentException("el acta necesita al menos un profesor");
        }
        if (acta.getRegistros().isEmpty()) {
            throw new IllegalArgumentException("el acta no tiene alumnos");
        }
        if (acta.getRegistros().size() > acta.getAula().capacidad()) {
            throw new IllegalArgumentException("el aula tiene capacidad para " + acta.getAula().capacidad() + " alumnos");
        }
        Set<String> vistos = new HashSet<>();
        for (Registro r : acta.getRegistros()) {
            if (!r.ausente() && (r.nota() < 1 || r.nota() > 10)) {
                throw new IllegalArgumentException("la nota de " + r.alumno().matricula() + " tiene que ser de 1 a 10");
            }
            if (!vistos.add(r.alumno().matricula())) {
                throw new IllegalArgumentException("el alumno " + r.alumno().matricula() + " está dos veces");
            }
        }
        dao.guardar(acta);
    }

    public List<Object[]> resumenes() throws SQLException {
        return dao.resumenes();
    }
}
```

`src/visual/PanelAulas.java`

```java
package visual;

import controlador.AulaControlador;
import dao.DatosDAO;
import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.sql.SQLException;
import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.table.DefaultTableModel;
import modelo.Aula;

public class PanelAulas extends JPanel {
    private final AulaControlador controlador = new AulaControlador();
    private final DefaultTableModel modelo = new DefaultTableModel(new String[]{"Número", "Capacidad"}, 0);
    private final JTextField txtNumero = new JTextField(5);
    private final JTextField txtCapacidad = new JTextField(5);

    public PanelAulas() {
        super(new BorderLayout(6, 6));
        setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));
        JTable tabla = new JTable(modelo);
        tabla.setPreferredScrollableViewportSize(new java.awt.Dimension(260, 100));
        JPanel form = new JPanel(new FlowLayout(FlowLayout.LEFT));
        JButton btnGuardar = new JButton("Guardar");
        form.add(new JLabel("Número:"));
        form.add(txtNumero);
        form.add(new JLabel("Capacidad:"));
        form.add(txtCapacidad);
        form.add(btnGuardar);
        add(new JScrollPane(tabla), BorderLayout.CENTER);
        add(form, BorderLayout.SOUTH);
        btnGuardar.addActionListener(e -> guardar());
        cargar();
    }

    private void cargar() {
        try {
            modelo.setRowCount(0);
            for (Aula a : new DatosDAO().aulas()) {
                modelo.addRow(new Object[]{a.numero(), a.capacidad()});
            }
        } catch (SQLException e) {
            JOptionPane.showMessageDialog(this, "Error de base de datos: " + e.getMessage());
        }
    }

    private void guardar() {
        try {
            controlador.registrar(txtNumero.getText(), txtCapacidad.getText());
            txtNumero.setText("");
            txtCapacidad.setText("");
            cargar();
        } catch (IllegalArgumentException e) {
            JOptionPane.showMessageDialog(this, e.getMessage());
        } catch (SQLException e) {
            JOptionPane.showMessageDialog(this, "Error de base de datos: " + e.getMessage());
        }
    }
}
```

`src/visual/PanelActa.java`

```java
package visual;

import controlador.ActaControlador;
import dao.DatosDAO;
import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Insets;
import java.sql.SQLException;
import java.time.LocalDate;
import java.time.format.DateTimeParseException;
import java.util.ArrayList;
import java.util.List;
import javax.swing.BorderFactory;
import javax.swing.DefaultListModel;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JComboBox;
import javax.swing.JComponent;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.ListSelectionModel;
import javax.swing.table.DefaultTableModel;
import modelo.ActaDeExamen;
import modelo.Alumno;
import modelo.Aula;
import modelo.Profesor;
import modelo.Registro;

public class PanelActa extends JPanel {
    private final ActaControlador controlador = new ActaControlador();
    private final JTextField txtFecha = new JTextField("2026-12-10", 10);
    private final JTextField txtCarrera = new JTextField("Licenciatura en Sistemas", 18);
    private final JTextField txtMateria = new JTextField(18);
    private final JComboBox<Aula> cmbAula = new JComboBox<>();
    private final DefaultListModel<Profesor> modeloProfesores = new DefaultListModel<>();
    private final JList<Profesor> lstProfesores = new JList<>(modeloProfesores);
    private final JComboBox<Alumno> cmbAlumno = new JComboBox<>();
    private final JTextField txtNota = new JTextField(3);
    private final JCheckBox chkAusente = new JCheckBox("Ausente");
    private final DefaultTableModel modeloRegistros = new DefaultTableModel(new String[]{"Alumno", "Nota"}, 0) {
        @Override
        public boolean isCellEditable(int f, int c) {
            return false;
        }
    };
    private final List<Registro> registros = new ArrayList<>();

    public PanelActa() {
        super(new BorderLayout(6, 6));
        setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));
        lstProfesores.setSelectionMode(ListSelectionModel.MULTIPLE_INTERVAL_SELECTION);
        lstProfesores.setVisibleRowCount(4);

        JPanel cabecera = new JPanel(new GridBagLayout());
        cabecera.setBorder(BorderFactory.createTitledBorder("Acta"));
        fila(cabecera, 0, "Fecha (aaaa-mm-dd):", txtFecha);
        fila(cabecera, 1, "Carrera:", txtCarrera);
        fila(cabecera, 2, "Materia:", txtMateria);
        fila(cabecera, 3, "Aula:", cmbAula);
        fila(cabecera, 4, "Tribunal:", new JScrollPane(lstProfesores));

        JPanel carga = new JPanel(new FlowLayout(FlowLayout.LEFT));
        JButton btnAgregar = new JButton("Agregar");
        JButton btnQuitar = new JButton("Quitar");
        carga.add(cmbAlumno);
        carga.add(new JLabel("Nota:"));
        carga.add(txtNota);
        carga.add(chkAusente);
        carga.add(btnAgregar);
        carga.add(btnQuitar);
        JTable tabla = new JTable(modeloRegistros);
        tabla.setPreferredScrollableViewportSize(new java.awt.Dimension(360, 100));
        JPanel registrosPanel = new JPanel(new BorderLayout(4, 4));
        registrosPanel.setBorder(BorderFactory.createTitledBorder("Registros"));
        registrosPanel.add(carga, BorderLayout.NORTH);
        registrosPanel.add(new JScrollPane(tabla), BorderLayout.CENTER);

        JButton btnGuardar = new JButton("Guardar acta");
        add(cabecera, BorderLayout.NORTH);
        add(registrosPanel, BorderLayout.CENTER);
        add(btnGuardar, BorderLayout.SOUTH);

        chkAusente.addActionListener(e -> txtNota.setEnabled(!chkAusente.isSelected()));
        btnAgregar.addActionListener(e -> agregar());
        btnQuitar.addActionListener(e -> {
            int f = tabla.getSelectedRow();
            if (f >= 0) {
                registros.remove(f);
                modeloRegistros.removeRow(f);
            }
        });
        btnGuardar.addActionListener(e -> guardar());
        cargarListas();
    }

    private void fila(JPanel p, int y, String etiqueta, JComponent campo) {
        GridBagConstraints c = new GridBagConstraints();
        c.insets = new Insets(3, 3, 3, 3);
        c.gridy = y;
        c.anchor = GridBagConstraints.LINE_END;
        p.add(new JLabel(etiqueta), c);
        c = new GridBagConstraints();
        c.insets = new Insets(3, 3, 3, 3);
        c.gridx = 1;
        c.gridy = y;
        c.fill = GridBagConstraints.HORIZONTAL;
        c.weightx = 1;
        p.add(campo, c);
    }

    private void cargarListas() {
        try {
            DatosDAO datos = new DatosDAO();
            datos.aulas().forEach(cmbAula::addItem);
            datos.profesores().forEach(modeloProfesores::addElement);
            datos.alumnos().forEach(cmbAlumno::addItem);
        } catch (SQLException e) {
            JOptionPane.showMessageDialog(this, "Error de base de datos: " + e.getMessage());
        }
    }

    private void agregar() {
        Alumno a = (Alumno) cmbAlumno.getSelectedItem();
        if (a == null) {
            return;
        }
        Integer nota = null;
        if (!chkAusente.isSelected()) {
            try {
                nota = Integer.parseInt(txtNota.getText().trim());
            } catch (NumberFormatException e) {
                JOptionPane.showMessageDialog(this, "La nota tiene que ser un número (o marcá Ausente)");
                return;
            }
        }
        registros.add(new Registro(a, nota));
        modeloRegistros.addRow(new Object[]{a, nota == null ? "ausente" : nota});
        txtNota.setText("");
    }

    private void guardar() {
        LocalDate fecha;
        try {
            fecha = LocalDate.parse(txtFecha.getText().trim());
        } catch (DateTimeParseException e) {
            JOptionPane.showMessageDialog(this, "La fecha tiene que tener el formato aaaa-mm-dd");
            return;
        }
        ActaDeExamen acta = new ActaDeExamen(fecha, "kaffa", txtCarrera.getText().trim(), txtMateria.getText().trim(), (Aula) cmbAula.getSelectedItem());
        acta.getProfesores().addAll(lstProfesores.getSelectedValuesList());
        acta.getRegistros().addAll(registros);
        try {
            controlador.guardar(acta);
            JOptionPane.showMessageDialog(this, "Acta " + acta.getId() + " guardada");
            registros.clear();
            modeloRegistros.setRowCount(0);
        } catch (IllegalArgumentException e) {
            JOptionPane.showMessageDialog(this, e.getMessage(), "Revisá el acta", JOptionPane.WARNING_MESSAGE);
        } catch (SQLException e) {
            JOptionPane.showMessageDialog(this, "La base rechazó el acta: " + e.getMessage());
        }
    }
}
```

`src/visual/PanelConsulta.java`

```java
package visual;

import controlador.ActaControlador;
import java.awt.BorderLayout;
import java.util.List;
import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.SwingWorker;
import javax.swing.table.DefaultTableModel;

public class PanelConsulta extends JPanel {
    private final ActaControlador controlador = new ActaControlador();
    private final DefaultTableModel modelo = new DefaultTableModel(new String[]{"Fecha", "Materia", "Aula", "Inscriptos", "Aprobados"}, 0);
    private final JLabel estado = new JLabel(" ");

    public PanelConsulta() {
        super(new BorderLayout(6, 6));
        setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));
        JTable tabla = new JTable(modelo);
        tabla.setPreferredScrollableViewportSize(new java.awt.Dimension(460, 120));
        JButton actualizar = new JButton("Actualizar");
        add(actualizar, BorderLayout.NORTH);
        add(new JScrollPane(tabla), BorderLayout.CENTER);
        add(estado, BorderLayout.SOUTH);
        actualizar.addActionListener(e -> cargar());
        cargar();
    }

    private void cargar() {
        estado.setText("Cargando…");
        new SwingWorker<List<Object[]>, Void>() {
            @Override
            protected List<Object[]> doInBackground() throws Exception {
                return controlador.resumenes();
            }

            @Override
            protected void done() {
                try {
                    modelo.setRowCount(0);
                    get().forEach(modelo::addRow);
                    estado.setText(modelo.getRowCount() + " actas");
                } catch (Exception e) {
                    estado.setText("Error: " + e.getMessage());
                }
            }
        }.execute();
    }
}
```

`src/visual/FrmPrincipal.java`

```java
package visual;

import java.awt.Dimension;
import java.util.function.Supplier;
import javax.swing.JComponent;
import javax.swing.JDesktopPane;
import javax.swing.JFrame;
import javax.swing.JInternalFrame;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.SwingUtilities;

public class FrmPrincipal extends JFrame {
    private final JDesktopPane mdi = new JDesktopPane();

    public FrmPrincipal() {
        super("Registración de Actas de Examen");
        mdi.setPreferredSize(new Dimension(900, 620));
        setContentPane(mdi);
        JMenuBar barra = new JMenuBar();
        JMenu datos = new JMenu("Datos");
        datos.add(item("Aulas", PanelAulas::new));
        JMenu actas = new JMenu("Actas");
        actas.add(item("Nueva acta", PanelActa::new));
        actas.add(item("Consultar", PanelConsulta::new));
        barra.add(datos);
        barra.add(actas);
        setJMenuBar(barra);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        pack();
        setLocationRelativeTo(null);
    }

    private JMenuItem item(String titulo, Supplier<JComponent> contenido) {
        JMenuItem i = new JMenuItem(titulo);
        i.addActionListener(e -> {
            JInternalFrame v = new JInternalFrame(titulo, true, true, true, true);
            v.setContentPane(contenido.get());
            v.pack();
            v.setVisible(true);
            mdi.add(v);
        });
        return i;
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new FrmPrincipal().setVisible(true));
    }
}
```

`LEEME.txt`

```
1. Cargar la base:   psql -h localhost -U imperio -d imperio -f schema.sql
2. Compilar:         javac -cp postgresql-42.7.4.jar -d out $(find src -name "*.java")
3. Ejecutar:         java -cp "out:postgresql-42.7.4.jar" visual.FrmPrincipal
   (db.properties tiene que estar en la carpeta desde donde se ejecuta)
```

### Misión R05-N08-M2 · El informe del tribunal

```meta
entrega: codigo
entorno: local
monedas: 6
xp: 30
```

#### Consigna

Con la base de las actas (el `schema.sql` de abajo ya trae tres actas cargadas),
escribí un programa de consola que muestre el **informe del tribunal**, con una
consulta por punto:

1. Por acta: materia, fecha, inscriptos, presentes, aprobados y el porcentaje de
   aprobación sobre los presentes (1 decimal).
2. Por alumno: cuántas actas rindió, cuántas aprobó y su promedio (de las notas, sin
   ausentes), ordenado por promedio de mayor a menor.
3. Los alumnos que estuvieron **ausentes** alguna vez.
4. El profesor que integró **más tribunales**.

Todo el SQL va en una clase `InformeDAO`; el `main` solo muestra.

#### Criterio de aprobación

- Usa `JOIN`, `GROUP BY`, `COUNT(nota)` para los presentes y `COALESCE` o `FILTER` donde haga falta.
- El porcentaje no se rompe si un acta no tiene presentes.

#### Salida esperada

```
1. Por acta
   Paradigmas III  2026-12-10  inscriptos 4, presentes 3, aprobados 2 (66.7%)
   Bases de Datos  2026-12-14  inscriptos 3, presentes 2, aprobados 2 (100.0%)
   Álgebra         2026-12-18  inscriptos 2, presentes 2, aprobados 1 (50.0%)
2. Por alumno
   Ferrari, Lía    rindió 3, aprobó 2, promedio 8.50
   Valdez, Kira    rindió 2, aprobó 2, promedio 8.50
   Tallo, Bron     rindió 2, aprobó 1, promedio 3.50
   Nuez, Pip       rindió 2, aprobó 0, promedio 2.00
3. Ausentes alguna vez: Ferrari, Lía / Nuez, Pip
4. Más tribunales: Ferrum, Maese (2)
```

#### Solución de referencia

`schema.sql`

```sql
DROP TABLE IF EXISTS registro;
DROP TABLE IF EXISTS acta_profesor;
DROP TABLE IF EXISTS acta;
DROP TABLE IF EXISTS alumno;
DROP TABLE IF EXISTS profesor;
DROP TABLE IF EXISTS aula;
CREATE TABLE aula (numero INTEGER PRIMARY KEY, capacidad INTEGER NOT NULL);
CREATE TABLE profesor (id SERIAL PRIMARY KEY, apellido_nombre VARCHAR(50) NOT NULL);
CREATE TABLE alumno (matricula VARCHAR(10) PRIMARY KEY, apellido_nombre VARCHAR(50) NOT NULL);
CREATE TABLE acta (id SERIAL PRIMARY KEY, fecha DATE NOT NULL, usuario VARCHAR(20) NOT NULL, carrera VARCHAR(40) NOT NULL,
                   materia VARCHAR(40) NOT NULL, aula_numero INTEGER NOT NULL REFERENCES aula(numero));
CREATE TABLE acta_profesor (acta_id INTEGER REFERENCES acta(id), profesor_id INTEGER REFERENCES profesor(id), PRIMARY KEY (acta_id, profesor_id));
CREATE TABLE registro (acta_id INTEGER REFERENCES acta(id), matricula VARCHAR(10) REFERENCES alumno(matricula),
                       nota INTEGER CHECK (nota BETWEEN 1 AND 10), PRIMARY KEY (acta_id, matricula));
INSERT INTO aula VALUES (101, 40);
INSERT INTO profesor (apellido_nombre) VALUES ('Kaffa, Arquitecta'), ('Ferrum, Maese'), ('Ofidia, Serpiente');
INSERT INTO alumno VALUES ('A-001', 'Valdez, Kira'), ('A-002', 'Tallo, Bron'), ('A-003', 'Ferrari, Lía'), ('A-004', 'Nuez, Pip');
INSERT INTO acta (fecha, usuario, carrera, materia, aula_numero) VALUES
    ('2026-12-10', 'kaffa', 'Sistemas', 'Paradigmas III', 101), ('2026-12-14', 'kaffa', 'Sistemas', 'Bases de Datos', 101),
    ('2026-12-18', 'ferrum', 'Sistemas', 'Álgebra', 101);
INSERT INTO acta_profesor VALUES (1, 1), (1, 2), (2, 1), (3, 2), (3, 3);
INSERT INTO registro VALUES (1, 'A-001', 9), (1, 'A-002', 4), (1, 'A-003', NULL), (1, 'A-004', 2),
                            (2, 'A-001', 8), (2, 'A-003', 7), (2, 'A-004', NULL),
                            (3, 'A-002', 3), (3, 'A-003', 10);
```

```java
// Jefe R05 - Mision 2: el informe del tribunal.
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

public class InformeTribunal {
    public static void main(String[] args) throws SQLException {
        Locale.setDefault(Locale.US);
        InformeDAO dao = new InformeDAO();
        System.out.println("1. Por acta");
        dao.porActa().forEach(l -> System.out.println("   " + l));
        System.out.println("2. Por alumno");
        dao.porAlumno().forEach(l -> System.out.println("   " + l));
        System.out.println("3. Ausentes alguna vez: " + String.join(" / ", dao.ausentes()));
        System.out.println("4. Más tribunales: " + dao.profesorConMasTribunales());
    }
}

class InformeDAO {
    List<String> porActa() throws SQLException {
        String sql = "SELECT a.materia, a.fecha, COUNT(r.matricula) AS inscriptos, COUNT(r.nota) AS presentes, "
                + "COUNT(*) FILTER (WHERE r.nota >= 4) AS aprobados "
                + "FROM acta a LEFT JOIN registro r ON r.acta_id = a.id GROUP BY a.id ORDER BY a.fecha";
        List<String> lineas = new ArrayList<>();
        try (Connection con = Conexion.abrir(); PreparedStatement ps = con.prepareStatement(sql); ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                int presentes = rs.getInt("presentes");
                int aprobados = rs.getInt("aprobados");
                double porcentaje = presentes == 0 ? 0 : 100.0 * aprobados / presentes;
                lineas.add(String.format("%-15s %s  inscriptos %d, presentes %d, aprobados %d (%.1f%%)", rs.getString("materia"),
                        rs.getDate("fecha"), rs.getInt("inscriptos"), presentes, aprobados, porcentaje));
            }
        }
        return lineas;
    }

    List<String> porAlumno() throws SQLException {
        String sql = "SELECT al.apellido_nombre, COUNT(r.acta_id) AS rindio, COUNT(*) FILTER (WHERE r.nota >= 4) AS aprobo, "
                + "ROUND(AVG(r.nota), 2) AS promedio FROM alumno al JOIN registro r ON r.matricula = al.matricula "
                + "GROUP BY al.matricula, al.apellido_nombre ORDER BY promedio DESC NULLS LAST, al.apellido_nombre";
        List<String> lineas = new ArrayList<>();
        try (Connection con = Conexion.abrir(); PreparedStatement ps = con.prepareStatement(sql); ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                lineas.add(String.format("%-15s rindió %d, aprobó %d, promedio %.2f", rs.getString(1), rs.getInt(2), rs.getInt(3), rs.getDouble(4)));
            }
        }
        return lineas;
    }

    List<String> ausentes() throws SQLException {
        String sql = "SELECT DISTINCT al.apellido_nombre FROM alumno al JOIN registro r ON r.matricula = al.matricula "
                + "WHERE r.nota IS NULL ORDER BY al.apellido_nombre";
        List<String> nombres = new ArrayList<>();
        try (Connection con = Conexion.abrir(); PreparedStatement ps = con.prepareStatement(sql); ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                nombres.add(rs.getString(1));
            }
        }
        return nombres;
    }

    String profesorConMasTribunales() throws SQLException {
        String sql = "SELECT p.apellido_nombre, COUNT(*) AS tribunales FROM acta_profesor ap JOIN profesor p ON p.id = ap.profesor_id "
                + "GROUP BY p.id, p.apellido_nombre ORDER BY tribunales DESC, p.apellido_nombre LIMIT 1";
        try (Connection con = Conexion.abrir(); PreparedStatement ps = con.prepareStatement(sql); ResultSet rs = ps.executeQuery()) {
            rs.next();
            return rs.getString(1) + " (" + rs.getInt(2) + ")";
        }
    }
}

final class Conexion {
    static final String URL = "jdbc:postgresql://localhost:5432/imperio";
    static final String USUARIO = "imperio";
    static final String CLAVE = "imperio";

    static Connection abrir() throws SQLException {
        return DriverManager.getConnection(URL, USUARIO, CLAVE);
    }
}
```

### Encargo R05-N08-E1 · El sistema de tu barrio

```meta
entrega: archivo
entorno: local
extensiones: zip, pdf
monedas: 1
xp: 40
```

#### Consigna

Elegí un comercio o institución que conozcas (un club, una ferretería, un consultorio,
una biblioteca popular) y construí **su** sistema de escritorio con todo lo del curso:

1. Un documento corto (PDF) con el problema, las reglas del negocio y el diagrama de
   clases.
2. La base con restricciones (script que se pueda volver a correr).
3. El código en cuatro paquetes, con al menos: un ABM completo, una operación que guarde
   en varias tablas con transacción y una consulta con `JOIN` y agregados.
4. Una ventana principal MDI con menú.
5. Al menos cinco pruebas de JUnit de un controlador (con un repositorio en memoria).

#### Criterio de aprobación

- El documento explica el problema y el diseño.
- Se cumplen los cinco puntos y el sistema funciona con la base del script.

#### Solución de referencia

```
No hay una solución única: se corrige con los criterios de aprobación.
Guía para la corrección:
- Diseño: ¿el diagrama coincide con el código? ¿Las relaciones (herencia, composición) tienen sentido?
- Base: ¿las restricciones protegen las reglas? ¿El script corre dos veces sin errores?
- Capas: ¿las ventanas están libres de SQL? ¿Las reglas están en los controladores?
- Transacción: ¿la operación compuesta es todo o nada?
- Pruebas: ¿prueban reglas del negocio (no solo getters)?
```

### Prueba del sello

#### ¿Por qué `ActaDeExamen` hereda de `Formulario` y no al revés?

Porque un acta *es un* formulario (con fecha, usuario, fecha de carga) con datos propios; `Formulario` es lo general.

#### ¿Qué relación tiene el acta con sus registros?

Composición: los registros pertenecen al acta y no tienen sentido sin ella (en la base, `ON DELETE CASCADE`).

#### ¿Cómo se guarda un alumno ausente?

Con la nota en `NULL`, no con un 0.

#### ¿Por qué el acta se guarda en una transacción?

Porque toca tres tablas: si falla un registro, no puede quedar la cabecera sin sus alumnos.

#### ¿Qué reglas valida la base y cuáles el controlador?

La base: notas de 1 a 10, alumnos sin repetir en un acta, aulas existentes. El controlador: al menos un profesor y la capacidad del aula, antes de guardar.

### Soluciones (docente)

Jefe final del curso (el 42 del índice de `18-Java`, *Caso de la cátedra*), a partir de `Extra/curso-final-paradigmas3-v2.md`, bloque B. El ejemplo guarda la primera acta, rechaza la segunda por capacidad (regla del controlador) y deshace la tercera por la nota 11 (regla de la base), dejando una sola acta guardada. La misión 1 se corrige ejecutando el sistema; el súper test la compila y crea los paneles sin pantalla contra la base del `schema.sql`.

## R05-N09 · La Encrucijada de los Denarios

```meta
tipo: ventana
padre: R05-N08
precio: 10
```

### Crónica

Salís de la sala del Tribunal con el sello del Dragón en la mano. En la plaza central del Imperio hay una fuente con forma de denario gigante, y de ella salen tres avenidas. Al final de una se ve una sala de juegos llena de luces; al final de otra, un río que corre rapidísimo; al final de la tercera, un puerto con barcos que llegan de todo el mundo.

{mentor} te espera sentada en el borde de la fuente, con una taza de café.

—Ya hablás la lengua del Imperio, {heroe}. Lo que sigue no es obligatorio: es **tuyo**. Pero antes de elegir, mirá hacia atrás. ¿Qué te llevás de este viaje?

### Objetivos

- Repasar todo el camino principal y reconocer lo que aprendiste.
- Conocer las Sendas optativas que salen de acá.

### Explicación

#### Lo que ya sabés hacer

- **La Aduana del Compilador**: compilar y ejecutar, tipos, operadores, textos, entrada por teclado, decisiones, bucles, arrays y métodos.
- **La Academia de los Moldes**: clases y objetos, constructores, encapsulamiento, referencias, herencia, polimorfismo, interfaces, composición, `enum`, `record` y diagramas UML.
- **Los Archivos Imperiales**: paquetes y `.jar`, listas, mapas y conjuntos, excepciones, lambdas, pruebas con JUnit y depuración.
- **La Bóveda Imperial**: archivos, SQL con PostgreSQL (tablas, consultas, procedimientos, triggers y roles), JDBC, DAO y transacciones.
- **El Palacio de las Ventanas**: Swing, layouts, componentes, tablas y árboles, MDI, `SwingWorker` y el estilo MVC de la cátedra, hasta un sistema de actas completo.

Con eso podés construir sistemas de gestión de escritorio con base de datos, rendir el final de *Paradigmas y Lenguajes III* y leer el código Java de otros. Lo que sigue son **especializaciones**.

#### Las Sendas

Cada Senda es un camino optativo: no hace falta para completar el curso, y su entrada se paga con **comodines** (los que ganaste con los encargos). Adentro, los nodos se pagan con denarios, como siempre.

- **Senda del Arcade Imperial**: un **juego 2D** con Swing y Java2D: dibujar en un lienzo, el bucle de juego con un `Timer`, teclado, sprites, colisiones y un juego completo.
- **Senda de las Corrientes**: **Java moderno**: *streams*, `Optional`, comparadores avanzados, patrones de diseño y concurrencia con hilos y `ExecutorService`.
- **Senda del Puerto de Spring**: **APIs web con Spring Boot**: proyectos con Maven, controladores REST, capas con DTO y validaciones, Lombok y persistencia con JPA en PostgreSQL.

### Misión R05-N09-M1 · Mirá hacia atrás

```meta
entrega: ninguna
entorno: navegador
monedas: 0
xp: 20
```

#### Consigna

Antes de elegir tu Senda, tomate cinco minutos:

1. ¿Cuál fue el tema que más te costó? ¿Qué te ayudó a entenderlo?
2. ¿Qué programa de todo el camino te dio más orgullo?
3. ¿Qué te gustaría construir ahora con Java?

Charlalo con el profe en la próxima clase (o escribíselo). Cuando lo tengas, marcá la misión como completada.

#### Criterio de aprobación

- Pensaste las tres preguntas y lo charlaste con el profe.

### Prueba del sello

#### ¿Cuántas Sendas salen de la Encrucijada y con qué se paga su entrada?

Tres (el Arcade Imperial, las Corrientes y el Puerto de Spring), y la entrada se paga con comodines.

#### ¿Hace falta completar una Senda para terminar el curso?

No: las Sendas son optativas.

### Soluciones (docente)

Nodo de cierre del tronco (tipo `ventana`), como la Encrucijada de los otros cursos. La misión es de reflexión y no se entrega.

