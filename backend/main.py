from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from models import db, Gym, Competition, Climb

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
        'date': comp.date.isoformat(),
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
        'date': comp.date.isoformat(),
        'status': comp.status,
        'climbs': [{
            'id': climb.id,
            'name': climb.name,
            'grade': climb.grade,
            'points': climb.points,
            'image_url': climb.image_url
        } for climb in climbs]
        }), 200

# Run the app
if __name__ == '__main__':
    app.run(debug=True)