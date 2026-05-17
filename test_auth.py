import sys
sys.path.insert(0, '.')

from app import app

app.testing = True
app.secret_key = 'test-secret-key'

def test_login_logout():
    with app.test_client() as client:
        # Test 1: GET /login returns 200 and shows login form
        resp = client.get('/login')
        assert resp.status_code == 200
        assert b'Sign in' in resp.data
        print("GET /login returns 200 and shows login form")

        # Test 2: POST /login with invalid email
        resp = client.post('/login', data={'email': 'invalid', 'password': ''})
        assert resp.status_code == 200
        assert b'Please enter a valid email address' in resp.data or b'Invalid email or password' in resp.data
        print("POST /login with invalid email returns error")

        # Test 3: POST /login with valid email but wrong password
        resp = client.post('/login', data={'email': 'demo@spendly.com', 'password': 'wrong'})
        assert resp.status_code == 200
        assert b'Invalid email or password' in resp.data
        print("POST /login with wrong password returns error")

        # Test 4: POST /login with valid credentials (demo user)
        resp = client.post('/login', data={'email': 'demo@spendly.com', 'password': 'demo123'}, follow_redirects=True)
        assert resp.status_code == 200
        # After login, we should see logout link and not see login link
        assert b'Logout' in resp.data
        assert b'Sign in' not in resp.data  # Because we are logged in, the base.html should show logout
        print("POST /login with valid credentials redirects and shows logout link")

        # Test 5: Accessing /login while logged in should redirect to landing (or profile in future)
        resp = client.get('/login')
        assert resp.status_code == 200
        # Since we are logged in, the base.html in the response should show logout link
        assert b'Logout' in resp.data
        print("GET /login while logged in shows logout link (already logged in)")

        # Test 6: GET /logout clears session and redirects to landing
        resp = client.get('/logout', follow_redirects=True)
        assert resp.status_code == 200
        # After logout, we should see sign in link and not see logout link
        assert b'Sign in' in resp.data
        assert b'Logout' not in resp.data
        print("GET /logout redirects and shows sign in link")

        # Test 7: After logout, accessing /login shows login form
        resp = client.get('/login')
        assert resp.status_code == 200
        assert b'Sign in' in resp.data
        print("After logout, GET /login shows login form")

        print("\nAll tests passed!")

if __name__ == '__main__':
    test_login_logout()