// xUnit de mentira (D119, Acto V): el alumno escribe sus pruebas igual que en un proyecto de verdad (using Xunit; [Fact],
// [Theory], [InlineData], Assert) y, al terminar el programa, el ejecutor las corre y muestra el resultado, como dotnet test.
// Se compila junto al código del alumno; no corre en el servidor.
#nullable enable
using System.Collections;
using System.Reflection;

namespace Xunit
{
    [AttributeUsage(AttributeTargets.Method)]
    public class FactAttribute : Attribute
    {
        public string? Skip { get; set; }
        public string? DisplayName { get; set; }
    }

    [AttributeUsage(AttributeTargets.Method)]
    public class TheoryAttribute : FactAttribute { }

    [AttributeUsage(AttributeTargets.Method, AllowMultiple = true)]
    public class InlineDataAttribute : Attribute
    {
        public object?[] Data { get; }
        public InlineDataAttribute(params object?[] data) => Data = data ?? new object?[] { null };
    }

    /** Lo que tira un Assert que no se cumple. */
    public class AssertFailedException : Exception
    {
        public AssertFailedException(string message) : base(message) { }
    }

    public static class Assert
    {
        private static string Show(object? value) => value switch
        {
            null => "null",
            string s => $"\"{s}\"",
            IEnumerable e => "[" + string.Join(", ", e.Cast<object?>().Select(Show)) + "]",
            _ => Convert.ToString(value, System.Globalization.CultureInfo.CurrentCulture) ?? "",
        };

        private static void Fail(string what, string detail) => throw new AssertFailedException($"Assert.{what}() falló\n{detail}");

        public static void Equal<T>(T expected, T actual)
        {
            bool same = expected is IEnumerable a && actual is IEnumerable b && expected is not string
                ? a.Cast<object?>().SequenceEqual(b.Cast<object?>())
                : EqualityComparer<T>.Default.Equals(expected, actual);
            if (!same) Fail("Equal", $"Esperado: {Show(expected)}\nObtenido: {Show(actual)}");
        }

        public static void Equal(double expected, double actual, int precision)
        {
            if (Math.Round(expected, precision) != Math.Round(actual, precision))
                Fail("Equal", $"Esperado: {expected} (con {precision} decimales)\nObtenido: {actual}");
        }

        public static void NotEqual<T>(T notExpected, T actual)
        {
            if (EqualityComparer<T>.Default.Equals(notExpected, actual)) Fail("NotEqual", $"No tenía que dar: {Show(actual)}");
        }

        public static void True(bool condition, string? userMessage = null)
        {
            if (!condition) Fail("True", userMessage ?? "Esperado: True\nObtenido: False");
        }

        public static void False(bool condition, string? userMessage = null)
        {
            if (condition) Fail("False", userMessage ?? "Esperado: False\nObtenido: True");
        }

        public static void Null(object? value)
        {
            if (value is not null) Fail("Null", $"Esperado: null\nObtenido: {Show(value)}");
        }

        public static void NotNull(object? value)
        {
            if (value is null) Fail("NotNull", "Esperado: algo que no sea null\nObtenido: null");
        }

        public static void Contains(string expectedSubstring, string? actual)
        {
            if (actual is null || !actual.Contains(expectedSubstring)) Fail("Contains", $"No encontré: {Show(expectedSubstring)}\nEn: {Show(actual)}");
        }

        public static void DoesNotContain(string expectedSubstring, string? actual)
        {
            if (actual is not null && actual.Contains(expectedSubstring)) Fail("DoesNotContain", $"No tenía que estar: {Show(expectedSubstring)}\nEn: {Show(actual)}");
        }

        public static void Contains<T>(T expected, IEnumerable<T> collection)
        {
            if (!collection.Contains(expected)) Fail("Contains", $"No encontré: {Show(expected)}\nEn: {Show(collection)}");
        }

        public static void DoesNotContain<T>(T expected, IEnumerable<T> collection)
        {
            if (collection.Contains(expected)) Fail("DoesNotContain", $"No tenía que estar: {Show(expected)}\nEn: {Show(collection)}");
        }

        public static void Empty(IEnumerable collection)
        {
            if (collection.Cast<object?>().Any()) Fail("Empty", $"Esperado: vacía\nObtenido: {Show(collection)}");
        }

        public static void NotEmpty(IEnumerable collection)
        {
            if (!collection.Cast<object?>().Any()) Fail("NotEmpty", "Esperado: con algo adentro\nObtenido: vacía");
        }

        public static T Single<T>(IEnumerable<T> collection)
        {
            var list = collection.ToList();
            if (list.Count != 1) Fail("Single", $"Esperado: un solo elemento\nObtenido: {list.Count}");
            return list[0];
        }

        public static void InRange<T>(T actual, T low, T high) where T : IComparable<T>
        {
            if (actual.CompareTo(low) < 0 || actual.CompareTo(high) > 0) Fail("InRange", $"Esperado: entre {low} y {high}\nObtenido: {actual}");
        }

        public static T Throws<T>(Action testCode) where T : Exception
        {
            try { testCode(); }
            catch (Exception e) when (e.GetType() == typeof(T)) { return (T)e; }
            catch (Exception e) { Fail("Throws", $"Esperada: {typeof(T).Name}\nSaltó: {e.GetType().Name}"); }
            Fail("Throws", $"Esperada: {typeof(T).Name}\nNo saltó ninguna excepción");
            return null!;
        }

        public static T Throws<T>(Func<object?> testCode) where T : Exception => Throws<T>(() => { testCode(); });

        public static async Task<T> ThrowsAsync<T>(Func<Task> testCode) where T : Exception
        {
            try { await testCode(); }
            catch (Exception e) when (e.GetType() == typeof(T)) { return (T)e; }
            catch (Exception e) { Fail("ThrowsAsync", $"Esperada: {typeof(T).Name}\nSaltó: {e.GetType().Name}"); }
            Fail("ThrowsAsync", $"Esperada: {typeof(T).Name}\nNo saltó ninguna excepción");
            return null!;
        }
    }
}

namespace Xunit.Sdk
{
    /** Busca las pruebas del programa y las corre, como dotnet test. Lo llama el ejecutor al terminar. */
    public static class Corredor
    {
        public static async Task<bool> CorrerAsync(Assembly assembly)
        {
            var tests = assembly.GetTypes()
                .SelectMany(t => t.GetMethods(BindingFlags.Instance | BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic)
                    .Where(m => m.GetCustomAttribute<FactAttribute>() != null)
                    .Select(m => (Type: t, Method: m)))
                .OrderBy(x => x.Type.MetadataToken).ThenBy(x => x.Method.MetadataToken)
                .ToList();
            if (tests.Count == 0) return false;

            int passed = 0, failed = 0, skipped = 0;
            var output = Console.Out;
            output.WriteLine("Corriendo las pruebas…");
            foreach (var (type, method) in tests)
            {
                var fact = method.GetCustomAttribute<FactAttribute>()!;
                var cases = method.GetCustomAttributes<InlineDataAttribute>().Select(d => d.Data).ToList();
                if (fact is not TheoryAttribute || cases.Count == 0) cases = new List<object?[]> { Array.Empty<object?>() };
                foreach (var data in cases)
                {
                    string name = fact.DisplayName ?? $"{type.Name}.{method.Name}";
                    if (data.Length > 0) name += "(" + string.Join(", ", data.Select(v => v is string s ? $"\"{s}\"" : Convert.ToString(v) ?? "null")) + ")";
                    if (fact.Skip != null) { skipped++; output.WriteLine($"  ⏭ {name}: salteada ({fact.Skip})"); continue; }
                    try
                    {
                        object? target = method.IsStatic ? null : Activator.CreateInstance(type);
                        var args = Argumentos(data, method.GetParameters());
                        var value = method.Invoke(target, args);
                        if (value is Task task) await task;
                        (target as IDisposable)?.Dispose();
                        passed++;
                        output.WriteLine($"  ✓ {name}");
                    }
                    catch (Exception e)
                    {
                        while (e is TargetInvocationException { InnerException: not null }) e = e.InnerException!;
                        failed++;
                        string why = e is AssertFailedException ? e.Message : $"saltó {e.GetType().Name}: {e.Message}";
                        output.WriteLine($"  ✗ {name}");
                        foreach (var line in why.Split('\n')) output.WriteLine($"      {line}");
                    }
                }
            }
            output.WriteLine();
            string summary = $"Pasaron {passed} de {passed + failed} pruebas.";
            if (skipped > 0) summary += $" Salteadas: {skipped}.";
            output.WriteLine(failed == 0 ? $"{summary} ✓ Todo en verde." : $"{summary} ✗ Fallaron {failed}.");
            return true;
        }

        private static object?[] Argumentos(object?[] data, ParameterInfo[] parameters)
        {
            if (data.Length != parameters.Length)
                throw new InvalidOperationException($"La prueba pide {parameters.Length} datos y el [InlineData] trae {data.Length}.");
            var args = new object?[data.Length];
            for (int i = 0; i < data.Length; i++)
            {
                var target = Nullable.GetUnderlyingType(parameters[i].ParameterType) ?? parameters[i].ParameterType;
                args[i] = data[i] is null || target.IsInstanceOfType(data[i]) ? data[i] : System.Convert.ChangeType(data[i], target);
            }
            return args;
        }
    }
}
