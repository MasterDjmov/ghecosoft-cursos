Aquí tienes la especificación completa y detallada de la guía de estilos y tokens del DevLevel Obsidian System ([Design_System]), diseñada para la estética de ciber-aprendizaje, gamificación e interfaces IDE de GhecoSoft-Code:

🎨 1. Paleta de Colores
Fondos y Superficies (Dark Obsidian Base)
Surface Base: #0B1326 (Obsidiana profundo, lienzo principal)
Surface Dim: #0B1326
Surface Bright: #31394D (Elevaciones iluminadas, bordes de sección)
Surface Container Lowest: #060E20 (Fondo de paneles profundos, terminales, sidebars)
Surface Container Low: #131B2E (Tarjetas de misiones, barras superiores/navbars)
Surface Container: #172036 (Superficies modulares intermedias)
Surface Container High: #1D263D (Tarjetas activas, bloques destacados)
Surface Container Highest: #242E47 (Estados hover e inputs activos)
Colores de Acento y Marca (Cyber Neon)
Primary (Cian Neón / Gheco Hologram): #06B6D4 / #22D3EE (Acciones principales, widgets activos, holograma del geco)
Secondary / Accent (Púrpura / Violeta Eléctrico): #8B5CF6 / #A855F7 (Puntos de experiencia, rareza de misiones, circuitos secundarios)
Success / Build OK (Verde Terminal): #10B981 (Tests pasados, estado online, salud)
Warning / Alert (Ámbar Neón): #F59E0B (Advertencias de compilación, misiones críticas)
Error / Bug (Rojo Neón): #EF4444 (Errores de sintaxis, fallos de build, límites de tiempo)
Tipografía y Contraste de Texto
On Surface (Texto Principal): #E2E8F0 (Blanco frío de alto contraste)
On Surface Variant (Texto Secundario): #94A3B8 (Gris azulado para metadatos, descripciones)
Outline / Bordes sutiles: #334155 o rgba(6, 182, 212, 0.2) (Trazos de circuito sutiles)
🔤 2. Tipografía
Familia Tipográfica Principal (Display & UI): Space Grotesk
Uso: Encabezados (h1, h2, h3), títulos de misiones, estadísticas y navegación HUD.
Personalidad: Geométrica, técnica y futurista.
Familia Tipográfica de Código (IDE & Terminales): JetBrains Mono / font-mono
Uso: Editor de código, logs de terminal, inspección de memoria, atajos de teclado y badges de nivel.
Familia para Textos de Lectura (Body): Inter / sans-serif optimizado
Uso: Guiones narrativos, explicaciones de conceptos y enunciados de retos.
📐 3. Formas, Espaciado y Sombras
Bordes y Redondez (Roundness): rounded-md / rounded-lg (esquinas técnicas de 4px a 8px, evitando bordes excesivamente redondeados para mantener el corte de hardware/dispositivo cibernético).
Efectos de Brillo & Sombras (Glow FX):
Cian Halo: box-shadow: 0 0 20px -3px rgba(6, 182, 212, 0.35)
Púrpura Halo: box-shadow: 0 0 20px -3px rgba(139, 92, 246, 0.35)
Elevación profunda: shadow-[0_4px_24px_-2px_rgba(0,0,0,0.7)]
Translucidez (Glassmorphism / Holograma):
backdrop-blur-md combinado con fondos de superficie al 80–90% (rgba(11, 19, 38, 0.85)).
🧩 4. Componentes Globales Registrados
TopNavBar (Web HUD): Barra superior fija con perfil de usuario, nivel ("LVL 42 ARCHITECT"), bóveda de bits/monedas, racha de fuego (local_fire_department) y selector de modos.
SideNavBar / Rail: Navegación lateral acoplada con enlaces a Roadmap, Misiones, Arena de Código PvP, Árbol de Habilidades y estado de red PROTOCOLO C9 // V1.4.0 ONLINE.
Player & Terminal Shell: Paneles divididos con área de ejecución, consola interactiva y asistente flotante del geco tutor.
¿Te gustaría exportar esta configuración como variables CSS / Tailwind config, o aplicarla en una nueva pantalla?