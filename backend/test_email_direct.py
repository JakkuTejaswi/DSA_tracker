import os
from email_utils import send_password_reset_email
from dotenv import load_dotenv

load_dotenv()

# Test with a known email
TEST_EMAIL = os.getenv("SMTP_USER") # Sending to self for testing

if not TEST_EMAIL:
    print("Error: SMTP_USER not set in .env")
else:
    print(f"Testing email sending to {TEST_EMAIL}...")
    result = send_password_reset_email(TEST_EMAIL, "test_token_123")
    if result:
        print("Success! Email sent.")
    else:
        print("Failed. Check the error message above.")
