# API Authentication Guide

## Overview
This guide covers all authentication methods supported by NexaCloud SaaS platform. Proper authentication ensures secure access to all API endpoints.

---

## 1. API Key Authentication

### Generating an API Key
1. Navigate to **Settings → Developer → API Keys**
2. Click **"Generate New Key"**
3. Label your key with a descriptive name (e.g., `production-backend`)
4. Select the required permission scopes
5. Click **"Create Key"** and copy it immediately — it will not be shown again

### Using Your API Key
Include your API key in the request header:
```
Authorization: Bearer YOUR_API_KEY
```

**Example cURL request:**
```bash
curl -H "Authorization: Bearer nxa_live_abc123..." \
     https://api.nexacloud.io/v1/users
```

---

## 2. OAuth 2.0 Authentication

NexaCloud supports OAuth 2.0 for third-party integrations.

### Authorization Code Flow
1. Redirect user to: `https://auth.nexacloud.io/oauth/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=YOUR_REDIRECT_URI&scope=read:users`
2. User logs in and approves permissions
3. Receive authorization code at your redirect URI
4. Exchange code for access token:

```bash
POST https://auth.nexacloud.io/oauth/token
Content-Type: application/json

{
  "grant_type": "authorization_code",
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET",
  "code": "RECEIVED_CODE",
  "redirect_uri": "YOUR_REDIRECT_URI"
}
```

### Token Refresh
Access tokens expire after **3600 seconds (1 hour)**. Use the refresh token to obtain a new one:
```bash
POST https://auth.nexacloud.io/oauth/token
{
  "grant_type": "refresh_token",
  "refresh_token": "YOUR_REFRESH_TOKEN",
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET"
}
```

---

## 3. Common Authentication Errors

### Error 401 — Unauthorized
**Cause:** Missing or invalid API key / token.
**Resolution:**
- Verify the `Authorization` header is present and correctly formatted
- Check that the API key has not expired or been revoked
- Ensure no trailing whitespace in the key

### Error 403 — Forbidden
**Cause:** Valid credentials but insufficient permissions.
**Resolution:**
- Review the scopes assigned to the API key
- Contact your organization admin to update permissions
- Check if the resource requires a higher subscription tier

### Error 429 — Rate Limited
**Cause:** Too many requests in a short period.
**Resolution:**
- Implement exponential backoff in your application
- Review rate limit headers: `X-RateLimit-Remaining` and `X-RateLimit-Reset`
- Consider upgrading your plan for higher limits

---

## 4. JWT Token Validation

All JWT tokens issued by NexaCloud use **RS256** signing algorithm.
- Token issuer: `https://auth.nexacloud.io`
- Token audience: `https://api.nexacloud.io`
- Public keys: `https://auth.nexacloud.io/.well-known/jwks.json`

**Validate tokens using:**
```python
import jwt
from jwt import PyJWKClient

jwks_client = PyJWKClient("https://auth.nexacloud.io/.well-known/jwks.json")
signing_key = jwks_client.get_signing_key_from_jwt(token)
payload = jwt.decode(token, signing_key.key, algorithms=["RS256"])
```

---

## 5. Security Best Practices
- **Never** commit API keys to version control
- Use environment variables or secrets managers
- Rotate API keys every 90 days
- Use the minimum required permission scopes
- Enable IP whitelisting for production keys in **Settings → Security**
- Monitor API key usage in the **Developer Dashboard**

---

## Support
If you encounter authentication issues not covered here, contact:
- **Email:** api-support@nexacloud.io
- **Developer Forum:** https://community.nexacloud.io
- **Status Page:** https://status.nexacloud.io
