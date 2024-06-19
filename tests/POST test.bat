# Ignore SSL Certificate Errors
Add-Type @"
using System.Net;
using System.Security.Cryptography.X509Certificates;
public class TrustAllCertsPolicy : ICertificatePolicy {
    public bool CheckValidationResult(
        ServicePoint srvPoint, X509Certificate certificate,
        WebRequest request, int certificateProblem) {
        return true;
    }
}
"@
[System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAllCertsPolicy

# Send the HTTP Request
$DebugPreference = "Continue"
Invoke-RestMethod -Uri https://admissionsrocket.xyz:3443/webhook -Method Post -Body '{}' -ContentType 'application/json' -Debug
