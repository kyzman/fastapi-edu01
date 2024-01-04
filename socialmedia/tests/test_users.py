from fastapi.testclient import TestClient

import pytest

from app.database import get_db, Base
from app.main import app
from app import schemas

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:loop@localhost:5432/socialmedia_test"
SQLALCHEMY_DATABASE_URL = (f'postgresql://{settings.database_username}:{settings.database_password}@'
                           f'{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test')

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    # run code before we run test
    Base.metadata.create_all(bind=engine)

    yield TestClient(app)

    # run code after test finishes
    Base.metadata.drop_all(bind=engine)


def test_root(client):
    res = client.get("/")

    assert res.json().get('message') == "Hello World!"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post("/users/", json={"email": "hello123@gmail.com", "password": "password123"})

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201