# Service Level Agreement (SLA)

## Overview
This Service Level Agreement defines the service commitments NexaCloud makes to its customers regarding uptime, support response times, and performance guarantees.

---

## 1. Uptime Guarantee

| Plan | Monthly Uptime SLA | Downtime Allowance |
|------|--------------------|--------------------|
| Starter | 99.5% | ~3.65 hours/month |
| Professional | 99.9% | ~43.8 minutes/month |
| Business | 99.95% | ~21.9 minutes/month |
| Enterprise | 99.99% | ~4.38 minutes/month |

**Measurement:** Uptime is calculated monthly, excluding scheduled maintenance windows announced at least 72 hours in advance.

---

## 2. Support Response Times

### By Plan Tier

| Priority | Starter | Professional | Business | Enterprise |
|----------|---------|--------------|----------|------------|
| P1 - Critical (outage) | 8 hrs | 4 hrs | 1 hr | 15 min |
| P2 - High (degraded) | 24 hrs | 8 hrs | 4 hrs | 1 hr |
| P3 - Medium (bug) | 3 days | 2 days | 1 day | 4 hrs |
| P4 - Low (question) | 5 days | 3 days | 2 days | 1 day |

### Priority Definitions
- **P1 — Critical:** Complete service outage, data loss, security breach. All users affected.
- **P2 — High:** Significant degradation of core functionality. Partial user impact.
- **P3 — Medium:** Non-critical bug with available workaround. Limited user impact.
- **P4 — Low:** General inquiries, how-to questions, feature requests.

---

## 3. SLA Credits

If NexaCloud fails to meet the uptime SLA, customers are eligible for service credits:

| Uptime Achieved | Credit |
|-----------------|--------|
| 99.0% – 99.49% | 10% of monthly fee |
| 95.0% – 98.99% | 25% of monthly fee |
| Below 95.0% | 50% of monthly fee |

**Credit Limitations:**
- Credits are applied to the next billing cycle, not issued as cash refunds
- Maximum credit per month is 50% of the monthly subscription fee
- Credits must be requested within 30 days of the qualifying incident
- Submit credit requests at: **https://support.nexacloud.io/sla-credit**

---

## 4. Scheduled Maintenance

- Planned maintenance occurs **every 3rd Sunday, 2:00 AM–4:00 AM UTC**
- 72-hour advance notice via email and status page
- Emergency maintenance may occur with shorter notice; affected customers are notified immediately
- Scheduled maintenance does not count against SLA uptime calculations

---

## 5. Exclusions

The SLA does not apply to downtime caused by:
- Force majeure events (natural disasters, internet backbone failures)
- Customer's own infrastructure or configuration
- Third-party service failures outside NexaCloud's control
- Customer-initiated modifications that cause instability
- Denial-of-service attacks during active response

---

## 6. Incident Communication

During incidents, NexaCloud communicates via:
- **Status Page:** https://status.nexacloud.io (real-time updates)
- **Email Notifications:** To account administrators
- **In-App Banner:** Displayed during active incidents
- **Slack Integration:** Available for Business and Enterprise plans

---

## 7. Requesting SLA Credits

1. Visit **https://support.nexacloud.io/sla-credit**
2. Log in with your account credentials
3. Select the affected time period and incident reference number
4. Submit your credit request
5. Our SLA team will review and respond within **5 business days**

---

## Contact
- **SLA Team:** sla@nexacloud.io
- **Status Page:** https://status.nexacloud.io
- **Enterprise Escalation:** enterprise-support@nexacloud.io
