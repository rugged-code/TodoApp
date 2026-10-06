from enum import verify

from sqlalchemy.dialects.mysql import expression

from test.utils import *
from router.auth import get_db, authenticate_user, create_access_token, SECRET_KEY, ALGORITHMS, get_current_user
from jose import jwt
from datetime import timedelta
import pytest
from fastapi import HTTPException

app.dependency_overrides[get_db] = override_get_db

def test_authenticate_user(test_user):
    db = TestSessionLocal()
    authenticated_user = authenticate_user(test_user.username, 'testpass', db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    non_existence_user = authenticate_user('wrong_user_name', 'testpass', db)
    assert non_existence_user is False

    wrong_password_user = authenticate_user(test_user.username, 'wrongpassword', db)
    assert wrong_password_user is False

def test_create_access_token(test_user):
    username = 'username'
    user_id = 1
    role = 'user'
    expires_delta = timedelta(days=1)

    token = create_access_token(username, user_id, role, expires_delta)

    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHMS], options = {'verify_signature' :   False})
    assert decoded_token['sub'] == username
    assert decoded_token['user_id'] == user_id
    assert decoded_token['role'] == role