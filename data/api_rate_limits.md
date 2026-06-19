# API Rate Limits & Throttling Guide

## Overview
NexaCloud enforces rate limits to ensure fair usage and platform stability. This document explains rate limit policies, how to read rate limit headers, and strategies to avoid hitting limits.

---

## 1. Rate Limit Tiers

### By Plan

| Plan | Requests/Minute | Requests/Hour | Requests/Day | Burst Allowance |
|------|-----------------|---------------|--------------|-----------------|
| Starter | 60 | 1,000 | 10,000 | 100 req/10sec |
| Professional | 300 | 10,000 | 100,000 | 500 req/10sec |
| Business | 1,000 | 50,000 | 1,000,000 | 2,000 req/10sec |
| Enterprise | Custom | Custom | Custom | Negotiated |

### By Endpoint Category

| Endpoint Category | Rate Limit |
|-------------------|------------|
| `/v1/users` | 100 req/min |
| `/v1/data` | 200 req/min |
| `/v1/reports` | 20 req/min |
| `/v1/auth` | 30 req/min |
| `/v1/webhooks` | 50 req/min |
| `/v1/search` | 60 req/min |

---

## 2. Rate Limit Response Headers

Every API response includes rate limit information in the headers:

```
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 247
X-RateLimit-Reset: 1720000060
X-RateLimit-Window: 60
Retry-After: 15
```

| Header | Description |
|--------|-------------|
| `X-RateLimit-Limit` | Total requests allowed in the current window |
| `X-RateLimit-Remaining` | Requests remaining in current window |
| `X-RateLimit-Reset` | Unix timestamp when the window resets |
| `X-RateLimit-Window` | Window duration in seconds |
| `Retry-After` | Seconds to wait before retrying (only on 429 responses) |

---

## 3. HTTP 429 — Too Many Requests

When you exceed a rate limit, the API returns:

```json
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
Retry-After: 30

{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Retry after 30 seconds.",
    "limit": 60,
    "remaining": 0,
    "reset_at": "2024-10-15T14:32:00Z"
  }
}
```

---

## 4. Best Practices to Avoid Rate Limiting

### Implement Exponential Backoff
```python
import time
import random
import requests

def api_call_with_backoff(url, headers, max_retries=5):
    for attempt in range(max_retries):
        response = requests.get(url, headers=headers)
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 2 ** attempt))
            jitter = random.uniform(0, 1)
            time.sleep(retry_after + jitter)
        else:
            return response
    raise Exception("Max retries exceeded")
```

### Request Batching
Instead of individual requests per item, use batch endpoints:
```bash
# Inefficient: 100 individual calls
GET /v1/users/user_001
GET /v1/users/user_002
...

# Efficient: 1 batch call
POST /v1/users/batch
{"ids": ["user_001", "user_002", ..., "user_100"]}
```

### Caching Responses
Cache API responses locally for frequently accessed, rarely changing data:
- User profiles: Cache for 5 minutes
- Configuration data: Cache for 1 hour
- Static content: Cache for 24 hours

### Request Queuing
Implement a request queue with controlled throughput:
```python
import asyncio
import aiohttp

async def throttled_requests(urls, rate=50):
    """Send requests at a controlled rate of `rate` per second."""
    semaphore = asyncio.Semaphore(rate)
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_with_limit(session, url, semaphore) for url in urls]
        return await asyncio.gather(*tasks)
```

---

## 5. Monitoring Rate Limit Usage

View your API usage in real-time:
1. Go to **Developer Dashboard → API Usage**
2. Select a time range (hourly, daily, monthly)
3. Identify endpoints approaching limits

**Alerts:** Configure rate limit alerts in **Settings → Notifications → API Alerts** to receive warnings when usage reaches 80% of your limit.

---

## 6. Increasing Rate Limits

- **Starter/Professional:** Upgrade to a higher plan
- **Business:** Contact your account manager for custom limits
- **Enterprise:** Rate limits are negotiated during contract
- **Temporary Burst:** Available upon request for planned high-traffic events (minimum 48 hours notice)

---

## 7. IP-Based Rate Limiting

In addition to API key limits, NexaCloud applies IP-based limits:
- Max **1,000 requests/minute per IP** regardless of plan
- IPs triggering rate limits repeatedly may be temporarily blocked
- Contact security@nexacloud.io if your IP is incorrectly blocked

---

## Contact
- **API Support:** api-support@nexacloud.io
- **Developer Forum:** https://community.nexacloud.io/api
- **Rate Limit Increase Requests:** https://support.nexacloud.io/rate-limit
