from datetime import datetime

from flask import Blueprint, jsonify, request

from auth import get_or_create_user, require_auth

from models import db


users_bp = Blueprint("users", __name__)


@users_bp.route("/api/users/me", methods=["GET"])
@require_auth
def get_me():
    user = get_or_create_user()
    return jsonify({
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "dob": user.dob.isoformat() if user.dob else None,
    })

@users_bp.route("/api/users/me", methods=["PATCH"])
@require_auth
def update_me():
    user = get_or_create_user()
    data = request.get_json()

    if "name" in data:
        user.name = data["name"]
    if "dob" in data:
        user.dob = datetime.strptime(data["dob"], "%Y-%m-%d").date()

    db.session.commit()
    return jsonify({
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "dob": user.dob.isoformat() if user.dob else None,
    }), 200