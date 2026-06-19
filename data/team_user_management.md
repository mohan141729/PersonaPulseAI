# Team & User Management Guide

## Overview
This guide explains how to manage users, roles, and permissions within your NexaCloud organization.

---

## 1. User Roles

NexaCloud has four built-in roles:

| Role | Description | Key Permissions |
|------|-------------|-----------------|
| **Owner** | Full control, only one per org | Billing, delete org, all admin actions |
| **Admin** | Organization management | Add/remove users, configure SSO, view all data |
| **Member** | Standard access | Use all features, manage own profile |
| **Viewer** | Read-only access | View data and reports, cannot make changes |

### Changing a User's Role
1. **Admin Panel → Users**
2. Click on the user's name
3. Under **"Role"**, select the new role from dropdown
4. Click **"Save Changes"**

Only Owners and Admins can change roles. A user cannot change their own role.

---

## 2. Inviting New Users

### Sending an Invitation
1. Go to **Admin Panel → Users → Invite Users**
2. Enter the email address(es) — you can paste multiple emails separated by commas
3. Select the role for the new user(s)
4. Optionally: add a personal message to the invitation email
5. Click **"Send Invitations"**

The invited user will receive an email to create their account. The invitation link expires in **72 hours**.

### Resending an Invitation
If the invite expired or wasn't received:
1. **Admin Panel → Users → Pending Invitations**
2. Find the user and click **"Resend"**

### Bulk Invite via CSV
For inviting many users at once:
1. Download the CSV template from **Admin Panel → Users → Import Users**
2. Fill in columns: `email`, `first_name`, `last_name`, `role`
3. Upload the CSV and preview the users
4. Confirm the import

---

## 3. Removing Users

### Deactivating vs Deleting

**Deactivation** (recommended):
- User cannot log in but data is preserved
- Can be reactivated later
- Steps: **Admin Panel → Users → [User] → Deactivate Account**

**Permanent Deletion:**
- Removes user and all their personal data
- Cannot be undone
- Their created content is attributed to the admin who deleted them
- Steps: **Admin Panel → Users → [User] → Delete Account**

### When a User Leaves Your Organization
1. Deactivate their account immediately
2. Transfer ownership of their projects/documents if needed
3. Revoke any API keys they created under your org: **Admin Panel → API Keys → Filter by User**
4. Remove them from any active SSO groups in your Identity Provider

---

## 4. Permissions & Access Control

### Feature-Level Permissions
Configure what each role can access:
1. **Admin Panel → Settings → Permissions**
2. Toggle on/off features per role
3. Click **"Save"**

Example configurations:
- Prevent Viewers from exporting data
- Allow Members to manage integrations
- Restrict API key creation to Admins only

### Project-Level Permissions
Individual projects can have separate access controls:
1. Open the project
2. Click **"Share"** or **"Settings → Access"**
3. Add users with project-specific roles: Editor, Commenter, Viewer

---

## 5. Single Sign-On (SSO) User Management

When SSO is enabled, user provisioning can be handled automatically:

### SCIM Provisioning (Automatic Sync)
SCIM syncs your Identity Provider's user directory with NexaCloud:
- New employees added to your IdP → Auto-created in NexaCloud
- Employee leaves company → Auto-deactivated in NexaCloud
- Role changes in IdP → Synced to NexaCloud

**Setup:** Admin Panel → SSO → SCIM Provisioning → Enable & copy the SCIM endpoint URL

### Manual SSO Management
Without SCIM, manage users manually. SSO users still need to be invited to NexaCloud first.

---

## 6. Usage Limits by Plan

| Feature | Starter | Professional | Business | Enterprise |
|---------|---------|--------------|----------|------------|
| Max Users | 5 | 25 | 100 | Unlimited |
| Guest Users | ✗ | 5 | 20 | Unlimited |
| Custom Roles | ✗ | ✗ | ✓ | ✓ |
| SCIM Provisioning | ✗ | ✗ | ✓ | ✓ |
| Audit Logs | 30 days | 90 days | 1 year | 7 years |

---

## 7. Audit Log

Every user management action is logged:
- **Admin Panel → Audit Log**
- Filter by: Action type, User, Date range
- Export audit logs as CSV for compliance

Logged actions include: login, logout, role changes, invitations, deletions, permission changes, API key creation/revocation.

---

## Contact
- **Admin Support:** admin-support@nexacloud.io
- **Enterprise User Management:** enterprise@nexacloud.io
