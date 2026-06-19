# Troubleshooting Common Errors

## Overview
This guide covers the most frequently encountered errors on the NexaCloud platform and their step-by-step resolutions.

---

## 1. Authentication & Access Errors

### Error 401 — Unauthorized
**Symptom:** API returns `{"error": "Unauthorized"}` on every request.

**Causes & Fixes:**
1. **Missing Authorization header** → Add `Authorization: Bearer YOUR_API_KEY` to all requests
2. **Expired token** → Refresh your access token using the refresh endpoint
3. **Revoked API key** → Generate a new key in **Settings → Developer → API Keys**
4. **Wrong environment key** → Ensure you're using a Live key for production, Test key for staging

### Error 403 — Forbidden
**Symptom:** Valid credentials but access denied.

**Fixes:**
1. Check the key's permission scopes — ensure `write:data` or `admin` scope is enabled
2. Your plan may not include this feature — check plan limits at **Settings → Subscription**
3. IP whitelist may be blocking your request — check **Settings → Security → IP Whitelist**

---

## 2. Connection & Network Errors

### ECONNREFUSED / Connection Timeout
**Symptom:** Cannot connect to `api.nexacloud.io`.

**Checklist:**
- [ ] Check **https://status.nexacloud.io** for active incidents
- [ ] Verify your DNS resolves `api.nexacloud.io` correctly: `nslookup api.nexacloud.io`
- [ ] Ensure port 443 (HTTPS) is not blocked by firewall
- [ ] Try from a different network to rule out local connectivity issues
- [ ] Disable VPN temporarily — some VPN configurations cause routing issues

### SSL/TLS Certificate Errors
**Symptom:** `SSL_CERTIFICATE_VERIFY_FAILED` or similar.

**Fixes:**
1. Ensure system time is synchronized (certificate validation requires accurate time)
2. Update your SSL certificate store: `pip install --upgrade certifi`
3. For corporate environments, install your organization's root CA certificate

---

## 3. Database & Data Errors

### Error: "Resource Not Found" (404)
**Symptom:** Querying for a record that should exist returns 404.

**Causes:**
- Record was deleted (check audit log in **Admin → Audit Log**)
- Wrong organization context (check `X-Organization-ID` header)
- Accessing a resource in a different region — ensure API endpoint matches your data region

### Data Sync Issues
**Symptom:** Data changes not reflected immediately across integrations.

**Fix:**
- Webhooks have a **~2 second propagation delay** in normal conditions
- During high load, delay may increase to **30 seconds**
- Force a manual sync via: `POST /v1/sync/trigger`
- Check webhook delivery status in **Settings → Webhooks → Delivery Log**

---

## 4. Performance Issues

### Slow API Response Times
**Benchmark:** API responses should be under 200ms for 95% of requests.

**If experiencing slow responses:**
1. Check if you're hitting rate limits — see `X-RateLimit-Remaining` header
2. Large payload requests (>1MB) are throttled — paginate or compress data
3. `/v1/reports` endpoints process asynchronously — use the job ID to poll for completion
4. Enable response compression by setting `Accept-Encoding: gzip` header

### High Memory Usage (SDK)
**Symptom:** NexaCloud Python SDK consuming excessive memory.

**Fix:**
```python
# Use streaming for large data exports instead of loading all at once
with nexacloud.data.stream(query={"limit": 10000}) as stream:
    for batch in stream.iter_batches(batch_size=100):
        process(batch)
```

---

## 5. Webhook Delivery Failures

### Webhook Not Receiving Events
**Troubleshooting Steps:**
1. Verify webhook URL is publicly accessible (not localhost)
2. Check webhook signature validation: `X-NexaCloud-Signature` header must match HMAC-SHA256
3. Your endpoint must return HTTP 200 within **5 seconds** — NexaCloud retries on non-200 responses
4. View delivery attempts in **Settings → Webhooks → [Webhook Name] → Delivery Log**

### Retry Policy
- **Attempt 1:** Immediately
- **Attempt 2:** 5 minutes later
- **Attempt 3:** 30 minutes later
- **Attempt 4:** 2 hours later
- **Attempt 5:** 24 hours later
- After 5 failures, webhook is **disabled** and admin is notified

---

## 6. File Upload Errors

### Error: "File Too Large"
- Maximum file size: **50MB** (Starter/Professional), **500MB** (Business), **5GB** (Enterprise)
- For files over 50MB, use multipart upload: `POST /v1/files/multipart-upload`

### Unsupported File Type
Supported file types: PDF, DOCX, XLSX, CSV, PNG, JPG, SVG, ZIP
If you need support for another format, submit a request at **https://feedback.nexacloud.io**

---

## 7. Getting More Help

If these steps don't resolve your issue:
1. Collect your **Request ID** from the `X-Request-ID` response header
2. Note the **timestamp** and **error message** exactly
3. Contact support with these details for faster resolution

**Support Channels:**
- **Live Chat:** Available on support portal (Business/Enterprise plans)
- **Email:** support@nexacloud.io
- **Community:** https://community.nexacloud.io
