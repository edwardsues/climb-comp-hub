from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from models import db, Gym, Competition, Climb, Registration
from auth import require_auth, get_or_create_user

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
CORS(app)

# routes:
@app.route('/')
def home():
    return {'message': 'API running'}

#####################################
#           public routes           #
#####################################
@app.route("/api/gyms", methods=["GET"])
def get_gyms():
    gyms = Gym.query.all()
    
    return jsonify([{
        'id': gym.id,
        'name': gym.name,
        'address': gym.address
    } for gym in gyms]), 200

@app.route("/api/competitions", methods=["GET"])
def get_comps():
    comps = Competition.query.all()
    return jsonify([{
        'id': comp.id,
        'gym_id': comp.gym_id,
        'name': comp.name,
        'start_time': comp.start_time.isoformat(),
        'end_time': comp.end_time.isoformat(),
        'status': comp.status
    } for comp in comps]), 200

@app.route("/api/competitions/<int:comp_id>", methods=["GET"])
def get_comp_details(comp_id):
    # return 404 if the comp_id doesn't exist
    comp = Competition.query.get_or_404(comp_id)
    
    # get all the climbs for this comp
    climbs = Climb.query.filter_by(competition_id=comp_id).all()

    return jsonify({
        'id': comp_id,
        'gym_id': comp.gym_id,
        'name': comp.name,
        'start_time': comp.start_time.isoformat(),
        'end_time': comp.end_time.isoformat(),
        'status': comp.status,
        'climbs': [{
            'id': climb.id,
            'name': climb.name,
            'grade': climb.grade,
            'points': climb.points,
            'image_url': climb.image_url
        } for climb in climbs]
        }), 200

#####################################
#           climber routes          #
#####################################
@app.route("/api/registrations", methods=["GET"])
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
        'status': reg.competition.status
    } for reg in registrations]), 200



@app.route("/api/competitions/<int:comp_id>/register", methods=["POST"])
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
    

# Run the app
if __name__ == '__main__':
    app.run(debug=True)