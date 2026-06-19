# Downtime & Scheduled Maintenance Policy

## Overview
This document explains how NexaCloud handles planned maintenance, emergency incidents, and communicates service disruptions to customers.

---

## 1. Scheduled Maintenance Windows

### Regular Maintenance
NexaCloud performs routine maintenance on a predictable schedule to minimize disruption:

| Window | Schedule | Duration |
|--------|----------|----------|
| Primary | 3rd Sunday of each month, 2:00–4:00 AM UTC | Up to 2 hours |
| Secondary | Last Wednesday of each month, 3:00–4:00 AM UTC | Up to 1 hour |
| Emergency | As needed (announced ASAP) | Varies |

### What Happens During Maintenance
- API endpoints may return `503 Service Unavailable`
- The web dashboard may be inaccessible
- In-progress jobs are paused and resumed automatically after maintenance
- Scheduled reports may be delayed by the maintenance duration

### What Is NOT Affected
- Stored data — all data is preserved during maintenance
- Webhook retries — queued events are delivered after maintenance
- Billing — no charges are affected by maintenance windows

---

## 2. Advance Notifications

NexaCloud provides advance notice before all planned maintenance:

| Maintenance Type | Advance Notice | Notification Channels |
|-----------------|----------------|----------------------|
| Scheduled | 72 hours | Email, Status Page, In-App Banner |
| Extended (>2 hrs) | 7 days | Email, Status Page, In-App Banner, Slack |
| Emergency | As soon as possible | Status Page, Email |

To receive maintenance notifications:
- **Email:** All account owners are subscribed automatically. Others can opt in at **Settings → Notifications → Maintenance Alerts**
- **Slack:** Enable in **Settings → Integrations → Slack → Maintenance Notifications**
- **Status Page Subscription:** https://status.nexacloud.io → Click "Subscribe to Updates"
- **RSS Feed:** https://status.nexacloud.io/feed.rss

---

## 3. Incident Response

### Incident Severity Levels

| Level | Definition | Response Time | Example |
|-------|-----------|---------------|---------|
| SEV-1 | Full service outage | 15 minutes | API unreachable for all users |
| SEV-2 | Major degradation | 30 minutes | 50%+ API errors |
| SEV-3 | Partial degradation | 2 hours | Slow response times for some users |
| SEV-4 | Minor issue | 8 hours | Single feature intermittently slow |

### Incident Response Phases

**1. Detection** (0–15 min)
- Automated monitoring alerts on-call engineer
- Initial assessment and severity assignment

**2. Communication** (15–30 min)
- Status page updated with incident description
- Customer notifications sent (email/Slack)
- Engineering team assembled

**3. Mitigation** (Varies by severity)
- Active work to restore service
- Status page updated every 30 minutes
- Customer questions handled by support team

**4. Resolution**
- Full service restoration confirmed
- "All Systems Operational" update on status page
- Customer notification sent

**5. Post-Incident Review (PIR)** (within 5 business days)
- Root cause analysis published on status page
- Steps taken to prevent recurrence
- Enterprise customers receive detailed PIR report

---

## 4. Status Page

All service status is communicated at: **https://status.nexacloud.io**

### System Components Tracked
- API Gateway
- Web Dashboard
- Authentication Service
- Database (read/write)
- File Storage
- Webhook Delivery
- Email Notifications
- Analytics & Reporting

### Status Indicators
| Status | Meaning |
|--------|---------|
| 🟢 Operational | Fully functional |
| 🟡 Degraded Performance | Slower than normal |
| 🟠 Partial Outage | Some users/features affected |
| 🔴 Major Outage | Most users affected |
| ⚫ Maintenance | Planned downtime in progress |

---

## 5. SLA Credits During Unplanned Downtime

If unplanned downtime causes your monthly uptime to fall below your SLA:
1. NexaCloud proactively calculates SLA breaches after each month
2. Eligible credits are automatically applied to your next invoice (Business+ plans)
3. Starter/Professional customers can request credits at **https://support.nexacloud.io/sla-credit**

See the **Service Level Agreement** document for full credit calculation details.

---

## 6. Business Continuity

NexaCloud's infrastructure is designed for resilience:
- **Multi-Region:** Data replicated across multiple availability zones
- **Automatic Failover:** Traffic rerouted within 60 seconds of zone failure
- **Database Backups:** Continuous backups with point-in-time recovery up to 30 days
- **CDN:** Static assets served from global CDN with 99.99% uptime

---

## Contact During Incidents
- **Status Page:** https://status.nexacloud.io
- **Support (active incidents):** support@nexacloud.io with subject "INCIDENT: [Issue]"
- **Enterprise Hotline:** Available to Enterprise customers in your contract
