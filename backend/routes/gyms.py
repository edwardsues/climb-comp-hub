from flask import Blueprint, jsonify

from models import Gym

gyms_bp = Blueprint("gyms", __name__, url_prefix="/api/gyms")

@gyms_bp.route("", methods=["GET"])
def get_gyms():
    """Get information about all gyms"""
    gyms = Gym.query.all()

    return jsonify([{
        'id': gym.id,
        'name': gym.name,
        'address': gym.address
    } for gym in gyms]), 200

@gyms_bp.route("/<int:gym_id>", methods=["GET"])
def get_gym(gym_id):
    gym = Gym.query.get_or_404(gym_id)

    return jsonify({
        'id': gym.id,
        'name': gym.name,
        'address': gym.address,
        'comps': [{
            'id': comp.id,
            'name': comp.name,
            'start_time': comp.start_time.isoformat(),
            'end_time': comp.end_time.isoformat(),
        } for comp in gym.competitions]
    })