# from typing import Annotated
import jwt
from fastapi.testclient import TestClient


from main import app


client = TestClient(app)

def test_login_sets_tokens_and_cookies():

    response = client.post("/api/v1/auth/login", json={
        "email": "thebackdoors182@gmail.com",
        "password": "test123",
        "remember_me": True
    })
    assert response.status_code == 200

    data = response.json()

    assert "token" in data
    assert "csrf" in data is not None
    assert "user" in data


    # assert data["token"]["access_token"] is None
    # assert data["token"]["refresh_token"] is None
    assert "access_token" not in data["token"]
    assert "refresh_token" not in data["token"]
    assert data["token"]["expires_at"] is not None
    assert data["token"]["expires_in"] is not None

    cookies = response.cookies

    assert "access_token" in cookies
    assert "refresh_token" in cookies
    assert "csrf_token" in cookies

    assert cookies.get("access_token") != cookies.get("refresh_token")


def test_refresh_reuses_refresh_token_when_remember_me_false_browser():

    login_resp = client.post("/api/v1/auth/login", json={
        "email": "thebackdoors182@gmail.com",
        "password": "test123",
        "remember_me": False
    })
    assert login_resp.status_code == 200
    old_refresh_token = login_resp.cookies.get("refresh_token")
    assert old_refresh_token is not None

    # set cookie on client instead of per-request
    client.cookies.set("refresh_token", old_refresh_token)
    csrf_token = login_resp.cookies.get("csrf_token")

    # call refresh
    refresh_resp = client.post(
        "/api/v1/auth/refresh", headers={"X-CSRF-Token": csrf_token},
    )
    assert refresh_resp.status_code == 200

    # cookie should still contain the same refresh token
    new_refresh_token = refresh_resp.cookies.get("refresh_token")
    assert new_refresh_token == old_refresh_token


def test_refresh_rotates_refresh_token_when_remember_me_true_browser():

    # Step 1: login
    resp = client.post(
        "/api/v1/auth/login",
        json={"email": "thebackdoors182@gmail.com", "password": "test123", "remember_me": True}
    )
    old_refresh_token = resp.cookies.get("refresh_token")
    csrf_token = resp.cookies.get("csrf_token")

    assert old_refresh_token is not None

    resp2 = client.post("/api/v1/auth/refresh",
                        headers={"X-CSRF-Token": csrf_token})
    new_refresh_token = resp2.cookies.get("refresh_token")
    assert new_refresh_token is not None

    # Step 3: assert rotation
    assert new_refresh_token != old_refresh_token

    # Step 4: check payload differences
    old_payload = jwt.decode(old_refresh_token, options={"verify_signature": False})
    new_payload = jwt.decode(new_refresh_token, options={"verify_signature": False})

    # jti and iat should differ
    assert new_payload.get("jti") != old_payload.get("jti")
    assert new_payload.get("iat") != old_payload.get("iat")

def test_logout_clears_cookies():

    login_resp = client.post("/api/v1/auth/login", json={
        "email": "thebackdoors182@gmail.com",
        "password": "test123",
        "remember_me": True
    })
    assert login_resp.status_code == 200
    assert "access_token" in login_resp.cookies
    assert "refresh_token" in login_resp.cookies
    assert "csrf_token" in login_resp.cookies

    # now logout
    logout_resp = client.post("/api/v1/auth/logout")
    assert logout_resp.status_code == 200
    data = logout_resp.json()
    assert data["detail"] == "Successfully logged out"

    # cookies should be cleared
    cookies = logout_resp.cookies
    assert cookies.get("access_token") is None
    assert cookies.get("refresh_token") is None
    assert cookies.get("csrf_token") is None

#edge cases

def test_login_fails_with_invalid_user():

    response = client.post("/api/v1/auth/login", json={
        "email": "randomshit@example.com",
        "password": "sdfjkgdfkljgdfjklgd",
        "remember_me": False
    })

    # your route should reject this
    assert response.status_code == 401
    data = response.json()
    assert data["message"] == "Invalid credentials"
    assert data["error_code"] == "UNAUTHORIZED"

    cookies = response.cookies
    assert cookies.get("access_token") is None
    assert cookies.get("refresh_token") is None
    assert cookies.get("csrf_token") is None

