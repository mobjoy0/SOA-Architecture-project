using CoreWCF;

namespace billing_service.contracts;

[ServiceContract (Namespace = "http://billing.com/")]
public interface IBillingService
{
    [OperationContract]
    string PayInvoice();
    
    [OperationContract]
    string GetAllPayments();
}