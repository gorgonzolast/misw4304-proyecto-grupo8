import os
import re
import uuid
from flask import request
from ..models.models import Blacklist, db


# --------------------- Utils ---------------------


def validate_token(auth_header):
    # Validate token is present
    if not auth_header or not auth_header.startswith("Bearer "):
        return False, 403, "Falta el token de autorización"

    # Validate token is valid
    token = auth_header.split("Bearer ")[1]
    valid_token = os.getenv("SECRET_TOKEN")
    if token != valid_token:
        return False, 401, "Token de autorización inválido"

    return True, 200, None


def validate_data(data):
    # Validate parameters are present
    required_params = ["email", "app_uuid"]
    for param in required_params:
        if param not in data:
            return False, 400, f"Falta el parámetro {param}"

    # Validate data types
    for param in required_params:
        if not isinstance(data[param], str):
            return False, 422, f"{param} debe ser un string."

    # Validate email
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(email_regex, data["email"]):
        return False, 422, "email no es un email válido"

    # Validate app_uuid
    try:
        uuid.UUID(data["app_uuid"], version=4)
    except ValueError:
        return False, 422, "app_uuid no es un UUID válido"

    # If blocked_reason is present, validate it
    if "blocked_reason" in data:
        if not isinstance(data["blocked_reason"], str):
            return (
                False,
                422,
                "blocked_reason debe ser un string.",
            )
        if len(data["blocked_reason"]) > 255:
            return (
                False,
                413,
                "blocked_reason debe tener máximo 255 caracteres",
            )

    return True, 200, None


# --------------------- Services ---------------------


def add_email_to_blacklist(data, auth_header):
    # Validate Token
    is_valid_token, status_code_token, message_token = validate_token(auth_header)
    if not is_valid_token:
        return {"msg": message_token}, status_code_token

    # Validate data
    is_data_valid, status_code_data, message_data = validate_data(data)
    if not is_data_valid:
        return {"msg": message_data}, status_code_data

    # Check if email is already blacklisted
    blacklisted = Blacklist.query.filter_by(email=data["email"]).first()
    if blacklisted:
        return {"msg": "Email ya está en la lista negra"}, 409

    # Add email to blacklist
    blacklist = Blacklist(
        email=data["email"],
        app_uuid=data["app_uuid"],
        client_ip=request.remote_addr,
        blocked_reason=data.get("blocked_reason"),
    )
    db.session.add(blacklist)
    db.session.commit()

    # Return response
    return {"msg": "Email no añadido a la lista negra"}, 201


def is_email_blacklisted(email, auth_header):
    # Validate Token
    is_valid_token, status_code_token, message_token = validate_token(auth_header)
    if not is_valid_token:
        return {"msg": message_token}, status_code_token

    # Check if email is blacklisted
    blacklisted = Blacklist.query.filter_by(email=email).first()

    # Return response
    if not blacklisted:
        return {"blacklisted": False}, 200
    else:
        return {
            "blacklisted": True,
            "blocked_reason": blacklisted.blocked_reason or "No especificado",
        }, 200


def reset_db():
    db.drop_all()
    db.create_all()
    return {"msg": "Todos los datos fueron eliminados"}, 200
