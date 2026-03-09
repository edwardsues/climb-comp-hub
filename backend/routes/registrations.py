from flask import Blueprint, jsonify

from auth import get_or_create_user, require_auth
from models import Competition, Registration
from models import db


registrations_bp = Blueprint("registrations", __name__)


@registrations_bp.route("/api/registrations", methods=["GET"])
@require_auth
def view_registered_comps():
    """View which competitions the current user is registered for."""
    user = get_or_create_user()

    registrations = Registration.query.filter_by(user_id=user.id).all()
    return jsonify([{
        'id': reg.competition.id,
        'name': reg.competition.name,
        'start_time': reg.competition.start_time.isoformat(),
        'end_time': reg.competition.end_time.isoformat(),
    } for reg in registrations]), 200



@registrations_bp.route("/api/competitions/<int:comp_id>/register", methods=["POST"])
@require_auth
def register_for_comp(comp_id):
    comp = Competition.query.get_or_404(comp_id)

    # get the user
    user = get_or_create_user()

    # check if the user is registered for this competition
    this_reg = Registration.query.filter_by(
        user_id = user.id, competition_id=comp.id
    ).first()
    if this_reg:
        return jsonify({"error": "Already registered for this competition"}), 409
    
    # check if the user is registered for another competition at this time
    overlapping = Registration.query.join(Competition).filter(
        Registration.user_id == user.id,
        Competition.start_time < comp.end_time,
        Competition.end_time > comp.start_time
    ).first()
    if overlapping:
        return jsonify({"error": "already registered for a competition during this time"}), 400
    
    new_reg = Registration(user_id = user.id, competition_id = comp.id)
    db.session.add(new_reg)
    db.session.commit()

    return jsonify({"message": "Successfully registered"}), 201