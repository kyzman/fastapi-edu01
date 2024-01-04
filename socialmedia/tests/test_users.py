import pytest
from jose import jwt

from app import schemas
from app.config import settings


# def test_root(client):
#     res = client.get("/")
#
#     assert res.json().get('message') == "Hello World!"
#     assert res.status_code == 200


def test_create_user(client):
    res = client.post("/users/", json={"email": "hello123@gmail.com", "password": "password123"})

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201


def test_login_user(test_user, client):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    uid = payload.get("user_id")
    assert uid == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code, detail", [
    ('wrongmail@mail.ru', 'pass123', 404, 'No user found'),
    ('testmail@mail.ru', 'WrongPassword', 403, 'Invalid password'),
    ('wrongmail@mail.ru', 'WrongPassword', 404, 'No user found'),
    (None, 'pass123', 422, [{'type': 'missing', 'loc': ['body', 'username'], 'msg': 'Field required', 'input': None, 'url': 'https://errors.pydantic.dev/2.5/v/missing'}]),
    ('testmail@mail.ru', None, 422, [{'type': 'missing', 'loc': ['body', 'password'], 'msg': 'Field required', 'input': None, 'url': 'https://errors.pydantic.dev/2.5/v/missing'}]),
])
def test_incorrect_login(test_user, client, email, password, status_code, detail):
    res = client.post("/login", data={"username": email, "password": password})

    assert res.status_code == status_code
    assert res.json().get('detail') == detail
