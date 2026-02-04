from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
CORS(app)

# routes:
@app.route('/')
def home():
    return {'message': 'API running'}

# Run the app
if __name__ == '__main__':
    app.run(debug=True)