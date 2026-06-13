import requests

BASE_URL = "http://127.0.0.1:8000"

def test_flow():
    email = "testuser_multipart@example.com"
    password = "password123"
    username = "testuser_multipart"
    
    print(f"Registering {email}...")
    requests.post(f"{BASE_URL}/users/register", json={
        "email": email,
        "password": password,
        "username": username
    })
    
    # Login with multipart/form-data (using files parameter in requests to mimic FormData)
    print(f"Logging in as {email} with multipart/form-data...")
    files = {
        'username': (None, email),
        'password': (None, password)
    }
    # Note: requests.post with 'files' but no 'data' sends multipart/form-data
    login_res = requests.post(f"{BASE_URL}/users/login", files=files)
    
    print(f"Login Status: {login_res.status_code}")
    print(f"Login Body: {login_res.text}")

if __name__ == "__main__":
    test_flow()
