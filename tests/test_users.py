import pytest
from app import schemas
from jose import jwt
from app.config import settings

def test_create_user(client):
    res = client.post("/users", json={"email": "funny@example.com", "password": "password123"})
    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "funny@example.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post('/login', data={"username": test_user['email'], "password": test_user['password']})
    new_token = schemas.Token(**res.json())
    payload = jwt.decode(new_token.access_token, settings.secret_key, algorithms=settings.algorithm)
    id = payload.get("user_id")
    assert res.status_code == 200
    assert id == test_user['id']
    assert new_token.token_type == "bearer"

@pytest.mark.parametrize('email, password, status_code', [
    ('wrong@example.com', 'password123', 403),
    ('funny@example.com', 'wrong', 403),
    ('wrong@example.com', 'wrong', 403),
    (None, 'password123', 422),
    ('funny@example.com', None, 422)
])

def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post('/login', data={'username': email, 'password': password})
    assert res.status_code == status_code