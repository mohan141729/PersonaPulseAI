# Mobile App Support Guide

## Overview
NexaCloud is available on iOS and Android. This guide covers setup, common issues, and troubleshooting for the mobile apps.

---

## 1. Downloading the App

| Platform | Download Link | Minimum Version |
|----------|---------------|-----------------|
| iOS | App Store → Search "NexaCloud" | iOS 15.0+ |
| Android | Google Play → Search "NexaCloud" | Android 9.0+ |

The mobile app supports the same account as the web platform — no separate registration needed.

---

## 2. Setting Up the Mobile App

### First-Time Login
1. Open the NexaCloud app
2. Tap **"Sign In"**
3. Enter your email and password
4. If your organization uses SSO, tap **"Sign in with SSO"** instead and enter your company domain
5. Complete 2FA if enabled on your account
6. Allow notifications when prompted (recommended for ticket alerts)

### Biometric Login (Face ID / Fingerprint)
After your first login:
1. Go to **Profile → Security → Biometric Login**
2. Toggle **"Enable Biometric Login"**
3. Follow the device prompt to set up Face ID or fingerprint

---

## 3. Features Available on Mobile

| Feature | iOS | Android | Notes |
|---------|-----|---------|-------|
| View & manage tickets | ✓ | ✓ | Full functionality |
| Reply to tickets | ✓ | ✓ | |
| Push notifications | ✓ | ✓ | |
| View dashboard/reports | ✓ | ✓ | Read-only on mobile |
| Create reports | ✗ | ✗ | Use web app |
| API key management | ✗ | ✗ | Use web app |
| User management (admin) | Limited | Limited | Basic operations only |
| File upload | ✓ | ✓ | Up to 25MB |
| Offline mode | Limited | Limited | View recently synced data |

---

## 4. Push Notifications

### Enabling Notifications
1. **Profile → Notifications → Push Notifications**
2. Toggle on the notification types you want:
   - New ticket assigned to me
   - Ticket reply received
   - SLA breach warnings
   - System alerts
   - Billing alerts

### Not Receiving Notifications?
**iOS:**
1. iPhone **Settings → NexaCloud → Notifications**
2. Ensure **"Allow Notifications"** is ON
3. Check that Do Not Disturb / Focus modes aren't blocking app notifications

**Android:**
1. **Settings → Apps → NexaCloud → Notifications**
2. Enable all notification categories
3. Check battery optimization: **Settings → Battery → NexaCloud → Don't Optimize**

---

## 5. Common Mobile Issues

### App Crashes on Launch
1. Force-close the app and reopen it
2. Check for app updates in the App Store / Google Play
3. Restart your device
4. If the issue persists, uninstall and reinstall the app (your data is cloud-based, nothing is lost)

### "Cannot Connect" Error
1. Check your internet connection (try loading a website)
2. Check **https://status.nexacloud.io** for active incidents
3. Try switching between WiFi and mobile data
4. If on corporate WiFi, ask IT if nexacloud.io is whitelisted

### Sync Issues (Data Not Updating)
1. Pull down to refresh on the main screen
2. Go to **Profile → Sync → Force Sync**
3. Log out and log back in if sync problems persist

### Login Loop / Stuck on Login Screen
1. Clear app cache:
   - iOS: Reinstall app
   - Android: **Settings → Apps → NexaCloud → Clear Cache**
2. Ensure your account is active (check web login)
3. If SSO is enabled for your org, ensure your SSO session is valid

---

## 6. Data Usage & Offline Mode

NexaCloud mobile uses approximately **5–20 MB/month** of mobile data for normal usage.

**Offline Access:**
- Recently viewed tickets and data are cached for offline reading
- Changes made offline sync automatically when connectivity is restored
- Offline mode is available but limited — cannot create new tickets while offline

**Reduce Data Usage:**
- **Profile → Settings → Images → Load on WiFi Only**
- Disables auto-loading of attachments on mobile data

---

## 7. Privacy on Mobile

The NexaCloud app:
- Does NOT access your contacts, photos, or camera without explicit permission
- Camera/photos access is only requested when you choose to attach a file to a ticket
- Location is NOT tracked at any time
- Biometric data (Face ID/fingerprint) stays on your device — NexaCloud never receives it

---

## 8. Reporting App Bugs

If you find a bug:
1. **Profile → Help → Report a Bug**
2. Include a description and, if possible, a screenshot
3. Enable **Diagnostic Logs** before reproducing the bug: **Profile → Settings → Diagnostic Logging → Enable**

---

## Contact
- **Mobile App Support:** mobile-support@nexacloud.io
- **App Store Reviews:** We respond to all reviews within 3 business days
- **Feature Requests:** https://feedback.nexacloud.io/mobile
