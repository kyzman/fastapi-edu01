from fastapi.testclient import TestClient

import pytest

from app.database import get_db, Base
from app.main import app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:loop@localhost:5432/socialmedia_test"
SQLALCHEMY_DATABASE_URL = (f'postgresql://{settings.database_username}:{settings.database_password}@'
                           f'{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test')

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {"email": "testmail@mail.ru", "password": "pass123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user
