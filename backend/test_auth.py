import requests

BASE_URL = "http://127.0.0.1:8000"

def test_flow():
    # 1. Register
    email = "testuser_new@example.com"
    password = "password123"
    username = "testuser_new"
    
    print(f"Registering {email}...")
    reg_res = requests.post(f"{BASE_URL}/users/register", json={
        "email": email,
        "password": password,
        "username": username
    })
    print(f"Registration Status: {reg_res.status_code}")
    print(f"Registration Body: {reg_res.text}")
    
    # 2. Login (even if registration failed because it already exists)
    login_email = email
    print(f"Logging in as {login_email}...")
    login_res = requests.post(f"{BASE_URL}/users/login", data={
        "username": login_email,
        "password": password
    })
    print(f"Login Status: {login_res.status_code}")
    print(f"Login Body: {login_res.text}")

if __name__ == "__main__":
    test_flow()
