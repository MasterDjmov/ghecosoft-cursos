# RAMA S01 · Senda del Arcade Imperial: un juego 2D con Swing

```meta
tipo: senda
posicion: 6
```

## S01-N01 · El lienzo y el bucle de juego

```meta
tipo: tema
padre: R05-N09
precio: 3
moneda: comodin
criatura: slime
ejecutable: no
```

### Crónica

Al final de la primera avenida está el **Arcade Imperial**: una sala oscura llena de máquinas con pantallas que brillan. En ninguna hay botones ni formularios: hay figuras que **se mueven solas**, sesenta veces por segundo.

—Hasta ahora tus ventanas esperaban que alguien tocara algo —dice {mentor}—. Un juego no espera: **dibuja, mueve y vuelve a dibujar**, una y otra vez, aunque nadie toque nada. Acá aprendés a pintar en un lienzo y a darle un corazón que late, {heroe}.

### Objetivos

- Dibujar formas, colores y texto en un `JPanel` sobrescribiendo `paintComponent`.
- Usar `Graphics2D` con antialiasing.
- Armar el bucle de juego con un `javax.swing.Timer`: actualizar y redibujar.
- Separar el **estado** del juego (los datos) del **dibujo**.

### Antes de empezar

- La Encrucijada de los Denarios (todo el camino principal, en especial Swing).

### Explicación

#### Dibujar en un panel
Para dibujar a mano, se extiende `JPanel` y se sobrescribe `paintComponent`. Swing lo
llama cada vez que hace falta pintar el panel:
```java
class Lienzo extends JPanel {
    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);                       // primero, el fondo
        Graphics2D g2 = (Graphics2D) g;
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);   // bordes suaves
        g2.setColor(new Color(30, 30, 60));
        g2.fillRect(0, 0, getWidth(), getHeight());     // el cielo
        g2.setColor(Color.YELLOW);
        g2.fillOval(100, 80, 40, 40);                   // un sol
        g2.setColor(Color.WHITE);
        g2.drawString("Puntos: 0", 10, 20);
    }
}
```
El origen `(0, 0)` es la esquina **superior izquierda**; `x` crece hacia la derecha e
`y` **hacia abajo**.

| Método | Dibuja |
|---|---|
| `fillRect(x, y, ancho, alto)` / `drawRect` | un rectángulo relleno / su borde |
| `fillOval(x, y, ancho, alto)` / `drawOval` | un óvalo (círculo si ancho = alto) |
| `drawLine(x1, y1, x2, y2)` | una línea |
| `fillPolygon(xs, ys, n)` | un polígono |
| `drawString(texto, x, y)` | texto (`y` es la base de la letra) |
| `setColor`, `setFont`, `setStroke` | color, letra, grosor de línea |

**Nunca** llames a `paintComponent` vos: para pedir que se redibuje, se llama a
`repaint()`, y Swing lo hace cuando puede (en el EDT).

#### El bucle de juego
Un juego repite siempre lo mismo: **actualizar** el estado (mover, chocar, contar) y
**dibujar**. En Swing, el bucle más simple es un `javax.swing.Timer`, que llama a un
`ActionListener` cada tantos milisegundos, **en el EDT**:
```java
Timer reloj = new Timer(16, e -> {      // unos 60 cuadros por segundo
    actualizar();
    repaint();
});
reloj.start();
```
No uses un `while (true)` con `Thread.sleep` en el EDT: congela la ventana (es el
problema del `SwingWorker`, al revés).

#### Estado y dibujo, separados
El panel **dibuja** lo que dice un objeto `Mundo` que guarda el **estado** (posiciones,
velocidades, puntos) y sabe `actualizar()`. Así la lógica se puede probar sin ventanas
(con JUnit) y el dibujo queda simple.
```java
class Mundo {
    double x = 50, vx = 120;          // posición y velocidad (píxeles por segundo)

    void actualizar(double dt) {      // dt: segundos desde el cuadro anterior
        x += vx * dt;
        if (x > 400 || x < 0) {
            vx = -vx;                 // rebota en los bordes
        }
    }
}
```
Multiplicar la velocidad por `dt` hace que el movimiento sea el mismo aunque el `Timer`
no llegue siempre a tiempo.

### Código de ejemplo

```java
/*
 * El lienzo y el bucle de juego: pelotas que rebotan en la pantalla del Arcade.
 * Ejecutar con: java Rebote.java
 */
import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.SwingUtilities;
import javax.swing.Timer;

public class Rebote {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Arcade Imperial · Rebote");
            Pantalla pantalla = new Pantalla();
            f.setContentPane(pantalla);
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setResizable(false);
            f.setLocationRelativeTo(null);
            f.setVisible(true);
            pantalla.arrancar();
        });
    }
}

class Pelota {
    double x, y, vx, vy;
    final int radio;
    final Color color;

    Pelota(double x, double y, double vx, double vy, int radio, Color color) {
        this.x = x;
        this.y = y;
        this.vx = vx;
        this.vy = vy;
        this.radio = radio;
        this.color = color;
    }
}

class Mundo {
    static final int ANCHO = 480;
    static final int ALTO = 320;
    final List<Pelota> pelotas = new ArrayList<>();
    int rebotes = 0;

    Mundo(long semilla) {
        Random r = new Random(semilla);
        for (int i = 0; i < 6; i++) {
            Color c = Color.getHSBColor(r.nextFloat(), 0.7f, 1f);
            pelotas.add(new Pelota(40 + r.nextInt(ANCHO - 80), 40 + r.nextInt(ALTO - 80),
                    -150 + r.nextInt(300), -150 + r.nextInt(300), 10 + r.nextInt(15), c));
        }
    }

    void actualizar(double dt) {
        for (Pelota p : pelotas) {
            p.x += p.vx * dt;
            p.y += p.vy * dt;
            if (p.x < p.radio || p.x > ANCHO - p.radio) {
                p.vx = -p.vx;
                p.x = Math.max(p.radio, Math.min(ANCHO - p.radio, p.x));
                rebotes++;
            }
            if (p.y < p.radio || p.y > ALTO - p.radio) {
                p.vy = -p.vy;
                p.y = Math.max(p.radio, Math.min(ALTO - p.radio, p.y));
                rebotes++;
            }
        }
    }
}

class Pantalla extends JPanel {
    private final Mundo mundo = new Mundo(2026);
    private final Timer reloj;
    private long ultimo;

    Pantalla() {
        setPreferredSize(new Dimension(Mundo.ANCHO, Mundo.ALTO));
        reloj = new Timer(16, e -> {
            long ahora = System.nanoTime();
            double dt = Math.min(0.05, (ahora - ultimo) / 1e9);    // segundos desde el cuadro anterior
            ultimo = ahora;
            mundo.actualizar(dt);
            repaint();
        });
    }

    void arrancar() {
        ultimo = System.nanoTime();
        reloj.start();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g2.setColor(new Color(20, 20, 40));
        g2.fillRect(0, 0, getWidth(), getHeight());
        for (Pelota p : mundo.pelotas) {
            g2.setColor(p.color);
            g2.fillOval((int) (p.x - p.radio), (int) (p.y - p.radio), p.radio * 2, p.radio * 2);
            g2.setColor(Color.WHITE);
            g2.setStroke(new BasicStroke(2));
            g2.drawOval((int) (p.x - p.radio), (int) (p.y - p.radio), p.radio * 2, p.radio * 2);
        }
        g2.setFont(new Font(Font.MONOSPACED, Font.BOLD, 14));
        g2.setColor(Color.WHITE);
        g2.drawString("Rebotes: " + mundo.rebotes, 10, 20);
    }
}
```

### ¿Para qué sirve?

Dibujar a mano en un panel sirve para juegos, pero también para gráficos de un sistema (un gráfico de barras de ventas, el plano de un salón con las mesas ocupadas, un tablero de ajedrez). El bucle de actualizar y dibujar es la base de todos los motores de juegos, de Minecraft a Unity.

### Errores habituales

**Slime: `paint` en lugar de `paintComponent`.** Sobrescribir `paint` borra los bordes
y los componentes hijos. Va `paintComponent`, llamando primero a
`super.paintComponent(g)`.

**Ogro: el rastro.** Sin `super.paintComponent(g)` (o sin pintar el fondo), cada cuadro
se dibuja encima del anterior y las figuras dejan un rastro.

**Troll: el bucle con `Thread.sleep` en el EDT.** Congela la ventana: nada se
redibuja. Usá un `javax.swing.Timer`.

**Esqueleto: el `Timer` equivocado.** Hay un `java.util.Timer` y un `javax.swing.Timer`.
El de Swing corre en el EDT; el otro no, y tocar la interfaz desde él trae errores.

**Ogro: la velocidad que depende de la compu.** Si movés "5 píxeles por cuadro", en
una compu lenta el juego va más lento. Multiplicá por `dt`.

### Misión S01-N01-M1 · El reloj del Arcade

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Dibujá un **reloj analógico** en un panel de 300×300: el círculo del reloj, las 12
marcas de las horas y dos agujas (minutero y segundero) que se mueven con un `Timer`.
El reloj arranca en 00:00 y avanza **un segundo de juego cada 50 ms** (así se ve moverse
el minutero). Mostrá también la hora en texto abajo (`mm:ss`). La lógica (los segundos
transcurridos y los ángulos) va en una clase `Reloj` separada del dibujo.

#### Criterio de aprobación

- Dibuja con `paintComponent` y `Graphics2D` con antialiasing.
- Usa un `javax.swing.Timer` y `repaint()`.
- La clase `Reloj` calcula los ángulos; el panel solo dibuja.

#### Solución de referencia

```java
// Mision 1 - El reloj del Arcade: dibujar con trigonometria y un Timer.
import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.SwingUtilities;
import javax.swing.Timer;

public class RelojArcade {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Reloj del Arcade");
            f.setContentPane(new PanelReloj());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

class Reloj {
    private int segundos = 0;

    void avanzar() {
        segundos = (segundos + 1) % 3600;
    }

    double anguloSegundero() {
        return Math.toRadians(segundos % 60 * 6);
    }

    double anguloMinutero() {
        return Math.toRadians(segundos / 60.0 * 6);
    }

    String texto() {
        return String.format("%02d:%02d", segundos / 60, segundos % 60);
    }
}

class PanelReloj extends JPanel {
    private final Reloj reloj = new Reloj();

    PanelReloj() {
        setPreferredSize(new Dimension(300, 330));
        new Timer(50, e -> {
            reloj.avanzar();
            repaint();
        }).start();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        int cx = 150;
        int cy = 150;
        int r = 120;
        g2.setColor(new Color(245, 240, 225));
        g2.fillOval(cx - r, cy - r, 2 * r, 2 * r);
        g2.setColor(Color.DARK_GRAY);
        g2.setStroke(new BasicStroke(3));
        g2.drawOval(cx - r, cy - r, 2 * r, 2 * r);
        for (int h = 0; h < 12; h++) {
            double a = Math.toRadians(h * 30);
            g2.drawLine((int) (cx + Math.sin(a) * (r - 15)), (int) (cy - Math.cos(a) * (r - 15)),
                    (int) (cx + Math.sin(a) * r), (int) (cy - Math.cos(a) * r));
        }
        aguja(g2, cx, cy, reloj.anguloMinutero(), r - 35, 5, Color.BLACK);
        aguja(g2, cx, cy, reloj.anguloSegundero(), r - 20, 2, Color.RED);
        g2.setColor(Color.BLACK);
        g2.drawString(reloj.texto(), cx - 18, 320);
    }

    private void aguja(Graphics2D g2, int cx, int cy, double angulo, int largo, int grosor, Color color) {
        g2.setColor(color);
        g2.setStroke(new BasicStroke(grosor));
        g2.drawLine(cx, cy, (int) (cx + Math.sin(angulo) * largo), (int) (cy - Math.cos(angulo) * largo));
    }
}
```

### Misión S01-N01-M2 · La lluvia de estrellas

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Hacé un fondo de **estrellas que caen**: 80 estrellas en posiciones al azar (con
`Random(7)`), cada una con su velocidad (entre 40 y 160 píxeles por segundo) y un tamaño
según la velocidad (las rápidas, más grandes y más brillantes, como si estuvieran más
cerca). Cuando una sale por abajo, vuelve a aparecer arriba en otra `x`. Usá `dt` en la
actualización.

#### Criterio de aprobación

- Las estrellas están en una lista y se actualizan en una clase aparte del dibujo.
- El movimiento usa `dt`.
- Las que salen por abajo reaparecen arriba.

#### Solución de referencia

```java
// Mision 2 - La lluvia de estrellas: muchos objetos, dt y reaparicion.
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.SwingUtilities;
import javax.swing.Timer;

public class LluviaEstrellas {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Lluvia de estrellas");
            f.setContentPane(new PanelCielo());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

class Cielo {
    static final int ANCHO = 400;
    static final int ALTO = 300;
    final List<double[]> estrellas = new ArrayList<>();     // {x, y, velocidad}
    private final Random azar = new Random(7);

    Cielo() {
        for (int i = 0; i < 80; i++) {
            estrellas.add(new double[]{azar.nextInt(ANCHO), azar.nextInt(ALTO), 40 + azar.nextInt(121)});
        }
    }

    void actualizar(double dt) {
        for (double[] e : estrellas) {
            e[1] += e[2] * dt;
            if (e[1] > ALTO) {
                e[1] = 0;
                e[0] = azar.nextInt(ANCHO);
            }
        }
    }
}

class PanelCielo extends JPanel {
    private final Cielo cielo = new Cielo();
    private long ultimo = System.nanoTime();

    PanelCielo() {
        setPreferredSize(new Dimension(Cielo.ANCHO, Cielo.ALTO));
        new Timer(16, e -> {
            long ahora = System.nanoTime();
            cielo.actualizar(Math.min(0.05, (ahora - ultimo) / 1e9));
            ultimo = ahora;
            repaint();
        }).start();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g2.setColor(Color.BLACK);
        g2.fillRect(0, 0, getWidth(), getHeight());
        for (double[] e : cielo.estrellas) {
            int tam = (int) (e[2] / 40);
            int brillo = (int) (95 + e[2]);
            g2.setColor(new Color(brillo, brillo, 255));
            g2.fillOval((int) e[0], (int) e[1], tam, tam);
        }
    }
}
```

### Misión S01-N01-M3 · El dibujo del castillo

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Dibujá (sin animación) un **castillo** del Imperio usando solo figuras: un cielo con un
degradado (`GradientPaint`), el suelo, dos torres con almenas (un bucle de rectángulos),
el portón con arco (un óvalo + un rectángulo), un techo triangular (`fillPolygon`) y una
bandera. Organizá el dibujo en métodos (`dibujarCielo`, `dibujarTorre(x)`, …) y usá
`Graphics2D`.

#### Criterio de aprobación

- Usa `GradientPaint`, `fillPolygon` y un bucle para las almenas.
- El dibujo está repartido en métodos con nombre.

#### Solución de referencia

```java
// Mision 3 - El dibujo del castillo: figuras, degradado y poligonos.
import java.awt.Color;
import java.awt.Dimension;
import java.awt.GradientPaint;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.SwingUtilities;

public class Castillo {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("El castillo del Imperio");
            f.setContentPane(new PanelCastillo());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

class PanelCastillo extends JPanel {
    PanelCastillo() {
        setPreferredSize(new Dimension(420, 300));
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        dibujarCielo(g2);
        dibujarSuelo(g2);
        dibujarMuralla(g2);
        dibujarTorre(g2, 60);
        dibujarTorre(g2, 300);
        dibujarPorton(g2);
    }

    private void dibujarCielo(Graphics2D g2) {
        g2.setPaint(new GradientPaint(0, 0, new Color(40, 60, 140), 0, 230, new Color(250, 170, 110)));
        g2.fillRect(0, 0, getWidth(), 230);
    }

    private void dibujarSuelo(Graphics2D g2) {
        g2.setColor(new Color(70, 120, 60));
        g2.fillRect(0, 230, getWidth(), 70);
    }

    private void dibujarMuralla(Graphics2D g2) {
        g2.setColor(new Color(150, 150, 160));
        g2.fillRect(110, 130, 200, 100);
        almenas(g2, 110, 130, 200);
    }

    private void dibujarTorre(Graphics2D g2, int x) {
        g2.setColor(new Color(130, 130, 145));
        g2.fillRect(x, 90, 60, 140);
        almenas(g2, x, 90, 60);
        g2.setColor(new Color(150, 40, 40));
        g2.fillPolygon(new int[]{x - 5, x + 30, x + 65}, new int[]{80, 30, 80}, 3);
        g2.setColor(Color.DARK_GRAY);
        g2.drawLine(x + 30, 30, x + 30, 10);
        g2.setColor(new Color(240, 200, 60));
        g2.fillPolygon(new int[]{x + 30, x + 50, x + 30}, new int[]{10, 15, 20}, 3);
        g2.setColor(new Color(40, 40, 60));
        g2.fillRect(x + 22, 120, 16, 24);
    }

    private void almenas(Graphics2D g2, int x, int y, int ancho) {
        g2.setColor(new Color(120, 120, 135));
        for (int ax = x; ax < x + ancho; ax += 20) {
            g2.fillRect(ax, y - 12, 10, 12);
        }
    }

    private void dibujarPorton(Graphics2D g2) {
        g2.setColor(new Color(90, 55, 30));
        g2.fillOval(180, 160, 60, 50);
        g2.fillRect(180, 185, 60, 45);
    }
}
```

### Encargo S01-N01-E1 · El gráfico de ventas

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Dibujar a mano no es solo para juegos. Hacé un panel que dibuje un **gráfico de barras**
con las ventas de un comercio en 6 meses (`{120, 340, 280, 410, 190, 360}`): ejes, una
barra por mes con su valor arriba, los nombres de los meses abajo y la barra más alta de
otro color. Las barras tienen que **escalar** al alto del panel (calculá la escala con el
máximo). Bonus: que las barras "crezcan" al abrir la ventana con un `Timer`.

#### Criterio de aprobación

- La escala se calcula a partir del valor máximo y del alto del panel.
- La barra más alta se distingue.

#### Solución de referencia

```java
// Encargo - El grafico de ventas: dibujar datos escalados, con animacion de entrada.
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.SwingUtilities;
import javax.swing.Timer;

public class GraficoVentas {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Ventas del semestre");
            f.setContentPane(new PanelGrafico());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

class PanelGrafico extends JPanel {
    private final int[] ventas = {120, 340, 280, 410, 190, 360};
    private final String[] meses = {"Ene", "Feb", "Mar", "Abr", "May", "Jun"};
    private double progreso = 0;

    PanelGrafico() {
        setPreferredSize(new Dimension(460, 300));
        Timer t = new Timer(16, null);
        t.addActionListener(e -> {
            progreso = Math.min(1, progreso + 0.03);
            repaint();
            if (progreso >= 1) {
                t.stop();
            }
        });
        t.start();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        int margen = 40;
        int base = getHeight() - margen;
        int alto = getHeight() - 2 * margen;
        int max = 0;
        int iMax = 0;
        for (int i = 0; i < ventas.length; i++) {
            if (ventas[i] > max) {
                max = ventas[i];
                iMax = i;
            }
        }
        g2.setColor(Color.BLACK);
        g2.drawLine(margen, base, getWidth() - 10, base);
        g2.drawLine(margen, base, margen, margen - 10);
        int ancho = (getWidth() - margen - 20) / ventas.length;
        for (int i = 0; i < ventas.length; i++) {
            int h = (int) (ventas[i] * alto / (double) max * progreso);
            int x = margen + 10 + i * ancho;
            g2.setColor(i == iMax ? new Color(220, 120, 30) : new Color(60, 120, 200));
            g2.fillRect(x, base - h, ancho - 14, h);
            g2.setColor(Color.BLACK);
            g2.drawString(String.valueOf(ventas[i]), x + 4, base - h - 4);
            g2.drawString(meses[i], x + 6, base + 16);
        }
    }
}
```

### Prueba del sello

#### ¿Qué método se sobrescribe para dibujar en un `JPanel`?

`paintComponent(Graphics g)`, llamando primero a `super.paintComponent(g)`.

#### ¿Dónde está el punto (0, 0) y hacia dónde crece `y`?

En la esquina superior izquierda; `y` crece hacia abajo.

#### ¿Cómo se pide que el panel se vuelva a dibujar?

Con `repaint()`; nunca llamando a `paintComponent` directamente.

#### ¿Por qué el bucle de juego usa un `javax.swing.Timer` y no un `while` con `sleep`?

Porque el `Timer` de Swing llama al código en el EDT sin bloquearlo; un `while` con `sleep` en el EDT congela la ventana.

#### ¿Para qué se multiplica la velocidad por `dt`?

Para que el movimiento dependa del tiempo real y no de cuántos cuadros por segundo logra la compu.

### Soluciones (docente)

Senda nueva: el capítulo 18 de FullCursos no tiene juegos con Swing (los videojuegos del curso original están en C++ con SDL). Usa lo visto en la rama 5 (Swing, EDT) y lo lleva al dibujo a mano. Las prácticas se corrigen ejecutándolas; el súper test las compila y dibuja el primer cuadro sin pantalla.

## S01-N02 · Teclado, movimiento y estados

```meta
tipo: tema
padre: S01-N01
precio: 10
criatura: goblin
ejecutable: no
```

### Crónica

En la máquina del fondo del Arcade, una nave espera en el centro de la pantalla. No se mueve. Tiene el motor encendido, pero nadie la maneja.

—Un juego que no escucha es una película —dice {mentor}—. Enseñale a la nave a **escuchar las teclas**: que avance mientras las apretás y que frene cuando las soltás. Y que el juego sepa **en qué momento está**: esperando, jugando, en pausa o terminado, {heroe}.

### Objetivos

- Leer el teclado con *key bindings* (`InputMap` y `ActionMap`).
- Guardar qué teclas están apretadas para mover de forma continua.
- Mover con velocidad, aceleración y límites de la pantalla.
- Organizar el juego en estados con un `enum`: menú, jugando, pausa, fin.

### Antes de empezar

- El lienzo y el bucle de juego.

### Explicación

#### Dos formas de escuchar el teclado
- `KeyListener`: simple, pero solo funciona si el panel tiene el **foco**, y el foco se
  pierde fácil (un clic en otro lado y el juego deja de responder).
- **Key bindings**: se asocia una tecla con una acción en el `InputMap` y el `ActionMap`
  del panel, y funciona aunque el foco esté en otro componente de la ventana. Es la forma
  recomendada en Swing.
```java
InputMap entrada = getInputMap(WHEN_IN_FOCUSED_WINDOW);
ActionMap acciones = getActionMap();
entrada.put(KeyStroke.getKeyStroke("pressed LEFT"), "izq-apretada");
entrada.put(KeyStroke.getKeyStroke("released LEFT"), "izq-soltada");
acciones.put("izq-apretada", new AbstractAction() {
    @Override
    public void actionPerformed(ActionEvent e) {
        teclas.add("LEFT");
    }
});
```

#### Movimiento continuo: el conjunto de teclas apretadas
Si movés la nave en el evento de la tecla, el movimiento depende de la repetición del
teclado (se traba al principio). Lo correcto es **recordar qué teclas están apretadas**
en un `Set` y, en cada actualización del bucle, mover según ese conjunto:
```java
Set<String> teclas = new HashSet<>();      // "LEFT", "RIGHT", "SPACE"…

void actualizar(double dt) {
    if (teclas.contains("LEFT")) {
        vx -= ACELERACION * dt;
    }
    …
    x += vx * dt;
    vx *= 0.9;                              // rozamiento: frena de a poco
    x = Math.max(0, Math.min(ANCHO - ANCHO_NAVE, x));   // no sale de la pantalla
}
```

#### Estados del juego
Un juego pasa por momentos distintos, y en cada uno las teclas y el dibujo significan
otra cosa. Se modela con un `enum`:
```java
enum Estado { MENU, JUGANDO, PAUSA, FIN }

void actualizar(double dt) {
    switch (estado) {
        case JUGANDO -> moverTodo(dt);
        case MENU, PAUSA, FIN -> { }        // nada se mueve
    }
}
```
El dibujo también mira el estado: en `MENU` muestra el título, en `PAUSA` un cartel
encima del juego, en `FIN` el puntaje final.

#### Un mundo que se puede probar
Como el `Mundo` recibe las teclas como un `Set<String>` y un `dt`, se puede probar con
JUnit sin ventana: "si está apretada RIGHT durante 1 segundo, la nave se mueve a la
derecha", "la nave no sale de la pantalla", "con P el juego pasa a PAUSA".

### Código de ejemplo

```java
/*
 * Teclado, movimiento y estados: la nave del Arcade.
 * Flechas para mover, Espacio para empezar, P para pausa.
 */
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.event.ActionEvent;
import java.util.HashSet;
import java.util.Set;
import javax.swing.AbstractAction;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.KeyStroke;
import javax.swing.SwingUtilities;
import javax.swing.Timer;

public class NaveArcade {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Arcade Imperial · Nave");
            f.setContentPane(new PantallaNave());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setResizable(false);
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

enum Estado { MENU, JUGANDO, PAUSA }

class MundoNave {
    static final int ANCHO = 480;
    static final int ALTO = 320;
    static final double ACELERACION = 900;
    Estado estado = Estado.MENU;
    double x = ANCHO / 2.0, y = ALTO / 2.0, vx, vy;
    double tiempo = 0;

    void tecla(String tecla) {                 // teclas que cambian el estado (al apretar)
        switch (tecla) {
            case "SPACE" -> {
                if (estado == Estado.MENU) {
                    estado = Estado.JUGANDO;
                }
            }
            case "P" -> {
                if (estado == Estado.JUGANDO) {
                    estado = Estado.PAUSA;
                } else if (estado == Estado.PAUSA) {
                    estado = Estado.JUGANDO;
                }
            }
            default -> { }
        }
    }

    void actualizar(double dt, Set<String> apretadas) {
        if (estado != Estado.JUGANDO) {
            return;
        }
        tiempo += dt;
        if (apretadas.contains("LEFT")) {
            vx -= ACELERACION * dt;
        }
        if (apretadas.contains("RIGHT")) {
            vx += ACELERACION * dt;
        }
        if (apretadas.contains("UP")) {
            vy -= ACELERACION * dt;
        }
        if (apretadas.contains("DOWN")) {
            vy += ACELERACION * dt;
        }
        x += vx * dt;
        y += vy * dt;
        vx *= Math.pow(0.05, dt);              // rozamiento que no depende de los cuadros por segundo
        vy *= Math.pow(0.05, dt);
        x = Math.max(15, Math.min(ANCHO - 15, x));
        y = Math.max(15, Math.min(ALTO - 15, y));
    }
}

class PantallaNave extends JPanel {
    private final MundoNave mundo = new MundoNave();
    private final Set<String> apretadas = new HashSet<>();
    private long ultimo = System.nanoTime();

    PantallaNave() {
        setPreferredSize(new Dimension(MundoNave.ANCHO, MundoNave.ALTO));
        for (String t : new String[]{"LEFT", "RIGHT", "UP", "DOWN", "SPACE", "P"}) {
            enlazar(t);
        }
        new Timer(16, e -> {
            long ahora = System.nanoTime();
            mundo.actualizar(Math.min(0.05, (ahora - ultimo) / 1e9), apretadas);
            ultimo = ahora;
            repaint();
        }).start();
    }

    private void enlazar(String tecla) {
        getInputMap(WHEN_IN_FOCUSED_WINDOW).put(KeyStroke.getKeyStroke("pressed " + tecla), tecla + "+");
        getInputMap(WHEN_IN_FOCUSED_WINDOW).put(KeyStroke.getKeyStroke("released " + tecla), tecla + "-");
        getActionMap().put(tecla + "+", new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (apretadas.add(tecla)) {
                    mundo.tecla(tecla);
                }
            }
        });
        getActionMap().put(tecla + "-", new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                apretadas.remove(tecla);
            }
        });
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g2.setColor(new Color(15, 15, 35));
        g2.fillRect(0, 0, getWidth(), getHeight());
        int x = (int) mundo.x;
        int y = (int) mundo.y;
        g2.setColor(new Color(80, 200, 255));
        g2.fillPolygon(new int[]{x, x - 14, x + 14}, new int[]{y - 16, y + 12, y + 12}, 3);
        g2.setColor(Color.WHITE);
        g2.setFont(new Font(Font.MONOSPACED, Font.BOLD, 14));
        g2.drawString(String.format("Tiempo: %.1f s", mundo.tiempo), 10, 20);
        if (mundo.estado == Estado.MENU) {
            cartel(g2, "ARCADE IMPERIAL — Espacio para empezar");
        } else if (mundo.estado == Estado.PAUSA) {
            cartel(g2, "PAUSA — P para seguir");
        }
    }

    private void cartel(Graphics2D g2, String texto) {
        g2.setColor(new Color(0, 0, 0, 170));
        g2.fillRect(0, getHeight() / 2 - 30, getWidth(), 60);
        g2.setColor(Color.YELLOW);
        int ancho = g2.getFontMetrics().stringWidth(texto);
        g2.drawString(texto, (getWidth() - ancho) / 2, getHeight() / 2 + 5);
    }
}
```

### ¿Para qué sirve?

Leer el teclado de forma continua y organizar el programa en estados es la base de cualquier juego, pero la idea de **estados** aparece en todo el software: un pedido (pendiente, pagado, enviado), un cajero automático (esperando tarjeta, pidiendo PIN, operando) o un reproductor (detenido, reproduciendo, en pausa).

### Errores habituales

**Ogro: el juego que no responde.** Con `KeyListener`, si el panel pierde el foco, las
teclas dejan de llegar. Con key bindings y `WHEN_IN_FOCUSED_WINDOW`, no pasa.

**Ogro: el movimiento a los saltos.** Mover la nave dentro del evento de la tecla
depende de la repetición del teclado. Guardá las teclas apretadas en un `Set` y mové en
el bucle.

**Ogro: la nave que se escapa.** Sin limitar la posición al tamaño de la pantalla, la
nave sale y no vuelve.

**Troll: la tecla que queda "pegada".** Si solo escuchás `pressed` y no `released`, la
tecla queda en el conjunto para siempre.

**Ogro: la pausa que no pausa.** Si el `actualizar` no mira el estado, en `PAUSA` todo
sigue moviéndose aunque no se vea el cartel.

### Misión S01-N02-M1 · El mundo probado

```meta
entrega: archivo
entorno: local
extensiones: zip, java
monedas: 4
xp: 10
```

#### Consigna

Escribí pruebas de JUnit para la clase `MundoNave` del ejemplo (copiala a un archivo
propio, sin la parte de Swing), que comprueben:

1. En `MENU`, las flechas no mueven la nave.
2. `SPACE` pasa a `JUGANDO` y `P` alterna entre `JUGANDO` y `PAUSA`.
3. Con `RIGHT` apretada durante un segundo (en pasos de 0.016 s), la nave se movió a la
   derecha.
4. Con `LEFT` apretada mucho tiempo, la nave no pasa del borde izquierdo (`x` ≥ 15).
5. En `PAUSA`, el tiempo no avanza.

#### Criterio de aprobación

- Las cinco pruebas pasan y no abren ninguna ventana.
- Las pruebas simulan el paso del tiempo llamando a `actualizar` en un bucle.

#### Solución de referencia

`Estado.java`

```java
public enum Estado { MENU, JUGANDO, PAUSA }
```

`MundoNave.java`

```java
import java.util.Set;

public class MundoNave {
    static final int ANCHO = 480;
    static final int ALTO = 320;
    static final double ACELERACION = 900;
    Estado estado = Estado.MENU;
    double x = ANCHO / 2.0, y = ALTO / 2.0, vx, vy;
    double tiempo = 0;

    void tecla(String tecla) {
        switch (tecla) {
            case "SPACE" -> {
                if (estado == Estado.MENU) {
                    estado = Estado.JUGANDO;
                }
            }
            case "P" -> {
                if (estado == Estado.JUGANDO) {
                    estado = Estado.PAUSA;
                } else if (estado == Estado.PAUSA) {
                    estado = Estado.JUGANDO;
                }
            }
            default -> { }
        }
    }

    void actualizar(double dt, Set<String> apretadas) {
        if (estado != Estado.JUGANDO) {
            return;
        }
        tiempo += dt;
        if (apretadas.contains("LEFT")) {
            vx -= ACELERACION * dt;
        }
        if (apretadas.contains("RIGHT")) {
            vx += ACELERACION * dt;
        }
        if (apretadas.contains("UP")) {
            vy -= ACELERACION * dt;
        }
        if (apretadas.contains("DOWN")) {
            vy += ACELERACION * dt;
        }
        x += vx * dt;
        y += vy * dt;
        vx *= Math.pow(0.05, dt);
        vy *= Math.pow(0.05, dt);
        x = Math.max(15, Math.min(ANCHO - 15, x));
        y = Math.max(15, Math.min(ALTO - 15, y));
    }
}
```

`MundoNaveTest.java`

```java
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Set;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class MundoNaveTest {
    private MundoNave mundo;

    @BeforeEach
    void preparar() {
        mundo = new MundoNave();
    }

    private void simular(double segundos, Set<String> teclas) {
        for (double t = 0; t < segundos; t += 0.016) {
            mundo.actualizar(0.016, teclas);
        }
    }

    @Test
    void enElMenuLasFlechasNoMueven() {
        simular(1, Set.of("RIGHT"));
        assertEquals(MundoNave.ANCHO / 2.0, mundo.x, 0.001);
    }

    @Test
    void espacioEmpiezaYPAlternaLaPausa() {
        mundo.tecla("SPACE");
        assertEquals(Estado.JUGANDO, mundo.estado);
        mundo.tecla("P");
        assertEquals(Estado.PAUSA, mundo.estado);
        mundo.tecla("P");
        assertEquals(Estado.JUGANDO, mundo.estado);
    }

    @Test
    void conDerechaSeMueveALaDerecha() {
        mundo.tecla("SPACE");
        simular(1, Set.of("RIGHT"));
        assertTrue(mundo.x > MundoNave.ANCHO / 2.0);
    }

    @Test
    void noPasaDelBordeIzquierdo() {
        mundo.tecla("SPACE");
        simular(10, Set.of("LEFT"));
        assertEquals(15, mundo.x, 0.001);
    }

    @Test
    void enPausaElTiempoNoAvanza() {
        mundo.tecla("SPACE");
        simular(1, Set.of());
        double antes = mundo.tiempo;
        mundo.tecla("P");
        simular(1, Set.of());
        assertEquals(antes, mundo.tiempo, 0.0001);
    }
}
```

### Misión S01-N02-M2 · El carro de la mina

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Hacé un juego mínimo: un carro de mina que se mueve **solo en horizontal** sobre un riel
con las flechas (con aceleración y rozamiento) y **salta** con Espacio (con gravedad:
`vy += 900 * dt`, y al tocar el riel vuelve a apoyarse). No puede saltar si ya está en el
aire. Con `Escape` se vuelve al menú (estado `MENU`) y con `Enter` se empieza. La lógica
va en una clase `MundoCarro` separada, con estados en un `enum`.

#### Criterio de aprobación

- Usa key bindings con `pressed` y `released`.
- El salto usa gravedad y no permite saltar en el aire.
- Los estados son un `enum` y el dibujo cambia según el estado.

#### Solución de referencia

```java
// Mision 2 - El carro de la mina: aceleracion, gravedad, salto y estados.
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.event.ActionEvent;
import java.util.HashSet;
import java.util.Set;
import javax.swing.AbstractAction;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.KeyStroke;
import javax.swing.SwingUtilities;
import javax.swing.Timer;

public class CarroMina {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("El carro de la mina");
            f.setContentPane(new PantallaCarro());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

enum EstadoCarro { MENU, JUGANDO }

class MundoCarro {
    static final int ANCHO = 480;
    static final int RIEL = 240;
    EstadoCarro estado = EstadoCarro.MENU;
    double x = 60, y = RIEL, vx, vy;
    boolean enElAire = false;

    void tecla(String t) {
        if (t.equals("ENTER") && estado == EstadoCarro.MENU) {
            estado = EstadoCarro.JUGANDO;
        } else if (t.equals("ESCAPE")) {
            estado = EstadoCarro.MENU;
        } else if (t.equals("SPACE") && estado == EstadoCarro.JUGANDO && !enElAire) {
            vy = -420;
            enElAire = true;
        }
    }

    void actualizar(double dt, Set<String> teclas) {
        if (estado != EstadoCarro.JUGANDO) {
            return;
        }
        if (teclas.contains("LEFT")) {
            vx -= 700 * dt;
        }
        if (teclas.contains("RIGHT")) {
            vx += 700 * dt;
        }
        vx *= Math.pow(0.1, dt);
        x = Math.max(20, Math.min(ANCHO - 20, x + vx * dt));
        if (enElAire) {
            vy += 900 * dt;
            y += vy * dt;
            if (y >= RIEL) {
                y = RIEL;
                vy = 0;
                enElAire = false;
            }
        }
    }
}

class PantallaCarro extends JPanel {
    private final MundoCarro mundo = new MundoCarro();
    private final Set<String> teclas = new HashSet<>();
    private long ultimo = System.nanoTime();

    PantallaCarro() {
        setPreferredSize(new Dimension(MundoCarro.ANCHO, 300));
        for (String t : new String[]{"LEFT", "RIGHT", "SPACE", "ENTER", "ESCAPE"}) {
            getInputMap(WHEN_IN_FOCUSED_WINDOW).put(KeyStroke.getKeyStroke("pressed " + t), t + "+");
            getInputMap(WHEN_IN_FOCUSED_WINDOW).put(KeyStroke.getKeyStroke("released " + t), t + "-");
            getActionMap().put(t + "+", new AbstractAction() {
                @Override
                public void actionPerformed(ActionEvent e) {
                    if (teclas.add(t)) {
                        mundo.tecla(t);
                    }
                }
            });
            getActionMap().put(t + "-", new AbstractAction() {
                @Override
                public void actionPerformed(ActionEvent e) {
                    teclas.remove(t);
                }
            });
        }
        new Timer(16, e -> {
            long ahora = System.nanoTime();
            mundo.actualizar(Math.min(0.05, (ahora - ultimo) / 1e9), teclas);
            ultimo = ahora;
            repaint();
        }).start();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g2.setColor(new Color(50, 35, 30));
        g2.fillRect(0, 0, getWidth(), getHeight());
        g2.setColor(Color.GRAY);
        g2.fillRect(0, MundoCarro.RIEL + 12, getWidth(), 6);
        int x = (int) mundo.x;
        int y = (int) mundo.y;
        g2.setColor(new Color(160, 110, 60));
        g2.fillRect(x - 20, y - 18, 40, 22);
        g2.setColor(Color.DARK_GRAY);
        g2.fillOval(x - 16, y + 2, 10, 10);
        g2.fillOval(x + 6, y + 2, 10, 10);
        if (mundo.estado == EstadoCarro.MENU) {
            g2.setColor(Color.YELLOW);
            g2.drawString("EL CARRO DE LA MINA — Enter para empezar, flechas y Espacio", 60, 120);
        }
    }
}
```

### Misión S01-N02-M3 · El semáforo del cruce

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Los estados no son solo para juegos. Hacé un **semáforo** animado con un `enum
Luz { VERDE, AMARILLA, ROJA }` donde cada valor sabe **cuántos segundos dura** y **cuál
es la siguiente**. Un `Timer` avanza el tiempo; cuando se cumple la duración, el
semáforo pasa a la siguiente luz. Dibujá el semáforo con las tres luces (la activa,
encendida) y la cuenta regresiva. Con la tecla `N` (modo nocturno) el semáforo pasa a
titilar en amarillo; con `N` de nuevo vuelve al ciclo normal.

#### Criterio de aprobación

- El `enum` tiene la duración y la siguiente luz como datos o métodos.
- Hay un modo nocturno que cambia el comportamiento.

#### Solución de referencia

```java
// Mision 3 - El semaforo del cruce: una maquina de estados con un enum.
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.event.ActionEvent;
import javax.swing.AbstractAction;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.KeyStroke;
import javax.swing.SwingUtilities;
import javax.swing.Timer;

public class Semaforo {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Semáforo");
            f.setContentPane(new PanelSemaforo());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

enum Luz {
    VERDE(5), AMARILLA(2), ROJA(4);

    final int segundos;

    Luz(int segundos) {
        this.segundos = segundos;
    }

    Luz siguiente() {
        return switch (this) {
            case VERDE -> AMARILLA;
            case AMARILLA -> ROJA;
            case ROJA -> VERDE;
        };
    }
}

class PanelSemaforo extends JPanel {
    private Luz luz = Luz.VERDE;
    private double enEstaLuz = 0;
    private boolean nocturno = false;
    private double reloj = 0;

    PanelSemaforo() {
        setPreferredSize(new Dimension(160, 330));
        getInputMap(WHEN_IN_FOCUSED_WINDOW).put(KeyStroke.getKeyStroke('n'), "nocturno");
        getInputMap(WHEN_IN_FOCUSED_WINDOW).put(KeyStroke.getKeyStroke('N'), "nocturno");
        getActionMap().put("nocturno", new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                nocturno = !nocturno;
                luz = Luz.VERDE;
                enEstaLuz = 0;
            }
        });
        new Timer(50, e -> {
            reloj += 0.05;
            if (!nocturno) {
                enEstaLuz += 0.05;
                if (enEstaLuz >= luz.segundos) {
                    luz = luz.siguiente();
                    enEstaLuz = 0;
                }
            }
            repaint();
        }).start();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g2.setColor(Color.DARK_GRAY);
        g2.fillRoundRect(40, 20, 80, 240, 20, 20);
        boolean titila = nocturno && ((int) (reloj * 2)) % 2 == 0;
        lampara(g2, 40, !nocturno && luz == Luz.ROJA, Color.RED);
        lampara(g2, 115, (!nocturno && luz == Luz.AMARILLA) || titila, Color.ORANGE);
        lampara(g2, 190, !nocturno && luz == Luz.VERDE, Color.GREEN);
        g2.setColor(Color.BLACK);
        g2.drawString(nocturno ? "modo nocturno" : luz + " " + (int) Math.ceil(luz.segundos - enEstaLuz) + " s", 40, 300);
    }

    private void lampara(Graphics2D g2, int y, boolean encendida, Color color) {
        g2.setColor(encendida ? color : color.darker().darker().darker());
        g2.fillOval(55, y, 50, 50);
    }
}
```

### Encargo S01-N02-E1 · El reproductor de música

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Modelá los estados de un **reproductor**: `DETENIDO`, `REPRODUCIENDO` y `PAUSADO`, con
una lista de 4 temas (nombre y duración en segundos). Botones (o teclas) `Play/Pausa`,
`Stop`, `Siguiente` y `Anterior`. Un `Timer` avanza el tiempo solo cuando está
reproduciendo; al terminar un tema pasa al siguiente (y después del último se detiene).
Mostrá el tema, el estado y una barra de progreso dibujada a mano.

#### Criterio de aprobación

- Los estados son un `enum` y las transiciones tienen sentido (Stop vuelve el tiempo a 0).
- La barra de progreso se dibuja con `paintComponent`.

#### Solución de referencia

```java
// Encargo - El reproductor de musica: estados y una barra dibujada.
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.Graphics;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.SwingUtilities;
import javax.swing.Timer;

public class Reproductor {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Reproductor");
            f.setContentPane(new PanelReproductor());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

enum EstadoReproductor { DETENIDO, REPRODUCIENDO, PAUSADO }

class PanelReproductor extends JPanel {
    private final String[] temas = {"Marcha del Imperio", "Vals de la Bóveda", "Canción del Arcade", "Balada de Kaffa"};
    private final int[] duraciones = {12, 8, 10, 6};
    private int actual = 0;
    private double segundo = 0;
    private EstadoReproductor estado = EstadoReproductor.DETENIDO;

    PanelReproductor() {
        super(new BorderLayout());
        JPanel pantalla = new JPanel() {
            @Override
            protected void paintComponent(Graphics g) {
                super.paintComponent(g);
                g.setColor(new Color(25, 25, 40));
                g.fillRect(0, 0, getWidth(), getHeight());
                g.setColor(Color.WHITE);
                g.drawString(temas[actual] + " (" + estado + ")", 12, 22);
                g.setColor(Color.GRAY);
                g.fillRect(12, 40, getWidth() - 24, 10);
                g.setColor(new Color(90, 200, 120));
                g.fillRect(12, 40, (int) ((getWidth() - 24) * segundo / duraciones[actual]), 10);
                g.setColor(Color.WHITE);
                g.drawString(String.format("%d / %d s", (int) segundo, duraciones[actual]), 12, 70);
            }
        };
        pantalla.setPreferredSize(new Dimension(340, 80));
        JPanel botones = new JPanel(new FlowLayout());
        JButton anterior = new JButton("⏮");
        JButton play = new JButton("⏯");
        JButton stop = new JButton("⏹");
        JButton siguiente = new JButton("⏭");
        botones.add(anterior);
        botones.add(play);
        botones.add(stop);
        botones.add(siguiente);
        add(pantalla, BorderLayout.CENTER);
        add(botones, BorderLayout.SOUTH);
        play.addActionListener(e -> estado = estado == EstadoReproductor.REPRODUCIENDO ? EstadoReproductor.PAUSADO : EstadoReproductor.REPRODUCIENDO);
        stop.addActionListener(e -> {
            estado = EstadoReproductor.DETENIDO;
            segundo = 0;
        });
        siguiente.addActionListener(e -> cambiar(1));
        anterior.addActionListener(e -> cambiar(-1));
        new Timer(100, e -> {
            if (estado == EstadoReproductor.REPRODUCIENDO) {
                segundo += 0.1;
                if (segundo >= duraciones[actual]) {
                    if (actual == temas.length - 1) {
                        estado = EstadoReproductor.DETENIDO;
                        segundo = 0;
                    } else {
                        cambiar(1);
                    }
                }
            }
            pantalla.repaint();
        }).start();
    }

    private void cambiar(int delta) {
        actual = Math.floorMod(actual + delta, temas.length);
        segundo = 0;
    }
}
```

### Prueba del sello

#### ¿Por qué conviene usar key bindings en lugar de `KeyListener`?

Porque funcionan aunque el panel no tenga el foco (con `WHEN_IN_FOCUSED_WINDOW`); con `KeyListener`, si el foco se va, el juego deja de responder.

#### ¿Por qué se guardan las teclas apretadas en un `Set`?

Para mover de forma continua en cada actualización del bucle, sin depender de la repetición del teclado.

#### ¿Qué pasa si no escuchás el evento `released` de una tecla?

La tecla queda "apretada" para siempre en el conjunto.

#### ¿Para qué sirve modelar los estados del juego con un `enum`?

Para que el comportamiento y el dibujo cambien según el momento (menú, jugando, pausa, fin) de forma clara y sin variables booleanas sueltas.

#### ¿Cómo se prueba la lógica de un juego sin abrir ventanas?

Separándola en una clase (el mundo) que recibe las teclas y el `dt`, y llamando a `actualizar` desde JUnit.

### Soluciones (docente)

Nodo nuevo de la Senda. Las pruebas de la misión 1 corren con JUnit (el súper test las ejecuta). El rozamiento con `Math.pow(0.05, dt)` hace que frene igual con cualquier cantidad de cuadros por segundo; un `vx *= 0.9` por cuadro también sirve, pero depende de la velocidad del bucle.

## S01-N03 · Sprites, colisiones y animación

```meta
tipo: tema
padre: S01-N02
precio: 10
criatura: orc
ejecutable: no
```

### Crónica

En la máquina más ruidosa del Arcade, una arquera recoge monedas que caen del cielo mientras esquiva rocas. Cada cosa en pantalla es una figura con su dibujo, su posición y su caja invisible: cuando dos cajas se tocan, algo pasa.

—Un juego es un montón de **entidades** que se mueven y se chocan —dice {mentor}—. Cada una tiene su dibujo, su caja y su manera de actualizarse. Cuando las cajas se tocan: puntos, daño o explosión. Así de simple, {heroe}, y así de poderoso.

### Objetivos

- Representar las cosas del juego como entidades con posición, tamaño y velocidad.
- Detectar colisiones con rectángulos (`Rectangle.intersects`).
- Agregar y quitar entidades de una lista durante el juego sin errores.
- Dibujar sprites con `BufferedImage` y animarlos por cuadros.
- Generar enemigos y objetos al azar con una semilla.

### Antes de empezar

- Teclado, movimiento y estados.
- Herencia, polimorfismo y listas (ramas 2 y 3).

### Explicación

#### Entidades
Todo lo que aparece en el juego (el jugador, las monedas, las rocas) comparte lo mismo:
posición, tamaño, velocidad, cómo se actualiza y cómo se dibuja. Una clase abstracta lo
junta, y cada tipo la especializa (¡polimorfismo!):
```java
abstract class Entidad {
    double x, y, vx, vy;
    final int ancho, alto;
    boolean viva = true;

    void actualizar(double dt) {
        x += vx * dt;
        y += vy * dt;
    }

    Rectangle caja() {
        return new Rectangle((int) x, (int) y, ancho, alto);
    }

    abstract void dibujar(Graphics2D g);
}
```

#### Colisiones con rectángulos
La forma más común de detectar un choque es comparar las **cajas** (rectángulos
alineados con los ejes):
```java
if (jugador.caja().intersects(moneda.caja())) {
    puntos += 10;
    moneda.viva = false;
}
```
`Rectangle.intersects` dice si dos rectángulos se superponen. Para figuras redondas se
puede comparar la distancia entre los centros con la suma de los radios.

#### Agregar y quitar mientras se recorre
Durante el bucle aparecen monedas nuevas y desaparecen las recogidas. Borrar de la
lista mientras se la recorre con un for-each lanza `ConcurrentModificationException`
(lo viste con las colecciones). El patrón seguro:
1. Recorré y **marcá** (`viva = false`) lo que hay que borrar.
2. Al final de la actualización, borrá con `entidades.removeIf(e -> !e.viva)`.
3. Las nuevas se agregan a una lista aparte y se suman al final.

#### Sprites con `BufferedImage`
Un **sprite** es una imagen pequeña. Se puede cargar de un archivo PNG
(`ImageIO.read(new File("moneda.png"))`) o **dibujar una vez** en una `BufferedImage` y
reutilizarla en cada cuadro (más rápido que dibujar figuras cada vez):
```java
BufferedImage moneda = new BufferedImage(16, 16, BufferedImage.TYPE_INT_ARGB);   // con transparencia
Graphics2D g = moneda.createGraphics();
g.setColor(new Color(240, 200, 60));
g.fillOval(0, 0, 16, 16);
g.dispose();
…
g2.drawImage(moneda, (int) x, (int) y, null);
```

#### Animación por cuadros
Una animación son varias imágenes (cuadros) que se alternan. Se guarda un contador de
tiempo y se elige el cuadro según él:
```java
BufferedImage[] cuadros = …;             // por ejemplo, 4 posiciones de una moneda girando
int cuadro = (int) (tiempo * 8) % cuadros.length;    // 8 cuadros por segundo
g2.drawImage(cuadros[cuadro], x, y, null);
```

#### El azar con semilla
Para que el juego sea distinto cada vez, las monedas y rocas aparecen en posiciones al
azar (`Random`). Con una **semilla fija** la partida es siempre igual, lo que sirve para
probar y para comparar puntajes.

### Código de ejemplo

```java
/*
 * Sprites, colisiones y animación: la arquera que junta monedas y esquiva rocas.
 * Flechas izquierda y derecha para moverse.
 */
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Rectangle;
import java.awt.RenderingHints;
import java.awt.event.ActionEvent;
import java.awt.image.BufferedImage;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;
import javax.swing.AbstractAction;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.KeyStroke;
import javax.swing.SwingUtilities;
import javax.swing.Timer;

public class LluviaDeMonedas {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Arcade Imperial · Lluvia de monedas");
            f.setContentPane(new PantallaMonedas());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setResizable(false);
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

abstract class Entidad {
    double x, y, vx, vy;
    final int ancho, alto;
    boolean viva = true;

    Entidad(double x, double y, int ancho, int alto) {
        this.x = x;
        this.y = y;
        this.ancho = ancho;
        this.alto = alto;
    }

    void actualizar(double dt) {
        x += vx * dt;
        y += vy * dt;
    }

    Rectangle caja() {
        return new Rectangle((int) x, (int) y, ancho, alto);
    }

    abstract void dibujar(Graphics2D g, double tiempo);
}

class Arquera extends Entidad {
    Arquera(double x, double y) {
        super(x, y, 28, 28);
    }

    @Override
    void dibujar(Graphics2D g, double tiempo) {
        g.setColor(new Color(90, 200, 120));
        g.fillRoundRect((int) x, (int) y, ancho, alto, 10, 10);
        g.setColor(Color.WHITE);
        g.fillOval((int) x + 7, (int) y + 7, 5, 5);
        g.fillOval((int) x + 16, (int) y + 7, 5, 5);
    }
}

class Moneda extends Entidad {
    static final BufferedImage[] CUADROS = crearCuadros();

    Moneda(double x, double y) {
        super(x, y, 16, 16);
        vy = 120;
    }

    private static BufferedImage[] crearCuadros() {
        BufferedImage[] cuadros = new BufferedImage[4];
        int[] anchos = {16, 11, 4, 11};                 // la moneda "gira": se angosta y se ensancha
        for (int i = 0; i < cuadros.length; i++) {
            cuadros[i] = new BufferedImage(16, 16, BufferedImage.TYPE_INT_ARGB);
            Graphics2D g = cuadros[i].createGraphics();
            g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
            g.setColor(new Color(240, 200, 60));
            g.fillOval((16 - anchos[i]) / 2, 0, anchos[i], 16);
            g.dispose();
        }
        return cuadros;
    }

    @Override
    void dibujar(Graphics2D g, double tiempo) {
        g.drawImage(CUADROS[(int) (tiempo * 10) % CUADROS.length], (int) x, (int) y, null);
    }
}

class Roca extends Entidad {
    Roca(double x, double y) {
        super(x, y, 22, 22);
        vy = 170;
    }

    @Override
    void dibujar(Graphics2D g, double tiempo) {
        g.setColor(new Color(120, 110, 100));
        g.fillOval((int) x, (int) y, ancho, alto);
    }
}

class MundoMonedas {
    static final int ANCHO = 480;
    static final int ALTO = 360;
    final Arquera arquera = new Arquera(ANCHO / 2.0, ALTO - 40);
    final List<Entidad> cosas = new ArrayList<>();
    private final Random azar;
    int puntos = 0;
    int vidas = 3;
    double tiempo = 0;
    private double proxima = 0;

    MundoMonedas(long semilla) {
        azar = new Random(semilla);
    }

    void actualizar(double dt, Set<String> teclas) {
        if (vidas == 0) {
            return;
        }
        tiempo += dt;
        arquera.vx = (teclas.contains("LEFT") ? -260 : 0) + (teclas.contains("RIGHT") ? 260 : 0);
        arquera.actualizar(dt);
        arquera.x = Math.max(0, Math.min(ANCHO - arquera.ancho, arquera.x));

        proxima -= dt;
        if (proxima <= 0) {                                   // aparece algo nuevo
            double x = azar.nextInt(ANCHO - 24);
            cosas.add(azar.nextInt(4) == 0 ? new Roca(x, -24) : new Moneda(x, -16));
            proxima = 0.45;
        }
        for (Entidad e : cosas) {
            e.actualizar(dt);
            if (e.caja().intersects(arquera.caja())) {
                e.viva = false;
                if (e instanceof Moneda) {
                    puntos += 10;
                } else {
                    vidas--;
                }
            } else if (e.y > ALTO) {
                e.viva = false;                               // se fue por abajo
            }
        }
        cosas.removeIf(e -> !e.viva);                         // borrar al final, no durante el recorrido
    }
}

class PantallaMonedas extends JPanel {
    private final MundoMonedas mundo = new MundoMonedas(2026);
    private final Set<String> teclas = new HashSet<>();
    private long ultimo = System.nanoTime();

    PantallaMonedas() {
        setPreferredSize(new Dimension(MundoMonedas.ANCHO, MundoMonedas.ALTO));
        for (String t : new String[]{"LEFT", "RIGHT"}) {
            getInputMap(WHEN_IN_FOCUSED_WINDOW).put(KeyStroke.getKeyStroke("pressed " + t), t + "+");
            getInputMap(WHEN_IN_FOCUSED_WINDOW).put(KeyStroke.getKeyStroke("released " + t), t + "-");
            getActionMap().put(t + "+", new AbstractAction() {
                @Override
                public void actionPerformed(ActionEvent e) {
                    teclas.add(t);
                }
            });
            getActionMap().put(t + "-", new AbstractAction() {
                @Override
                public void actionPerformed(ActionEvent e) {
                    teclas.remove(t);
                }
            });
        }
        new Timer(16, e -> {
            long ahora = System.nanoTime();
            mundo.actualizar(Math.min(0.05, (ahora - ultimo) / 1e9), teclas);
            ultimo = ahora;
            repaint();
        }).start();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g2.setColor(new Color(25, 30, 60));
        g2.fillRect(0, 0, getWidth(), getHeight());
        for (Entidad e : mundo.cosas) {
            e.dibujar(g2, mundo.tiempo);
        }
        mundo.arquera.dibujar(g2, mundo.tiempo);
        g2.setColor(Color.WHITE);
        g2.setFont(new Font(Font.MONOSPACED, Font.BOLD, 14));
        g2.drawString("Puntos: " + mundo.puntos + "   Vidas: " + mundo.vidas, 10, 20);
        if (mundo.vidas == 0) {
            g2.setColor(Color.YELLOW);
            g2.drawString("FIN DEL JUEGO", MundoMonedas.ANCHO / 2 - 55, MundoMonedas.ALTO / 2);
        }
    }
}
```

### ¿Para qué sirve?

Las entidades con caja de colisión son la base de casi todos los juegos 2D (plataformas, naves, deportes). Las mismas ideas aparecen fuera de los juegos: detectar si dos turnos se superponen en una agenda, si un punto del mapa está dentro de una zona de reparto, o si dos elementos de una interfaz se tapan.

### Errores habituales

**Troll: borrar mientras se recorre.** `cosas.remove(e)` dentro del for-each lanza
`ConcurrentModificationException`. Marcá y borrá después con `removeIf`.

**Ogro: la colisión que no se detecta.** Si un objeto se mueve muy rápido, en un cuadro
está antes del jugador y en el siguiente ya pasó: nunca se superponen. Limitá la
velocidad o usá cuadros más cortos.

**Ogro: la lista que crece sin fin.** Si las cosas que salen de la pantalla no se
borran, la lista crece, el juego se pone lento y se queda sin memoria.

**Goblin: la imagen que no se encuentra.** `ImageIO.read` con una ruta equivocada lanza
`IIOException: Can't read input file!`. Revisá la carpeta desde la que ejecutás.

**Ogro: crear la imagen en cada cuadro.** Armar la `BufferedImage` dentro de
`paintComponent` es lentísimo: creala una vez y reutilizala.

### Misión S01-N03-M1 · Las colisiones probadas

```meta
entrega: archivo
entorno: local
extensiones: zip, java
monedas: 4
xp: 10
```

#### Consigna

Escribí una clase `Colisiones` con tres métodos `static` y probala con JUnit:

- `boolean rectangulos(double x1, double y1, double a1, double h1, double x2, double y2, double a2, double h2)`: si dos rectángulos se superponen (sin usar `Rectangle`: con comparaciones).
- `boolean circulos(double x1, double y1, double r1, double x2, double y2, double r2)`: si dos círculos se tocan.
- `boolean puntoEnRectangulo(double px, double py, double x, double y, double a, double h)`.

Las pruebas tienen que cubrir casos que se superponen, que no, que apenas se tocan en
el borde (decidí si cuenta y documentalo) y uno adentro del otro.

#### Criterio de aprobación

- Los tres métodos están implementados con comparaciones.
- Hay al menos ocho pruebas y pasan.

#### Solución de referencia

`Colisiones.java`

```java
/** Detección de colisiones. Tocarse justo en el borde NO cuenta como colisión. */
public final class Colisiones {
    private Colisiones() {
    }

    public static boolean rectangulos(double x1, double y1, double a1, double h1, double x2, double y2, double a2, double h2) {
        return x1 < x2 + a2 && x2 < x1 + a1 && y1 < y2 + h2 && y2 < y1 + h1;
    }

    public static boolean circulos(double x1, double y1, double r1, double x2, double y2, double r2) {
        double dx = x1 - x2;
        double dy = y1 - y2;
        double radios = r1 + r2;
        return dx * dx + dy * dy < radios * radios;
    }

    public static boolean puntoEnRectangulo(double px, double py, double x, double y, double a, double h) {
        return px >= x && px < x + a && py >= y && py < y + h;
    }
}
```

`ColisionesTest.java`

```java
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class ColisionesTest {
    @Test
    void rectangulosSuperpuestos() {
        assertTrue(Colisiones.rectangulos(0, 0, 10, 10, 5, 5, 10, 10));
    }

    @Test
    void rectangulosSeparados() {
        assertFalse(Colisiones.rectangulos(0, 0, 10, 10, 20, 0, 10, 10));
    }

    @Test
    void rectangulosQueSoloSeTocanEnElBordeNoChocan() {
        assertFalse(Colisiones.rectangulos(0, 0, 10, 10, 10, 0, 10, 10));
    }

    @Test
    void unRectanguloAdentroDeOtro() {
        assertTrue(Colisiones.rectangulos(0, 0, 100, 100, 40, 40, 5, 5));
    }

    @Test
    void circulosQueSeTocan() {
        assertTrue(Colisiones.circulos(0, 0, 5, 8, 0, 5));
    }

    @Test
    void circulosLejanos() {
        assertFalse(Colisiones.circulos(0, 0, 5, 30, 30, 5));
    }

    @Test
    void puntoAdentro() {
        assertTrue(Colisiones.puntoEnRectangulo(5, 5, 0, 0, 10, 10));
    }

    @Test
    void puntoEnElBordeDerechoQuedaAfuera() {
        assertFalse(Colisiones.puntoEnRectangulo(10, 5, 0, 0, 10, 10));
    }
}
```

### Misión S01-N03-M2 · Los meteoros

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Hacé una nave que **dispara** (Espacio) contra meteoros que caen. Entidades: `Nave`,
`Disparo` (sube rápido) y `Meteoro` (baja, con tamaño al azar). Cada disparo que toca un
meteoro los destruye a los dos y suma puntos (más puntos cuanto más chico el meteoro). Un
meteoro que toca la nave le quita una vida. Los disparos que salen por arriba se borran.
Solo puede haber 3 disparos a la vez. Usá una clase abstracta `Entidad` y `removeIf`.

#### Criterio de aprobación

- Jerarquía de entidades con una clase abstracta.
- Las colisiones disparo-meteoro y meteoro-nave funcionan.
- No hay `ConcurrentModificationException`: se marca y se borra al final.

#### Solución de referencia

```java
// Mision 2 - Los meteoros: disparos, colisiones entre listas y removeIf.
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Rectangle;
import java.awt.RenderingHints;
import java.awt.event.ActionEvent;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;
import javax.swing.AbstractAction;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.KeyStroke;
import javax.swing.SwingUtilities;
import javax.swing.Timer;

public class Meteoros {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Meteoros");
            f.setContentPane(new PantallaMeteoros());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

abstract class Cuerpo {
    double x, y, vy;
    final int tam;
    boolean vivo = true;

    Cuerpo(double x, double y, int tam, double vy) {
        this.x = x;
        this.y = y;
        this.tam = tam;
        this.vy = vy;
    }

    void mover(double dt) {
        y += vy * dt;
    }

    Rectangle caja() {
        return new Rectangle((int) x, (int) y, tam, tam);
    }

    abstract Color color();
}

class Disparo extends Cuerpo {
    Disparo(double x, double y) {
        super(x, y, 4, -420);
    }

    @Override
    Color color() {
        return Color.YELLOW;
    }
}

class Meteoro extends Cuerpo {
    Meteoro(double x, int tam) {
        super(x, -tam, tam, 90 + 3000.0 / tam);
    }

    @Override
    Color color() {
        return new Color(150, 120, 100);
    }
}

class MundoMeteoros {
    static final int ANCHO = 420;
    static final int ALTO = 360;
    double naveX = ANCHO / 2.0;
    final List<Disparo> disparos = new ArrayList<>();
    final List<Meteoro> meteoros = new ArrayList<>();
    private final Random azar = new Random(11);
    int puntos = 0;
    int vidas = 3;
    private double proximo = 0;

    void disparar() {
        if (disparos.size() < 3 && vidas > 0) {
            disparos.add(new Disparo(naveX + 8, ALTO - 50));
        }
    }

    void actualizar(double dt, Set<String> teclas) {
        if (vidas == 0) {
            return;
        }
        naveX += ((teclas.contains("RIGHT") ? 1 : 0) - (teclas.contains("LEFT") ? 1 : 0)) * 250 * dt;
        naveX = Math.max(0, Math.min(ANCHO - 20, naveX));
        proximo -= dt;
        if (proximo <= 0) {
            meteoros.add(new Meteoro(azar.nextInt(ANCHO - 40), 14 + azar.nextInt(26)));
            proximo = 0.8;
        }
        disparos.forEach(d -> d.mover(dt));
        meteoros.forEach(m -> m.mover(dt));
        Rectangle nave = new Rectangle((int) naveX, ALTO - 40, 20, 20);
        for (Meteoro m : meteoros) {
            for (Disparo d : disparos) {
                if (d.vivo && m.vivo && d.caja().intersects(m.caja())) {
                    d.vivo = false;
                    m.vivo = false;
                    puntos += 400 / m.tam;
                }
            }
            if (m.vivo && m.caja().intersects(nave)) {
                m.vivo = false;
                vidas--;
            }
            if (m.y > ALTO) {
                m.vivo = false;
            }
        }
        disparos.removeIf(d -> !d.vivo || d.y < -10);
        meteoros.removeIf(m -> !m.vivo);
    }
}

class PantallaMeteoros extends JPanel {
    private final MundoMeteoros mundo = new MundoMeteoros();
    private final Set<String> teclas = new HashSet<>();
    private long ultimo = System.nanoTime();

    PantallaMeteoros() {
        setPreferredSize(new Dimension(MundoMeteoros.ANCHO, MundoMeteoros.ALTO));
        for (String t : new String[]{"LEFT", "RIGHT"}) {
            getInputMap(WHEN_IN_FOCUSED_WINDOW).put(KeyStroke.getKeyStroke("pressed " + t), t + "+");
            getInputMap(WHEN_IN_FOCUSED_WINDOW).put(KeyStroke.getKeyStroke("released " + t), t + "-");
            getActionMap().put(t + "+", accion(() -> teclas.add(t)));
            getActionMap().put(t + "-", accion(() -> teclas.remove(t)));
        }
        getInputMap(WHEN_IN_FOCUSED_WINDOW).put(KeyStroke.getKeyStroke("pressed SPACE"), "disparar");
        getActionMap().put("disparar", accion(mundo::disparar));
        new Timer(16, e -> {
            long ahora = System.nanoTime();
            mundo.actualizar(Math.min(0.05, (ahora - ultimo) / 1e9), teclas);
            ultimo = ahora;
            repaint();
        }).start();
    }

    private AbstractAction accion(Runnable r) {
        return new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                r.run();
            }
        };
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g2.setColor(Color.BLACK);
        g2.fillRect(0, 0, getWidth(), getHeight());
        for (Cuerpo c : mundo.meteoros) {
            g2.setColor(c.color());
            g2.fillOval((int) c.x, (int) c.y, c.tam, c.tam);
        }
        for (Cuerpo c : mundo.disparos) {
            g2.setColor(c.color());
            g2.fillRect((int) c.x, (int) c.y, c.tam, 10);
        }
        g2.setColor(new Color(80, 200, 255));
        int x = (int) mundo.naveX;
        g2.fillPolygon(new int[]{x + 10, x, x + 20}, new int[]{MundoMeteoros.ALTO - 44, MundoMeteoros.ALTO - 20, MundoMeteoros.ALTO - 20}, 3);
        g2.setColor(Color.WHITE);
        g2.drawString("Puntos: " + mundo.puntos + "  Vidas: " + mundo.vidas, 10, 18);
    }
}
```

### Misión S01-N03-M3 · El caminante animado

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Armá una **animación por cuadros**: generá por código 4 cuadros de un personaje
caminando (en `BufferedImage`, por ejemplo moviendo las piernas en cada cuadro) y otros
4 caminando hacia la izquierda (espejados con `AffineTransform` o dibujados al revés).
El personaje camina de un lado al otro de la pantalla; cuando llega al borde, se da vuelta
y usa la otra animación. La velocidad de la animación (cuadros por segundo) se puede
cambiar con las flechas arriba y abajo, y se muestra en pantalla.

#### Criterio de aprobación

- Los cuadros se crean una sola vez, en `BufferedImage`.
- El cuadro que se muestra depende del tiempo y de la velocidad de animación.
- El personaje cambia de animación al darse vuelta.

#### Solución de referencia

```java
// Mision 3 - El caminante animado: cuadros en BufferedImage y animacion por tiempo.
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.event.ActionEvent;
import java.awt.image.BufferedImage;
import javax.swing.AbstractAction;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.KeyStroke;
import javax.swing.SwingUtilities;
import javax.swing.Timer;

public class Caminante {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("El caminante");
            f.setContentPane(new PanelCaminante());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

class PanelCaminante extends JPanel {
    private final BufferedImage[] derecha = new BufferedImage[4];
    private final BufferedImage[] izquierda = new BufferedImage[4];
    private double x = 20;
    private int direccion = 1;
    private double tiempo = 0;
    private int cuadrosPorSegundo = 8;

    PanelCaminante() {
        setPreferredSize(new Dimension(420, 160));
        int[] piernas = {-6, 0, 6, 0};
        for (int i = 0; i < 4; i++) {
            derecha[i] = cuadro(piernas[i], false);
            izquierda[i] = cuadro(piernas[i], true);
        }
        getInputMap(WHEN_IN_FOCUSED_WINDOW).put(KeyStroke.getKeyStroke("pressed UP"), "mas");
        getInputMap(WHEN_IN_FOCUSED_WINDOW).put(KeyStroke.getKeyStroke("pressed DOWN"), "menos");
        getActionMap().put("mas", new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                cuadrosPorSegundo = Math.min(30, cuadrosPorSegundo + 2);
            }
        });
        getActionMap().put("menos", new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                cuadrosPorSegundo = Math.max(2, cuadrosPorSegundo - 2);
            }
        });
        new Timer(16, e -> {
            tiempo += 0.016;
            x += direccion * 90 * 0.016;
            if (x > getWidth() - 40 || x < 0) {
                direccion = -direccion;
                x = Math.max(0, Math.min(getWidth() - 40, x));
            }
            repaint();
        }).start();
    }

    private BufferedImage cuadro(int paso, boolean espejo) {
        BufferedImage img = new BufferedImage(40, 60, BufferedImage.TYPE_INT_ARGB);
        Graphics2D g = img.createGraphics();
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        if (espejo) {
            g.translate(40, 0);
            g.scale(-1, 1);
        }
        g.setColor(new Color(240, 200, 160));
        g.fillOval(12, 2, 16, 16);
        g.setColor(new Color(60, 110, 200));
        g.fillRect(14, 18, 12, 22);
        g.setColor(Color.DARK_GRAY);
        g.fillRect(15 + paso, 40, 5, 18);
        g.fillRect(21 - paso, 40, 5, 18);
        g.setColor(Color.WHITE);
        g.fillOval(22, 7, 4, 4);
        g.dispose();
        return img;
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        g.setColor(new Color(200, 230, 255));
        g.fillRect(0, 0, getWidth(), getHeight());
        g.setColor(new Color(90, 160, 80));
        g.fillRect(0, 120, getWidth(), 40);
        BufferedImage[] animacion = direccion > 0 ? derecha : izquierda;
        int cuadro = (int) (tiempo * cuadrosPorSegundo) % animacion.length;
        g.drawImage(animacion[cuadro], (int) x, 62, null);
        g.setColor(Color.BLACK);
        g.drawString("Animación: " + cuadrosPorSegundo + " cuadros por segundo (flechas arriba y abajo)", 10, 18);
    }
}
```

### Encargo S01-N03-E1 · El salón de las mesas

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Las colisiones sirven fuera de los juegos. Hacé el **plano de un salón** con 8 mesas
(rectángulos) dibujadas en un panel. Al hacer clic en una mesa, se marca como ocupada (o
se libera si ya lo estaba); para saber qué mesa se tocó, usá un "punto dentro de
rectángulo" con la posición del mouse (`MouseListener`). Las mesas ocupadas se dibujan
en rojo y las libres en verde, y arriba se muestra cuántas hay libres. Una mesa se puede
**arrastrar** para reacomodar el salón, pero no se puede soltar encima de otra (si choca,
vuelve a su lugar).

#### Criterio de aprobación

- Usa `MouseListener`/`MouseMotionListener` y detecta la mesa con un punto en rectángulo.
- Al arrastrar, detecta el choque con las otras mesas.

#### Solución de referencia

```java
// Encargo - El salon de las mesas: clic y arrastre con deteccion de colisiones.
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Point;
import java.awt.Rectangle;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.util.ArrayList;
import java.util.List;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.SwingUtilities;

public class SalonMesas {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Salón de la posada");
            f.setContentPane(new PanelSalon());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

class Mesa {
    final Rectangle forma;
    final int numero;
    boolean ocupada;

    Mesa(int numero, int x, int y) {
        this.numero = numero;
        this.forma = new Rectangle(x, y, 60, 40);
    }
}

class PanelSalon extends JPanel {
    private final List<Mesa> mesas = new ArrayList<>();
    private Mesa arrastrada;
    private Point desde;
    private Point origen;
    private boolean movio;

    PanelSalon() {
        setPreferredSize(new Dimension(420, 300));
        for (int i = 0; i < 8; i++) {
            mesas.add(new Mesa(i + 1, 30 + (i % 4) * 95, 60 + (i / 4) * 110));
        }
        MouseAdapter mouse = new MouseAdapter() {
            @Override
            public void mousePressed(MouseEvent e) {
                arrastrada = mesaEn(e.getPoint());
                if (arrastrada != null) {
                    desde = e.getPoint();
                    origen = arrastrada.forma.getLocation();
                    movio = false;
                }
            }

            @Override
            public void mouseDragged(MouseEvent e) {
                if (arrastrada != null) {
                    arrastrada.forma.setLocation(origen.x + e.getX() - desde.x, origen.y + e.getY() - desde.y);
                    movio = true;
                    repaint();
                }
            }

            @Override
            public void mouseReleased(MouseEvent e) {
                if (arrastrada == null) {
                    return;
                }
                if (!movio) {
                    arrastrada.ocupada = !arrastrada.ocupada;
                } else if (chocaConOtra(arrastrada)) {
                    arrastrada.forma.setLocation(origen);
                }
                arrastrada = null;
                repaint();
            }
        };
        addMouseListener(mouse);
        addMouseMotionListener(mouse);
    }

    private Mesa mesaEn(Point p) {
        for (Mesa m : mesas) {
            if (m.forma.contains(p)) {
                return m;
            }
        }
        return null;
    }

    private boolean chocaConOtra(Mesa mesa) {
        for (Mesa m : mesas) {
            if (m != mesa && m.forma.intersects(mesa.forma)) {
                return true;
            }
        }
        return false;
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        long libres = mesas.stream().filter(m -> !m.ocupada).count();
        g.setColor(Color.BLACK);
        g.drawString("Mesas libres: " + libres + " de " + mesas.size() + " (clic: ocupar/liberar, arrastrar: mover)", 10, 20);
        for (Mesa m : mesas) {
            g.setColor(m.ocupada ? new Color(220, 80, 70) : new Color(90, 180, 100));
            g.fillRoundRect(m.forma.x, m.forma.y, m.forma.width, m.forma.height, 10, 10);
            g.setColor(Color.WHITE);
            g.drawString("Mesa " + m.numero, m.forma.x + 8, m.forma.y + 24);
        }
    }
}
```

### Prueba del sello

#### ¿Qué tiene en común toda entidad de un juego?

Posición, tamaño, velocidad, una forma de actualizarse y una forma de dibujarse (y una caja para las colisiones).

#### ¿Cómo se detecta si dos rectángulos se superponen?

Con `Rectangle.intersects`, o comparando que cada uno empiece antes de que termine el otro en los dos ejes.

#### ¿Cómo se borran entidades de una lista mientras se la recorre?

Marcándolas (`viva = false`) y borrándolas al final con `removeIf`.

#### ¿Por qué conviene crear los sprites una sola vez en una `BufferedImage`?

Porque crearlos o dibujarlos desde cero en cada cuadro es mucho más lento.

#### ¿Cómo se elige qué cuadro de una animación mostrar?

Con el tiempo transcurrido: `(int) (tiempo * cuadrosPorSegundo) % cantidadDeCuadros`.

### Soluciones (docente)

Nodo nuevo de la Senda. La misión 1 corre con JUnit en el súper test; las demás se corrigen ejecutándolas. En el ejemplo, las rocas y las monedas salen de una semilla fija, así la partida es igual cada vez.

## S01-N04 · Jefe del Arcade: el Guardián de la Máquina

```meta
tipo: jefe
padre: S01-N03
precio: 10
criatura: dragon
insignia: Campeón del Arcade
insignia_descripcion: Venciste al Guardián de la Máquina: programaste un juego 2D completo en Java.
```

### Crónica

La última máquina del Arcade está apagada. Tiene un cartel escrito a mano: *"Juego no incluido"*. Adentro solo hay una pantalla negra y un joystick.

—El Guardián de la Máquina no se vence jugando —dice {mentor}, sonriendo detrás de su taza—. Se vence **haciendo el juego**. Menú, niveles, puntos, vidas, un final. Todo lo que aprendiste en la Senda, junto. Es tu máquina, {heroe}: que tenga tu nombre.

### Objetivos

- Construir un juego 2D completo con estados, entidades, colisiones, puntaje y niveles.
- Guardar el mejor puntaje en un archivo entre partidas.
- Organizar el juego en clases: mundo, entidades, estados, pantalla.

### Antes de empezar

- Toda la Senda del Arcade.

### Explicación

#### La estructura de un juego completo
```
Juego (main)            → crea la ventana
Pantalla (JPanel)       → teclado, bucle con Timer, dibujo según el estado
Mundo                   → el estado del juego: entidades, puntos, vidas, nivel, estado
Entidad y subclases     → jugador, enemigos, objetos
Records (archivo)       → lee y guarda el mejor puntaje
```
El **mundo** no sabe nada de Swing: recibe teclas y `dt`, y se puede probar con JUnit.
La **pantalla** no tiene reglas del juego: dibuja lo que el mundo dice.

#### Niveles
Un nivel es una **configuración**: más enemigos, más velocidad, menos tiempo. Se puede
guardar en un `record` o calcular a partir del número de nivel:
```java
record Nivel(int numero, double velocidadEnemigos, double segundosEntreEnemigos, int puntosParaPasar) {
    static Nivel numero(int n) {
        return new Nivel(n, 100 + n * 30, Math.max(0.25, 1.0 - n * 0.12), n * 100);
    }
}
```

#### El mejor puntaje
Se guarda en un archivo de texto con `Files.writeString` al terminar la partida, y se
lee al arrancar (si el archivo no existe, el récord es 0). Todo lo que viste en la rama
de archivos, al servicio del juego.

### Código de ejemplo

El esqueleto de un juego completo: el mundo con estados, niveles y récord, separado de
la pantalla. Este ejemplo es de consola a propósito: **simula** una partida entera sin
ventana (con teclas preprogramadas) para mostrar que el mundo funciona solo, igual que
en una prueba.

```java
/*
 * Jefe del Arcade: el mundo de un juego completo, probado sin ventana.
 * Simula una partida con teclas preprogramadas y muestra cómo cambian los estados.
 */
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Random;
import java.util.Set;

public class SimulacionArcade {
    public static void main(String[] args) throws IOException {
        Locale.setDefault(Locale.US);
        Path archivoRecord = Path.of("record.txt");
        Files.deleteIfExists(archivoRecord);
        MundoJuego mundo = new MundoJuego(42, new Records(archivoRecord));
        System.out.println("Estado inicial: " + mundo.estado + ", récord " + mundo.record());
        mundo.tecla("ENTER");

        // Una "jugadora" automática: persigue la moneda más baja y esquiva a los enemigos cercanos
        String estadoAnterior = "";
        for (int cuadro = 0; cuadro < 60 * 90 && mundo.estado != EstadoJuego.FIN; cuadro++) {
            mundo.actualizar(1.0 / 60, mundo.decidir());
            String estado = mundo.estado + " nivel " + mundo.nivel.numero();
            if (!estado.equals(estadoAnterior)) {
                System.out.printf("t=%5.1f s  %-22s puntos %4d  vidas %d%n", cuadro / 60.0, estado, mundo.puntos, mundo.vidas);
                estadoAnterior = estado;
            }
        }
        if (mundo.estado != EstadoJuego.FIN) {
            System.out.println("La jugadora deja la máquina a los 90 segundos");
            mundo.terminar();
        }
        System.out.println("Fin: " + mundo.puntos + " puntos. Récord guardado: " + mundo.record());
        Files.deleteIfExists(archivoRecord);
    }
}

enum EstadoJuego { MENU, JUGANDO, NIVEL_SUPERADO, FIN }

record Nivel(int numero, double velocidadEnemigos, double segundosEntreEnemigos, int puntosParaPasar) {
    static Nivel numero(int n) {
        return new Nivel(n, 90 + n * 35, Math.max(0.3, 1.1 - n * 0.2), n * 60);
    }
}

class Objeto {
    double x, y;
    final double vy;
    final boolean esMoneda;
    boolean vivo = true;

    Objeto(double x, double y, double vy, boolean esMoneda) {
        this.x = x;
        this.y = y;
        this.vy = vy;
        this.esMoneda = esMoneda;
    }
}

class Records {
    private final Path archivo;

    Records(Path archivo) {
        this.archivo = archivo;
    }

    int leer() {
        try {
            return Files.exists(archivo) ? Integer.parseInt(Files.readString(archivo).trim()) : 0;
        } catch (IOException | NumberFormatException e) {
            return 0;
        }
    }

    void guardarSiEsMejor(int puntos) {
        if (puntos > leer()) {
            try {
                Files.writeString(archivo, String.valueOf(puntos));
            } catch (IOException e) {
                // sin récord no se corta el juego
            }
        }
    }
}

class MundoJuego {
    static final int ANCHO = 480;
    static final int ALTO = 360;
    EstadoJuego estado = EstadoJuego.MENU;
    Nivel nivel = Nivel.numero(1);
    double jugadorX = ANCHO / 2.0;
    final List<Objeto> objetos = new ArrayList<>();
    int puntos = 0;
    int vidas = 3;
    private double proximo = 0;
    private double pausaNivel = 0;
    private final Random azar;
    private final Records records;

    MundoJuego(long semilla, Records records) {
        this.azar = new Random(semilla);
        this.records = records;
    }

    int record() {
        return records.leer();
    }

    void tecla(String t) {
        if (t.equals("ENTER") && (estado == EstadoJuego.MENU || estado == EstadoJuego.FIN)) {
            estado = EstadoJuego.JUGANDO;
            puntos = 0;
            vidas = 3;
            nivel = Nivel.numero(1);
            objetos.clear();
        }
    }

    void terminar() {
        estado = EstadoJuego.FIN;
        records.guardarSiEsMejor(puntos);
    }

    Set<String> decidir() {
        Objeto objetivo = null;
        for (Objeto o : objetos) {
            if (o.esMoneda && (objetivo == null || o.y > objetivo.y)) {
                objetivo = o;
            }
        }
        for (Objeto o : objetos) {
            if (!o.esMoneda && o.y > ALTO - 120 && Math.abs(o.x - jugadorX) < 30) {
                return Set.of(o.x > jugadorX ? "LEFT" : "RIGHT");
            }
        }
        if (objetivo == null || Math.abs(objetivo.x - jugadorX) < 6) {
            return Set.of();
        }
        return Set.of(objetivo.x > jugadorX ? "RIGHT" : "LEFT");
    }

    void actualizar(double dt, Set<String> teclas) {
        if (estado == EstadoJuego.NIVEL_SUPERADO) {
            pausaNivel -= dt;
            if (pausaNivel <= 0) {
                nivel = Nivel.numero(nivel.numero() + 1);
                objetos.clear();
                estado = EstadoJuego.JUGANDO;
            }
            return;
        }
        if (estado != EstadoJuego.JUGANDO) {
            return;
        }
        jugadorX += ((teclas.contains("RIGHT") ? 1 : 0) - (teclas.contains("LEFT") ? 1 : 0)) * 240 * dt;
        jugadorX = Math.max(10, Math.min(ANCHO - 10, jugadorX));
        proximo -= dt;
        if (proximo <= 0) {
            boolean moneda = azar.nextInt(3) > 0;
            objetos.add(new Objeto(10 + azar.nextInt(ANCHO - 20), -10, moneda ? 110 : nivel.velocidadEnemigos(), moneda));
            proximo = nivel.segundosEntreEnemigos();
        }
        for (Objeto o : objetos) {
            o.y += o.vy * dt;
            boolean toca = Math.abs(o.x - jugadorX) < 18 && Math.abs(o.y - (ALTO - 30)) < 18;
            if (toca) {
                o.vivo = false;
                if (o.esMoneda) {
                    puntos += 10;
                } else {
                    vidas--;
                }
            } else if (o.y > ALTO) {
                o.vivo = false;
            }
        }
        objetos.removeIf(o -> !o.vivo);
        if (vidas <= 0) {
            estado = EstadoJuego.FIN;
            records.guardarSiEsMejor(puntos);
        } else if (puntos >= nivel.puntosParaPasar() && nivel.numero() < 5) {
            estado = EstadoJuego.NIVEL_SUPERADO;
            pausaNivel = 2;
        }
    }
}
```

### Salida esperada

```
Estado inicial: MENU, récord 0
t=  0.0 s  JUGANDO nivel 1        puntos    0  vidas 3
t= 11.0 s  NIVEL_SUPERADO nivel 1 puntos   60  vidas 3
t= 13.0 s  JUGANDO nivel 2        puntos   60  vidas 3
t= 20.8 s  NIVEL_SUPERADO nivel 2 puntos  120  vidas 3
t= 22.9 s  JUGANDO nivel 3        puntos  120  vidas 3
t= 30.0 s  NIVEL_SUPERADO nivel 3 puntos  180  vidas 3
t= 32.0 s  JUGANDO nivel 4        puntos  180  vidas 3
t= 39.9 s  NIVEL_SUPERADO nivel 4 puntos  240  vidas 3
t= 42.0 s  JUGANDO nivel 5        puntos  240  vidas 3
La jugadora deja la máquina a los 90 segundos
Fin: 720 puntos. Récord guardado: 720
```

### ¿Para qué sirve?

Terminar un juego completo enseña lo que ningún ejercicio suelto enseña: organizar un programa que crece, decidir qué va en cada clase y probar lo que no se puede ver. Además, un juego terminado es la mejor carta de presentación para un portfolio o una entrevista.

### Errores habituales

**Dragón: el juego en una sola clase.** Con las reglas, el dibujo y el teclado mezclados
en el `paintComponent`, cada cambio rompe algo. Separá mundo y pantalla.

**Ogro: el nivel que no reinicia.** Al pasar de nivel o volver a empezar, hay que
limpiar las listas y reiniciar los contadores; si no, el nivel nuevo arranca con los
enemigos del anterior.

**Goblin: el archivo del récord roto.** Si alguien edita `record.txt` y deja una letra,
`parseInt` corta el juego. Atrapá la excepción y usá 0.

**Ogro: el juego imposible.** Si la dificultad crece sin tope, en el nivel 10 no se
puede jugar. Poné límites (`Math.max`, un nivel máximo).

### Misión S01-N04-M1 · Tu juego del Arcade

```meta
entrega: archivo
entorno: local
extensiones: zip
monedas: 6
xp: 40
```

#### Consigna

Programá **tu** juego 2D completo con Swing. Puede ser el de la simulación del ejemplo
con ventana, o uno propio (un *breakout*, un *snake*, un juego de plataformas simple).
Tiene que tener:

1. Estados: menú, jugando, pausa, nivel superado y fin, con lo que se ve en cada uno.
2. Al menos dos tipos de entidades con una jerarquía (clase abstracta o interfaz).
3. Colisiones, puntaje y vidas.
4. Al menos 3 niveles que aumentan la dificultad.
5. El mejor puntaje guardado en un archivo.
6. El mundo separado de la pantalla, con **al menos 4 pruebas de JUnit** del mundo.

Entregá un zip con el código, las pruebas y un `LEEME.txt` con las teclas y cómo
compilar.

#### Criterio de aprobación

- Se cumplen los seis puntos y el juego se puede jugar de principio a fin.
- Las pruebas del mundo pasan sin abrir ventanas.

#### Solución de referencia

`Juego.java`

```java
// Jefe S01 - Mision 1 (referencia): la simulacion del ejemplo, con ventana.
// Se juega con las flechas; Enter empieza, P pausa.
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.event.ActionEvent;
import java.nio.file.Path;
import java.util.HashSet;
import java.util.Set;
import javax.swing.AbstractAction;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.KeyStroke;
import javax.swing.SwingUtilities;
import javax.swing.Timer;

public class Juego {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("Arcade Imperial");
            f.setContentPane(new PantallaJuego());
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            f.pack();
            f.setResizable(false);
            f.setLocationRelativeTo(null);
            f.setVisible(true);
        });
    }
}

class PantallaJuego extends JPanel {
    private final MundoJuego mundo = new MundoJuego(System.nanoTime(), new Records(Path.of("record.txt")));
    private final Set<String> teclas = new HashSet<>();
    private boolean pausa = false;
    private long ultimo = System.nanoTime();

    PantallaJuego() {
        setPreferredSize(new Dimension(MundoJuego.ANCHO, MundoJuego.ALTO));
        for (String t : new String[]{"LEFT", "RIGHT"}) {
            getInputMap(WHEN_IN_FOCUSED_WINDOW).put(KeyStroke.getKeyStroke("pressed " + t), t + "+");
            getInputMap(WHEN_IN_FOCUSED_WINDOW).put(KeyStroke.getKeyStroke("released " + t), t + "-");
            getActionMap().put(t + "+", accion(() -> teclas.add(t)));
            getActionMap().put(t + "-", accion(() -> teclas.remove(t)));
        }
        getInputMap(WHEN_IN_FOCUSED_WINDOW).put(KeyStroke.getKeyStroke("pressed ENTER"), "enter");
        getActionMap().put("enter", accion(() -> mundo.tecla("ENTER")));
        getInputMap(WHEN_IN_FOCUSED_WINDOW).put(KeyStroke.getKeyStroke("pressed P"), "pausa");
        getActionMap().put("pausa", accion(() -> pausa = !pausa && mundo.estado == EstadoJuego.JUGANDO));
        new Timer(16, e -> {
            long ahora = System.nanoTime();
            if (!pausa) {
                mundo.actualizar(Math.min(0.05, (ahora - ultimo) / 1e9), teclas);
            }
            ultimo = ahora;
            repaint();
        }).start();
    }

    private AbstractAction accion(Runnable r) {
        return new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                r.run();
            }
        };
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g2.setColor(new Color(20, 22, 45));
        g2.fillRect(0, 0, getWidth(), getHeight());
        for (Objeto o : mundo.objetos) {
            g2.setColor(o.esMoneda ? new Color(240, 200, 60) : new Color(200, 70, 70));
            g2.fillOval((int) o.x - 8, (int) o.y - 8, 16, 16);
        }
        g2.setColor(new Color(90, 200, 120));
        g2.fillRoundRect((int) mundo.jugadorX - 14, MundoJuego.ALTO - 44, 28, 28, 8, 8);
        g2.setColor(Color.WHITE);
        g2.setFont(new Font(Font.MONOSPACED, Font.BOLD, 14));
        g2.drawString("Nivel " + mundo.nivel.numero() + "  Puntos " + mundo.puntos + "  Vidas " + mundo.vidas + "  Récord " + mundo.record(), 10, 20);
        String cartel = switch (mundo.estado) {
            case MENU -> "ARCADE IMPERIAL — Enter para jugar";
            case NIVEL_SUPERADO -> "¡Nivel superado!";
            case FIN -> "FIN — " + mundo.puntos + " puntos. Enter para jugar de nuevo";
            case JUGANDO -> pausa ? "PAUSA" : null;
        };
        if (cartel != null) {
            g2.setColor(Color.YELLOW);
            int ancho = g2.getFontMetrics().stringWidth(cartel);
            g2.drawString(cartel, (getWidth() - ancho) / 2, getHeight() / 2);
        }
    }
}
```

`EstadoJuego.java`

```java
public enum EstadoJuego { MENU, JUGANDO, NIVEL_SUPERADO, FIN }
```

`Nivel.java`

```java
public record Nivel(int numero, double velocidadEnemigos, double segundosEntreEnemigos, int puntosParaPasar) {
    static Nivel numero(int n) {
        return new Nivel(n, 90 + n * 35, Math.max(0.3, 1.1 - n * 0.2), n * 60);
    }
}
```

`Objeto.java`

```java
public class Objeto {
    double x, y;
    final double vy;
    final boolean esMoneda;
    boolean vivo = true;

    Objeto(double x, double y, double vy, boolean esMoneda) {
        this.x = x;
        this.y = y;
        this.vy = vy;
        this.esMoneda = esMoneda;
    }
}
```

`Records.java`

```java
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class Records {
    private final Path archivo;

    Records(Path archivo) {
        this.archivo = archivo;
    }

    int leer() {
        try {
            return Files.exists(archivo) ? Integer.parseInt(Files.readString(archivo).trim()) : 0;
        } catch (IOException | NumberFormatException e) {
            return 0;
        }
    }

    void guardarSiEsMejor(int puntos) {
        if (puntos > leer()) {
            try {
                Files.writeString(archivo, String.valueOf(puntos));
            } catch (IOException e) {
                // sin récord no se corta el juego
            }
        }
    }
}
```

`MundoJuego.java`

```java
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.Set;

public class MundoJuego {
    static final int ANCHO = 480;
    static final int ALTO = 360;
    EstadoJuego estado = EstadoJuego.MENU;
    Nivel nivel = Nivel.numero(1);
    double jugadorX = ANCHO / 2.0;
    final List<Objeto> objetos = new ArrayList<>();
    int puntos = 0;
    int vidas = 3;
    private double proximo = 0;
    private double pausaNivel = 0;
    private final Random azar;
    private final Records records;

    MundoJuego(long semilla, Records records) {
        this.azar = new Random(semilla);
        this.records = records;
    }

    int record() {
        return records.leer();
    }

    void tecla(String t) {
        if (t.equals("ENTER") && (estado == EstadoJuego.MENU || estado == EstadoJuego.FIN)) {
            estado = EstadoJuego.JUGANDO;
            puntos = 0;
            vidas = 3;
            nivel = Nivel.numero(1);
            objetos.clear();
        }
    }

    void actualizar(double dt, Set<String> teclas) {
        if (estado == EstadoJuego.NIVEL_SUPERADO) {
            pausaNivel -= dt;
            if (pausaNivel <= 0) {
                nivel = Nivel.numero(nivel.numero() + 1);
                objetos.clear();
                estado = EstadoJuego.JUGANDO;
            }
            return;
        }
        if (estado != EstadoJuego.JUGANDO) {
            return;
        }
        jugadorX += ((teclas.contains("RIGHT") ? 1 : 0) - (teclas.contains("LEFT") ? 1 : 0)) * 240 * dt;
        jugadorX = Math.max(10, Math.min(ANCHO - 10, jugadorX));
        proximo -= dt;
        if (proximo <= 0) {
            boolean moneda = azar.nextInt(3) > 0;
            objetos.add(new Objeto(10 + azar.nextInt(ANCHO - 20), -10, moneda ? 110 : nivel.velocidadEnemigos(), moneda));
            proximo = nivel.segundosEntreEnemigos();
        }
        for (Objeto o : objetos) {
            o.y += o.vy * dt;
            boolean toca = Math.abs(o.x - jugadorX) < 18 && Math.abs(o.y - (ALTO - 30)) < 18;
            if (toca) {
                o.vivo = false;
                if (o.esMoneda) {
                    puntos += 10;
                } else {
                    vidas--;
                }
            } else if (o.y > ALTO) {
                o.vivo = false;
            }
        }
        objetos.removeIf(o -> !o.vivo);
        if (vidas <= 0) {
            estado = EstadoJuego.FIN;
            records.guardarSiEsMejor(puntos);
        } else if (puntos >= nivel.puntosParaPasar() && nivel.numero() < 5) {
            estado = EstadoJuego.NIVEL_SUPERADO;
            pausaNivel = 2;
        }
    }
}
```

`MundoJuegoTest.java`

```java
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Set;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class MundoJuegoTest {
    private Path archivo;
    private MundoJuego mundo;

    @BeforeEach
    void preparar() throws Exception {
        archivo = Files.createTempFile("record", ".txt");
        Files.delete(archivo);
        mundo = new MundoJuego(1, new Records(archivo));
    }

    @Test
    void arrancaEnElMenuYEnterEmpieza() {
        assertEquals(EstadoJuego.MENU, mundo.estado);
        mundo.tecla("ENTER");
        assertEquals(EstadoJuego.JUGANDO, mundo.estado);
    }

    @Test
    void elJugadorNoSaleDeLaPantalla() {
        mundo.tecla("ENTER");
        for (int i = 0; i < 600; i++) {
            mundo.actualizar(1.0 / 60, Set.of("RIGHT"));
        }
        assertTrue(mundo.jugadorX <= MundoJuego.ANCHO - 10);
    }

    @Test
    void unaMonedaQueToca() {
        mundo.tecla("ENTER");
        mundo.objetos.add(new Objeto(mundo.jugadorX, MundoJuego.ALTO - 30, 0, true));
        mundo.actualizar(0.001, Set.of());
        assertEquals(10, mundo.puntos);
    }

    @Test
    void sinVidasTerminaYGuardaElRecord() {
        mundo.tecla("ENTER");
        mundo.puntos = 30;
        mundo.vidas = 1;
        mundo.objetos.add(new Objeto(mundo.jugadorX, MundoJuego.ALTO - 30, 0, false));
        mundo.actualizar(0.001, Set.of());
        assertEquals(EstadoJuego.FIN, mundo.estado);
        assertEquals(30, mundo.record());
    }

    @Test
    void losNivelesSonMasDificiles() {
        assertTrue(Nivel.numero(3).velocidadEnemigos() > Nivel.numero(1).velocidadEnemigos());
        assertTrue(Nivel.numero(3).segundosEntreEnemigos() < Nivel.numero(1).segundosEntreEnemigos());
    }
}
```

### Prueba del sello

#### ¿Qué partes tiene un juego bien organizado?

La pantalla (teclado, bucle, dibujo), el mundo (el estado y las reglas), las entidades y, si hace falta, una clase para guardar datos como el récord.

#### ¿Por qué el mundo no debe saber nada de Swing?

Para poder probarlo con JUnit sin ventanas y cambiar el dibujo sin tocar las reglas.

#### ¿Cómo se representa un nivel?

Como una configuración (por ejemplo, un `record`) con los valores que cambian: velocidad, frecuencia de enemigos, puntos para pasar.

#### ¿Qué hay que hacer al pasar de nivel o volver a empezar?

Reiniciar las listas y los contadores que corresponden.

### Soluciones (docente)

Jefe de la Senda. El ejemplo simula una partida sin ventana con una "jugadora" automática (semilla 42) para que la salida sea verificable; la referencia de la misión es la misma lógica con ventana y sus pruebas. Se corrige jugando el juego del alumno y corriendo sus pruebas.
