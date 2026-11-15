// El Puerto de Elefa (D119, Senda del Puerto S03): la API del Puerto, que en la historia está escrita en PHP, corre acá
// como una copia de mentira, sin red. Puerto.CreateClient() da un HttpClient de verdad (BaseAddress http://puerto/)
// cuyos pedidos los atiende esta copia, como app.CreateClient() con la ventanilla. Cada cliente tiene su propio Puerto,
// que arranca siempre igual. Mismo mundo que el Puerto de JavaScript (js-sandbox/world.js): mensajes, demoras y errores.
#nullable enable
using System.Net.Http;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

public static class Puerto
{
    /** Un HttpClient que le habla al Puerto de Elefa sin salir del navegador. */
    public static HttpClient CreateClient()
    {
        var app = WebApplication.Create();
        var mensajes = new List<MensajeDelPuerto>
        {
            new(1, "Elefa", "Bienvenida al Puerto, Ceci."),
            new(2, "Nilo", "Llegó un barco con cuerdas para el Conservatorio."),
        };
        var barcos = new[]
        {
            new BarcoDelPuerto(1, "La Gaviota", "violines"),
            new BarcoDelPuerto(2, "El Ancla Azul", "cuerdas"),
            new BarcoDelPuerto(3, "La Marea", "sal"),
            new BarcoDelPuerto(4, "El Faro Viejo", "partituras"),
        };
        int tormenta = 0;

        app.MapGet("/hola", () => Results.Ok(new { mensaje = "¡Hola, Ceci! Te escribe Elefa desde el Puerto.", de = "Elefa" }));
        app.MapGet("/barcos", () => Results.Ok(barcos));
        app.MapGet("/barcos/{id:int}", (int id) => barcos.FirstOrDefault(b => b.Id == id) is { } barco
            ? Results.Ok(barco)
            : Results.NotFound(new { error = $"No hay ningún barco con el número {id}." }));
        app.MapGet("/mensajes", () => Results.Ok(mensajes));
        app.MapGet("/mensajes/{id:int}", (int id) => mensajes.FirstOrDefault(m => m.Id == id) is { } mensaje
            ? Results.Ok(mensaje)
            : Results.NotFound(new { error = $"No hay ningún mensaje con el número {id}." }));
        app.MapPost("/mensajes", (MensajeNuevo? nuevo) =>
        {
            if (string.IsNullOrWhiteSpace(nuevo?.Texto)) return Results.UnprocessableEntity(new { error = "Falta el texto del mensaje." });
            var mensaje = new MensajeDelPuerto(mensajes.Count == 0 ? 1 : mensajes.Max(m => m.Id) + 1, nuevo.De ?? "Ceci", nuevo.Texto);
            mensajes.Add(mensaje);
            return Results.Created($"/mensajes/{mensaje.Id}", mensaje);
        });
        // Las cargas que Pico revolvió: una sin nombre y otra con cantidad negativa (para no confiar en lo que llega).
        app.MapGet("/cargas", () => Results.Ok(new object[]
        {
            new { nombre = "violines", cantidad = 4 },
            new { nombre = (string?)null, cantidad = 2 },
            new { nombre = "cuerdas", cantidad = -3 },
            new { nombre = "resina", cantidad = 6 },
        }));
        app.MapGet("/lento", async () =>
        {
            await Task.Delay(3000);
            return Results.Ok(new { mensaje = "Perdón la demora: la marea estaba alta." });
        });
        app.MapGet("/tormenta", () => ++tormenta < 3
            ? Results.Json(new { error = "El Puerto está cerrado por tormenta." }, 503)
            : Results.Ok(new { mensaje = "Pasó la tormenta: salen los barcos." }));
        app.MapGet("/error", () => Results.Json(new { error = "Se cayó una grúa en el muelle. Probá más tarde." }, 500));
        app.MapGet("/roto", () => Results.Text("{\"mensaje\": \"esto se cortó a la mit", "application/json"));
        app.MapPost("/eco", (object? recibido) => Results.Ok(new { recibido }));

        return new HttpClient(new Muelle(app)) { BaseAddress = new Uri("http://puerto/") };
    }

    /** Atiende cada pedido con la copia del Puerto, y respeta el Timeout del cliente y los CancellationToken. */
    private sealed class Muelle(WebApplication app) : HttpMessageHandler
    {
        protected override async Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
        {
            var atender = app.Atender(request);
            if (cancellationToken.CanBeCanceled && await Task.WhenAny(atender, Task.Delay(Timeout.Infinite, cancellationToken)) != atender)
            {
                cancellationToken.ThrowIfCancellationRequested();
            }
            return await atender;
        }
    }
}

internal sealed record BarcoDelPuerto(int Id, string Nombre, string Carga);
internal sealed record MensajeDelPuerto(int Id, string De, string Texto);
internal sealed record MensajeNuevo(string? De, string? Texto);
