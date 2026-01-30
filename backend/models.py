from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class Gym(db.Model):
    __tablename__ = 'gyms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text, nullable=False)

    competitions = db.relationship('Competition', backref='gym', lazy=True)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    dob = db.Column(db.Date)
    role = db.Column(db.String(20), default='climber')
    gym_id = db.Column(db.Integer, db.ForeignKey('gyms.id'))

    attempts = db.relationship('Attempt', backref='user', lazy=True)
    registrations = db.relationship('Registration', backref='user', lazy=True)

class Competition(db.Model):
    __tablename__ = 'competitions'
    
    id = db.Column(db.Integer, primary_key=True)
    gym_id = db.Column(db.Integer, db.ForeignKey('gyms.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='active')
    
    climbs = db.relationship('Climb', backref='competition', lazy=True)
    registrations = db.relationship('Registration', backref='competition', lazy=True)

class Registration(db.Model):
    __tablename__ = 'registrations'
    
    competition_id = db.Column(db.Integer, db.ForeignKey('competitions.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    registered_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
class Climb(db.Model):
    __tablename__ = 'climbs'
    
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey('competitions.id'), nullable=False)
    name = db.Column(db.String(255))
    grade = db.Column(db.String(10), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(500))
    
    attempts = db.relationship('Attempt', backref='climb', lazy=True)
    
    def __init__(self, **kwargs):
        super(Climb, self).__init__(**kwargs)
        # If no name provided, default to points value
        if not self.name:
            self.name = str(self.points)

class Attempt(db.Model):
    __tablename__ = 'attempts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    climb_id = db.Column(db.Integer, db.ForeignKey('climbs.id'), nullable=False)
    competition_id = db.Column(db.Integer, db.ForeignKey('competitions.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    attempts_to_top = db.Column(db.Integer)
    video_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'climb_id'),)