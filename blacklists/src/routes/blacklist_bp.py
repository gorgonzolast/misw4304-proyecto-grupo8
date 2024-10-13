from flask import request, Blueprint
from ..services.blacklist_service import (
    add_email_to_blacklist,
    is_email_blacklisted,
    reset_db,
)


blacklist_bp = Blueprint("blacklist", __name__)


# 1. Add an email to the blacklist
@blacklist_bp.route("/blacklists", methods=["POST"])
def create():
    data = request.get_json()
    auth_header = request.headers.get("Authorization")
    return add_email_to_blacklist(data, auth_header)


# 2. Check if an email is blacklisted
@blacklist_bp.route("/blacklists/<string:email>", methods=["GET"])
def get(email):
    auth_header = request.headers.get("Authorization")
    return is_email_blacklisted(email, auth_header)


# 3. Health check
@blacklist_bp.route("/blacklists/ping", methods=["GET"])
def ping():
    return "pong", 200


# 4. Reset the database
@blacklist_bp.route("/blacklists/reset", methods=["POST"])
def reset():
    return reset_db()
