from flask import Blueprint, jsonify

from models import Climb, Competition


competitions_bp = Blueprint("competitions", __name__, url_prefix="/api/competitions")

@competitions_bp.route("", methods=["GET"])
def get_comps():
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

@competitions_bp.route("/<int:comp_id>", methods=["GET"])
def get_comp_details(comp_id):
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