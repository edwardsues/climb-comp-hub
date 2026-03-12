from flask import Blueprint, jsonify, request

from auth import get_or_create_user, require_auth
from models import Attempt, Climb, Registration, db


attempts_bp = Blueprint("attempts", __name__, url_prefix="/api/attempts")

@attempts_bp.route("", methods=["POST"])
@require_auth
def log_attempt():
    """Log a new attempt"""
    user = get_or_create_user()
    data = request.get_json()

    climb_id = data.get("climb_id")
    climb = Climb.query.get_or_404(climb_id)

    # check if the user is even registered for the competition
    this_reg = Registration.query.filter_by(
        user_id = user.id, competition_id=climb.competition_id
    ).first()
    if not this_reg:
        return jsonify({"error": "Not registered for this competition"}), 403


    # check if the attempt already exists: user_id + climb_id
    existing = Attempt.query.filter_by(user_id=user.id, climb_id=climb_id).first()
    if existing:
        return jsonify({"error": "Attempt already logged for this climb"}), 409
    
    attempt = Attempt(
        user_id = user.id,
        climb_id = climb.id,
        competition_id = climb.competition_id,
        completed = data.get("completed", False),
        attempts_to_top = data.get("attempts_to_top"),
    )

    # TODO: update user points

    db.session.add(attempt)
    db.session.commit()

    return jsonify({
        "id": attempt.id,
        "climb_id": attempt.climb_id,
        "completed": attempt.completed,
        "attempts_to_top": attempt.attempts_to_top
    }), 201

@attempts_bp.route("/<int:attempt_id>", methods=["PATCH"])
@require_auth
def update_attempt(attempt_id):
    """Update an existing attempt"""

    user = get_or_create_user()
    attempt = Attempt.query.get_or_404(attempt_id)
    data = request.get_json()

    if user.id != attempt.user_id:
        return jsonify({"error": "You can only update your own attempts."}), 403
    
    if "completed" in data:
        attempt.completed = data["completed"]
    if "attempts_to_top" in data:
        attempt.attempts_to_top = data["attempts_to_top"]

    db.session.commit()

    return jsonify({
        "id": attempt.id,
        "climb_id": attempt.climb_id,
        "completed": attempt.completed,
        "attempts_to_top": attempt.attempts_to_top
    }), 200