from flask import Blueprint, jsonify, request

from auth import get_or_create_user, require_auth, require_permission
from models import Attempt, Climb, Competition, Registration, db


competitions_bp = Blueprint("competitions", __name__, url_prefix="/api/competitions")

@competitions_bp.route("", methods=["GET"])
def get_comps():
    """Get all competitions"""
    comps = Competition.query.all()
    return jsonify([{
        'id': comp.id,
        'name': comp.name,
        'start_time': comp.start_time.isoformat(),
        'end_time': comp.end_time.isoformat(),
        'gym': {
            'id': comp.gym.id,
            'name': comp.gym.name,
            'address': comp.gym.address,
        }
    } for comp in comps]), 200

@competitions_bp.route("", methods=["POST"])
@require_auth
@require_permission("create:competitions")
def create_comp():
    """Create a new competition"""
    user = get_or_create_user()
    data = request.get_json()

    missing = [f for f in ["name", "start_time", "end_time"] if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    comp = Competition(
        gym_id=user.gym_id,
        name=data["name"],
        start_time=data["start_time"],
        end_time=data["end_time"],
    )

    db.session.add(comp)
    db.session.commit()

    return jsonify({
        "id": comp.id,
        "gym_id": comp.gym_id,
        "name": comp.name,
        "start_time": comp.start_time.isoformat(),
        "end_time": comp.end_time.isoformat(),
    }), 200

@competitions_bp.route("/<int:comp_id>", methods=["GET"])
def get_comp_details(comp_id):
    """Get details for a specific competition"""
    comp = Competition.query.get_or_404(comp_id)
    climbs = Climb.query.filter_by(competition_id=comp_id).all()

    return jsonify({
        'id': comp_id,
        'name': comp.name,
        'start_time': comp.start_time.isoformat(),
        'end_time': comp.end_time.isoformat(),
        'gym': {
            'id': comp.gym.id,
            'name': comp.gym.name,
            'address': comp.gym.address,
        },
        'climbs': [{
            'id': climb.id,
            'name': climb.name,
            'grade': climb.grade,
            'points': climb.points,
            'image_url': climb.image_url
        } for climb in climbs]
    }), 200

@competitions_bp.route("/<int:comp_id>", methods=["PATCH"])
@require_auth
@require_permission("update:competitions")
def update_comp(comp_id):
    """Update a specific competition"""
    user = get_or_create_user()
    comp = Competition.query.get_or_404(comp_id)

    # compare gym_ids befre updating
    if user.gym_id != comp.gym_id:
        return jsonify({"error": "Forbidden"}), 403
    
    data = request.get_json()
    
    if "name" in data:
        comp.name = data["name"]
    if "start_time" in data:
        comp.start_time = data["start_time"]
    if "end_time" in data:
        comp.end_time = data["end_time"]

    db.session.commit()
    return jsonify({
        "id": comp.id,
        "name": comp.name,
        "start_time": comp.start_time.isoformat(),
        "end_time": comp.end_time.isoformat(),
    }), 200

@competitions_bp.route("/<int:comp_id>", methods=["DELETE"])
@require_auth
@require_permission("delete:competitions")
def delete_comp(comp_id):
    user = get_or_create_user()
    comp = Competition.query.get_or_404(comp_id)

    if user.gym_id != comp.gym_id:
        return jsonify({"error": "Forbidden"}), 403

    db.session.delete(comp)
    db.session.commit()
    return jsonify({"message": "Competition deleted"}), 200

@competitions_bp.route("/<int:comp_id>/attempts", methods=["GET"])
@require_auth
def get_attempts(comp_id): 
    user = get_or_create_user()
    comp = Competition.query.get_or_404(comp_id)

    # check that the user is registered for this competition
    this_reg = Registration.query.filter_by(
        user_id = user.id, competition_id=comp.id
    ).first()
    if not this_reg:
        return jsonify({"error": "Not registered for this competition"}), 403
    
    attempts = Attempt.query.filter_by(user_id=user.id, competition_id=comp.id).all()
    
    return jsonify([{
        'id': attempt.id,
        'climb_id': attempt.climb_id,
        'completed': attempt.completed,
        'attempts_to_top': attempt.attempts_to_top,
    } for attempt in attempts]), 200