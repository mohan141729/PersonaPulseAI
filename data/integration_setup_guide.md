# Third-Party Integration Setup Guide

## Overview
NexaCloud integrates with over 100 popular tools and platforms. This guide walks you through setting up the most common integrations.

---

## 1. Slack Integration

### Setup Steps
1. Navigate to **Settings → Integrations → Slack**
2. Click **"Connect Slack Workspace"**
3. Authorize NexaCloud in the Slack OAuth flow
4. Select channels for different notification types:
   - `#alerts` for critical system alerts
   - `#support` for new support tickets
   - `#billing` for payment notifications
5. Click **"Save Configuration"**

### Available Slack Notifications
- New support ticket created
- SLA breach warning (1 hour before breach)
- System maintenance announcement
- API usage at 80% of rate limit
- Billing payment failed

### Slash Commands (in Slack)
```
/nexacloud status          — Check current system status
/nexacloud ticket [ID]     — Look up a support ticket
/nexacloud usage           — Check API usage today
```

---

## 2. GitHub Integration

### Use Cases
- Automatically create GitHub issues from support tickets
- Link code commits to resolved bugs
- Trigger deployments via NexaCloud webhooks

### Setup
1. Go to **Settings → Integrations → GitHub**
2. Click **"Authorize GitHub"** and select your repositories
3. Configure mapping rules:
   - P1 tickets → Auto-create GitHub issue with `critical` label
   - Resolved ticket → Close linked GitHub issue

### Webhook Configuration
```json
{
  "event": "ticket.created",
  "filter": {"priority": "P1"},
  "action": {
    "type": "github_create_issue",
    "repo": "your-org/your-repo",
    "labels": ["bug", "critical", "nexacloud"]
  }
}
```

---

## 3. Jira Integration

### Setup Steps
1. Go to **Settings → Integrations → Jira**
2. Enter your Jira Cloud URL (e.g., `https://yourcompany.atlassian.net`)
3. Generate a Jira API token at **id.atlassian.com → Security → API Tokens**
4. Enter your Atlassian email and API token
5. Map NexaCloud ticket priorities to Jira issue types:
   - P1 → Blocker
   - P2 → Critical
   - P3 → Major
   - P4 → Minor

---

## 4. Zapier Integration

NexaCloud offers a native Zapier app for no-code integrations.

### Popular Zap Templates
1. **New NexaCloud ticket → Create Trello card**
2. **NexaCloud payment received → Add row to Google Sheets**
3. **NexaCloud API alert → Send SMS via Twilio**
4. **New user signup → Add to Mailchimp list**

### API Key for Zapier
1. Generate a dedicated Zapier API key in **Settings → Developer → API Keys**
2. Use scope: `read:tickets, read:users, read:billing`
3. Enter this key when configuring NexaCloud in Zapier

---

## 5. Salesforce Integration

### CRM Sync Setup
1. Go to **Settings → Integrations → Salesforce**
2. Authenticate with your Salesforce org (OAuth)
3. Configure sync direction:
   - **NexaCloud → Salesforce:** Sync new accounts, billing changes
   - **Salesforce → NexaCloud:** Sync contact updates, deal stages
4. Set sync frequency: Real-time (webhook) or Scheduled (hourly/daily)

### Field Mapping
```
NexaCloud Account.email    → Salesforce Contact.Email
NexaCloud Account.company  → Salesforce Account.Name
NexaCloud Subscription.plan → Salesforce Opportunity.Product
NexaCloud Ticket.status    → Salesforce Case.Status
```

---

## 6. Google Workspace Integration

### SSO Setup (Google OAuth)
1. Go to **Admin Panel → SSO → Google Workspace**
2. Enter your Google Workspace domain
3. Configure user provisioning:
   - **Auto-provision:** New Google Workspace users get NexaCloud access automatically
   - **Manual:** Admin must approve each new user

### Google Calendar Integration
- Schedule maintenance windows that sync to team Google Calendars
- Set up in: **Settings → Integrations → Google Calendar**

---

## 7. REST API Webhooks (Generic)

For custom integrations, use NexaCloud's webhook system:

### Creating a Webhook
```bash
POST /v1/webhooks
{
  "url": "https://your-server.com/nexacloud-events",
  "events": ["ticket.created", "ticket.resolved", "billing.payment_failed"],
  "secret": "your_webhook_secret_for_hmac_validation"
}
```

### Validating Webhook Signatures
```python
import hmac
import hashlib

def validate_webhook(payload: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    received = signature.replace("sha256=", "")
    return hmac.compare_digest(expected, received)
```

---

## Troubleshooting Integrations

| Issue | Solution |
|-------|----------|
| OAuth connection failing | Clear browser cookies, retry in incognito |
| Webhook not receiving events | Check firewall, verify public URL, review delivery log |
| Data sync delay | Check sync logs in **Settings → Integrations → [Name] → Sync Log** |
| Authentication expired | Re-authorize the integration from **Settings → Integrations** |

## Support
- **Integration Docs:** https://docs.nexacloud.io/integrations
- **Integration Support:** integrations@nexacloud.io
