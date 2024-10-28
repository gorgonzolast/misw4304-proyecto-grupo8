import os
import json

# -------------------------- 0. Mock data -----------------------------

blacklist_data = {
    "email": "test@gmail.com",
    "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
    "blocked_reason": "Spam",
}

headers = {"Authorization": f"Bearer {os.getenv('SECRET_TOKEN')}"}


# --------------------- 1. Add email to blacklist ---------------------


def test_add_email(test_client):
    response = test_client.post(
        "/blacklists",
        json=blacklist_data,
        headers=headers,
        content_type="application/json",
    )
    assert response.status_code == 201
    response_data = json.loads(response.data)
    assert response_data["msg"] == "Email añadido a la lista negra"


def test_add_email_no_token(test_client):
    response = test_client.post(
        "/blacklists",
        json=blacklist_data,
        content_type="application/json",
    )
    assert response.status_code == 403
    response_data = json.loads(response.data)
    assert response_data["msg"] == "Falta el token de autorización"


def test_add_email_invalid_token(test_client):
    headers = {"Authorization": "Bearer invalid_token"}
    response = test_client.post(
        "/blacklists",
        json=blacklist_data,
        headers=headers,
        content_type="application/json",
    )
    assert response.status_code == 401
    response_data = json.loads(response.data)
    assert response_data["msg"] == "Token de autorización inválido"


def test_add_email_no_email(test_client):
    blacklist_data_copy = blacklist_data.copy()
    blacklist_data_copy.pop("email")
    response = test_client.post(
        "/blacklists",
        json=blacklist_data_copy,
        headers=headers,
        content_type="application/json",
    )
    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert response_data["msg"] == "Falta el parámetro email"


def test_add_email_no_app_uuid(test_client):
    blacklist_data_copy = blacklist_data.copy()
    blacklist_data_copy.pop("app_uuid")
    response = test_client.post(
        "/blacklists",
        json=blacklist_data_copy,
        headers=headers,
        content_type="application/json",
    )
    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert response_data["msg"] == "Falta el parámetro app_uuid"


def test_add_email_invalid_type_email(test_client):
    blacklist_data_copy = blacklist_data.copy()
    blacklist_data_copy["email"] = 123
    response = test_client.post(
        "/blacklists",
        json=blacklist_data_copy,
        headers=headers,
        content_type="application/json",
    )
    assert response.status_code == 422
    response_data = json.loads(response.data)
    assert response_data["msg"] == "email debe ser un string."


def test_add_email_invalid_type_app_uuid(test_client):
    blacklist_data_copy = blacklist_data.copy()
    blacklist_data_copy["app_uuid"] = 123
    response = test_client.post(
        "/blacklists",
        json=blacklist_data_copy,
        headers=headers,
        content_type="application/json",
    )
    assert response.status_code == 422
    response_data = json.loads(response.data)
    assert response_data["msg"] == "app_uuid debe ser un string."


def test_add_email_invalid_type_blocked_reason(test_client):
    blacklist_data_copy = blacklist_data.copy()
    blacklist_data_copy["blocked_reason"] = 123
    response = test_client.post(
        "/blacklists",
        json=blacklist_data_copy,
        headers=headers,
        content_type="application/json",
    )
    assert response.status_code == 422
    response_data = json.loads(response.data)
    assert response_data["msg"] == "blocked_reason debe ser un string."


def test_add_email_invalid_email(test_client):
    blacklist_data_copy = blacklist_data.copy()
    blacklist_data_copy["email"] = "invalid_email"
    response = test_client.post(
        "/blacklists",
        json=blacklist_data_copy,
        headers=headers,
        content_type="application/json",
    )
    assert response.status_code == 422
    response_data = json.loads(response.data)
    assert response_data["msg"] == "email no es un email válido"


def test_add_email_invalid_app_uuid(test_client):
    blacklist_data_copy = blacklist_data.copy()
    blacklist_data_copy["app_uuid"] = "invalid_uuid"
    response = test_client.post(
        "/blacklists",
        json=blacklist_data_copy,
        headers=headers,
        content_type="application/json",
    )
    assert response.status_code == 422
    response_data = json.loads(response.data)
    assert response_data["msg"] == "app_uuid no es un UUID válido"


def test_add_email_invalid_blocked_reason(test_client):
    blacklist_data_copy = blacklist_data.copy()
    blacklist_data_copy["blocked_reason"] = "a" * 256
    response = test_client.post(
        "/blacklists",
        json=blacklist_data_copy,
        headers=headers,
        content_type="application/json",
    )
    assert response.status_code == 413
    response_data = json.loads(response.data)
    assert response_data["msg"] == "blocked_reason debe tener máximo 255 caracteres"


# --------------------- 2. Check if email is blacklisted ---------------------


def test_email_blacklisted(test_client):
    response = test_client.post(
        "/blacklists",
        json=blacklist_data,
        headers=headers,
        content_type="application/json",
    )
    response = test_client.get(
        f"/blacklists/{blacklist_data['email']}",
        headers=headers,
        content_type="application/json",
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["blacklisted"] == True
    assert response_data["blocked_reason"] == blacklist_data["blocked_reason"]


def test_email_not_blacklisted(test_client):
    response = test_client.get(
        f"/blacklists/{blacklist_data['email']}",
        headers=headers,
        content_type="application/json",
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["blacklisted"] == False
    assert response_data.get("blocked_reason") == None


def test_email_not_blacklisted_no_token(test_client):
    response = test_client.get(
        f"/blacklists/{blacklist_data['email']}",
        content_type="application/json",
    )
    assert response.status_code == 403
    response_data = json.loads(response.data)
    assert response_data["msg"] == "Falta el token de autorización"


def test_email_not_blacklisted_invalid_token(test_client):
    headers = {"Authorization": "Bearer invalid_token"}
    response = test_client.get(
        f"/blacklists/{blacklist_data['email']}",
        headers=headers,
        content_type="application/json",
    )
    assert response.status_code == 401
    response_data = json.loads(response.data)
    assert response_data["msg"] == "Token de autorización inválido"


# --------------------- 3. Health check --------------------------------


def test_ping(test_client):
    response = test_client.get("blacklists/ping")
    assert response.status_code == 200
    assert response.data == b"pong"


# --------------------- 4. Database cleanup -----------------------------


def test_cleanup(test_client):
    response = test_client.post("/blacklists/reset")
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["msg"] == "Todos los datos fueron eliminados"
