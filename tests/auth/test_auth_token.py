from fastapi.testclient import TestClient
from main import app  # import your FastAPI app with the /parlons route
from app.core.security import SecurityInstance
from datetime import datetime, timedelta, timezone

client = TestClient(app)
route_test = "api/v1/parlons"

def make_token(user_id, client_type="browser", token_type="access"):

    return SecurityInstance.create_token(
        data={"sub": str(user_id), "client_type": client_type, "type": token_type},
        expires_delta=timedelta(minutes=SecurityInstance.jwt_min)
    )

def test_browser_access_valid_cookie():
    token = make_token(1, client_type="browser")
    client.cookies.set("access_token", token)
    client.cookies.set("csrf_token", "valid")

    response = client.get(
        route_test,
        headers={"X-CSRF-Token": "valid"}
    )
    assert response.status_code == 200
    # breakpoint()
    data = response.json()
    assert "page" in data
    assert "page_size" in data
    assert "total_items" in data
    assert "data" in data

def test_app_access_valid_header():
    client = TestClient(app)
    token = make_token(1, client_type="app")

    response = client.get(
        route_test,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

# edge cases
def test_auth_route_with_refresh_token():
    client = TestClient(app)
    token = make_token(1, client_type="browser",token_type="refresh")

    client.cookies.set("access_token", token)
    client.cookies.set("csrf_token", "valid")

    response = client.get("api/v1/parlons", headers={"X-CSRF-Token": "valid"})
    assert response.status_code == 401
def test_refresh_route_with_access_token():
    client = TestClient(app)
    token = make_token(1, client_type="browser")
    client.cookies.set("access_token", token)
    response = client.post("api/v1/auth/refresh", headers={"X-CSRF-Token": "valid"})
    assert response.status_code == 401

def test_browser_access_missing_cookie():
    client = TestClient(app)
    response = client.get("api/v1/parlons")
    assert response.status_code == 401

def test_app_access_with_csrf_present():
    token = make_token(1, client_type="app")
    client.cookies.set("csrf_token", 'valid')
    response = client.get(
        "api/v1/parlons",
        headers={"Authorization": f"Bearer {token}", "X-CSRF-Token": "bad"},
    )
    assert response.status_code == 401

def test_wrong_client_type_in_token():
    # Token says "app" but request is browser
    token = make_token(1, client_type="app")
    client.cookies.set("csrf_token", 'valid')
    client.cookies.set("access_token", token)
    response = client.get(
        "api/v1/parlons",
    )
    assert response.status_code == 401


def test_both_cookie_and_header_present():
    token_browser = make_token(1, client_type="browser")
    token_app = make_token(1, client_type="app")
    client.cookies.set("access_token", token_browser)
    response = client.get(
        route_test,
        headers={"Authorization": f"Bearer {token_app}"}
    )
    assert response.status_code == 401



