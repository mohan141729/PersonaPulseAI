# Performance Optimization Guide

## Overview
This guide provides strategies and best practices for maximizing the performance of your NexaCloud integration and application built on the NexaCloud platform.

---

## 1. API Performance Best Practices

### Use Field Selection (Sparse Fieldsets)
Only request the fields you need to reduce payload size and processing time:

```bash
# Bad — returns all fields
GET /v1/users/usr_123

# Good — returns only name and email
GET /v1/users/usr_123?fields=id,name,email
```

**Impact:** Reduces response payload by 60–80% for large objects.

### Pagination for Large Datasets
Never request unbounded data sets. Always paginate:

```bash
# Get first 100 users
GET /v1/users?limit=100&page=1

# Get next 100
GET /v1/users?limit=100&page=2
```

**Cursor-based pagination** (recommended for large datasets):
```bash
GET /v1/events?limit=100&after=evt_abc123
```

### Enable GZIP Compression
Add `Accept-Encoding: gzip` header to compress response bodies by 70–90%:

```python
import requests

response = requests.get(
    "https://api.nexacloud.io/v1/data",
    headers={
        "Authorization": "Bearer YOUR_API_KEY",
        "Accept-Encoding": "gzip"
    }
)
```

---

## 2. Caching Strategies

### Client-Side Caching with ETags
NexaCloud returns `ETag` and `Last-Modified` headers for cacheable resources:

```python
import requests

cache = {}

def get_with_cache(url, api_key):
    headers = {"Authorization": f"Bearer {api_key}"}
    if url in cache:
        headers["If-None-Match"] = cache[url]["etag"]
    
    response = requests.get(url, headers=headers)
    if response.status_code == 304:
        return cache[url]["data"]  # Not modified, use cached
    
    cache[url] = {"etag": response.headers.get("ETag"), "data": response.json()}
    return response.json()
```

### Recommended Cache TTLs

| Resource Type | Recommended TTL |
|---------------|-----------------|
| User profiles | 5 minutes |
| Ticket details | 1 minute |
| Analytics reports | 15 minutes |
| Configuration/settings | 1 hour |
| Product catalog | 24 hours |

---

## 3. Database Query Optimization

### Use Filters to Reduce Result Sets
```bash
# Unoptimized — fetches all tickets then filters client-side
GET /v1/tickets

# Optimized — server-side filtering
GET /v1/tickets?status=open&priority=P1&created_after=2024-01-01
```

### Indexed Filter Fields
These fields have database indexes for fast filtering:
- `status`, `priority`, `created_at`, `updated_at`
- `user_id`, `organization_id`, `assignee_id`
- `tags` (array field, uses GIN index)

### Avoid N+1 Query Patterns
```python
# Bad — N+1 queries
tickets = get_tickets()
for ticket in tickets:
    user = get_user(ticket.user_id)  # 1 query per ticket

# Good — use include parameter to eager load related data
tickets = get_tickets(include=["user", "assignee"])  # 1 query total
```

Use `?include=user,organization,comments` to eager-load related resources.

---

## 4. Webhook Performance

### Use Async Processing
Process webhooks asynchronously to respond within 5 seconds:

```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

@app.post("/webhook")
async def handle_webhook(payload: dict, background_tasks: BackgroundTasks):
    # Respond immediately
    background_tasks.add_task(process_webhook_async, payload)
    return {"status": "accepted"}

async def process_webhook_async(payload: dict):
    # Do heavy processing here
    await heavy_database_operations(payload)
```

---

## 5. SDK Performance Tips

### Connection Pooling
```python
import nexacloud
from nexacloud import NexaCloudClient

# Configure connection pool (default is 10)
client = NexaCloudClient(
    api_key="YOUR_API_KEY",
    connection_pool_size=25,  # Increase for high concurrency
    timeout=30
)
```

### Batch Operations
Use batch endpoints to reduce network round trips:

```python
# Create 50 records in 1 API call instead of 50 calls
users_to_create = [{"name": f"User {i}", "email": f"user{i}@example.com"} for i in range(50)]
result = client.users.batch_create(users_to_create)
```

---

## 6. Performance Monitoring

### Built-In Metrics Dashboard
Access performance metrics at **Dashboard → Analytics → API Performance**:
- P50, P95, P99 response time percentiles
- Error rate by endpoint
- Throughput (requests per minute)
- Cache hit rate

### Setting Up Alerts
```json
{
  "alert_name": "High Latency Alert",
  "metric": "api.response_time_p95",
  "threshold": 2000,
  "unit": "milliseconds",
  "duration": "5 minutes",
  "notification_channels": ["slack", "email"]
}
```

---

## 7. Performance Benchmarks

| Operation | Expected Latency | Notes |
|-----------|-----------------|-------|
| Simple GET request | < 50ms | Cached resources |
| Complex GET with filters | < 200ms | Indexed filters |
| POST/PUT with validation | < 300ms | Synchronous |
| Report generation | 2–30 seconds | Async job |
| Batch import (1000 records) | 5–15 seconds | Background processing |
| Full text search | < 500ms | Uses Elasticsearch |

---

## Support
- **Performance Issues:** performance@nexacloud.io
- **Optimization Consultation (Enterprise):** Book a session via your account manager
- **Developer Docs:** https://docs.nexacloud.io/performance
