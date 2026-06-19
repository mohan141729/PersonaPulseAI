# Two-Factor Authentication (2FA) Guide

## Overview
Two-factor authentication adds an extra layer of security to your NexaCloud account.
Even if someone gets your password, they can't log in without your second factor.

---

## 1. Enabling 2FA

### Using an Authenticator App (Recommended)
Works with Google Authenticator, Authy, Microsoft Authenticator, 1Password, etc.

1. Go to **Settings → Security → Two-Factor Authentication**
2. Click **"Enable 2FA"**
3. Choose **"Authenticator App"**
4. Scan the QR code shown on screen with your authenticator app
5. Enter the 6-digit code shown in your app to verify it's working
6. Click **"Confirm & Enable"**
7. **Download your backup codes** — save these somewhere safe (you get 10 codes, each usable once)

### Using SMS (Less Secure, but Available)
1. Same path: **Settings → Security → 2FA**
2. Choose **"SMS"**
3. Enter your mobile number with country code (e.g., +1 555-0123)
4. Enter the verification code sent to your phone
5. Done — you'll receive SMS codes at each login

**Note:** SMS 2FA is less secure than app-based 2FA. We recommend using an authenticator app if possible. SMS is not available for Enterprise accounts due to security policy.

---

## 2. Logging In With 2FA

1. Enter your email and password as usual
2. When prompted, open your authenticator app and enter the current 6-digit code
3. Codes refresh every 30 seconds — enter it before it expires
4. Check "Trust this device for 30 days" to skip 2FA on trusted devices

---

## 3. Backup Codes

You received 10 backup codes when you set up 2FA. Each code:
- Is 8 digits long
- Can only be used ONCE
- Never expires

**When to use:** When you don't have access to your phone or authenticator app.

### Viewing Remaining Backup Codes
Go to **Settings → Security → 2FA → Manage → View Backup Codes**

### Regenerating Backup Codes
If you've used most of your backup codes or think they may be compromised:
1. **Settings → Security → 2FA → Manage → Regenerate Backup Codes**
2. This invalidates all old codes and creates 10 new ones
3. You'll need to confirm with your current 2FA method first

---

## 4. Lost Access to 2FA Device

### Option A: Use a Backup Code
1. On the 2FA prompt, click **"Use backup code"**
2. Enter one of your 8-digit backup codes

### Option B: Account Recovery (No Backup Codes)
Contact support at **security@nexacloud.io** with:
- Government-issued photo ID
- Account email address
- Recent billing information (last 4 digits of card on file)

Recovery takes **3–5 business days** due to identity verification requirements.

---

## 5. Disabling 2FA

We strongly recommend keeping 2FA enabled. If you need to disable it:
1. **Settings → Security → 2FA → Manage → Disable 2FA**
2. Confirm with your current 2FA code
3. Note: Organization admins can enforce mandatory 2FA, in which case individual users cannot disable it

---

## 6. 2FA for Teams (Admin)

As an organization admin, you can:
- **Enforce 2FA for all users:** Admin Panel → Security → Require 2FA
- **View 2FA status per user:** Admin Panel → Users → [User] → Security
- **Exempt specific users:** Not available — enforcement applies to all

When mandatory 2FA is enabled, users who haven't set it up will be prompted on their next login.

---

## Common Issues

| Problem | Solution |
|---------|----------|
| Code rejected even though it's correct | Check your device clock is synced (NTP). Codes are time-based. |
| QR code won't scan | Try entering the setup key manually (shown below the QR code) |
| SMS code never arrives | Check phone has signal, try resending. Contact support if persistent. |
| Lost phone, no backup codes | Contact security@nexacloud.io for manual recovery |

---

## Contact
- **Security Team:** security@nexacloud.io
- **Account Recovery:** https://support.nexacloud.io/2fa-recovery
