from flask import Blueprint, jsonify, request

from auth import get_or_create_user, require_auth, require_permission
from models import Climb, Competition, db


climbs_bp = Blueprint("climbs", __name__, url_prefix="/api/competitions")

@climbs_bp.route("/<int:comp_id>/climbs", methods=["GET"])
def get_climbs(comp_id):
    """Get all climbs for a competition"""
    Competition.query.get_or_404(comp_id)
    climbs = Climb.query.filter_by(competition_id=comp_id).all()

    return jsonify([{
        "id": climb.id,
        "name": climb.name,
        "grade": climb.grade,
        "points": climb.points,
        "image_url": climb.image_url,
    } for climb in climbs]), 200

@climbs_bp.route("/<int:comp_id>/climbs", methods=["POST"])
@require_auth
@require_permission("create:climbs")
def create_climb(comp_id):
    """Create a new climb for a competition"""
    user = get_or_create_user()
    comp = Competition.query.get_or_404(comp_id)

    if user.gym_id != comp.gym_id:
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json()

    missing = [f for f in ["grade", "points"] if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    climb = Climb(
        competition_id=comp_id,
        grade=data["grade"],
        points=data["points"],
        name=data.get("name"),
        image_url=data.get("image_url"),
    )

    db.session.add(climb)
    db.session.commit()

    return jsonify({
        "id": climb.id,
        "name": climb.name,
        "grade": climb.grade,
        "points": climb.points,
        "image_url": climb.image_url,
    }), 201

@climbs_bp.route("/<int:comp_id>/climbs/<int:climb_id>", methods=["PATCH"])
@require_auth
@require_permission("update:climbs")
def update_climb(comp_id, climb_id):
    """Update a climb"""
    user = get_or_create_user()
    comp = Competition.query.get_or_404(comp_id)

    if user.gym_id != comp.gym_id:
        return jsonify({"error": "Forbidden"}), 403

    climb = Climb.query.filter_by(id=climb_id, competition_id=comp_id).first_or_404()
    data = request.get_json()

    if "name" in data:
        climb.name = data["name"]
    if "grade" in data:
        climb.grade = data["grade"]
    if "points" in data:
        climb.points = data["points"]
    if "image_url" in data:
        climb.image_url = data["image_url"]

    db.session.commit()

    return jsonify({
        "id": climb.id,
        "name": climb.name,
        "grade": climb.grade,
        "points": climb.points,
        "image_url": climb.image_url,
    }), 200

@climbs_bp.route("/<int:comp_id>/climbs/<int:climb_id>", methods=["DELETE"])
@require_auth
@require_permission("delete:climbs")
def delete_climb(comp_id, climb_id):
    """Delete a climb"""
    user = get_or_create_user()
    comp = Competition.query.get_or_404(comp_id)

    if user.gym_id != comp.gym_id:
        return jsonify({"error": "Forbidden"}), 403

    climb = Climb.query.filter_by(id=climb_id, competition_id=comp_id).first_or_404()

    db.session.delete(climb)
    db.session.commit()

    return jsonify({"message": "Climb deleted"}), 200
