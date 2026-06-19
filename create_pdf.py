"""
create_pdf.py
-------------
This script generates the required PDF knowledge base document.
Run this once before ingesting documents.

I used fpdf2 for this since it's pure Python and doesn't need anything external.
The content mirrors the password_reset_guide.md but formatted as a PDF.

Usage:
    python create_pdf.py
"""

from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os

class PDFDoc(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(67, 56, 202)  # indigo
        self.cell(0, 10, "NexaCloud Support", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.set_draw_color(67, 56, 202)
        self.set_line_width(0.5)
        self.line(10, 22, 200, 22)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()} | NexaCloud Password Reset Guide | Confidential", align="C")

    def section_title(self, title):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(67, 56, 202)
        self.ln(4)
        self.cell(0, 8, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(200, 200, 230)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.set_text_color(30, 30, 30)
        self.ln(2)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 6, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

    def bullet_item(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 6, f"- {text}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def sub_title(self, text):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(30, 30, 30)
        self.ln(2)
        self.cell(0, 7, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def create_password_reset_pdf(output_path: str):
    pdf = PDFDoc()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(20, 20, 20)
    pdf.ln(2)
    pdf.cell(0, 12, "Password Reset & Account Recovery Guide", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, "NexaCloud SaaS Platform | Customer Support Documentation", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(6)

    # Section 1
    pdf.section_title("1. Standard Password Reset")
    pdf.body_text(
        "If you have forgotten your NexaCloud password, you can reset it easily using your "
        "registered email address. The reset link is valid for 30 minutes from the time it is sent."
    )
    pdf.sub_title("Steps to Reset Your Password:")
    steps = [
        "Visit the NexaCloud login page at https://app.nexacloud.io/login",
        "Click 'Forgot Password?' link below the login button",
        "Enter your registered email address and click 'Send Reset Link'",
        "Check your inbox (and spam/junk folder) for an email from noreply@nexacloud.io",
        "Click the reset link in the email - it expires in 30 minutes",
        "Create a new password meeting the requirements listed below",
        "Click 'Update Password' and log in with your new credentials"
    ]
    for i, step in enumerate(steps, 1):
        pdf.bullet_item(f"Step {i}: {step}")
    pdf.ln(2)

    # Password requirements
    pdf.sub_title("Password Requirements:")
    reqs = [
        "Minimum 12 characters in length",
        "At least 1 uppercase letter (A-Z)",
        "At least 1 lowercase letter (a-z)",
        "At least 1 number (0-9)",
        "At least 1 special character: !@#$%^&*",
        "Cannot reuse your last 5 passwords"
    ]
    for r in reqs:
        pdf.bullet_item(r)

    # Section 2
    pdf.section_title("2. Did Not Receive the Reset Email?")
    pdf.body_text(
        "If you did not receive the password reset email within 5 minutes, try the following steps:"
    )
    checks = [
        "Check your Spam and Junk mail folders",
        "Make sure you are checking the correct email account",
        "Add noreply@nexacloud.io to your contacts or whitelist",
        "Wait 5 minutes - emails may be delayed during peak periods",
        "Try the reset process again from a different browser or incognito mode",
        "Contact your IT administrator if your company filters automated emails"
    ]
    for c in checks:
        pdf.bullet_item(c)

    # Section 3
    pdf.section_title("3. Account Locked Due to Failed Login Attempts")
    pdf.body_text(
        "NexaCloud accounts are automatically locked after 5 consecutive failed login attempts "
        "as a security measure. You will receive an email notification when this happens."
    )
    pdf.sub_title("Self-Service Unlock (Available 24/7):")
    unlock_steps = [
        "Visit https://app.nexacloud.io/unlock",
        "Enter your account email address",
        "Complete identity verification (email code + security question)",
        "Your account will be unlocked immediately after successful verification"
    ]
    for step in unlock_steps:
        pdf.bullet_item(step)

    pdf.ln(2)
    pdf.sub_title("Admin Unlock (For Organization Accounts):")
    pdf.body_text(
        "If you are part of an organization, your Organization Admin can unlock your account by navigating to: "
        "Admin Panel > Users > Active Users, searching for your name, and clicking 'Unlock Account'."
    )

    # Section 4
    pdf.section_title("4. Two-Factor Authentication (2FA) Issues")
    pdf.body_text(
        "If you have lost access to your 2FA device or authenticator app, follow these steps:"
    )
    tfa_steps = [
        "On the 2FA login prompt, click 'Use Backup Code'",
        "Enter one of your 8-digit backup codes (provided when 2FA was set up)",
        "Each backup code can only be used once",
        "After logging in, go to Settings > Security to reconfigure your 2FA device"
    ]
    for s in tfa_steps:
        pdf.bullet_item(s)

    pdf.ln(2)
    pdf.sub_title("No Backup Codes Available?")
    pdf.body_text(
        "If you no longer have your backup codes, contact security@nexacloud.io with: "
        "your account email, a government-issued photo ID, and your organization name. "
        "Manual account recovery takes 3-5 business days due to identity verification requirements."
    )

    # Section 5
    pdf.section_title("5. SSO (Single Sign-On) Password Reset")
    pdf.body_text(
        "If your organization uses Single Sign-On (Google Workspace, Azure AD, or Okta), "
        "your password is managed by your Identity Provider - NOT by NexaCloud. "
        "You must reset your password through your company's IT team or identity provider portal. "
        "NexaCloud admins can temporarily disable SSO under Admin > SSO Settings > Emergency Bypass "
        "if access is urgently needed."
    )

    # Section 6
    pdf.section_title("6. Account Recovery After Deactivation")
    pdf.body_text(
        "If your account was deactivated by an administrator or due to non-payment, reactivation is possible:"
    )
    react_steps = [
        "Accounts deactivated within the last 30 days can be reactivated",
        "Email accounts@nexacloud.io from your registered email address",
        "Provide your account email and a brief business justification for reactivation",
        "Reactivation is typically processed within 1 business day",
        "Accounts deactivated for more than 30 days are permanently deleted per our data retention policy"
    ]
    for r in react_steps:
        pdf.bullet_item(r)

    # Section 7 - Contact
    pdf.section_title("7. Contact Support")
    pdf.body_text("If none of the above steps resolved your issue, please reach out to us:")
    contacts = [
        "Account & Password Support: accounts@nexacloud.io",
        "Security Issues & 2FA Recovery: security@nexacloud.io",
        "Support Portal: https://support.nexacloud.io",
        "Live Chat: Available Mon-Fri 9AM-6PM UTC (Business and Enterprise plans)"
    ]
    for c in contacts:
        pdf.bullet_item(c)

    pdf.ln(4)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 6, "Document Version: 3.2 | Last Updated: October 2024 | NexaCloud Inc.", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    # Save
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    pdf.output(output_path)
    print(f"[+] PDF created: {output_path}")


if __name__ == "__main__":
    output = os.path.join("data", "password_reset_guide.pdf")
    create_password_reset_pdf(output)
    print("Done! The PDF knowledge base document is ready.")
