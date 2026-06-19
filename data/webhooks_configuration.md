# Webhooks Configuration Guide

## Overview
Webhooks let NexaCloud push real-time event notifications to your server.
Instead of polling the API every few seconds, your server receives instant updates whenever something happens.

---

## 1. How Webhooks Work

```
NexaCloud Event (e.g., ticket created)
        ↓
NexaCloud sends HTTP POST to your server URL
        ↓
Your server receives payload → processes it → returns HTTP 200
        ↓
NexaCloud marks delivery as successful
```

If your server returns anything other than 2xx, NexaCloud retries (see retry policy below).

---

## 2. Setting Up a Webhook

### Creating Your First Webhook
1. Go to **Settings → Webhooks → Create Webhook**
2. Fill in:
   - **Endpoint URL:** Your server's HTTPS URL (e.g., `https://yourapp.com/hooks/nexacloud`)
   - **Events:** Select which events to subscribe to
   - **Secret:** A random string for signature validation (generate one or use ours)
3. Click **"Create Webhook"**
4. NexaCloud will send a test ping to verify the endpoint is reachable

### Via API
```bash
POST /v1/webhooks
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY

{
  "url": "https://yourapp.com/hooks/nexacloud",
  "events": ["ticket.created", "ticket.resolved", "billing.payment_failed"],
  "secret": "your_hmac_secret_here",
  "active": true
}
```

---

## 3. Available Events

### Support Ticket Events
| Event | Triggered When |
|-------|----------------|
| `ticket.created` | A new support ticket is opened |
| `ticket.updated` | Ticket status, priority, or fields change |
| `ticket.resolved` | Ticket is marked as resolved |
| `ticket.escalated` | Ticket priority is increased |
| `ticket.assigned` | Ticket is assigned to an agent |

### Billing Events
| Event | Triggered When |
|-------|----------------|
| `billing.payment_succeeded` | Payment processed successfully |
| `billing.payment_failed` | Payment attempt fails |
| `billing.subscription_renewed` | Subscription auto-renews |
| `billing.subscription_cancelled` | Subscription is cancelled |
| `billing.invoice_created` | New invoice is generated |

### User Events
| Event | Triggered When |
|-------|----------------|
| `user.created` | New user account created |
| `user.deactivated` | User account is deactivated |
| `user.role_changed` | User role is updated |

### System Events
| Event | Triggered When |
|-------|----------------|
| `system.alert` | Performance or availability alert triggered |
| `api.rate_limit_warning` | API usage reaches 80% of limit |

---

## 4. Payload Structure

Every webhook delivery includes:

```json
{
  "id": "evt_01HNXYZ789...",
  "type": "ticket.created",
  "created_at": "2024-10-15T14:32:00Z",
  "api_version": "2024-10-01",
  "data": {
    "object": {
      "id": "tkt_001",
      "subject": "Cannot reset password",
      "status": "open",
      "priority": "P2",
      "user_email": "customer@example.com",
      "created_at": "2024-10-15T14:32:00Z"
    }
  }
}
```

---

## 5. Validating Webhook Signatures

Always validate that events are genuinely from NexaCloud using HMAC-SHA256:

```python
import hmac
import hashlib
from flask import Flask, request, abort

app = Flask(__name__)
WEBHOOK_SECRET = "your_webhook_secret"

@app.route("/hooks/nexacloud", methods=["POST"])
def handle_webhook():
    # Get the signature from the header
    signature = request.headers.get("X-NexaCloud-Signature", "")
    
    # Compute expected signature
    payload_bytes = request.get_data()
    expected_sig = "sha256=" + hmac.new(
        WEBHOOK_SECRET.encode(),
        payload_bytes,
        hashlib.sha256
    ).hexdigest()
    
    # Compare signatures (use compare_digest to prevent timing attacks)
    if not hmac.compare_digest(signature, expected_sig):
        abort(400, "Invalid signature")
    
    # Process the event
    event = request.json
    handle_event(event)
    return {"status": "ok"}, 200

def handle_event(event):
    if event["type"] == "ticket.created":
        # do something
        pass
    elif event["type"] == "billing.payment_failed":
        # notify your team
        pass
```

---

## 6. Retry Policy

If your endpoint doesn't return 2xx within 5 seconds, NexaCloud retries:

| Attempt | Timing |
|---------|--------|
| 1st | Immediately |
| 2nd | 5 minutes later |
| 3rd | 30 minutes later |
| 4th | 2 hours later |
| 5th | 24 hours later |

After 5 failed attempts, the webhook is **disabled** and the organization owner is notified by email.

---

## 7. Viewing Delivery Logs

Check the history of webhook deliveries:
1. **Settings → Webhooks → [Webhook Name] → Delivery Log**
2. See: timestamp, event type, HTTP status, response time, response body
3. Manually retry any failed delivery by clicking **"Retry"**

---

## 8. Testing Webhooks Locally

Use [ngrok](https://ngrok.com) to expose your local server during development:
```bash
ngrok http 3000
# Gives you: https://abc123.ngrok.io
# Use this URL as your webhook endpoint in NexaCloud
```

You can also send test events from **Settings → Webhooks → [Webhook] → Send Test Event**.

---

## Contact
- **Webhook Support:** api-support@nexacloud.io
- **Developer Docs:** https://docs.nexacloud.io/webhooks
