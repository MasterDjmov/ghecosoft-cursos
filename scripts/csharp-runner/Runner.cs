// Compila y ejecuta C# en el navegador: nada de esto corre en el servidor. Consola, teclado y carpeta son de mentira:
// la salida queda en memoria, el teclado sale de la Entrada y cada ejecución tiene una carpeta vacía que se borra al final.
using System.Globalization;
using System.Reflection;
using System.Runtime.InteropServices.JavaScript;
using System.Text;
using System.Text.Json;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;

public partial class Runner
{
    private const string Usings = "global using System; global using System.Collections.Generic; global using System.IO; global using System.Linq; global using System.Net.Http; global using System.Net.Http.Json; global using System.Threading; global using System.Threading.Tasks; global using Microsoft.AspNetCore.Builder; global using Microsoft.AspNetCore.Http;";
    private const int MaxOutput = 200_000;

    private static List<MetadataReference> references;

    public static void Main() { }

    [JSImport("globalThis.csharpCompiled")]
    private static partial void NotifyCompiled();

    /** La Bóveda (Prelude/Sqlite.cs): le pasa el SQL al SQLite en WebAssembly del worker, que contesta en el acto. */
    [JSImport("globalThis.csharpSql")]
    private static partial string Sql(string request);

    private static Assembly prelude;
    private static MetadataReference preludeReference;

    /**
     * La xUnit, la Bóveda y la ventanilla de mentira (Prelude/*.cs): se compilan una sola vez, al cargar (compilar en
     * WebAssembly es lento), y el programa del alumno las usa como una biblioteca más.
     */
    private static MetadataReference Prelude(CSharpParseOptions options)
    {
        if (preludeReference != null) return preludeReference;
        var assembly = typeof(Runner).Assembly;
        var trees = new List<SyntaxTree> { CSharpSyntaxTree.ParseText(Usings, options) };
        foreach (var name in assembly.GetManifestResourceNames().Where(n => n.StartsWith("prelude/")))
        {
            using var reader = new StreamReader(assembly.GetManifestResourceStream(name));
            trees.Add(CSharpSyntaxTree.ParseText(reader.ReadToEnd(), options, name, Encoding.UTF8));
        }
        var compilation = CSharpCompilation.Create("Conservatorio.Prelude", trees, References(),
            new CSharpCompilationOptions(OutputKind.DynamicallyLinkedLibrary, nullableContextOptions: NullableContextOptions.Enable, concurrentBuild: false));
        using var image = new MemoryStream();
        var result = compilation.Emit(image);
        if (!result.Success) throw new InvalidOperationException("Prelude: " + string.Join("\n", result.Diagnostics.Where(d => d.Severity == DiagnosticSeverity.Error)));
        prelude = Assembly.Load(image.ToArray());
        AppDomain.CurrentDomain.AssemblyResolve += (_, e) => new AssemblyName(e.Name).Name == "Conservatorio.Prelude" ? prelude : null;
        preludeReference = MetadataReference.CreateFromImage(image.ToArray());
        return preludeReference;
    }

    /** Las referencias del framework, para que el compilador conozca Console, List<T>…; se leen una sola vez. */
    private static List<MetadataReference> References()
    {
        if (references != null) return references;
        references = new();
        var assembly = typeof(Runner).Assembly;
        foreach (var name in assembly.GetManifestResourceNames().Where(n => n.StartsWith("ref/")))
        {
            using var stream = assembly.GetManifestResourceStream(name);
            references.Add(MetadataReference.CreateFromStream(stream));
        }
        return references;
    }

    private static readonly CultureInfo Riojana = MakeCulture();

    /** Como en una compu de acá: coma decimal y punto de miles, para que el programa dé lo mismo que con dotnet. */
    private static CultureInfo MakeCulture() => new CultureInfo("es-AR");

    /** Corta el programa que imprime sin parar, antes de que se coma la memoria. */
    private sealed class LimitedWriter(StringBuilder target) : StringWriter(target, Riojana)
    {
        public override void Write(char value) { Check(1); base.Write(value); }
        public override void Write(string value) { Check(value?.Length ?? 0); base.Write(value); }
        public override void Write(char[] buffer, int index, int count) { Check(count); base.Write(buffer, index, count); }
        private void Check(int more)
        {
            if (GetStringBuilder().Length + more > MaxOutput) throw new IOException("La salida es demasiado larga: ¿hay un bucle que no termina?");
        }
    }

    [JSExport]
    public static async Task<string> Run(string code, string stdin)
    {
        var options = new CSharpParseOptions(LanguageVersion.Preview);
        var trees = new List<SyntaxTree> { CSharpSyntaxTree.ParseText(code, options, "Programa.cs", Encoding.UTF8), CSharpSyntaxTree.ParseText(Usings, options) };
        var references = References().Append(Prelude(options));
        CSharpCompilation Compile(OutputKind kind) => CSharpCompilation.Create("Programa", trees, references,
            new CSharpCompilationOptions(kind, nullableContextOptions: NullableContextOptions.Enable, concurrentBuild: false));

        var image = new MemoryStream();
        var result = Compile(OutputKind.ConsoleApplication).Emit(image);
        // Un archivo de pruebas no tiene programa principal (CS5001): se compila como biblioteca y solo se corren las pruebas.
        if (!result.Success && result.Diagnostics.Where(d => d.Severity == DiagnosticSeverity.Error).All(d => d.Id == "CS5001"))
        {
            image = new MemoryStream();
            result = Compile(OutputKind.DynamicallyLinkedLibrary).Emit(image);
        }
        var spanish = Riojana;
        string Show(Diagnostic d) => CSharpDiagnosticFormatter.Instance.Format(d, spanish);
        var errors = result.Diagnostics.Where(d => d.Severity == DiagnosticSeverity.Error).Select(Show).ToArray();
        // Las de null (CS86xx) son ruido para quien empieza: Console.ReadLine() ya daría una.
        var warnings = result.Diagnostics.Where(d => d.Severity == DiagnosticSeverity.Warning && !d.Id.StartsWith("CS86")).Select(Show).ToArray();
        if (!result.Success) return JsonSerializer.Serialize(new { compiled = false, errors, warnings });

        NotifyCompiled();

        var output = new StringBuilder();
        var writer = new LimitedWriter(output);
        Console.SetOut(writer);
        Console.SetError(writer);
        Console.SetIn(new StringReader(stdin ?? ""));
        CultureInfo.CurrentCulture = Riojana;
        CultureInfo.CurrentUICulture = Riojana;

        var folder = Path.Combine(Path.GetTempPath(), "programa-" + Guid.NewGuid().ToString("N"));
        Directory.CreateDirectory(folder);
        Directory.SetCurrentDirectory(folder);

        AppDomain.CurrentDomain.SetData("Conservatorio.Sql", new Func<string, string>(Sql));

        string curse = null;
        try
        {
            var assembly = Assembly.Load(image.ToArray());
            await RunMain(assembly);
            // Si el programa tiene pruebas ([Fact], [Theory]), se corren al final, como dotnet test.
            await (Task)prelude.GetType("Xunit.Sdk.Corredor").GetMethod("CorrerAsync").Invoke(null, new object[] { assembly });
        }
        catch (TargetInvocationException e) { curse = Scroll(e.InnerException); }
        catch (Exception e) { curse = Scroll(e); }

        Directory.SetCurrentDirectory(Path.GetTempPath());
        try { Directory.Delete(folder, true); } catch (IOException) { }

        return JsonSerializer.Serialize(new { compiled = true, errors, warnings, output = output.ToString(), curse });
    }

    private static async Task RunMain(Assembly assembly)
    {
        {
            var entry = assembly.EntryPoint;
            if (entry == null) return;
            // Con await en el programa principal, la entrada de verdad espera bloqueando (acá no se puede): se llama a la que devuelve el Task.
            var main = entry.DeclaringType.GetMethods(BindingFlags.Static | BindingFlags.NonPublic | BindingFlags.Public)
                .FirstOrDefault(m => m != entry && m.Name.Contains("Main") && typeof(Task).IsAssignableFrom(m.ReturnType)) ?? entry;
            var value = main.Invoke(null, main.GetParameters().Length == 0 ? null : new object[] { Array.Empty<string>() });
            if (value is Task task) await task;
        }
    }

    /** El pergamino de la maldición, sin las líneas de la maquinaria que invoca al programa. */
    private static string Scroll(Exception e)
    {
        var lines = e.ToString().Split('\n').Where(l => !l.Contains("System.Reflection.") && !l.Contains("Runner.Run"));
        return string.Join("\n", lines).TrimEnd();
    }
}
