import jwt
from fastapi import FastAPI
from fastapi.testclient import TestClient

from main import inmuebles

secret_key = 'W0bkRHQVe8P[kF[Nx|11]R{|rWL"VxXgkafD:j;.2;Uw7yk>^6_12_J*`[Iik{+'

def test_valid_auth_token_returns_success():
    # This is necessary to make startup behavior happen
    with TestClient(inmuebles) as client:
        response = client.get("/inmuebles/", headers={'access-token': jwt.encode({
                        "sub": "1234567890",
                        "name": "John Doe",
                        "iat": 1216239022,
                        "exp": 1811232323,}, key=secret_key, algorithm='HS256')})
        assert response.status_code == 200

def test_improperly_encoded_auth_token_returns_error():
    # This is necessary to make startup behavior happen
    with TestClient(inmuebles) as client:
        response = client.get("/inmuebles/", headers={'access-token': jwt.encode({
                        "sub": "1234567890",
                        "name": "John Doe",
                        "iat": 1216239022,
                        }, key="wrong_key", algorithm='HS256')})
        assert response.status_code == 401

def test_expired_auth_token_returns_error():
    # This is necessary to make startup behavior happen
    with TestClient(inmuebles) as client:
        response = client.get("/inmuebles/", headers={'access-token': jwt.encode({
                        "sub": "1234567890",
                        "name": "John Doe",
                        "iat": 1216239022,
                        "exp": 1011232323,
                        }, key=secret_key, algorithm='HS256')})
        assert response.status_code == 401

def test_no_auth_token_returns_error():
    # This is necessary to make startup behavior happen
    with TestClient(inmuebles) as client:
        response = client.get("/inmuebles/")
        assert response.status_code == 401
    
