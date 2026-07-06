from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_short_password():
    response = client.post(
        "/api/v1/evaluate",
        json={
        "username": "testuser",
        "email": "test.user@example.com",
        "password": "19ap.d`"
    })
    assert response.status_code == 200
    assert response.json()["score"] == 0
    assert response.json()["feedback"]["warning"] == "The password is too short."

    response = client.post(
        "/api/v1/evaluate",
        json={
        "username": "testuser",
        "email": "test.user@example.com",
        "password": "a9.%$FK"
    })
    assert response.status_code == 200
    assert response.json()["score"] == 0
    assert response.json()["feedback"]["warning"] == "The password is too short."

def test_personal_data_password():
    response = client.post(
        "/api/v1/evaluate",
        json={
        "username": "DaVid",
        "email": "david.martinez@runner.com",
        "password": "david_martinez"
    })
    assert response.status_code == 200
    assert response.json()["score"] == 0
    assert "Please choose a password completely unrelated to your personal data." in response.json()["feedback"]["suggestions"]
    
    response = client.post(
        "/api/v1/evaluate",
        json={
        "username": "DaVid",
        "email": "davidmartinez@runner.com",
        "password": "d@v!dmArtine2"
    })
    print(response.json())
    assert response.status_code == 200
    assert response.json()["score"] < 2


def test_no_small_leters_password():
    response = client.post(
        "/api/v1/evaluate",
        json={
        "username": "testuser",
        "email": "test.user@example.com",
        "password": "19D.CZ!.DAVMP!>4AMD`"
    })
    assert response.status_code == 200
    assert response.json()["score"] < 3
    assert "Consider using small and capital letters, numbers, and symbols to increase password strength." in response.json()["feedback"]["suggestions"]

    response = client.post(
        "/api/v1/evaluate",
        json={
        "username": "testuser",
        "email": "test.user@example.com",
        "password": "PDS!#.AM10>!ADM!.,"
    })
    assert response.status_code == 200
    assert response.json()["score"] < 3
    assert "Consider using small and capital letters, numbers, and symbols to increase password strength." in response.json()["feedback"]["suggestions"]

def test_no_capital_leters_password():
    response = client.post(
        "/api/v1/evaluate",
        json={
        "username": "testuser",
        "email": "test.user@example.com",
        "password": "19d.cz!.davmp!>4amd`"
    })
    assert response.status_code == 200
    assert response.json()["score"] < 3
    assert "Consider using small and capital letters, numbers, and symbols to increase password strength." in response.json()["feedback"]["suggestions"]

    response = client.post(
        "/api/v1/evaluate",
        json={
        "username": "testuser",
        "email": "test.user@example.com",
        "password": "pds!#.am10>!adm!.,"
    })
    assert response.status_code == 200
    assert response.json()["score"] < 3
    assert "Consider using small and capital letters, numbers, and symbols to increase password strength." in response.json()["feedback"]["suggestions"] 

def test_no_numbers_password():
    response = client.post(
        "/api/v1/evaluate",
        json={
        "username": "testuser",
        "email": "test.user@example.com",
        "password": "CL!#CAt.v%@$fmpF.fp"
    })
    assert response.status_code == 200
    assert response.json()["score"] < 3
    assert "Consider using small and capital letters, numbers, and symbols to increase password strength." in response.json()["feedback"]["suggestions"] 

    response = client.post(
        "/api/v1/evaluate",
        json={
        "username": "testuser",
        "email": "test.user@example.com",
        "password": "pF!#.cvfVDA!ASCAm!.,"
    })
    assert response.status_code == 200
    assert response.json()["score"] < 3
    assert "Consider using small and capital letters, numbers, and symbols to increase password strength." in response.json()["feedback"]["suggestions"] 

def test_no_special_characters_password():
    response = client.post(
        "/api/v1/evaluate",
        json={
        "username": "testuser",
        "email": "test.user@example.com",
        "password": "v5g240vsLVvsw64AV10f"
    })
    assert response.status_code == 200
    assert response.json()["score"] < 3
    assert "Consider using small and capital letters, numbers, and symbols to increase password strength." in response.json()["feedback"]["suggestions"]

    response = client.post(
        "/api/v1/evaluate",
        json={
        "username": "testuser",
        "email": "test.user@example.com",
        "password": "DA40aFkfs428Fk134"
    })
    assert response.status_code == 200
    assert response.json()["score"] < 3
    assert "Consider using small and capital letters, numbers, and symbols to increase password strength." in response.json()["feedback"]["suggestions"]

def test_easy_password():
    response = client.post(
        "/api/v1/evaluate",
        json={
        "username": "testuser",
        "email": "test.user@example.com",
        "password": "password123!"
    })
    assert response.status_code == 200
    assert response.json()["score"] < 2

    response = client.post(
        "/api/v1/evaluate",
        json={
        "username": "testuser",
        "email": "test.user@example.com",
        "password": "qweasdzxc"
    })
    assert response.status_code == 200
    assert response.json()["score"] < 2


    response = client.post(
        "/api/v1/evaluate",
        json={
        "username": "david",
        "email": "david@example.com",
        "password": "divad123"
    })
    assert response.status_code == 200
    assert response.json()["score"] < 2


def test_strong_password():
    response = client.post(
        "/api/v1/evaluate",
        json={
        "username": "testuser",
        "email": "test.user@example.com",
        "password": ".c0#!0jas>AFDLacz.1fk"
    })
    assert response.status_code == 200
    assert response.json()["score"] > 2

    response = client.post(
        "/api/v1/evaluate",
        json={
        "username": "testuser",
        "email": "test.user@example.com",
        "password": "Turtle_Fan_123!"
    })
    assert response.status_code == 200
    assert response.json()["score"] > 2


    response = client.post(
        "/api/v1/evaluate",
        json={
        "username": "david",
        "email": "david@example.com",
        "password": "D@v!d_M@rt!n3z_glass"
    })
    assert response.status_code == 200
    assert response.json()["score"] > 2