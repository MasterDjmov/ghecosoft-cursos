// Prueba de aceptación del ejecutor de C# en Chrome: consola, teclado, cultura, await, archivos en una carpeta de mentira,
// errores y topes. Correrla después de tocar scripts/csharp-runner o resources/js/runners/csharp*:
//   node scripts/csharp-micro/probar-ejecutor.mjs
import { openChrome } from './chrome.mjs';

const CASES = [
    ['consola', 'Console.WriteLine("Hola");\nConsole.Write("do");\nConsole.WriteLine(2 + 3);', {}, { output: 'Hola\ndo5\n' }],
    ['teclado', 'var n = Console.ReadLine();\nvar e = int.Parse(Console.ReadLine()!);\nConsole.WriteLine($"{n} {e + 1}");', { stdin: 'Ana\n14\n' }, { output: 'Ana 15\n' }],
    ['ReadLine sin entrada da null', 'Console.WriteLine(Console.ReadLine() is null);', {}, { output: 'True\n' }],
    ['coma decimal, como en una compu de acá', 'double d = 3.5; decimal p = 1234.5m;\nConsole.WriteLine(d);\nConsole.WriteLine($"{p:N2} {p:F1}");\nConsole.WriteLine(double.Parse("2,5") + 1);', {}, { output: '3,5\n1.234,50 1234,5\n3,5\n' }],
    ['LINQ, listas y records', 'var l = new List<int>{3,1,2};\nConsole.WriteLine(string.Join(",", l.OrderBy(x => x)));\nConsole.WriteLine(new Nota("do", 4));\nrecord Nota(string Nombre, int Duracion);', {}, { output: '1,2,3\nNota { Nombre = do, Duracion = 4 }\n' }],
    ['await en el programa principal', 'Console.WriteLine("antes");\nawait Task.Delay(20);\nConsole.WriteLine("después");', {}, { output: 'antes\ndespués\n' }],
    ['clase con Main', 'class P { static void Main() { System.Console.WriteLine("main"); } }', {}, { output: 'main\n' }],
    ['archivos: en una carpeta de mentira que arranca vacía', 'File.WriteAllText("a.txt", "hola");\nConsole.WriteLine(File.ReadAllText("a.txt"));\nConsole.WriteLine(Directory.GetFiles(".").Length);', {}, { output: 'hola\n1\n' }],
    ['la siguiente ejecución no ve esos archivos', 'Console.WriteLine(File.Exists("a.txt"));', {}, { output: 'False\n' }],
    ['Random con semilla da siempre lo mismo', 'var r = new Random(42);\nConsole.WriteLine(r.Next(100));', {}, { same: true }],
    ['error de compilación con línea y en español', 'Console.WriteLine("hola")\nConsole.WriteLine("chau");', {}, { error: ['Programa.cs(1,26)', 'CS1002', 'Se esperaba', 'Slime'] }],
    ['tipos que no encajan', 'int x = "hola";', {}, { error: ['CS0029', 'Goblin'] }],
    ['nombre que no existe', 'Console.WriteLine(nada);', {}, { error: ['CS0103', 'Esqueleto'] }],
    ['maldición con la salida de antes', 'Console.WriteLine("antes");\nint[] a = new int[1];\nConsole.WriteLine(a[3]);', {}, { output: 'antes\n', error: ['IndexOutOfRange', 'Orco', 'Index was outside'] }],
    ['null', 'string? s = null;\nConsole.WriteLine(s!.Length);', {}, { error: ['NullReference', 'Troll'] }],
    ['while (true) se corta', 'while (true) { }', { timeout: 1500 }, { timedOut: true }],
    ['imprimir sin parar no se come la memoria', 'while (true) Console.WriteLine("xxxxxxxxxxxxxxxx");', { timeout: 3000 }, { error: ['demasiado larga'] }],
    ['después de un corte vuelve a andar', 'Console.WriteLine("volví");', {}, { output: 'volví\n' }],
    ['recursión sin fin', 'int F(int n) => F(n + 1) + 1;\nConsole.WriteLine(F(0));', { timeout: 4000 }, { anyError: true }],
    // Acto V: la xUnit, la Bóveda y la ventanilla de mentira (scripts/csharp-runner/Prelude), y la carrera sin hilos.
    ['xUnit: un archivo de pruebas sin programa principal', 'using Xunit;\npublic class P {\n [Fact] public void Bien() => Assert.Equal(4, 2 + 2);\n [Theory]\n [InlineData(1, 2)]\n [InlineData(2, 5)]\n public void Doble(int a, int b) => Assert.Equal(b, a * 2);\n}', {}, { output: 'Corriendo las pruebas…\n  ✓ P.Bien\n  ✓ P.Doble(1, 2)\n  ✗ P.Doble(2, 5)\n      Assert.Equal() falló\n      Esperado: 5\n      Obtenido: 4\n\nPasaron 2 de 3 pruebas. ✗ Fallaron 1.\n' }],
    ['la Bóveda: SQLite con parámetros, lector y escalar', 'using Microsoft.Data.Sqlite;\nusing var con = new SqliteConnection("Data Source=boveda.db");\ncon.Open();\nvar cmd = con.CreateCommand();\ncmd.CommandText = "CREATE TABLE t (id INTEGER PRIMARY KEY, n TEXT)";\ncmd.ExecuteNonQuery();\ncmd.CommandText = "INSERT INTO t (n) VALUES ($n)";\ncmd.Parameters.AddWithValue("$n", "violín");\nConsole.WriteLine(cmd.ExecuteNonQuery());\ncmd.Parameters.Clear();\ncmd.CommandText = "SELECT id, n FROM t";\nusing var r = cmd.ExecuteReader();\nwhile (r.Read()) Console.WriteLine($"{r.GetInt32(0)} {r.GetString(1)}");\nvar c = con.CreateCommand(); c.CommandText = "SELECT COUNT(*) FROM t";\nConsole.WriteLine((long)c.ExecuteScalar()!);', {}, { output: '1\n1 violín\n1\n' }],
    ['la Bóveda arranca vacía en cada ejecución', 'using Microsoft.Data.Sqlite;\nvar con = new SqliteConnection("Data Source=boveda.db"); con.Open();\nvar c = con.CreateCommand(); c.CommandText = "SELECT * FROM t";\ntry { c.ExecuteReader(); } catch (SqliteException e) { Console.WriteLine(e.Message); }', {}, { output: "SQLite Error 1: 'no such table: t'.\n" }],
    ['la ventanilla: rutas, códigos y JSON', 'var app = WebApplication.CreateBuilder(args).Build();\nvar l = new List<Nota> { new(1, "do") };\napp.MapGet("/notas/{id:int}", (int id) => l.FirstOrDefault(n => n.Id == id) is { } n ? Results.Ok(n) : Results.NotFound());\napp.MapPost("/notas", (Nota n) => { l.Add(n); return Results.Created($"/notas/{n.Id}", n); });\nvar cli = app.CreateClient();\nvar r = await cli.GetAsync("/notas/1");\nConsole.WriteLine($"{(int)r.StatusCode} {await r.Content.ReadAsStringAsync()}");\nConsole.WriteLine((int)(await cli.GetAsync("/notas/9")).StatusCode);\nConsole.WriteLine((int)(await cli.PostAsJsonAsync("/notas", new Nota(2, "re"))).StatusCode);\nConsole.WriteLine((int)(await cli.DeleteAsync("/notas/1")).StatusCode);\nrecord Nota(int Id, string Nombre);', {}, { output: '200 {"id":1,"nombre":"do"}\n404\n201\n405\n' }],
    ['la carrera pierde aplausos y el candado la arregla', 'int a = 0;\nasync Task Mal() { for (int i = 0; i < 100; i++) { int v = a; await Task.Yield(); a = v + 1; } }\nawait Task.WhenAll(Enumerable.Range(0, 10).Select(_ => Mal()));\nConsole.WriteLine(a);\nvar candado = new SemaphoreSlim(1); int b = 0;\nasync Task Bien() { for (int i = 0; i < 100; i++) { await candado.WaitAsync(); try { int v = b; await Task.Yield(); b = v + 1; } finally { candado.Release(); } } }\nawait Task.WhenAll(Enumerable.Range(0, 10).Select(_ => Bien()));\nConsole.WriteLine(b);', {}, { output: '100\n1000\n' }],
    // Senda del Puerto (S03): el Puerto de Elefa de mentira (Prelude/Puerto.cs).
    ['el Puerto: GET, 404 y POST', 'var p = Puerto.CreateClient();\nConsole.WriteLine(await p.GetStringAsync("hola"));\nvar b = await p.GetFromJsonAsync<List<Barco>>("barcos");\nConsole.WriteLine($"{b!.Count} {b[1].Nombre} {b[1].Carga}");\nvar r = await p.GetAsync("barcos/9");\nConsole.WriteLine($"{(int)r.StatusCode} {await r.Content.ReadAsStringAsync()}");\nvar c = await p.PostAsJsonAsync("mensajes", new { de = "Ceci", texto = "Hola" });\nConsole.WriteLine($"{(int)c.StatusCode} {await c.Content.ReadAsStringAsync()}");\nConsole.WriteLine((int)(await p.PostAsJsonAsync("mensajes", new { de = "Ceci" })).StatusCode);\nrecord Barco(int Id, string Nombre, string Carga);', {}, { output: '{"mensaje":"¡Hola, Ceci! Te escribe Elefa desde el Puerto.","de":"Elefa"}\n4 El Ancla Azul cuerdas\n404 {"error":"No hay ningún barco con el número 9."}\n201 {"id":3,"de":"Ceci","texto":"Hola"}\n422\n' }],
    ['el Puerto: Timeout, token, tormenta y JSON roto', 'var p = Puerto.CreateClient();\np.Timeout = TimeSpan.FromMilliseconds(300);\ntry { await p.GetAsync("lento"); } catch (TaskCanceledException) { Console.WriteLine("tardó"); }\nvar q = Puerto.CreateClient();\nusing var cts = new CancellationTokenSource(200);\ntry { await q.GetAsync("lento", cts.Token); } catch (OperationCanceledException) { Console.WriteLine("cancelado"); }\nfor (int i = 1; i <= 3; i++) Console.WriteLine((int)(await q.GetAsync("tormenta")).StatusCode);\ntry { await q.GetFromJsonAsync<object>("roto"); } catch (System.Text.Json.JsonException) { Console.WriteLine("roto"); }\ntry { await q.GetStringAsync("error"); } catch (HttpRequestException e) { Console.WriteLine((int?)e.StatusCode); }', { timeout: 4000 }, { output: 'tardó\ncancelado\n503\n503\n200\nroto\n500\n' }],
    ['la ventanilla le pasa el pedido al Puerto', 'var puerto = Puerto.CreateClient();\nvar app = WebApplication.CreateBuilder(args).Build();\napp.MapGet("/llegadas", async () => Results.Ok((await puerto.GetFromJsonAsync<List<Barco>>("barcos"))!.Select(b => b.Nombre)));\nConsole.WriteLine(await app.CreateClient().GetStringAsync("/llegadas"));\nrecord Barco(int Id, string Nombre, string Carga);', {}, { output: '["La Gaviota","El Ancla Azul","La Marea","El Faro Viejo"]\n' }],
    ['no hay red: HttpClient no llega a ningún lado', 'try { var h = new System.Net.Http.HttpClient(); var t = await h.GetStringAsync("http://127.0.0.1:1/"); Console.WriteLine("salió"); } catch (Exception e) { Console.WriteLine("sin red"); }', { timeout: 4000 }, { notOutput: 'salió' }],
];

const chrome = await openChrome();
const t0 = Date.now();
const first = await chrome.run('Console.WriteLine("listo");');
console.log(`Primera carga: ${((Date.now() - t0) / 1000).toFixed(1)} s → ${JSON.stringify(first.output)} ${first.error ?? ''}`);
let failed = 0;
for (const [name, code, options, want] of CASES) {
    const t = Date.now();
    const got = await chrome.run(code, options);
    const problems = [];
    if (want.output !== undefined && got.output !== want.output) problems.push(`salida ${JSON.stringify(got.output)}`);
    for (const part of want.error ?? []) if (!(got.error ?? '').includes(part)) problems.push(`falta «${part}» en: ${got.error}`);
    if (want.timedOut && !got.timedOut) problems.push(`no se cortó: ${JSON.stringify(got)}`);
    if (want.anyError && !got.error) problems.push('sin error');
    if (want.notOutput && (got.output ?? '').includes(want.notOutput)) problems.push('salió a la red');
    if (want.same) { const again = await chrome.run(code, options); if (again.output !== got.output || !got.output) problems.push('no da lo mismo'); }
    console.log(`${problems.length ? '✗' : '✓'} ${name} (${Date.now() - t} ms)${problems.length ? '\n    ' + problems.join('\n    ') : ''}`);
    failed += problems.length ? 1 : 0;
}
chrome.close();
console.log(failed ? `${failed} fallaron` : `${CASES.length} de ${CASES.length}`);
process.exit(failed ? 1 : 0);
