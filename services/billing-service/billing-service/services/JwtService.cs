using System.IdentityModel.Tokens.Jwt;

namespace billing_service.services;

public class JwtService
{
    public int ExtractUserId(string jwtToken)
    {
        if (string.IsNullOrEmpty(jwtToken))
            return -1;

        if (jwtToken.StartsWith("Bearer "))
            jwtToken = jwtToken.Substring("Bearer ".Length);

        var handler = new JwtSecurityTokenHandler();
        var jwt = handler.ReadJwtToken(jwtToken);

        var userIdClaim = jwt.Claims.FirstOrDefault(c => c.Type == "id");
    
        if (userIdClaim == null)
            return -1;
        
        if (int.TryParse(userIdClaim.Value, out int userId))
            return userId;

        return -1; 
    }
}