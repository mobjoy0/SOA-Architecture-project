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
            var httpReq = OperationContext.Current.IncomingMessageProperties
                [HttpRequestMessageProperty.Name] as HttpRequestMessageProperty;

            string authHeader = httpReq?.Headers["Authorization"];
            var userId = _jwtService.ExtractUserId(authHeader);

            if (userId == -1)
                return "Unauthorized: no JWT provided";
            
            
            if (_databaseService.GetPaymentStatus(userId))
            {
                return "Failed: Payment is already done";
            }
           
            var authResult = CallAuthPayEndpoint(authHeader).Result;

            if (authResult)
            {
                // Add payment to database with Paid = true
                var paymentId = _databaseService.AddPayment(userId);
                return $"Payment successful! Payment ID: {paymentId}, User ID: {userId}";
            }
            else
            {
                return "Payment failed at auth service:";
            }
        }
        catch (Exception ex)
        {
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
            
            // Forward Authorization header to auth service
            if (!string.IsNullOrEmpty(authHeader))
            {
                if (authHeader.StartsWith("Bearer "))
                    request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", authHeader.Substring("Bearer ".Length));
                else
                    request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", authHeader);
            }

            // Add billing service API key for verification
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