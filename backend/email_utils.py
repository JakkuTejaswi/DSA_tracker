import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# SMTP Configuration
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

def send_password_reset_email(to_email: str, reset_token: str):
    """Send a password-reset link to the given email address."""

    reset_link = f"{FRONTEND_URL}/reset-password?token={reset_token}"

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #f8fafc; padding: 40px; margin: 0; }}
        .container {{ max-width: 500px; margin: 0 auto; background: #1e293b; border-radius: 16px; padding: 40px; border: 1px solid #334155; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }}
        .hero-icon {{ font-size: 48px; margin-bottom: 20px; }}
        h1 {{ color: #6366f1; margin: 0 0 10px 0; font-size: 24px; }}
        p {{ color: #94a3b8; line-height: 1.6; font-size: 16px; }}
        .btn {{ display: inline-block; background: #6366f1; color: #ffffff !important; padding: 14px 32px; border-radius: 8px; text-decoration: none; font-weight: 600; margin: 25px 0; }}
        .divider {{ border-top: 1px solid #334155; margin: 30px 0; }}
        .note {{ font-size: 0.85rem; color: #64748b; line-height: 1.4; }}
        .footer {{ margin-top: 30px; text-align: center; color: #475569; font-size: 0.8rem; }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="hero-icon">🔐</div>
        <h1>Reset Your Password</h1>
        <p>Hi there,</p>
        <p>We received a request to reset your password for your DSA Tracker account. Click the button below to choose a new one. This link will expire in 1 hour.</p>
        
        <center>
          <a href="{reset_link}" class="btn">Reset Password</a>
        </center>
        
        <div class="divider"></div>
        
        <p class="note">If you didn't request this, you can safely ignore this email. Your password will remain unchanged.</p>
        <p class="note">If the button above doesn't work, copy and paste this link into your browser:</p>
        <p class="note" style="word-break: break-all; color: #6366f1;">{reset_link}</p>
      </div>
      <div class="footer">
        &copy; {1} DSA Tracker. All rights reserved.
      </div>
    </body>
    </html>
    """.replace("{1}", "2024") # Use static year for simplicity or pass it

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "DSA Tracker – Reset Your Password"
    msg["From"] = f"DSA Tracker <{SMTP_USER}>"
    msg["To"] = to_email
    msg.attach(MIMEText(html_body, "html"))

    # Fallback to console logging if credentials are missing
    if not SMTP_USER or not SMTP_PASS:
        print("\n" + "="*60)
        print("DEBUG: SMTP Credentials missing. Reset link would be:")
        print(f"TO: {to_email}")
        print(f"LINK: {reset_link}")
        print("="*60 + "\n")
        return True

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Email send error: {e}")
        # Still log the link to console so development can continue
        print(f"DEBUG: Failed to send email, but here is the link: {reset_link}")
        return False
