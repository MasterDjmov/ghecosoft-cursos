// La ventanilla (D119, Acto V): una API web de mentira con la forma de las minimal APIs de ASP.NET (WebApplication,
// MapGet/MapPost/MapPut/MapDelete, Results). En el navegador no se puede abrir un servidor: en vez de app.Run(), se le
// habla con app.CreateClient(), un HttpClient de verdad cuyos pedidos no salen a la red sino que los atiende la
// ventanilla (como WebApplicationFactory en las pruebas de ASP.NET). Se compila junto al código del alumno.
#nullable enable
using System.Net;
using System.Net.Http;
using System.Reflection;
using System.Text;
using System.Text.Encodings.Web;
using System.Text.Json;
using Microsoft.AspNetCore.Http;

namespace Microsoft.AspNetCore.Http
{
    /** Lo que contesta la ventanilla: un código de estado y, a veces, algo adentro. */
    public interface IResult
    {
        int StatusCode { get; }
        object? Value { get; }
    }

    internal sealed record Respuesta(int StatusCode, object? Value, string? Location = null, bool Texto = false) : IResult;

    public static class Results
    {
        public static IResult Ok(object? value = null) => new Respuesta(200, value);
        public static IResult Created(string? uri = null, object? value = null) => new Respuesta(201, value, uri);
        public static IResult Accepted(string? uri = null, object? value = null) => new Respuesta(202, value, uri);
        public static IResult NoContent() => new Respuesta(204, null);
        public static IResult BadRequest(object? error = null) => new Respuesta(400, error);
        public static IResult Unauthorized() => new Respuesta(401, null);
        public static IResult Forbid() => new Respuesta(403, null);
        public static IResult NotFound(object? value = null) => new Respuesta(404, value);
        public static IResult Conflict(object? error = null) => new Respuesta(409, error);
        public static IResult UnprocessableEntity(object? error = null) => new Respuesta(422, error);
        public static IResult StatusCode(int statusCode) => new Respuesta(statusCode, null);
        public static IResult Json(object? data, int? statusCode = null) => new Respuesta(statusCode ?? 200, data);
        public static IResult Text(string content, string? contentType = null, int? statusCode = null) => new Respuesta(statusCode ?? 200, content, null, true);
        public static IResult Problem(string? detail = null, int? statusCode = null, string? title = null) =>
            new Respuesta(statusCode ?? 500, new { title = title ?? "Hubo un problema", status = statusCode ?? 500, detail });
    }

    public static class StatusCodes
    {
        public const int Status200OK = 200, Status201Created = 201, Status204NoContent = 204, Status400BadRequest = 400,
            Status404NotFound = 404, Status409Conflict = 409, Status500InternalServerError = 500;
    }
}

namespace Microsoft.AspNetCore.Builder
{
    public class WebApplicationBuilder
    {
        public WebApplication Build() => new WebApplication();
    }

    public class RouteHandlerBuilder
    {
        public RouteHandlerBuilder WithName(string name) => this;
        public RouteHandlerBuilder WithTags(params string[] tags) => this;
    }

    public class WebApplication
    {
        internal static readonly JsonSerializerOptions Json = new(JsonSerializerDefaults.Web) { Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping };

        internal sealed record Ruta(string Metodo, string Patron, string[] Partes, Delegate Manejador);
        private readonly List<Ruta> rutas = new();

        internal WebApplication() { }

        public static WebApplicationBuilder CreateBuilder(string[]? args = null) => new();
        public static WebApplication Create(string[]? args = null) => new();

        private RouteHandlerBuilder Map(string method, string pattern, Delegate handler)
        {
            var parts = pattern.Trim('/').Split('/', StringSplitOptions.RemoveEmptyEntries);
            rutas.Add(new Ruta(method, pattern, parts, handler));
            return new RouteHandlerBuilder();
        }

        public RouteHandlerBuilder MapGet(string pattern, Delegate handler) => Map("GET", pattern, handler);
        public RouteHandlerBuilder MapPost(string pattern, Delegate handler) => Map("POST", pattern, handler);
        public RouteHandlerBuilder MapPut(string pattern, Delegate handler) => Map("PUT", pattern, handler);
        public RouteHandlerBuilder MapDelete(string pattern, Delegate handler) => Map("DELETE", pattern, handler);
        public RouteHandlerBuilder MapPatch(string pattern, Delegate handler) => Map("PATCH", pattern, handler);

        /** En una compu, abre el servidor y se queda esperando. Acá no hay red: se le habla con CreateClient(). */
        public void Run(string? url = null) => Console.WriteLine("(La ventanilla está abierta. En el navegador no hay red: probala con app.CreateClient().)");
        public Task RunAsync(string? url = null) { Run(url); return Task.CompletedTask; }

        /** Un HttpClient de verdad que le habla a esta ventanilla, sin red. */
        public HttpClient CreateClient() => new HttpClient(new Mostrador(this)) { BaseAddress = new Uri("http://ventanilla/") };

        private sealed class Mostrador(WebApplication app) : HttpMessageHandler
        {
            protected override Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken) => app.Atender(request);
        }

        private static bool Coincide(Ruta ruta, string[] segments, Dictionary<string, string> values)
        {
            if (ruta.Partes.Length != segments.Length) return false;
            for (int i = 0; i < segments.Length; i++)
            {
                var part = ruta.Partes[i];
                if (part.StartsWith('{') && part.EndsWith('}'))
                {
                    var inner = part[1..^1].Split(':');
                    var value = Uri.UnescapeDataString(segments[i]);
                    if (inner.Length > 1 && inner[1] == "int" && !int.TryParse(value, out _)) return false;
                    values[inner[0].TrimEnd('?')] = value;
                }
                else if (!part.Equals(segments[i], StringComparison.OrdinalIgnoreCase)) return false;
            }
            return true;
        }

        internal async Task<HttpResponseMessage> Atender(HttpRequestMessage request)
        {
            var uri = request.RequestUri!;
            var segments = uri.AbsolutePath.Trim('/').Split('/', StringSplitOptions.RemoveEmptyEntries);
            var query = uri.Query.TrimStart('?').Split('&', StringSplitOptions.RemoveEmptyEntries)
                .Select(p => p.Split('=', 2))
                .GroupBy(p => Uri.UnescapeDataString(p[0]), StringComparer.OrdinalIgnoreCase)
                .ToDictionary(g => g.Key, g => Uri.UnescapeDataString(g.First().Length > 1 ? g.First()[1].Replace('+', ' ') : ""), StringComparer.OrdinalIgnoreCase);

            bool pathExists = false;
            foreach (var ruta in rutas)
            {
                var values = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
                if (!Coincide(ruta, segments, values)) continue;
                pathExists = true;
                if (ruta.Metodo != request.Method.Method) continue;
                string? body = request.Content is null ? null : await request.Content.ReadAsStringAsync();
                try
                {
                    var args = Argumentos(ruta.Manejador.Method.GetParameters(), values, query, body);
                    if (args is null) return Armar(new Respuesta(400, new { error = "El cuerpo del pedido no es un JSON válido para esta ruta." }));
                    object? value = ruta.Manejador.DynamicInvoke(args);
                    if (value is Task task)
                    {
                        await task;
                        var type = task.GetType();
                        value = type.IsGenericType && type.GetProperty("Result") is { } result && result.PropertyType.Name != "VoidTaskResult" ? result.GetValue(task) : null;
                    }
                    return Armar(value as IResult ?? (value is string s ? new Respuesta(200, s, null, true) : new Respuesta(200, value)));
                }
                catch (Exception e)
                {
                    while (e is TargetInvocationException { InnerException: not null }) e = e.InnerException!;
                    return Armar(new Respuesta(500, $"Error en la ventanilla: {e.GetType().Name}: {e.Message}", null, true));
                }
            }
            return Armar(new Respuesta(pathExists ? 405 : 404, null));
        }

        private static object?[]? Argumentos(ParameterInfo[] parameters, Dictionary<string, string> route, Dictionary<string, string> query, string? body)
        {
            var args = new object?[parameters.Length];
            for (int i = 0; i < parameters.Length; i++)
            {
                var p = parameters[i];
                var type = Nullable.GetUnderlyingType(p.ParameterType) ?? p.ParameterType;
                bool simple = type.IsPrimitive || type.IsEnum || type == typeof(string) || type == typeof(decimal) || type == typeof(Guid) || type == typeof(DateTime);
                if (simple && (route.TryGetValue(p.Name!, out var text) || query.TryGetValue(p.Name!, out text)))
                    args[i] = type.IsEnum ? Enum.Parse(type, text, true) : type == typeof(Guid) ? Guid.Parse(text) : System.Convert.ChangeType(text, type, System.Globalization.CultureInfo.InvariantCulture);
                else if (!simple && !string.IsNullOrWhiteSpace(body))
                {
                    try { args[i] = JsonSerializer.Deserialize(body, p.ParameterType, Json); }
                    catch (JsonException) { return null; }
                }
                else args[i] = p.HasDefaultValue ? p.DefaultValue : p.ParameterType.IsValueType ? Activator.CreateInstance(p.ParameterType) : null;
            }
            return args;
        }

        private static HttpResponseMessage Armar(IResult result)
        {
            var response = new HttpResponseMessage((HttpStatusCode)result.StatusCode);
            if (result is Respuesta { Location: { } location }) response.Headers.Location = new Uri(location, UriKind.RelativeOrAbsolute);
            if (result.Value is not null)
            {
                response.Content = result is Respuesta { Texto: true }
                    ? new StringContent(result.Value.ToString() ?? "", Encoding.UTF8, "text/plain")
                    : new StringContent(JsonSerializer.Serialize(result.Value, result.Value.GetType(), Json), Encoding.UTF8, "application/json");
            }
            else response.Content = new StringContent("", Encoding.UTF8, "text/plain");
            return response;
        }
    }
}
