import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from app.db.database import Base, get_db
from app.db.models import User, Country, MainCategory
from app.core.security import SecurityInstance


# Use StaticPool to maintain the connection in memory across the session
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def authenticated_client(client, db_session):
    email = "test@example.com"
    password = "password123"
    hashed_pw = SecurityInstance.hash_password(password)

    from app.db.models import Role
    role = Role(id=1, name="superAdmin")
    db_session.add(role)
    db_session.commit()

    user = User(email=email, password=hashed_pw, verified=True, role_id=role.id)
    db_session.add(user)
    db_session.commit()

    login_resp = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password, "remember_me": False}
    )
    assert login_resp.status_code == 200

    csrf = login_resp.cookies.get("csrf_token")
    client.headers.update({"X-CSRF-Token": csrf})

    return client


def test_create_parlon_route(authenticated_client, db_session):
    country = Country(id=9999, country_name="Testland", code="TL")
    db_session.add(country)
    main_category = MainCategory(id=1, name="random cat")
    db_session.add(main_category)
    db_session.commit()

    response = authenticated_client.post("/api/v1/parlons", json={
        "business_name": "My Business",
        "country_id": 9999,
        "category_ids": [1]
    })

    assert response.status_code == 200
    assert response.json()["business_name"] == "My Business"
    assert response.json()["parlon_categories"][0]["main_category"]["name"] == "random cat"


def test_update_parlon_success(authenticated_client, db_session):
    country = Country(id=9999, country_name="Testland", code="TL")
    db_session.add(country)
    main_category = MainCategory(id=1, name="random cat")
    db_session.add(main_category)
    db_session.commit()

    parlon_resp = authenticated_client.post(
        "/api/v1/parlons",
        json={"business_name": "OldName", "country_id": 9999, "category_ids": [1]},
        headers={"X-CSRF-Token": authenticated_client.headers["X-CSRF-Token"]}
    )
    uuid = parlon_resp.json()["id"]

    resp = authenticated_client.put(
        f"/api/v1/parlons/{uuid}",
        json={"business_name": "NewName"}
    )

    assert resp.status_code == 200
    assert resp.json()["business_name"] == "NewName"


def test_update_parlon_not_found(authenticated_client):
    resp = authenticated_client.put(
        "/api/v1/parlons/nonexistent-uuid",
        json={"business_name": "Whatever"}
    )
    assert resp.status_code in (404, 400)


def test_update_parlon_invalid_country(authenticated_client, db_session):
    country = Country(id=9999, country_name="Testland", code="TL")
    db_session.add(country)
    main_category = MainCategory(id=1, name="random cat")
    db_session.add(main_category)
    db_session.commit()

    parlon_resp = authenticated_client.post(
        "/api/v1/parlons",
        json={"business_name": "My Business", "country_id": 9999, "category_ids": [1]},
        headers={"X-CSRF-Token": authenticated_client.headers["X-CSRF-Token"]}
    )
    uuid = parlon_resp.json()["id"]

    resp = authenticated_client.put(
        f"/api/v1/parlons/{uuid}",
        json={"country_id": 999}
    )
    assert resp.status_code in (404, 400)


def test_update_parlon_duplicate_name(authenticated_client, db_session):
    country = Country(id=9999, country_name="Testland", code="TL")
    db_session.add(country)
    main_category = MainCategory(id=1, name="random cat")
    db_session.add(main_category)
    db_session.commit()

    resp1 = authenticated_client.post(
        "/api/v1/parlons",
        json={"business_name": "FirstBusiness", "country_id": 9999, "category_ids": [1]},
        headers={"X-CSRF-Token": authenticated_client.headers["X-CSRF-Token"]}
    )
    resp2 = authenticated_client.post(
        "/api/v1/parlons",
        json={"business_name": "SecondBusiness", "country_id": 9999, "category_ids": [1]},
        headers={"X-CSRF-Token": authenticated_client.headers["X-CSRF-Token"]}
    )

    uuid2 = resp2.json()["id"]

    resp = authenticated_client.put(
        f"/api/v1/parlons/{uuid2}",
        json={"business_name": "FirstBusiness"}
    )
    assert resp.status_code in (400, 409)


def test_create_parlon_with_name_exists(authenticated_client, db_session):
    country = Country(id=9999, country_name="Testland", code="TL")
    db_session.add(country)
    main_category = MainCategory(id=1, name="random cat")
    db_session.add(main_category)
    db_session.commit()

    resp1 = authenticated_client.post(
        "/api/v1/parlons",
        json={"business_name": "My Business", "country_id": 9999, "category_ids": [1]}
    )
    assert resp1.status_code == 200

    resp2 = authenticated_client.post(
        "/api/v1/parlons",
        json={"business_name": "My Business", "country_id": 9999, "category_ids": [1]}
    )
    assert resp2.status_code in (400, 409)


def test_create_parlon_with_country_not_exists(authenticated_client, db_session):
    country = Country(id=9999, country_name="Testland", code="TL")
    db_session.add(country)
    main_category = MainCategory(id=1, name="random cat")
    db_session.add(main_category)
    db_session.commit()

    resp1 = authenticated_client.post(
        "/api/v1/parlons",
        json={"business_name": "My Business", "country_id": 9999, "category_ids": [1]}
    )
    assert resp1.status_code == 200

    resp2 = authenticated_client.post(
        "/api/v1/parlons",
        json={"business_name": "My Business", "country_id": 2, "category_ids": [1]}
    )
    assert resp2.status_code == 404


def test_update_parlon_no_changes(authenticated_client, db_session):
    country = Country(id=9999, country_name="Testland", code="TL")
    db_session.add(country)
    main_category = MainCategory(id=1, name="random cat")
    db_session.add(main_category)
    db_session.commit()

    parlon_resp = authenticated_client.post(
        "/api/v1/parlons",
        json={"business_name": "StableBusiness", "country_id": 9999, "category_ids": [1]}
    )
    uuid = parlon_resp.json()["id"]

    resp = authenticated_client.put(f"/api/v1/parlons/{uuid}", json={})
    assert resp.status_code == 200
    assert resp.json()["business_name"] == "StableBusiness"


def test_update_parlon_invalid_payload(authenticated_client, db_session):
    country = Country(id=9999, country_name="Testland", code="TL")
    db_session.add(country)
    main_category = MainCategory(id=1, name="random cat")
    db_session.add(main_category)
    db_session.commit()

    parlon_resp = authenticated_client.post(
        "/api/v1/parlons",
        json={"business_name": "TypedBusiness", "country_id": 9999, "category_ids": [1]}
    )
    uuid = parlon_resp.json()["id"]

    resp = authenticated_client.put(
        f"/api/v1/parlons/{uuid}",
        json={"country_id": "not-an-int"}
    )
    assert resp.status_code == 422