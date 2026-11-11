// La Bóveda (D119, Acto V): una Microsoft.Data.Sqlite de mentira, con la misma forma que la de verdad (SqliteConnection,
// CreateCommand, Parameters.AddWithValue, ExecuteReader…), que por dentro le pasa el SQL al SQLite en WebAssembly del
// navegador (sql.js, el de las micro-misiones de SQL). Cada ejecución empieza con una base vacía en memoria; no hay
// disco ni red. Se compila junto al código del alumno.
#nullable enable
using System.Collections;
using System.Text.Json;

namespace Microsoft.Data.Sqlite
{
    public class SqliteException : Exception
    {
        public int SqliteErrorCode { get; }
        public SqliteException(string message, int code) : base(message) => SqliteErrorCode = code;
    }

    /** El puente con el SQLite del navegador: lo deja puesto el ejecutor. */
    internal static class Puente
    {
        public static List<Resultado> Ejecutar(string sql, IEnumerable<SqliteParameter> parameters)
        {
            if (AppDomain.CurrentDomain.GetData("Conservatorio.Sql") is not Func<string, string> bridge)
                throw new InvalidOperationException("La Bóveda no está disponible acá.");
            var values = new Dictionary<string, object?>();
            foreach (var p in parameters)
            {
                object? v = p.Value is DBNull ? null : p.Value switch
                {
                    bool b => b ? 1 : 0,
                    DateTime d => d.ToString("yyyy-MM-dd HH:mm:ss"),
                    decimal m => (double)m,
                    Enum e => System.Convert.ToInt64(e),
                    _ => p.Value,
                };
                var name = p.ParameterName;
                if (name.Length > 0 && "$@:".Contains(name[0])) values[name] = v;
                else foreach (var prefix in "$@:") values[prefix + name] = v;
            }
            var answer = JsonDocument.Parse(bridge(JsonSerializer.Serialize(new { sql, values })));
            var root = answer.RootElement;
            if (root.TryGetProperty("error", out var error) && error.ValueKind == JsonValueKind.String)
            {
                var message = error.GetString() ?? "";
                int code = message.Contains("constraint failed") ? 19 : 1;
                throw new SqliteException($"SQLite Error {code}: '{message}'.", code);
            }
            var results = new List<Resultado>();
            foreach (var r in root.GetProperty("results").EnumerateArray())
            {
                var columns = r.GetProperty("columns").EnumerateArray().Select(c => c.GetString() ?? "").ToList();
                var rows = r.GetProperty("rows").EnumerateArray().Select(row => row.EnumerateArray().Select(Valor).ToArray()).ToList();
                results.Add(new Resultado(columns, rows, r.GetProperty("changes").GetInt32()));
            }
            return results;
        }

        private static object Valor(JsonElement e) => e.ValueKind switch
        {
            JsonValueKind.Null => DBNull.Value,
            JsonValueKind.String => e.GetString()!,
            JsonValueKind.Number => e.TryGetInt64(out long l) ? (object)l : e.GetDouble(),
            _ => e.ToString(),
        };
    }

    internal record Resultado(List<string> Columns, List<object[]> Rows, int Changes);

    public class SqliteConnection : IDisposable
    {
        public string ConnectionString { get; set; }
        public string DataSource => ConnectionString.Split(';').Select(p => p.Split('=', 2)).Where(p => p.Length == 2 && p[0].Trim().Equals("Data Source", StringComparison.OrdinalIgnoreCase)).Select(p => p[1].Trim()).FirstOrDefault() ?? "";
        private bool Abierta { get; set; }
        public System.Data.ConnectionState State => Abierta ? System.Data.ConnectionState.Open : System.Data.ConnectionState.Closed;

        public SqliteConnection() : this("") { }
        public SqliteConnection(string connectionString) => ConnectionString = connectionString;

        public void Open() => Abierta = true;
        public Task OpenAsync() { Open(); return Task.CompletedTask; }
        public void Close() => Abierta = false;
        public void Dispose() => Close();

        public SqliteCommand CreateCommand() => new SqliteCommand { Connection = this };

        public SqliteTransaction BeginTransaction()
        {
            Verificar("BeginTransaction");
            Puente.Ejecutar("BEGIN", Array.Empty<SqliteParameter>());
            return new SqliteTransaction(this);
        }

        internal void Verificar(string what)
        {
            if (!Abierta) throw new InvalidOperationException($"{what} can only be called when the connection is open.");
        }
    }

    public class SqliteTransaction : IDisposable
    {
        private bool done;
        public SqliteConnection Connection { get; }
        internal SqliteTransaction(SqliteConnection connection) => Connection = connection;

        public void Commit() { Terminar("COMMIT"); }
        public void Rollback() { Terminar("ROLLBACK"); }
        public void Dispose() { if (!done) Terminar("ROLLBACK"); }

        private void Terminar(string sql)
        {
            if (done) throw new InvalidOperationException("This SqliteTransaction has completed; it is no longer usable.");
            done = true;
            Puente.Ejecutar(sql, Array.Empty<SqliteParameter>());
        }
    }

    public class SqliteParameter
    {
        public string ParameterName { get; set; } = "";
        public object? Value { get; set; }
        public SqliteParameter() { }
        public SqliteParameter(string name, object? value) { ParameterName = name; Value = value; }
    }

    public class SqliteParameterCollection : IEnumerable<SqliteParameter>
    {
        private readonly List<SqliteParameter> items = new();
        public int Count => items.Count;
        public SqliteParameter this[int index] => items[index];
        public SqliteParameter this[string name] => items.First(p => p.ParameterName == name);

        public SqliteParameter AddWithValue(string parameterName, object? value)
        {
            var p = new SqliteParameter(parameterName, value);
            items.Add(p);
            return p;
        }

        public SqliteParameter Add(SqliteParameter parameter) { items.Add(parameter); return parameter; }
        public void Clear() => items.Clear();
        public IEnumerator<SqliteParameter> GetEnumerator() => items.GetEnumerator();
        IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
    }

    public class SqliteCommand : IDisposable
    {
        public SqliteConnection? Connection { get; set; }
        public SqliteTransaction? Transaction { get; set; }
        public string CommandText { get; set; } = "";
        public SqliteParameterCollection Parameters { get; } = new();

        public SqliteCommand() { }
        public SqliteCommand(string commandText, SqliteConnection connection) { CommandText = commandText; Connection = connection; }

        private List<Resultado> Ejecutar(string what)
        {
            if (Connection is null) throw new InvalidOperationException($"{what} can only be called when the command has a connection.");
            Connection.Verificar(what);
            if (string.IsNullOrWhiteSpace(CommandText)) throw new InvalidOperationException($"{what} can only be called when CommandText has been set.");
            return Puente.Ejecutar(CommandText, Parameters);
        }

        public int ExecuteNonQuery() => Ejecutar("ExecuteNonQuery").Sum(r => r.Changes);

        public object? ExecuteScalar()
        {
            var first = Ejecutar("ExecuteScalar").FirstOrDefault(r => r.Columns.Count > 0);
            return first is null || first.Rows.Count == 0 ? null : first.Rows[0][0];
        }

        public SqliteDataReader ExecuteReader() => new SqliteDataReader(Ejecutar("ExecuteReader").Where(r => r.Columns.Count > 0).ToList());

        public Task<int> ExecuteNonQueryAsync() => Task.FromResult(ExecuteNonQuery());
        public Task<object?> ExecuteScalarAsync() => Task.FromResult(ExecuteScalar());
        public Task<SqliteDataReader> ExecuteReaderAsync() => Task.FromResult(ExecuteReader());

        public void Dispose() { }
    }

    public class SqliteDataReader : IDisposable
    {
        private readonly List<Resultado> results;
        private int set;
        private int row = -1;

        internal SqliteDataReader(List<Resultado> results) => this.results = results;

        private Resultado Actual => set < results.Count ? results[set] : new Resultado(new(), new(), 0);
        private object[] Fila => row >= 0 && row < Actual.Rows.Count
            ? Actual.Rows[row]
            : throw new InvalidOperationException("No data exists for the row/column.");

        public bool HasRows => Actual.Rows.Count > 0;
        public int FieldCount => Actual.Columns.Count;

        public bool Read() => ++row < Actual.Rows.Count;
        public Task<bool> ReadAsync() => Task.FromResult(Read());

        public bool NextResult()
        {
            row = -1;
            return ++set < results.Count;
        }

        public string GetName(int ordinal) => Actual.Columns[ordinal];

        public int GetOrdinal(string name)
        {
            int i = Actual.Columns.FindIndex(c => c.Equals(name, StringComparison.OrdinalIgnoreCase));
            return i >= 0 ? i : throw new ArgumentOutOfRangeException(nameof(name), name, $"No hay ninguna columna «{name}».");
        }

        public object GetValue(int ordinal) => Fila[ordinal];
        public object this[int ordinal] => GetValue(ordinal);
        public object this[string name] => GetValue(GetOrdinal(name));
        public bool IsDBNull(int ordinal) => Fila[ordinal] is DBNull;

        private object NoNulo(int ordinal) => Fila[ordinal] is DBNull
            ? throw new InvalidCastException($"La columna «{GetName(ordinal)}» es NULL: preguntá antes con IsDBNull.")
            : Fila[ordinal];

        public string GetString(int ordinal) => System.Convert.ToString(NoNulo(ordinal), System.Globalization.CultureInfo.InvariantCulture)!;
        public int GetInt32(int ordinal) => System.Convert.ToInt32(NoNulo(ordinal));
        public long GetInt64(int ordinal) => System.Convert.ToInt64(NoNulo(ordinal));
        public double GetDouble(int ordinal) => System.Convert.ToDouble(NoNulo(ordinal));
        public decimal GetDecimal(int ordinal) => System.Convert.ToDecimal(NoNulo(ordinal));
        public bool GetBoolean(int ordinal) => System.Convert.ToInt64(NoNulo(ordinal)) != 0;
        public T GetFieldValue<T>(int ordinal) => (T)System.Convert.ChangeType(NoNulo(ordinal), Nullable.GetUnderlyingType(typeof(T)) ?? typeof(T));

        public void Close() { }
        public void Dispose() { }
    }
}
