// Ejecutor local de Java: la página le manda el código y este programa, en esta compu, lo compila con javac y
// lo corre con java, con la entrada de ejemplo y tiempo límite. Lo usa el docente al corregir (D69) y el alumno
// para probar su propio código (D85, lo baja de Herramientas → Ejecutor de Java). Java no tiene un compilador
// libre y completo para el navegador (D67): el código del alumno nunca se ejecuta en el servidor.
//
// Uso (JDK 17 o más, sin instalar nada):    java scripts/JavaRunner.java
// Otra plataforma además de las de siempre:  java scripts/JavaRunner.java --origin https://otra.ejemplo
//
// Seguridad: escucha solo en 127.0.0.1 y atiende únicamente pedidos del navegador que vengan de la plataforma
// (encabezado Origin, que una página no puede falsificar) dirigidos a 127.0.0.1/localhost (frena el DNS rebinding).
// Una extensión que reescriba el Origin (como CORS Unblock) rompe esto: hay que apagarla para esta plataforma.
// Anota cada pedido (método, ruta y origen, nunca el código) en la salida: con el servicio, journalctl --user -u javarunner.

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;
import java.util.concurrent.TimeUnit;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Stream;

public class JavaRunner {
    static final int PORT = 17017;
    static final String VERSION = "1";
    static final Set<String> ORIGINS = new TreeSet<>(List.of(
        "https://gamificado.lariojaclick.ar", "http://localhost:8000", "http://127.0.0.1:8000"));
    static final long COMPILE_SECONDS = 20;
    static final long RUN_MS = 5000;
    static final int MAX_OUTPUT = 256 * 1024;

    public static void main(String[] args) throws IOException {
        for (int i = 0; i + 1 < args.length; i++) {
            if (args[i].equals("--origin")) ORIGINS.add(args[++i].replaceAll("/+$", ""));
        }
        HttpServer server;
        try {
            server = HttpServer.create(new InetSocketAddress(InetAddress.getLoopbackAddress(), PORT), 0);
        } catch (java.net.BindException e) {
            System.out.println("Ya hay un ejecutor de Java abierto en esta compu (puerto " + PORT + "): no hace falta abrir otro.");
            return;
        }
        server.createContext("/", JavaRunner::handle);
        server.start();
        System.out.println("Ejecutor de Java listo en http://127.0.0.1:" + PORT + " (Java " + Runtime.version() + ").");
        System.out.println("Atiende a: " + String.join(", ", ORIGINS));
        System.out.println("Dejalo abierto mientras uses la plataforma; para cerrarlo, Ctrl+C o cerrá esta ventana.");
    }

    static synchronized void handle(HttpExchange ex) throws IOException {
        try (ex) {
            String origin = ex.getRequestHeaders().getFirst("Origin");
            String host = String.valueOf(ex.getRequestHeaders().getFirst("Host")).replaceAll(":\\d+$", "");
            // Una línea por pedido (sin el código): sirve para ver si el navegador llega hasta acá.
            System.out.println(java.time.LocalTime.now().withNano(0) + " " + ex.getRequestMethod() + " " + ex.getRequestURI().getPath()
                + " desde " + origin + " (host " + host + ")");
            if (!allowed(origin) || !(host.equals("127.0.0.1") || host.equals("localhost"))) {
                System.out.println("  rechazado: origen o host no permitidos" + ("http://127.0.0.1".equals(origin) ? " (¿una extensión como Page Assist o CORS Unblock cambió el origen?)" : ""));
                send(ex, 403, "{\"error\":\"origen no permitido\"}", null);
                return;
            }
            if (ex.getRequestMethod().equals("OPTIONS")) {
                send(ex, 204, null, origin);
                return;
            }
            String path = ex.getRequestURI().getPath();
            if (path.equals("/ping")) {
                send(ex, 200, "{\"ok\":true,\"version\":\"" + VERSION + "\",\"java\":" + json(Runtime.version().toString()) + "}", origin);
            } else if (path.equals("/run") && ex.getRequestMethod().equals("POST")) {
                Map<String, String> body = parseObject(new String(ex.getRequestBody().readAllBytes(), StandardCharsets.UTF_8));
                send(ex, 200, run(body.getOrDefault("code", ""), body.getOrDefault("stdin", "")), origin);
            } else {
                send(ex, 404, "{\"error\":\"no existe\"}", origin);
            }
        } catch (Exception e) {
            System.err.println("Error: " + e);
        }
    }

    /**
     * Solo orígenes exactos (producción, la copia local del puerto 8000 y los de --origin). No se acepta
     * «cualquier página de esta compu»: extensiones como CORS Unblock reescriben el Origin de cualquier sitio
     * a http://127.0.0.1, y así una página ajena podría correr código en la compu del docente.
     */
    static boolean allowed(String origin) {
        return origin != null && ORIGINS.contains(origin);
    }

    static void send(HttpExchange ex, int status, String body, String origin) throws IOException {
        if (origin != null) {
            ex.getResponseHeaders().set("Access-Control-Allow-Origin", origin);
            ex.getResponseHeaders().set("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
            ex.getResponseHeaders().set("Access-Control-Allow-Headers", "Content-Type");
            // Chrome pide permiso para que una página pública hable con la compu (Private/Local Network Access).
            ex.getResponseHeaders().set("Access-Control-Allow-Private-Network", "true");
            ex.getResponseHeaders().set("Vary", "Origin");
        }
        if (body == null) {
            ex.sendResponseHeaders(status, -1);
            return;
        }
        byte[] bytes = body.getBytes(StandardCharsets.UTF_8);
        ex.getResponseHeaders().set("Content-Type", "application/json; charset=utf-8");
        ex.sendResponseHeaders(status, bytes.length);
        ex.getResponseBody().write(bytes);
    }

    /** Compila y corre un archivo: la clase pública (o la que tiene main), con su package si lo declara. */
    static String run(String code, String stdin) throws Exception {
        Matcher pub = Pattern.compile("public\\s+(?:(?:final|abstract)\\s+)*(?:class|record|enum|interface)\\s+(\\w+)").matcher(code);
        String file = pub.find() ? pub.group(1) : "Main";
        // La clase con main: la última declaración antes del primer "static void main" (casi siempre, la pública).
        String mainClass = file;
        int main = code.indexOf("static void main");
        Matcher declared = Pattern.compile("\\b(?:class|record|enum)\\s+(\\w+)").matcher(main < 0 ? "" : code.substring(0, main));
        while (declared.find()) mainClass = declared.group(1);
        Matcher pkg = Pattern.compile("^\\s*package\\s+([\\w.]+)\\s*;", Pattern.MULTILINE).matcher(code);
        if (pkg.find()) mainClass = pkg.group(1) + "." + mainClass;

        Path dir = Files.createTempDirectory("ghecosoft-java-");
        try {
            Files.writeString(dir.resolve(file + ".java"), code);
            String java = Path.of(System.getProperty("java.home"), "bin", "java").toString();
            String javac = Path.of(System.getProperty("java.home"), "bin", "javac").toString();
            if (!Files.exists(Path.of(javac)) && !Files.exists(Path.of(javac + ".exe"))) {
                return "{\"compiled\":false,\"diagnostics\":" + json("Este Java no trae javac (es un JRE). Instalá el JDK: https://adoptium.net (Temurin 21, LTS).") + "}";
            }

            Result compiled = exec(List.of(javac, "-encoding", "UTF-8", "-Xlint:none", "-d", "out", file + ".java"), dir, "", COMPILE_SECONDS * 1000);
            if (compiled.timedOut || compiled.exit != 0) {
                String diagnostics = compiled.timedOut ? "javac tardó demasiado." : compiled.err + compiled.out;
                return "{\"compiled\":false,\"diagnostics\":" + json(diagnostics) + "}";
            }

            long started = System.nanoTime();
            Result ran = exec(List.of(java, "-Xmx256m", "-Xss8m", "-Dfile.encoding=UTF-8", "-Dstdout.encoding=UTF-8", "-Dstderr.encoding=UTF-8",
                "-cp", "out", mainClass), dir, stdin, RUN_MS);
            long ms = (System.nanoTime() - started) / 1_000_000;
            return "{\"compiled\":true,\"diagnostics\":" + json(compiled.err) + ",\"output\":" + json(ran.out) + ",\"errors\":" + json(ran.err)
                + ",\"exit\":" + ran.exit + ",\"timedOut\":" + ran.timedOut + ",\"truncated\":" + ran.truncated + ",\"ms\":" + ms + "}";
        } finally {
            try (Stream<Path> files = Files.walk(dir)) {
                files.sorted(Comparator.reverseOrder()).forEach(p -> p.toFile().delete());
            }
        }
    }

    record Result(String out, String err, int exit, boolean timedOut, boolean truncated) {}

    static Result exec(List<String> command, Path dir, String stdin, long timeoutMs) throws Exception {
        Process process = new ProcessBuilder(command).directory(dir.toFile()).start();
        Capture out = new Capture(process.getInputStream());
        Capture err = new Capture(process.getErrorStream());
        out.start();
        err.start();
        try (OutputStream in = process.getOutputStream()) {
            in.write(stdin.replace("\r\n", "\n").getBytes(StandardCharsets.UTF_8));
        } catch (IOException ignored) {
            // El programa terminó sin leer toda la entrada.
        }
        boolean finished = process.waitFor(timeoutMs, TimeUnit.MILLISECONDS);
        if (!finished) {
            process.descendants().forEach(ProcessHandle::destroyForcibly);
            process.destroyForcibly();
            process.waitFor(2, TimeUnit.SECONDS);
        }
        out.join(2000);
        err.join(2000);
        return new Result(out.text(), err.text(), finished ? process.exitValue() : -1, !finished, out.truncated || err.truncated);
    }

    /** Lee una salida hasta MAX_OUTPUT (un println en un bucle no llena la memoria). */
    static class Capture extends Thread {
        final InputStream stream;
        final ByteArrayOutputStream buffer = new ByteArrayOutputStream();
        volatile boolean truncated;

        Capture(InputStream stream) {
            this.stream = stream;
            setDaemon(true);
        }

        @Override
        public void run() {
            byte[] chunk = new byte[8192];
            try {
                for (int n; (n = stream.read(chunk)) > 0; ) {
                    int room = MAX_OUTPUT - buffer.size();
                    if (room > 0) buffer.write(chunk, 0, Math.min(n, room));
                    if (n > room) truncated = true;
                }
            } catch (IOException ignored) {
                // El proceso se cortó.
            }
        }

        synchronized String text() {
            return buffer.toString(StandardCharsets.UTF_8);
        }
    }

    // --- JSON mínimo: un objeto plano de strings de entrada y strings escapados de salida. ---

    static Map<String, String> parseObject(String s) {
        Map<String, String> map = new LinkedHashMap<>();
        int[] i = {0};
        skip(s, i);
        expect(s, i, '{');
        skip(s, i);
        if (s.charAt(i[0]) == '}') return map;
        while (true) {
            skip(s, i);
            String key = parseString(s, i);
            skip(s, i);
            expect(s, i, ':');
            skip(s, i);
            if (s.charAt(i[0]) == '"') {
                map.put(key, parseString(s, i));
            } else {
                int start = i[0];
                while (i[0] < s.length() && ",}".indexOf(s.charAt(i[0])) < 0) i[0]++;
                map.put(key, s.substring(start, i[0]).trim());
            }
            skip(s, i);
            if (s.charAt(i[0]) == ',') {
                i[0]++;
                continue;
            }
            expect(s, i, '}');
            return map;
        }
    }

    static String parseString(String s, int[] i) {
        expect(s, i, '"');
        StringBuilder sb = new StringBuilder();
        while (true) {
            char c = s.charAt(i[0]++);
            if (c == '"') return sb.toString();
            if (c != '\\') {
                sb.append(c);
                continue;
            }
            char e = s.charAt(i[0]++);
            switch (e) {
                case 'n' -> sb.append('\n');
                case 't' -> sb.append('\t');
                case 'r' -> sb.append('\r');
                case 'b' -> sb.append('\b');
                case 'f' -> sb.append('\f');
                case 'u' -> {
                    sb.append((char) Integer.parseInt(s.substring(i[0], i[0] + 4), 16));
                    i[0] += 4;
                }
                default -> sb.append(e);
            }
        }
    }

    static void skip(String s, int[] i) {
        while (i[0] < s.length() && Character.isWhitespace(s.charAt(i[0]))) i[0]++;
    }

    static void expect(String s, int[] i, char c) {
        if (i[0] >= s.length() || s.charAt(i[0]) != c) throw new IllegalArgumentException("JSON inválido");
        i[0]++;
    }

    static String json(String s) {
        StringBuilder sb = new StringBuilder("\"");
        for (char c : s.toCharArray()) {
            switch (c) {
                case '"' -> sb.append("\\\"");
                case '\\' -> sb.append("\\\\");
                case '\n' -> sb.append("\\n");
                case '\r' -> sb.append("\\r");
                case '\t' -> sb.append("\\t");
                default -> {
                    if (c < 0x20) sb.append(String.format("\\u%04x", (int) c));
                    else sb.append(c);
                }
            }
        }
        return sb.append('"').toString();
    }
}
