using Microsoft.Data.Sqlite;

namespace billing_service.services;

public class DatabaseService
{
    private readonly string _connectionString = "Data Source=billing.db";

    public DatabaseService()
    {
        InitializeDatabase();
    }

    private void InitializeDatabase()
    {
        using var connection = new SqliteConnection(_connectionString);
        connection.Open();

        var command = connection.CreateCommand();
        command.CommandText = @"
            CREATE TABLE IF NOT EXISTS Payments (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                UserId TEXT NOT NULL,
                Paid INTEGER NOT NULL DEFAULT 1,
                CreatedAt TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )";
        command.ExecuteNonQuery();
    }

    public int AddPayment(int userId)
    {
        using var connection = new SqliteConnection(_connectionString);
        connection.Open();

        var command = connection.CreateCommand();
        command.CommandText = @"
            INSERT INTO Payments (UserId, Paid, CreatedAt)
            VALUES (@userId, 1, @createdAt);
            SELECT last_insert_rowid();";
        
        command.Parameters.AddWithValue("@userId", userId);
        command.Parameters.AddWithValue("@createdAt", DateTime.UtcNow.ToString("o"));

        var paymentId = Convert.ToInt32(command.ExecuteScalar());
        return paymentId;
    }

    public bool GetPaymentStatus(int id)
    {
        using var connection = new SqliteConnection(_connectionString);
        connection.Open();

        var command = connection.CreateCommand();
        command.CommandText = "SELECT Paid FROM Payments WHERE Id = @id";
        command.Parameters.AddWithValue("@id", id);

        var result = command.ExecuteScalar();
        return result != null && Convert.ToInt32(result) == 1;
    }

    public List<(int Id, string UserId, bool Paid, string CreatedAt)> GetAllPayments()
    {
        var payments = new List<(int, string, bool, string)>();
        
        using var connection = new SqliteConnection(_connectionString);
        connection.Open();

        var command = connection.CreateCommand();
        command.CommandText = "SELECT Id, UserId, Paid, CreatedAt FROM Payments ORDER BY CreatedAt DESC";

        using var reader = command.ExecuteReader();
        while (reader.Read())
        {
            payments.Add((
                reader.GetInt32(0),
                reader.GetString(1),
                reader.GetInt32(2) == 1,
                reader.GetString(3)
            ));
        }

        return payments;
    }
}