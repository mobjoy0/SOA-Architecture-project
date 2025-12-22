using billing_service.contracts;
using CoreWCF;
using System.Net.Http;
using System.Net.Http.Headers;
using CoreWCF.Channels;

namespace billing_service.services;

public class BillingService : IBillingService
{
    private readonly JwtService _jwtService;
    private readonly HttpClient _httpClient;
    private readonly DatabaseService _databaseService;
    private const string AUTH_SERVICE_URL = "http://localhost:5048";
    private const string BILLING_API_KEY = "pay";

    public BillingService()
    {
        _jwtService = new JwtService();
        _httpClient = new HttpClient();
        _databaseService = new DatabaseService();
    }

    public string PayInvoice()
    {
        try
        {
            Console.WriteLine("PayInvoice called");

            var httpReq = OperationContext.Current.IncomingMessageProperties
                [HttpRequestMessageProperty.Name] as HttpRequestMessageProperty;

            string authHeader = httpReq?.Headers["Authorization"];
            Console.WriteLine($"Authorization header: {authHeader}");

            var userId = _jwtService.ExtractUserId(authHeader);
            Console.WriteLine($"Extracted User ID: {userId}");

            if (userId == -1)
            {
                Console.WriteLine("Unauthorized: no valid JWT");
                return "Unauthorized: no JWT provided";
            }

            bool paymentDone = _databaseService.GetPaymentStatus(userId);
            Console.WriteLine($"Payment status for user {userId}: {paymentDone}");

            if (paymentDone)
            {
                Console.WriteLine("Payment is already done");
                return "Failed: Payment is already done";
            }

            Console.WriteLine("Calling Auth service Pay endpoint...");
            var authResult = CallAuthPayEndpoint(authHeader).Result;
            Console.WriteLine($"Auth service result: {authResult}");

            if (authResult)
            {
                var paymentId = _databaseService.AddPayment(userId);
                Console.WriteLine($"Payment added to database. Payment ID: {paymentId}");
                return $"Payment successful! Payment ID: {paymentId}, User ID: {userId}";
            }
            else
            {
                Console.WriteLine("Payment failed at auth service");
                return "Payment failed at auth service:";
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Exception in PayInvoice: {ex.Message}");
            return $"Error processing payment: {ex.Message}";
        }
    }


    public string GetAllPayments()
    {
        try
        {
            var payments = _databaseService.GetAllPayments();
            
            if (payments.Count == 0)
                return "No payments found";

            var result = "All Payments:\n";
            foreach (var payment in payments)
            {
                result += $"ID: {payment.Id}, UserID: {payment.UserId}, Paid: {payment.Paid}, Date: {payment.CreatedAt}\n";
            }

            return result;
        }
        catch (Exception ex)
        {
            return $"Error retrieving payments: {ex.Message}";
        }
    }

    private async Task<bool> CallAuthPayEndpoint(string authHeader)
    {
        try
        {
            var request = new HttpRequestMessage(HttpMethod.Put, $"{AUTH_SERVICE_URL}/auth/pay");
            
            if (!string.IsNullOrEmpty(authHeader))
            {
                if (authHeader.StartsWith("Bearer "))
                    request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", authHeader.Substring("Bearer ".Length));
                else
                    request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", authHeader);
            }

            request.Headers.Add("X-Billing-Service-Key", BILLING_API_KEY);

            var response = await _httpClient.SendAsync(request);
            return response.IsSuccessStatusCode;
        }
        catch
        {
            return false;
        }
    }
}