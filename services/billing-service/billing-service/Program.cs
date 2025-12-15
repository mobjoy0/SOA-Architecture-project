using billing_service.contracts;
using billing_service.services;
using CoreWCF;
using CoreWCF.Configuration;
using CoreWCF.Description;
using CoreWCF.Channels;

var builder = WebApplication.CreateBuilder(args);

// Add logging
builder.Logging.ClearProviders();
builder.Logging.AddConsole();
builder.Logging.SetMinimumLevel(LogLevel.Debug);

// Add configuration
builder.Configuration.AddJsonFile("appsettings.json", optional: false, reloadOnChange: true);

// Register CoreWCF services
builder.Services.AddServiceModelServices();
builder.Services.AddServiceModelMetadata();

// Register services in DI
builder.Services.AddSingleton<JwtService>();
builder.Services.AddHttpClient(); 

var app = builder.Build();

// Add request logging middleware
app.Use(async (context, next) =>
{
    Console.WriteLine($"Request: {context.Request.Method} {context.Request.Path}");
    Console.WriteLine($"Content-Type: {context.Request.ContentType}");
    await next();
});

// Configure SOAP endpoint with plain HTTP
app.UseServiceModel(serviceBuilder =>
{
    serviceBuilder.AddService<BillingService>(options =>
    {
        options.DebugBehavior.IncludeExceptionDetailInFaults = true;
    });
    
    // Use BasicHttpBinding with no security (plain HTTP)
    serviceBuilder.AddServiceEndpoint<BillingService, IBillingService>(
        new BasicHttpBinding(BasicHttpSecurityMode.None),
        "/BillingService.svc"
    );

    // Enable WSDL metadata
    var serviceMetadataBehavior = app.Services.GetRequiredService<ServiceMetadataBehavior>();
    serviceMetadataBehavior.HttpGetEnabled = true;
});

app.Run();