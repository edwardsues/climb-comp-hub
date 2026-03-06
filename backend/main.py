from flask import Flask
from flask_cors import CORS
from config import Config
from models import db

from routes import competitions_bp, gyms_bp, registrations_bp, users_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
CORS(app)

# routes:
app.register_blueprint(competitions_bp)
app.register_blueprint(gyms_bp)
app.register_blueprint(registrations_bp)
app.register_blueprint(users_bp)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)