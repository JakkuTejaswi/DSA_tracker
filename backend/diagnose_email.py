import os
import smtplib
import traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

def test_email():
    print(f"DEBUG: Attempting to send from {SMTP_USER}")
    msg = MIMEMultipart()
    msg["Subject"] = "Test"
    msg["From"] = SMTP_USER
    msg["To"] = SMTP_USER
    msg.attach(MIMEText("Test message", "plain"))

    try:
        print(f"DEBUG: Connecting to {SMTP_HOST}:{SMTP_PORT}...")
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10)
        print("DEBUG: EHLO...")
        server.ehlo()
        print("DEBUG: StartTLS...")
        server.starttls()
        print("DEBUG: Login...")
        server.login(SMTP_USER, SMTP_PASS)
        print("DEBUG: Sending...")
        server.sendmail(SMTP_USER, [SMTP_USER], msg.as_string())
        server.quit()
        print("SUCCESS!")
    except Exception:
        print("FAILED!")
        traceback.print_exc()

if __name__ == "__main__":
    test_email()
