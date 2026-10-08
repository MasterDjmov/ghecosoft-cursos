from genjava import m

# S02: el Palacio de las Ventanas. Swing de verdad pero SIN abrir ventanas (D96: «la lógica sin ventana»): modelos
# de combo, lista, tabla y árbol, botones con doClick(), ButtonGroup, SwingWorker y el hilo de eventos funcionan
# sin pantalla, así la salida se puede comprobar en cualquier compu.

NODOS = [
    {
        "titulo": "S02-N01 · La primera ventana: JFrame, componentes y eventos",
        "misiones": [
            m(id="S02-N01-P1", titulo="El botón que reacciona",
              lugar="La entrada del Palacio de las Ventanas", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="ActionListener | boton.addActionListener(e -> …) · el programa no decide cuándo: reacciona al clic",
              recompensa="xp 10, oro 10",
              escena="""
                  En el Palacio de las Ventanas nadie escribe en la consola: hay paneles con botones. —Ya no decidís vos el orden —dice Kaffa—. El usuario toca cuando quiere y tu programa **reacciona**. Gheco aprieta un botón sin ventana, solo para ver qué pasa.
              """,
              sugiere="`boton.addActionListener(e -> …)` registra qué hacer cuando lo tocan. `doClick()` simula un clic, así se prueba sin ventana. `e.getActionCommand()` da el texto del botón.",
              desafio="Registrá la reacción del botón: que muestre «Tocaron: » y el texto del botón.",
              inicial='''
                  import javax.swing.JButton;

                  public class Boton {
                      public static void main(String[] args) {
                          JButton saludar = new JButton("Saludar");
                          saludar.___(e -> System.out.println("Tocaron: " + e.getActionCommand()));
                          saludar.doClick();
                          saludar.doClick();
                      }
                  }
              ''',
              solucion='''
                  import javax.swing.JButton;

                  public class Boton {
                      public static void main(String[] args) {
                          JButton saludar = new JButton("Saludar");
                          saludar.addActionListener(e -> System.out.println("Tocaron: " + e.getActionCommand()));
                          saludar.doClick();
                          saludar.doClick();
                      }
                  }
              ''',
              al_superar="Dos clics, dos reacciones. —El programa ya no manda —dice Zed—. Espera. Como un buen ladrón.",
              imagen=["La entrada del Palacio de las Ventanas: paneles de vidrio con botones luminosos.",
                      "Gheco apretando un botón de vidrio; Zed mirando con atención."]),
            m(id="S02-N01-P2", titulo="El cartel que cambia",
              lugar="La entrada del Palacio de las Ventanas", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Componentes y estado | JLabel muestra · JTextField recibe · el botón lee el campo y cambia el cartel",
              recompensa="xp 10, oro 10",
              escena="""
                  En la entrada hay un casillero para escribir el nombre y un cartel que saluda. Nadia escribe el suyo y aprieta el botón.
              """,
              sugiere="Un `JTextField` guarda lo que escribió el usuario (`getText()`) y un `JLabel` muestra un texto (`setText(...)`). Adentro del listener, se lee uno y se cambia el otro.",
              desafio="Completá el listener: el cartel muestra «Bienvenida, » y lo que hay en el campo.",
              inicial='''
                  import javax.swing.JButton;
                  import javax.swing.JLabel;
                  import javax.swing.JTextField;

                  public class Cartel {
                      public static void main(String[] args) {
                          JTextField nombre = new JTextField();
                          JLabel cartel = new JLabel("¿Quién llega?");
                          JButton entrar = new JButton("Entrar");
                          entrar.addActionListener(e -> cartel.setText(___));

                          System.out.println(cartel.getText());
                          nombre.setText("Nadia");
                          entrar.doClick();
                          System.out.println(cartel.getText());
                      }
                  }
              ''',
              solucion='''
                  import javax.swing.JButton;
                  import javax.swing.JLabel;
                  import javax.swing.JTextField;

                  public class Cartel {
                      public static void main(String[] args) {
                          JTextField nombre = new JTextField();
                          JLabel cartel = new JLabel("¿Quién llega?");
                          JButton entrar = new JButton("Entrar");
                          entrar.addActionListener(e -> cartel.setText("Bienvenida, " + nombre.getText()));

                          System.out.println(cartel.getText());
                          nombre.setText("Nadia");
                          entrar.doClick();
                          System.out.println(cartel.getText());
                      }
                  }
              ''',
              al_superar="«Bienvenida, Nadia.» Nadia sonríe apenas. Zed escribe su nombre y el cartel dice «Bienvenida, Zed». —Hay que arreglar eso —dice él.",
              imagen=["Un casillero de vidrio con «Nadia» escrito y un cartel arriba que dice «Bienvenida, Nadia».",
                      "Nadia sonriendo apenas; Zed riéndose del cartel."]),
            m(id="S02-N01-P3", titulo="El que atiende la ventana",
              lugar="La entrada del Palacio de las Ventanas", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="El hilo de eventos (EDT) | todo lo de Swing se toca desde UN hilo · SwingUtilities.invokeLater(...) le pasa el trabajo · invokeAndWait espera a que termine",
              recompensa="xp 15, oro 15",
              escena="""
                  En el Palacio hay un solo empleado que atiende las ventanas: el **hilo de eventos**. Si otro las toca, se arma lío. —Las ventanas se crean y se cambian **desde ese hilo** —dice Kaffa—. Se le pasa el trabajo y él lo hace.
              """,
              sugiere="`SwingUtilities.invokeAndWait(() -> …)` le pasa una tarea al hilo de eventos y espera a que termine. Adentro, `SwingUtilities.isEventDispatchThread()` da `true`. Por eso las ventanas se crean con `invokeLater`.",
              desafio="Completá el método que le pasa la tarea al hilo de eventos y espera.",
              inicial='''
                  import javax.swing.SwingUtilities;

                  public class Empleado {
                      public static void main(String[] args) throws Exception {
                          System.out.println("Desde el main, ¿es el hilo de eventos? " + SwingUtilities.isEventDispatchThread());
                          SwingUtilities.___(() ->
                                  System.out.println("Desde la tarea, ¿es el hilo de eventos? " + SwingUtilities.isEventDispatchThread()));
                          System.out.println("La tarea ya terminó");
                      }
                  }
              ''',
              solucion='''
                  import javax.swing.SwingUtilities;

                  public class Empleado {
                      public static void main(String[] args) throws Exception {
                          System.out.println("Desde el main, ¿es el hilo de eventos? " + SwingUtilities.isEventDispatchThread());
                          SwingUtilities.invokeAndWait(() ->
                                  System.out.println("Desde la tarea, ¿es el hilo de eventos? " + SwingUtilities.isEventDispatchThread()));
                          System.out.println("La tarea ya terminó");
                      }
                  }
              ''',
              al_superar="El `main` no es el que atiende; la tarea sí. —Un solo empleado y todos le pasan el trabajo —resume Nadia—. Como la ventanilla de la Aduana.",
              imagen=["Un único empleado del Palacio atendiendo una fila de pedidos frente a muchas ventanas.",
                      "Nadia comparándolo con la ventanilla de la Aduana."]),
        ],
    },
    {
        "titulo": "S02-N02 · Layouts: ordenar la ventana",
        "misiones": [
            m(id="S02-N02-P1", titulo="La grilla perfecta",
              lugar="El salón de vitrales del Palacio", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="GridLayout | new GridLayout(filas, columnas) · todas las celdas iguales · con 0 filas, las calcula según los componentes",
              recompensa="xp 10, oro 10",
              escena="""
                  En el salón de vitrales, un panel acomoda los botones en una grilla perfecta, todos del mismo tamaño. Si agregás uno, la grilla decide sola cuántas filas hacen falta.
              """,
              sugiere="Con `GridLayout(0, 3)`, las columnas son 3 y las filas se calculan: hacen falta tantas como para que entren todos. Para 7 botones en 3 columnas, `(7 + 3 - 1) / 3` filas.",
              desafio="Completá la cuenta de filas: los botones divididos por las columnas, redondeando para arriba.",
              inicial='''
                  public class Grilla {
                      public static void main(String[] args) {
                          int columnas = 3;
                          for (int botones : new int[] {3, 7, 9, 10}) {
                              int filas = ___;
                              System.out.println(botones + " botones en " + columnas + " columnas: " + filas + " filas");
                          }
                      }
                  }
              ''',
              solucion='''
                  public class Grilla {
                      public static void main(String[] args) {
                          int columnas = 3;
                          for (int botones : new int[] {3, 7, 9, 10}) {
                              int filas = (botones + columnas - 1) / columnas;
                              System.out.println(botones + " botones en " + columnas + " columnas: " + filas + " filas");
                          }
                      }
                  }
              ''',
              al_superar="Así razona el `GridLayout` por dentro. —No pongas cada botón en una coordenada —dice Kaffa—: elegí la regla y dejala trabajar.",
              imagen=["Un vitral dividido en una grilla perfecta de botones iguales, con una fila nueva apareciendo abajo.",
                      "Gheco contando filas con los dedos."]),
            m(id="S02-N02-P2", titulo="Norte, sur, este, oeste y centro",
              lugar="El salón de vitrales del Palacio", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="BorderLayout | cinco lugares: NORTH, SOUTH, EAST, WEST y CENTER · el centro se queda con todo el espacio que sobra",
              recompensa="xp 10, oro 10",
              escena="""
                  El panel principal del Palacio se divide como un mapa: arriba el título, abajo la barra de estado, a los costados los menús y en el centro, lo importante.
              """,
              sugiere="`BorderLayout` tiene cinco lugares con nombre: `BorderLayout.NORTH`, `SOUTH`, `EAST`, `WEST` y `CENTER`. Se elige al agregar: `panel.add(componente, BorderLayout.SOUTH)`.",
              desafio="Agregá la barra de estado en el sur.",
              inicial='''
                  import java.awt.BorderLayout;
                  import javax.swing.JLabel;
                  import javax.swing.JPanel;

                  public class Mapa {
                      public static void main(String[] args) {
                          JPanel panel = new JPanel(new BorderLayout());
                          panel.add(new JLabel("Registro de viajeros"), BorderLayout.NORTH);
                          panel.add(new JLabel("Tabla de viajeros"), BorderLayout.CENTER);
                          panel.add(new JLabel("3 viajeros cargados"), BorderLayout.___);
                          BorderLayout layout = (BorderLayout) panel.getLayout();
                          for (String lugar : new String[] {BorderLayout.NORTH, BorderLayout.CENTER, BorderLayout.SOUTH}) {
                              JLabel l = (JLabel) layout.getLayoutComponent(lugar);
                              System.out.println(lugar + ": " + l.getText());
                          }
                      }
                  }
              ''',
              solucion='''
                  import java.awt.BorderLayout;
                  import javax.swing.JLabel;
                  import javax.swing.JPanel;

                  public class Mapa {
                      public static void main(String[] args) {
                          JPanel panel = new JPanel(new BorderLayout());
                          panel.add(new JLabel("Registro de viajeros"), BorderLayout.NORTH);
                          panel.add(new JLabel("Tabla de viajeros"), BorderLayout.CENTER);
                          panel.add(new JLabel("3 viajeros cargados"), BorderLayout.SOUTH);
                          BorderLayout layout = (BorderLayout) panel.getLayout();
                          for (String lugar : new String[] {BorderLayout.NORTH, BorderLayout.CENTER, BorderLayout.SOUTH}) {
                              JLabel l = (JLabel) layout.getLayoutComponent(lugar);
                              System.out.println(lugar + ": " + l.getText());
                          }
                      }
                  }
              ''',
              al_superar="Título arriba, tabla en el centro, estado abajo. Cuando la ventana crezca, el centro se va a quedar con el espacio. —Como la plaza del Imperio —dice Zed.",
              imagen=["Un panel de vidrio dividido en cinco zonas con rosa de los vientos: norte, sur, este, oeste y centro.",
                      "Zed señalando el centro."]),
            m(id="S02-N02-P3", titulo="El formulario en la grilla de bolsas",
              lugar="El salón de vitrales del Palacio", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="GridBagLayout | cada componente con su GridBagConstraints: gridx (columna) y gridy (fila) · la etiqueta en la columna 0, el campo en la 1",
              recompensa="xp 15, oro 15",
              escena="""
                  El formulario de inscripción del Palacio tiene etiquetas a la izquierda y campos a la derecha, renglón por renglón. Para eso, la regla más flexible: el **GridBagLayout**.
              """,
              sugiere="Con `GridBagLayout`, cada componente lleva sus `GridBagConstraints`: `gridx` es la columna y `gridy` la fila. En un formulario, la etiqueta va en `gridx = 0` y el campo en `gridx = 1`, en la misma fila.",
              desafio="Completá la columna del campo: va a la derecha de su etiqueta.",
              inicial='''
                  import java.awt.GridBagConstraints;

                  public class Formulario {
                      public static void main(String[] args) {
                          String[] etiquetas = {"Nombre", "Pasaporte", "Oficio"};
                          for (int fila = 0; fila < etiquetas.length; fila++) {
                              GridBagConstraints etiqueta = new GridBagConstraints();
                              etiqueta.gridx = 0;
                              etiqueta.gridy = fila;
                              GridBagConstraints campo = new GridBagConstraints();
                              campo.gridx = ___;
                              campo.gridy = fila;
                              System.out.println(etiquetas[fila] + ": etiqueta en (" + etiqueta.gridx + ", " + etiqueta.gridy
                                      + "), campo en (" + campo.gridx + ", " + campo.gridy + ")");
                          }
                      }
                  }
              ''',
              solucion='''
                  import java.awt.GridBagConstraints;

                  public class Formulario {
                      public static void main(String[] args) {
                          String[] etiquetas = {"Nombre", "Pasaporte", "Oficio"};
                          for (int fila = 0; fila < etiquetas.length; fila++) {
                              GridBagConstraints etiqueta = new GridBagConstraints();
                              etiqueta.gridx = 0;
                              etiqueta.gridy = fila;
                              GridBagConstraints campo = new GridBagConstraints();
                              campo.gridx = 1;
                              campo.gridy = fila;
                              System.out.println(etiquetas[fila] + ": etiqueta en (" + etiqueta.gridx + ", " + etiqueta.gridy
                                      + "), campo en (" + campo.gridx + ", " + campo.gridy + ")");
                          }
                      }
                  }
              ''',
              al_superar="Tres renglones prolijos, etiqueta y campo. Nadia aprueba el formulario: es igual al de la Aduana, pero de vidrio.",
              imagen=["Un formulario de vidrio con etiquetas a la izquierda y campos a la derecha, sobre una grilla tenue.",
                      "Nadia firmando la aprobación."]),
        ],
    },
    {
        "titulo": "S02-N03 · Componentes: listas, opciones y controles",
        "misiones": [
            m(id="S02-N03-P1", titulo="La lista desplegable de armas",
              lugar="La armería del Palacio", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="JComboBox con objetos | DefaultComboBoxModel<Arma> · muestra el toString() · getSelectedItem() devuelve el OBJETO elegido",
              recompensa="xp 10, oro 10",
              escena="""
                  En la armería, el escribiente no deja escribir el arma: la elige de una **lista desplegable**. Así nadie escribe «espda».
              """,
              sugiere="Un combo puede guardar **objetos**: muestra su `toString()` y `getSelectedItem()` devuelve el objeto entero, con todos sus datos. Hay que castearlo: `(Arma) modelo.getSelectedItem()`.",
              desafio="Leé el arma elegida del modelo.",
              inicial='''
                  import javax.swing.DefaultComboBoxModel;

                  public class Armeria {
                      record Arma(String nombre, int danio) {
                          @Override
                          public String toString() { return nombre; }
                      }

                      public static void main(String[] args) {
                          DefaultComboBoxModel<Arma> modelo = new DefaultComboBoxModel<>(new Arma[] {
                                  new Arma("Espada", 12), new Arma("Arco", 9), new Arma("Lanza", 10)});
                          modelo.setSelectedItem(modelo.getElementAt(1));
                          Arma elegida = ___;
                          System.out.println("Opciones: " + modelo.getSize());
                          System.out.println("Eligió " + elegida + ", daño " + elegida.danio());
                      }
                  }
              ''',
              solucion='''
                  import javax.swing.DefaultComboBoxModel;

                  public class Armeria {
                      record Arma(String nombre, int danio) {
                          @Override
                          public String toString() { return nombre; }
                      }

                      public static void main(String[] args) {
                          DefaultComboBoxModel<Arma> modelo = new DefaultComboBoxModel<>(new Arma[] {
                                  new Arma("Espada", 12), new Arma("Arco", 9), new Arma("Lanza", 10)});
                          modelo.setSelectedItem(modelo.getElementAt(1));
                          Arma elegida = (Arma) modelo.getSelectedItem();
                          System.out.println("Opciones: " + modelo.getSize());
                          System.out.println("Eligió " + elegida + ", daño " + elegida.danio());
                      }
                  }
              ''',
              al_superar="El arco, con su daño y todo. —Si le pedís a la gente que escriba «arquero», alguien escribe «arqero» —dice Kaffa—. Ofrecé las opciones.",
              imagen=["Una lista desplegable de vidrio en la armería con Espada, Arco y Lanza; el Arco resaltado.",
                      "El escribiente de la armería anotando el pedido."]),
            m(id="S02-N03-P2", titulo="Una sola opción",
              lugar="La armería del Palacio", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="JRadioButton y ButtonGroup | los botones de un grupo se excluyen: elegir uno des-elige al otro",
              recompensa="xp 10, oro 10",
              escena="""
                  El pedido es para infantería **o** para caballería, nunca las dos. Zed tilda las dos a la vez, por probar. El formulario no lo deja.
              """,
              sugiere="Los `JRadioButton` agrupados en un `ButtonGroup` se excluyen: si se marca uno, se desmarca el otro. Sin el grupo, se pueden marcar los dos.",
              desafio="Agregá el segundo botón al grupo.",
              inicial='''
                  import javax.swing.ButtonGroup;
                  import javax.swing.JRadioButton;

                  public class Opciones {
                      public static void main(String[] args) {
                          JRadioButton infanteria = new JRadioButton("Infantería");
                          JRadioButton caballeria = new JRadioButton("Caballería");
                          ButtonGroup grupo = new ButtonGroup();
                          grupo.add(infanteria);
                          ___;
                          infanteria.setSelected(true);
                          caballeria.setSelected(true);
                          System.out.println("Infantería: " + infanteria.isSelected());
                          System.out.println("Caballería: " + caballeria.isSelected());
                      }
                  }
              ''',
              solucion='''
                  import javax.swing.ButtonGroup;
                  import javax.swing.JRadioButton;

                  public class Opciones {
                      public static void main(String[] args) {
                          JRadioButton infanteria = new JRadioButton("Infantería");
                          JRadioButton caballeria = new JRadioButton("Caballería");
                          ButtonGroup grupo = new ButtonGroup();
                          grupo.add(infanteria);
                          grupo.add(caballeria);
                          infanteria.setSelected(true);
                          caballeria.setSelected(true);
                          System.out.println("Infantería: " + infanteria.isSelected());
                          System.out.println("Caballería: " + caballeria.isSelected());
                      }
                  }
              ''',
              al_superar="Al marcar caballería, infantería se apaga sola. —El formulario sabe más reglas que yo —admite Zed.",
              imagen=["Dos círculos de vidrio, «Infantería» y «Caballería», unidos por un hilo de luz: uno encendido y otro apagado.",
                      "Zed intentando tildar los dos, sin éxito."]),
            m(id="S02-N03-P3", titulo="La barra que no se pasa",
              lugar="La armería del Palacio", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="JSlider y JProgressBar | tienen mínimo y máximo · setValue fuera del rango se ajusta solo al borde",
              recompensa="xp 15, oro 15",
              escena="""
                  El tamaño del escudo se elige con una **barra deslizante** de 1 a 10. Zed intenta poner 15, para tener el escudo más grande del Imperio.
              """,
              sugiere="Un `JSlider` (y una `JProgressBar`) tiene mínimo y máximo. Si se pide un valor fuera del rango, se ajusta solo al borde. `getValue()` dice el valor que quedó.",
              desafio="Leé el valor que quedó en la barra después de pedir 15.",
              inicial='''
                  import javax.swing.JSlider;

                  public class Barra {
                      public static void main(String[] args) {
                          JSlider tamanio = new JSlider(1, 10, 5);
                          System.out.println("Empieza en " + tamanio.getValue());
                          tamanio.setValue(15);
                          System.out.println("Pidió 15, quedó en " + ___);
                          tamanio.setValue(-3);
                          System.out.println("Pidió -3, quedó en " + tamanio.getValue());
                      }
                  }
              ''',
              solucion='''
                  import javax.swing.JSlider;

                  public class Barra {
                      public static void main(String[] args) {
                          JSlider tamanio = new JSlider(1, 10, 5);
                          System.out.println("Empieza en " + tamanio.getValue());
                          tamanio.setValue(15);
                          System.out.println("Pidió 15, quedó en " + tamanio.getValue());
                          tamanio.setValue(-3);
                          System.out.println("Pidió -3, quedó en " + tamanio.getValue());
                      }
                  }
              ''',
              al_superar="Diez, ni uno más. El escudo más grande del Imperio tendrá que esperar. —Los controles también validan —dice Nadia, satisfecha.",
              imagen=["Una barra deslizante de vidrio trabada en el 10 aunque Zed empuja más allá.",
                      "Nadia satisfecha con los brazos cruzados."]),
        ],
    },
    {
        "titulo": "S02-N04 · Tablas, árboles y diálogos",
        "misiones": [
            m(id="S02-N04-P1", titulo="La tabla que lee del modelo",
              lugar="La biblioteca del Palacio", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="TableModel | la JTable solo MUESTRA · el modelo dice cuántas filas y columnas hay y qué va en cada celda (getValueAt)",
              recompensa="xp 10, oro 10",
              escena="""
                  En la biblioteca, una tabla enorme muestra a los viajeros. Pero la tabla no sabe nada: le pregunta todo a su **modelo**.
              """,
              sugiere="Un `AbstractTableModel` propio responde `getRowCount()`, `getColumnCount()` y `getValueAt(fila, columna)`. La `JTable` solo pregunta y dibuja. En la columna 0 va el nombre y en la 1 el oficio.",
              desafio="Completá el `getValueAt`: columna 0, el nombre; si no, el oficio.",
              inicial='''
                  import java.util.List;
                  import javax.swing.table.AbstractTableModel;

                  public class Tabla {
                      record Viajero(String nombre, String oficio) { }

                      static class ModeloViajeros extends AbstractTableModel {
                          private final List<Viajero> viajeros;

                          ModeloViajeros(List<Viajero> viajeros) { this.viajeros = viajeros; }

                          public int getRowCount() { return viajeros.size(); }

                          public int getColumnCount() { return 2; }

                          public Object getValueAt(int fila, int columna) {
                              Viajero v = viajeros.get(fila);
                              return ___;
                          }
                      }

                      public static void main(String[] args) {
                          ModeloViajeros modelo = new ModeloViajeros(List.of(new Viajero("Zed", "aprendiz"), new Viajero("Nadia", "aduanera")));
                          for (int f = 0; f < modelo.getRowCount(); f++) {
                              System.out.println(modelo.getValueAt(f, 0) + " | " + modelo.getValueAt(f, 1));
                          }
                      }
                  }
              ''',
              solucion='''
                  import java.util.List;
                  import javax.swing.table.AbstractTableModel;

                  public class Tabla {
                      record Viajero(String nombre, String oficio) { }

                      static class ModeloViajeros extends AbstractTableModel {
                          private final List<Viajero> viajeros;

                          ModeloViajeros(List<Viajero> viajeros) { this.viajeros = viajeros; }

                          public int getRowCount() { return viajeros.size(); }

                          public int getColumnCount() { return 2; }

                          public Object getValueAt(int fila, int columna) {
                              Viajero v = viajeros.get(fila);
                              return columna == 0 ? v.nombre() : v.oficio();
                          }
                      }

                      public static void main(String[] args) {
                          ModeloViajeros modelo = new ModeloViajeros(List.of(new Viajero("Zed", "aprendiz"), new Viajero("Nadia", "aduanera")));
                          for (int f = 0; f < modelo.getRowCount(); f++) {
                              System.out.println(modelo.getValueAt(f, 0) + " | " + modelo.getValueAt(f, 1));
                          }
                      }
                  }
              ''',
              al_superar="«Zed | aprendiz.» Ya no dice «ladrón». La tabla lo muestra porque el modelo lo dice.",
              imagen=["Una tabla de vidrio enorme en la biblioteca del Palacio, con dos filas: Zed y Nadia.",
                      "Zed mirando su fila, conforme."]),
            m(id="S02-N04-P2", titulo="Agregar una fila",
              lugar="La biblioteca del Palacio", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="DefaultTableModel | addRow(new Object[]{…}) agrega · removeRow(i) borra · la tabla se entera sola",
              recompensa="xp 10, oro 10",
              escena="""
                  Llega Baldo a la biblioteca y hay que sumarlo al registro. Con el modelo por defecto de Swing, se agrega una fila y la tabla se actualiza sola.
              """,
              sugiere="`DefaultTableModel` ya trae `addRow(new Object[] {…})` y `removeRow(i)`. Avisa a la tabla en cada cambio, así se redibuja sola.",
              desafio="Agregá la fila de Baldo, «mercader».",
              inicial='''
                  import javax.swing.table.DefaultTableModel;

                  public class Filas {
                      public static void main(String[] args) {
                          DefaultTableModel modelo = new DefaultTableModel(new Object[] {"Nombre", "Oficio"}, 0);
                          modelo.addRow(new Object[] {"Zed", "aprendiz"});
                          modelo.addRow(new Object[] {"Nadia", "aduanera"});
                          modelo.___(new Object[] {"Baldo", "mercader"});
                          modelo.removeRow(0);
                          System.out.println("Filas: " + modelo.getRowCount());
                          for (int f = 0; f < modelo.getRowCount(); f++) {
                              System.out.println(modelo.getValueAt(f, 0) + " - " + modelo.getValueAt(f, 1));
                          }
                      }
                  }
              ''',
              solucion='''
                  import javax.swing.table.DefaultTableModel;

                  public class Filas {
                      public static void main(String[] args) {
                          DefaultTableModel modelo = new DefaultTableModel(new Object[] {"Nombre", "Oficio"}, 0);
                          modelo.addRow(new Object[] {"Zed", "aprendiz"});
                          modelo.addRow(new Object[] {"Nadia", "aduanera"});
                          modelo.addRow(new Object[] {"Baldo", "mercader"});
                          modelo.removeRow(0);
                          System.out.println("Filas: " + modelo.getRowCount());
                          for (int f = 0; f < modelo.getRowCount(); f++) {
                              System.out.println(modelo.getValueAt(f, 0) + " - " + modelo.getValueAt(f, 1));
                          }
                      }
                  }
              ''',
              al_superar="Baldo entra y, de paso, Zed borra la primera fila: la suya. —Era para probar removeRow —se defiende. Nadia lo vuelve a anotar.",
              imagen=["Una fila nueva apareciendo en la tabla de vidrio con «Baldo - mercader».",
                      "Nadia volviendo a anotar a Zed con cara de paciencia."]),
            m(id="S02-N04-P3", titulo="El árbol de los clanes",
              lugar="La biblioteca del Palacio", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="JTree | DefaultMutableTreeNode: cada nodo con sus hijos (add) · getChildCount() · muestra qué pertenece a qué",
              recompensa="xp 15, oro 15",
              escena="""
                  —Una tabla responde «¿quiénes son?»; un árbol, «¿qué pertenece a qué?» —dice Kaffa, y le pide a Zed el árbol del Imperio: cada región con sus lugares.
              """,
              sugiere="Un árbol se arma con `DefaultMutableTreeNode`: `region.add(new DefaultMutableTreeNode(\"Aduana\"))`. `getChildCount()` dice cuántos hijos tiene y `getChildAt(i)` da cada uno.",
              desafio="Agregá la región «Torre» a la raíz.",
              inicial='''
                  import javax.swing.tree.DefaultMutableTreeNode;

                  public class Arbol {
                      public static void main(String[] args) {
                          DefaultMutableTreeNode imperio = new DefaultMutableTreeNode("Imperio");
                          DefaultMutableTreeNode muralla = new DefaultMutableTreeNode("Muralla");
                          muralla.add(new DefaultMutableTreeNode("Aduana"));
                          muralla.add(new DefaultMutableTreeNode("Posada"));
                          DefaultMutableTreeNode torre = new DefaultMutableTreeNode("Torre");
                          torre.add(new DefaultMutableTreeNode("Ventana más alta"));
                          imperio.add(muralla);
                          ___;
                          System.out.println(imperio + ": " + imperio.getChildCount() + " regiones");
                          for (int i = 0; i < imperio.getChildCount(); i++) {
                              DefaultMutableTreeNode region = (DefaultMutableTreeNode) imperio.getChildAt(i);
                              System.out.println("- " + region + " (" + region.getChildCount() + " lugares)");
                          }
                      }
                  }
              ''',
              solucion='''
                  import javax.swing.tree.DefaultMutableTreeNode;

                  public class Arbol {
                      public static void main(String[] args) {
                          DefaultMutableTreeNode imperio = new DefaultMutableTreeNode("Imperio");
                          DefaultMutableTreeNode muralla = new DefaultMutableTreeNode("Muralla");
                          muralla.add(new DefaultMutableTreeNode("Aduana"));
                          muralla.add(new DefaultMutableTreeNode("Posada"));
                          DefaultMutableTreeNode torre = new DefaultMutableTreeNode("Torre");
                          torre.add(new DefaultMutableTreeNode("Ventana más alta"));
                          imperio.add(muralla);
                          imperio.add(torre);
                          System.out.println(imperio + ": " + imperio.getChildCount() + " regiones");
                          for (int i = 0; i < imperio.getChildCount(); i++) {
                              DefaultMutableTreeNode region = (DefaultMutableTreeNode) imperio.getChildAt(i);
                              System.out.println("- " + region + " (" + region.getChildCount() + " lugares)");
                          }
                      }
                  }
              ''',
              al_superar="El Imperio, con sus regiones y lugares. En la Torre hay uno solo: la ventana más alta. Zed lo mira un rato largo.",
              imagen=["Un árbol de vidrio con ramas: Imperio → Muralla (Aduana, Posada) y Torre (Ventana más alta).",
                      "Zed mirando la rama de la ventana más alta."]),
        ],
    },
    {
        "titulo": "S02-N05 · MDI y menús",
        "misiones": [
            m(id="S02-N05-P1", titulo="Los atajos del menú",
              lugar="El salón del trono del Palacio", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Menús y atajos | JMenuItem con setAccelerator(KeyStroke.getKeyStroke(\"control S\")) · el atajo se describe con un texto",
              recompensa="xp 10, oro 10",
              escena="""
                  El menú del salón del trono tiene atajos de teclado: Ctrl+S guarda, Ctrl+N abre una ficha nueva. Zed, que siempre buscó atajos, está en su salsa.
              """,
              sugiere="Un `JMenuItem` lleva su atajo con `setAccelerator(KeyStroke.getKeyStroke(\"control S\"))`. `getAccelerator()` lo devuelve.",
              desafio="Poné el atajo «control N» en el ítem «Nueva ficha».",
              inicial='''
                  import javax.swing.JMenu;
                  import javax.swing.JMenuItem;
                  import javax.swing.KeyStroke;

                  public class Atajos {
                      public static void main(String[] args) {
                          JMenu archivo = new JMenu("Archivo");
                          JMenuItem nueva = new JMenuItem("Nueva ficha");
                          JMenuItem guardar = new JMenuItem("Guardar");
                          nueva.setAccelerator(___);
                          guardar.setAccelerator(KeyStroke.getKeyStroke("control S"));
                          archivo.add(nueva);
                          archivo.add(guardar);
                          for (int i = 0; i < archivo.getItemCount(); i++) {
                              JMenuItem item = archivo.getItem(i);
                              System.out.println(item.getText() + ": " + item.getAccelerator());
                          }
                      }
                  }
              ''',
              solucion='''
                  import javax.swing.JMenu;
                  import javax.swing.JMenuItem;
                  import javax.swing.KeyStroke;

                  public class Atajos {
                      public static void main(String[] args) {
                          JMenu archivo = new JMenu("Archivo");
                          JMenuItem nueva = new JMenuItem("Nueva ficha");
                          JMenuItem guardar = new JMenuItem("Guardar");
                          nueva.setAccelerator(KeyStroke.getKeyStroke("control N"));
                          guardar.setAccelerator(KeyStroke.getKeyStroke("control S"));
                          archivo.add(nueva);
                          archivo.add(guardar);
                          for (int i = 0; i < archivo.getItemCount(); i++) {
                              JMenuItem item = archivo.getItem(i);
                              System.out.println(item.getText() + ": " + item.getAccelerator());
                          }
                      }
                  }
              ''',
              al_superar="Dos atajos en el menú Archivo. —Por fin un atajo legal —dice Nadia.",
              imagen=["Un menú de vidrio desplegado con «Nueva ficha · Ctrl+N» y «Guardar · Ctrl+S».",
                      "Zed sonriendo con los dedos sobre un teclado de cristal."]),
            m(id="S02-N05-P2", titulo="La ventana que no se abre dos veces",
              lugar="El salón del trono del Palacio", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="MDI sin duplicados | un mapa nombre → ventana interna abierta · si ya está, se trae al frente · si no, se crea",
              recompensa="xp 15, oro 15",
              escena="""
                  En el salón del trono, alguien toca tres veces «Tesorería» y aparecen tres ventanas de tesorería encimadas. El escritorio es un caos.
              """,
              sugiere="Se guardan las ventanas internas abiertas en un mapa por nombre. Antes de crear una, se pregunta si ya está (`containsKey`): si está, se la trae al frente; si no, se crea y se guarda.",
              desafio="Completá la condición: la ventana ya está abierta.",
              inicial='''
                  import java.util.LinkedHashMap;
                  import java.util.Map;

                  public class Escritorio {
                      static final Map<String, String> abiertas = new LinkedHashMap<>();

                      static void abrir(String nombre) {
                          if (___) {
                              System.out.println(nombre + ": ya estaba abierta, la traigo al frente");
                          } else {
                              abiertas.put(nombre, "ventana de " + nombre);
                              System.out.println(nombre + ": abierta");
                          }
                      }

                      public static void main(String[] args) {
                          abrir("Tesorería");
                          abrir("Registro");
                          abrir("Tesorería");
                          abrir("Tesorería");
                          System.out.println("Ventanas en el escritorio: " + abiertas.size());
                      }
                  }
              ''',
              solucion='''
                  import java.util.LinkedHashMap;
                  import java.util.Map;

                  public class Escritorio {
                      static final Map<String, String> abiertas = new LinkedHashMap<>();

                      static void abrir(String nombre) {
                          if (abiertas.containsKey(nombre)) {
                              System.out.println(nombre + ": ya estaba abierta, la traigo al frente");
                          } else {
                              abiertas.put(nombre, "ventana de " + nombre);
                              System.out.println(nombre + ": abierta");
                          }
                      }

                      public static void main(String[] args) {
                          abrir("Tesorería");
                          abrir("Registro");
                          abrir("Tesorería");
                          abrir("Tesorería");
                          System.out.println("Ventanas en el escritorio: " + abiertas.size());
                      }
                  }
              ''',
              al_superar="Dos ventanas, ni una de más. El escritorio del salón del trono vuelve a estar en orden.",
              imagen=["Un escritorio de vidrio con dos ventanitas internas ordenadas: «Tesorería» y «Registro».",
                      "Una tercera ventana de tesorería desvaneciéndose antes de aparecer."]),
            m(id="S02-N05-P3", titulo="La barra de estado",
              lugar="El salón del trono del Palacio", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Barra de estado | una etiqueta abajo que cuenta qué pasa · se actualiza en cada acción del usuario",
              recompensa="xp 15, oro 15",
              escena="""
                  Abajo de todo, el salón del trono tiene una barra que cuenta qué está pasando: cuántas fichas hay abiertas y quién está conectado.
              """,
              sugiere="La barra de estado es un `JLabel` que se actualiza con `setText(...)` después de cada acción. Conviene un método `actualizar()` que arme el texto, y llamarlo siempre que algo cambie.",
              desafio="Completá el texto de la barra con la cantidad de fichas y el usuario.",
              inicial='''
                  import javax.swing.JLabel;

                  public class Estado {
                      static final JLabel barra = new JLabel();
                      static int fichas = 0;
                      static final String usuario = "Zed";

                      static void actualizar() {
                          barra.setText(___);
                      }

                      public static void main(String[] args) {
                          actualizar();
                          System.out.println(barra.getText());
                          fichas += 2;
                          actualizar();
                          System.out.println(barra.getText());
                      }
                  }
              ''',
              solucion='''
                  import javax.swing.JLabel;

                  public class Estado {
                      static final JLabel barra = new JLabel();
                      static int fichas = 0;
                      static final String usuario = "Zed";

                      static void actualizar() {
                          barra.setText("Fichas abiertas: " + fichas + " | Usuario: " + usuario);
                      }

                      public static void main(String[] args) {
                          actualizar();
                          System.out.println(barra.getText());
                          fichas += 2;
                          actualizar();
                          System.out.println(barra.getText());
                      }
                  }
              ''',
              al_superar="La barra cuenta todo, sin que nadie pregunte. —Lo que no está a la vista, no existe —dice Nadia, que lo dice de todo.",
              imagen=["La barra de estado del salón del trono, abajo de todo, con «Fichas abiertas: 2 | Usuario: Zed».",
                      "Nadia señalando la barra."]),
        ],
    },
    {
        "titulo": "S02-N06 · SwingWorker: la base sin congelar la ventana",
        "misiones": [
            m(id="S02-N06-P1", titulo="El mensajero de la Bóveda",
              lugar="El registro del Palacio", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="SwingWorker | doInBackground() hace lo lento en otro hilo · execute() lo arranca · get() espera el resultado · la ventana no se congela",
              recompensa="xp 10, oro 10",
              escena="""
                  El registro le pide a la Bóveda diez mil viajeros y la ventana se congela. —El que atiende no puede ir a la Bóveda —dice Kaffa—. Mandá a un **mensajero**.
              """,
              sugiere="Un `SwingWorker` hace la tarea lenta en `doInBackground()`, en otro hilo, mientras el hilo de eventos sigue atendiendo. `execute()` lo manda y `get()` espera su resultado.",
              desafio="Completá el método que arranca al mensajero.",
              inicial='''
                  import javax.swing.SwingWorker;

                  public class Mensajero {
                      public static void main(String[] args) throws Exception {
                          SwingWorker<Integer, Void> mensajero = new SwingWorker<>() {
                              @Override
                              protected Integer doInBackground() {
                                  int total = 0;
                                  for (int i = 1; i <= 10000; i++) {
                                      total += i % 7;
                                  }
                                  return total;
                              }
                          };
                          mensajero.___();
                          System.out.println("La ventana sigue atendiendo...");
                          System.out.println("El mensajero trajo: " + mensajero.get());
                      }
                  }
              ''',
              solucion='''
                  import javax.swing.SwingWorker;

                  public class Mensajero {
                      public static void main(String[] args) throws Exception {
                          SwingWorker<Integer, Void> mensajero = new SwingWorker<>() {
                              @Override
                              protected Integer doInBackground() {
                                  int total = 0;
                                  for (int i = 1; i <= 10000; i++) {
                                      total += i % 7;
                                  }
                                  return total;
                              }
                          };
                          mensajero.execute();
                          System.out.println("La ventana sigue atendiendo...");
                          System.out.println("El mensajero trajo: " + mensajero.get());
                      }
                  }
              ''',
              al_superar="La ventana nunca se congeló y el mensajero volvió con el resultado. El escribiente deja de golpear la ventana.",
              imagen=["Un mensajero con alas bajando por una escalera hacia la Bóveda, mientras arriba la ventana sigue atendiendo.",
                      "El escribiente del registro, aliviado."]),
            m(id="S02-N06-P2", titulo="El mensajero que vuelve con malas noticias",
              lugar="El registro del Palacio", personajes="Zed, Gheco, Nadia, Kaffa",
              criatura="troll",
              carta="Errores en segundo plano | una excepción en doInBackground() llega envuelta en ExecutionException al hacer get() · getCause() dice qué pasó",
              recompensa="xp 15, oro 15",
              escena="""
                  Esta vez el mensajero no encuentra la Bóveda abierta. Si nadie le pregunta, el error se pierde en el camino y un **troll** se queda con él.
              """,
              sugiere="Si `doInBackground()` lanza una excepción, `get()` lanza una `ExecutionException` que la trae adentro: `e.getCause().getMessage()` dice qué pasó. Así la ventana puede mostrar un mensaje claro.",
              desafio="Completá el `catch` con la excepción que envuelve al error del mensajero.",
              inicial='''
                  import java.util.concurrent.ExecutionException;
                  import javax.swing.SwingWorker;

                  public class MalasNoticias {
                      public static void main(String[] args) throws Exception {
                          SwingWorker<Integer, Void> mensajero = new SwingWorker<>() {
                              @Override
                              protected Integer doInBackground() {
                                  throw new IllegalStateException("la Bóveda está cerrada");
                              }
                          };
                          mensajero.execute();
                          try {
                              System.out.println("Trajo: " + mensajero.get());
                          } catch (___ e) {
                              System.out.println("No se pudo: " + e.getCause().getMessage());
                          }
                      }
                  }
              ''',
              solucion='''
                  import java.util.concurrent.ExecutionException;
                  import javax.swing.SwingWorker;

                  public class MalasNoticias {
                      public static void main(String[] args) throws Exception {
                          SwingWorker<Integer, Void> mensajero = new SwingWorker<>() {
                              @Override
                              protected Integer doInBackground() {
                                  throw new IllegalStateException("la Bóveda está cerrada");
                              }
                          };
                          mensajero.execute();
                          try {
                              System.out.println("Trajo: " + mensajero.get());
                          } catch (ExecutionException e) {
                              System.out.println("No se pudo: " + e.getCause().getMessage());
                          }
                      }
                  }
              ''',
              al_superar="«No se pudo: la Bóveda está cerrada.» Un mensaje claro en lugar de una ventana muda. El troll se queda sin error que esconder.",
              imagen=["El mensajero volviendo con un pergamino que dice «la Bóveda está cerrada».",
                      "Un troll con las manos vacías."]),
            m(id="S02-N06-P3", titulo="Mostrar el resultado en la ventana",
              lugar="El registro del Palacio", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="done() | se ejecuta en el hilo de eventos cuando termina la tarea · ahí sí se puede tocar la ventana (setText)",
              recompensa="xp 15, oro 20",
              escena="""
                  El mensajero vuelve, pero no puede tocar la ventana él mismo: solo el que atiende puede. —Dejale el resultado en la puerta —dice Kaffa—: el método `done()`.
              """,
              sugiere="`done()` corre en el **hilo de eventos** cuando la tarea termina: ahí se cambia la ventana (`etiqueta.setText(...)`). Adentro, `get()` ya tiene el resultado. Para esperar en el `main` a que eso pase, se usa un `CountDownLatch`.",
              desafio="Completá el `done()`: poné en la etiqueta «Viajeros: » y el resultado.",
              inicial='''
                  import java.util.concurrent.CountDownLatch;
                  import javax.swing.JLabel;
                  import javax.swing.SwingUtilities;
                  import javax.swing.SwingWorker;

                  public class Done {
                      public static void main(String[] args) throws Exception {
                          JLabel etiqueta = new JLabel("Cargando...");
                          CountDownLatch listo = new CountDownLatch(1);
                          new SwingWorker<Integer, Void>() {
                              @Override
                              protected Integer doInBackground() {
                                  return 10000;
                              }

                              @Override
                              protected void done() {
                                  try {
                                      ___;
                                      System.out.println("done() en el hilo de eventos: " + SwingUtilities.isEventDispatchThread());
                                  } catch (Exception e) {
                                      etiqueta.setText("Error");
                                  }
                                  listo.countDown();
                              }
                          }.execute();
                          listo.await();
                          System.out.println(etiqueta.getText());
                      }
                  }
              ''',
              solucion='''
                  import java.util.concurrent.CountDownLatch;
                  import javax.swing.JLabel;
                  import javax.swing.SwingUtilities;
                  import javax.swing.SwingWorker;

                  public class Done {
                      public static void main(String[] args) throws Exception {
                          JLabel etiqueta = new JLabel("Cargando...");
                          CountDownLatch listo = new CountDownLatch(1);
                          new SwingWorker<Integer, Void>() {
                              @Override
                              protected Integer doInBackground() {
                                  return 10000;
                              }

                              @Override
                              protected void done() {
                                  try {
                                      etiqueta.setText("Viajeros: " + get());
                                      System.out.println("done() en el hilo de eventos: " + SwingUtilities.isEventDispatchThread());
                                  } catch (Exception e) {
                                      etiqueta.setText("Error");
                                  }
                                  listo.countDown();
                              }
                          }.execute();
                          listo.await();
                          System.out.println(etiqueta.getText());
                      }
                  }
              ''',
              al_superar="El mensajero deja el resultado y el que atiende lo pone en la ventana. —Cada uno en lo suyo —dice Kaffa—. Es lo mismo que vas a ver en el plano de cuatro salas.",
              imagen=["El mensajero dejando un pergamino en la puerta; el empleado del hilo de eventos lo coloca en la ventana.",
                      "Una etiqueta de vidrio que cambia de «Cargando...» a «Viajeros: 10000»."]),
        ],
    },
    {
        "titulo": "S02-N07 · MVC al estilo de la cátedra",
        "misiones": [
            m(id="S02-N07-P1", titulo="El SQL en el botón",
              lugar="La biblioteca del Palacio", personajes="Zed, Gheco, Nadia, Kaffa",
              criatura="ogro",
              carta="Controlador | la ventana NO decide reglas: le pasa los datos al controlador · el controlador valida y le pide al DAO que guarde",
              recompensa="xp 10, oro 10",
              escena="""
                  En el sistema viejo del Palacio, el botón «Guardar» valida, arma el SQL y guarda, todo junto. Cuando cambia una regla, se rompe la ventana. Un **ogro** vive feliz en ese botón.
              """,
              sugiere="En MVC, la vista solo junta los datos y llama al **controlador**. El controlador valida y, si está bien, le pide al **DAO** que guarde. Si no, devuelve el error para mostrar.",
              desafio="Completá el controlador: si el nombre es válido, que el DAO lo guarde.",
              inicial='''
                  import java.util.ArrayList;
                  import java.util.List;

                  public class Mvc {
                      static class ViajeroDAO {
                          final List<String> tabla = new ArrayList<>();

                          void insertar(String nombre) { tabla.add(nombre); }
                      }

                      static class ViajeroControlador {
                          private final ViajeroDAO dao;

                          ViajeroControlador(ViajeroDAO dao) { this.dao = dao; }

                          String guardar(String nombre) {
                              if (nombre == null || nombre.isBlank()) {
                                  return "Error: el nombre es obligatorio";
                              }
                              ___;
                              return "Guardado: " + nombre;
                          }
                      }

                      public static void main(String[] args) {
                          ViajeroDAO dao = new ViajeroDAO();
                          ViajeroControlador controlador = new ViajeroControlador(dao);
                          System.out.println(controlador.guardar("Baldo"));
                          System.out.println(controlador.guardar(" "));
                          System.out.println("En la tabla: " + dao.tabla);
                      }
                  }
              ''',
              solucion='''
                  import java.util.ArrayList;
                  import java.util.List;

                  public class Mvc {
                      static class ViajeroDAO {
                          final List<String> tabla = new ArrayList<>();

                          void insertar(String nombre) { tabla.add(nombre); }
                      }

                      static class ViajeroControlador {
                          private final ViajeroDAO dao;

                          ViajeroControlador(ViajeroDAO dao) { this.dao = dao; }

                          String guardar(String nombre) {
                              if (nombre == null || nombre.isBlank()) {
                                  return "Error: el nombre es obligatorio";
                              }
                              dao.insertar(nombre);
                              return "Guardado: " + nombre;
                          }
                      }

                      public static void main(String[] args) {
                          ViajeroDAO dao = new ViajeroDAO();
                          ViajeroControlador controlador = new ViajeroControlador(dao);
                          System.out.println(controlador.guardar("Baldo"));
                          System.out.println(controlador.guardar(" "));
                          System.out.println("En la tabla: " + dao.tabla);
                      }
                  }
              ''',
              al_superar="La regla vive en el controlador y el guardado en el DAO. El botón ya no sabe nada de SQL. El ogro se muda.",
              imagen=["Un plano con cuatro salas: Modelo, DAO, Controlador y Vista, con flechas entre ellas.",
                      "Un ogro saliendo de un botón de vidrio con sus cosas en una bolsa."]),
            m(id="S02-N07-P2", titulo="La vista que solo muestra",
              lugar="La biblioteca del Palacio", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Vista como interfaz | el controlador le habla a una interfaz Vista (mostrarMensaje) · la ventana real o una de consola la implementan",
              recompensa="xp 15, oro 15",
              escena="""
                  —Si el controlador habla con la ventana a través de una **interfaz** —dice Kaffa—, lo podés probar sin ventana. Es la D de SOLID, en el Palacio.
              """,
              sugiere="El controlador recibe una `Vista` (interfaz con `mostrarMensaje`). En la aplicación, la implementa la ventana; para probar, una vista de consola. El controlador no sabe cuál es.",
              desafio="Completá la llamada: el controlador le pide a la vista que muestre el mensaje.",
              inicial='''
                  public class VistaInterfaz {
                      interface Vista {
                          void mostrarMensaje(String texto);
                      }

                      static class Controlador {
                          private final Vista vista;

                          Controlador(Vista vista) { this.vista = vista; }

                          void inscribir(String nombre, int edad) {
                              String mensaje = edad >= 16 ? nombre + " inscripto" : nombre + " es menor: necesita autorización";
                              ___;
                          }
                      }

                      public static void main(String[] args) {
                          Vista consola = texto -> System.out.println("[Vista] " + texto);
                          Controlador c = new Controlador(consola);
                          c.inscribir("Zed", 19);
                          c.inscribir("Teo", 14);
                      }
                  }
              ''',
              solucion='''
                  public class VistaInterfaz {
                      interface Vista {
                          void mostrarMensaje(String texto);
                      }

                      static class Controlador {
                          private final Vista vista;

                          Controlador(Vista vista) { this.vista = vista; }

                          void inscribir(String nombre, int edad) {
                              String mensaje = edad >= 16 ? nombre + " inscripto" : nombre + " es menor: necesita autorización";
                              vista.mostrarMensaje(mensaje);
                          }
                      }

                      public static void main(String[] args) {
                          Vista consola = texto -> System.out.println("[Vista] " + texto);
                          Controlador c = new Controlador(consola);
                          c.inscribir("Zed", 19);
                          c.inscribir("Teo", 14);
                      }
                  }
              ''',
              al_superar="El controlador funciona igual con la ventana o con la consola. —Ahora sí lo puedo probar —dice Zed—, sin abrir nada.",
              imagen=["Un controlador de bronce conectado por un cable a dos pantallas intercambiables: una ventana de vidrio y una consola.",
                      "Kaffa señalando el cable con la taza."]),
            m(id="S02-N07-P3", titulo="La conexión en el archivo",
              lugar="La biblioteca del Palacio", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Configuración de la conexión | url, usuario y clave de la base en un .properties · nunca escritos en el código",
              recompensa="xp 15, oro 20",
              escena="""
                  El código viejo tenía la clave de la Bóveda escrita adentro, a la vista de cualquiera. —Lo que cambia según dónde corre, va en un archivo aparte —dice Kaffa—. Y la clave, nunca en el código.
              """,
              sugiere="`Properties.load(...)` lee `url`, `usuario` y `clave` de un archivo. El programa los usa sin conocerlos de antemano. Al mostrar la configuración, la clave se tapa.",
              desafio="Completá la lectura del usuario desde las propiedades.",
              inicial='''
                  import java.io.StringReader;
                  import java.util.Properties;

                  public class Conexion {
                      public static void main(String[] args) throws Exception {
                          String archivo = """
                                  db.url=jdbc:postgresql://localhost:5432/imperio
                                  db.usuario=palacio
                                  db.clave=vitral-secreto
                                  """;
                          Properties p = new Properties();
                          p.load(new StringReader(archivo));
                          String url = p.getProperty("db.url");
                          String usuario = ___;
                          String clave = p.getProperty("db.clave");
                          System.out.println("Conectando a " + url);
                          System.out.println("Usuario: " + usuario + ", clave: " + "*".repeat(clave.length()));
                      }
                  }
              ''',
              solucion='''
                  import java.io.StringReader;
                  import java.util.Properties;

                  public class Conexion {
                      public static void main(String[] args) throws Exception {
                          String archivo = """
                                  db.url=jdbc:postgresql://localhost:5432/imperio
                                  db.usuario=palacio
                                  db.clave=vitral-secreto
                                  """;
                          Properties p = new Properties();
                          p.load(new StringReader(archivo));
                          String url = p.getProperty("db.url");
                          String usuario = p.getProperty("db.usuario");
                          String clave = p.getProperty("db.clave");
                          System.out.println("Conectando a " + url);
                          System.out.println("Usuario: " + usuario + ", clave: " + "*".repeat(clave.length()));
                      }
                  }
              ''',
              al_superar="""
                  La clave no aparece por ningún lado. Zed, que hace un tiempo hubiera dado cualquier cosa por esa clave, la tapa él mismo.
                  En la cima del Palacio, el Tribunal de las Actas se reúne.
              """,
              imagen=["Un archivo de configuración de vidrio con la clave tapada con asteriscos.",
                      "En la cima del Palacio, una mesa de tribunal con un pergamino: «Registración de Actas de Examen»."]),
        ],
    },
    {
        "titulo": "S02-N08 · Jefe del Palacio: el Tribunal de las Actas",
        "misiones": [
            m(id="S02-N08-P1", titulo="El acta es un formulario",
              lugar="La cima del Palacio", personajes="Zed, Gheco, Nadia, Kaffa",
              criatura="dragon",
              carta="Herencia y composición | ActaDeExamen extends Formulario · el acta TIENE registros (alumno y nota) · nota de 1 a 10 o ausente",
              recompensa="xp 20, oro 20",
              escena="""
                  El Tribunal de las Actas pone el pergamino sobre la mesa: un acta es un **formulario** (con fecha y quién lo cargó) que **tiene** registros: cada alumno con su nota o «ausente». —Primero, el modelo —dice Kaffa.
              """,
              sugiere="`ActaDeExamen extends Formulario` hereda la fecha y quién la cargó. Tiene una lista de `Registro`. Una nota es válida si está entre 1 y 10, o si el alumno está ausente (nota `null`).",
              desafio="Completá la condición de nota inválida: no es `null` y está fuera de 1 a 10.",
              inicial='''
                  import java.util.ArrayList;
                  import java.util.List;

                  public class Acta1 {
                      public static void main(String[] args) {
                          ActaDeExamen acta = new ActaDeExamen("2026-12-10", "Nadia", "Paradigmas III");
                          acta.registrar(new Registro("Zed", 9));
                          acta.registrar(new Registro("Teo", null));
                          acta.registrar(new Registro("Mira", 12));
                          System.out.println(acta.materia + ", cargada por " + acta.cargadaPor + " el " + acta.fecha);
                          acta.registros.forEach(r -> System.out.println("- " + r.alumno() + ": " + (r.nota() == null ? "ausente" : r.nota())));
                      }
                  }

                  record Registro(String alumno, Integer nota) { }

                  abstract class Formulario {
                      final String fecha;
                      final String cargadaPor;

                      Formulario(String fecha, String cargadaPor) {
                          this.fecha = fecha;
                          this.cargadaPor = cargadaPor;
                      }
                  }

                  class ActaDeExamen extends Formulario {
                      final String materia;
                      final List<Registro> registros = new ArrayList<>();

                      ActaDeExamen(String fecha, String cargadaPor, String materia) {
                          super(fecha, cargadaPor);
                          this.materia = materia;
                      }

                      void registrar(Registro r) {
                          if (___) {
                              System.out.println("Rechazado: nota inválida para " + r.alumno());
                              return;
                          }
                          registros.add(r);
                      }
                  }
              ''',
              solucion='''
                  import java.util.ArrayList;
                  import java.util.List;

                  public class Acta1 {
                      public static void main(String[] args) {
                          ActaDeExamen acta = new ActaDeExamen("2026-12-10", "Nadia", "Paradigmas III");
                          acta.registrar(new Registro("Zed", 9));
                          acta.registrar(new Registro("Teo", null));
                          acta.registrar(new Registro("Mira", 12));
                          System.out.println(acta.materia + ", cargada por " + acta.cargadaPor + " el " + acta.fecha);
                          acta.registros.forEach(r -> System.out.println("- " + r.alumno() + ": " + (r.nota() == null ? "ausente" : r.nota())));
                      }
                  }

                  record Registro(String alumno, Integer nota) { }

                  abstract class Formulario {
                      final String fecha;
                      final String cargadaPor;

                      Formulario(String fecha, String cargadaPor) {
                          this.fecha = fecha;
                          this.cargadaPor = cargadaPor;
                      }
                  }

                  class ActaDeExamen extends Formulario {
                      final String materia;
                      final List<Registro> registros = new ArrayList<>();

                      ActaDeExamen(String fecha, String cargadaPor, String materia) {
                          super(fecha, cargadaPor);
                          this.materia = materia;
                      }

                      void registrar(Registro r) {
                          if (r.nota() != null && (r.nota() < 1 || r.nota() > 10)) {
                              System.out.println("Rechazado: nota inválida para " + r.alumno());
                              return;
                          }
                          registros.add(r);
                      }
                  }
              ''',
              al_superar="El 12 de Mira rebota; el ausente de Teo entra como ausente. El primer juez del Tribunal asiente.",
              imagen=["El Tribunal de las Actas: tres jueces de toga en la cima del Palacio, con un acta de examen sobre la mesa.",
                      "Zed escribiendo las reglas del acta; Nadia como la que la cargó."]),
            m(id="S02-N08-P2", titulo="El aula que no alcanza",
              lugar="La cima del Palacio", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Reglas del enunciado | capacidad del aula: no puede haber más alumnos que lugares · un alumno no aparece dos veces (Set)",
              recompensa="xp 20, oro 25",
              escena="""
                  El segundo juez lee dos reglas más: la cantidad de alumnos no puede superar la **capacidad del aula**, y un alumno **no puede aparecer dos veces** en la misma acta.
              """,
              sugiere="Un `HashSet` de alumnos dice si ya estaba (`add` devuelve `false`). Antes de agregar, se revisa que haya lugar: si `inscriptos.size()` ya es la capacidad, se rechaza.",
              desafio="Completá la condición de aula llena.",
              inicial='''
                  import java.util.HashSet;
                  import java.util.Set;

                  public class Acta2 {
                      static final int CAPACIDAD = 3;
                      static final Set<String> inscriptos = new HashSet<>();

                      static void inscribir(String alumno) {
                          if (___) {
                              System.out.println(alumno + ": el aula está llena");
                          } else if (!inscriptos.add(alumno)) {
                              System.out.println(alumno + ": ya estaba en el acta");
                          } else {
                              System.out.println(alumno + ": inscripto (" + inscriptos.size() + "/" + CAPACIDAD + ")");
                          }
                      }

                      public static void main(String[] args) {
                          for (String a : new String[] {"Zed", "Teo", "Zed", "Mira", "Sol"}) {
                              inscribir(a);
                          }
                      }
                  }
              ''',
              solucion='''
                  import java.util.HashSet;
                  import java.util.Set;

                  public class Acta2 {
                      static final int CAPACIDAD = 3;
                      static final Set<String> inscriptos = new HashSet<>();

                      static void inscribir(String alumno) {
                          if (inscriptos.size() >= CAPACIDAD) {
                              System.out.println(alumno + ": el aula está llena");
                          } else if (!inscriptos.add(alumno)) {
                              System.out.println(alumno + ": ya estaba en el acta");
                          } else {
                              System.out.println(alumno + ": inscripto (" + inscriptos.size() + "/" + CAPACIDAD + ")");
                          }
                      }

                      public static void main(String[] args) {
                          for (String a : new String[] {"Zed", "Teo", "Zed", "Mira", "Sol"}) {
                              inscribir(a);
                          }
                      }
                  }
              ''',
              al_superar="Zed no entra dos veces y Sol se queda afuera: no hay lugar. El segundo juez asiente.",
              imagen=["Un aula de piedra con tres bancos ocupados y una alumna esperando en la puerta.",
                      "Un cartel en la puerta: «Capacidad: 3»."]),
            m(id="S02-N08-P3", titulo="El promedio del acta",
              lugar="La cima del Palacio", personajes="Zed, Gheco, Nadia, Kaffa",
              carta="Resumen del acta | los ausentes no cuentan para el promedio · filter + mapToInt + average · Optional por si nadie se presentó",
              recompensa="xp 25, oro 30",
              escena="""
                  El último juez pide el resumen del acta: cuántos se presentaron, cuántos aprobaron (4 o más) y el promedio de los presentes. Los ausentes **no** cuentan para el promedio.
              """,
              sugiere="Con un stream: `filter(r -> r.nota() != null)` deja los presentes; `mapToInt(Registro::nota).average()` da un `OptionalDouble` (puede estar vacío si nadie vino). `orElse(0)` resuelve ese caso.",
              desafio="Completá el filtro de los presentes.",
              inicial='''
                  import java.util.List;

                  public class Acta3 {
                      record Registro(String alumno, Integer nota) { }

                      public static void main(String[] args) {
                          List<Registro> acta = List.of(new Registro("Zed", 9), new Registro("Teo", null),
                                  new Registro("Mira", 4), new Registro("Sol", 2));
                          List<Registro> presentes = acta.stream().filter(r -> ___).toList();
                          long aprobados = presentes.stream().filter(r -> r.nota() >= 4).count();
                          double promedio = presentes.stream().mapToInt(Registro::nota).average().orElse(0);
                          System.out.println("Presentes: " + presentes.size() + " de " + acta.size());
                          System.out.println("Aprobados: " + aprobados);
                          System.out.println("Promedio: " + promedio);
                      }
                  }
              ''',
              solucion='''
                  import java.util.List;

                  public class Acta3 {
                      record Registro(String alumno, Integer nota) { }

                      public static void main(String[] args) {
                          List<Registro> acta = List.of(new Registro("Zed", 9), new Registro("Teo", null),
                                  new Registro("Mira", 4), new Registro("Sol", 2));
                          List<Registro> presentes = acta.stream().filter(r -> r.nota() != null).toList();
                          long aprobados = presentes.stream().filter(r -> r.nota() >= 4).count();
                          double promedio = presentes.stream().mapToInt(Registro::nota).average().orElse(0);
                          System.out.println("Presentes: " + presentes.size() + " de " + acta.size());
                          System.out.println("Aprobados: " + aprobados);
                          System.out.println("Promedio: " + promedio);
                      }
                  }
              ''',
              al_superar="""
                  Tres presentes, dos aprobados, promedio 5. El Tribunal de las Actas golpea el martillo tres veces y le entrega a Zed el **Sello del Palacio**.
                  —Ya sabés construir ventanas —dice Kaffa—. Y con la Bóveda debajo, sistemas enteros.
              """,
              imagen=["Los tres jueces del Tribunal golpeando el martillo a la vez.",
                      "Zed recibiendo un sello de vidrio con la forma de una ventana; Nadia y Gheco aplaudiendo."]),
        ],
    },
]
